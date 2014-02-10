from src.platform.jboss.interfaces import JINTERFACES
from cprint import FingerPrint
from requests import exceptions
from log import LOG
import utility


class FPrint(FingerPrint):
    
    def __init__(self):
        self.platform = "jboss"
        self.version = "5.1"
        self.title = JINTERFACES.WM
        self.uri = "/admin-console/login.seam"
        self.port = 8080
        self.hash = None 
    
    def check(self, ip, port=None):
        """
        """
        try:
            rport = self.port if port is None else port
            request = utility.requests_get("http://{0}:{1}{2}".format(
                                    ip, rport, self.uri))

            # JBoss 5.1 and 6.0 share images, so we can't fingerprint those, but
            # we can check the web server version and a lack of a 6 in the AS title
            if "JBoss AS Administration Console 1.2.0" in request.content and \
               "JBoss AS 6 Admin Console" not in request.content:
                return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform,
                                                        ip, rport),
                                                        LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                          ip, rport),
                                                          LOG.DEBUG)

        return False
