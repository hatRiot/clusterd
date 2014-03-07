from src.platform.jboss.interfaces import JINTERFACES
from requests import exceptions
from log import LOG
from cprint import FingerPrint
import utility


class FPrint(FingerPrint):

    def __init__(self):
        self.platform = 'jboss'
        self.version = 'Any'
        self.title = JINTERFACES.HD
        self.uri = "/"
        self.port = 8080
        self.hash = None

    def check(self, ip, port = None):
        """ This fingerprint is used to check HTTP headers from the responding
        server.  I explicitely note how unreliable these are, as there are
        many instaces were the results may be incorrect/inconclusive.
        """

        versions = {
                      "JBoss-3.2" : "3.2",
                      "JBoss-4.0" : "4.0",
                      "JBoss-4.2" : "4.2",
                      "JBoss-5.0" : "5.0",  # could be 5.0 or 5.1, treat as 5.0
                      "JBossAS-6" : "6.0"   # could be 6.0 or 6.1, treat as 6.0
                   }

        try:
            rport = self.port if port is None else port
            url = "http://{0}:{1}".format(ip, rport)

            response = utility.requests_get(url)
            if 'x-powered-by' in response.headers:
                powered_by = response.headers['x-powered-by']
                for val in versions.keys():
                    if val in powered_by:
                        self.version = versions[val]
                        return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip,
                                                    rport), LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                    ip, rport), LOG.DEBUG)

        return False            
