from src.platform.glassfish.interfaces import GINTERFACES
from requests import exceptions
from log import LOG
from cprint import FingerPrint
import utility


class FPrint(FingerPrint):

    def __init__(self):
        self.platform = 'glassfish'
        self.version = 'Any'
        self.title = GINTERFACES.HD
        self.uri = '/'
        self.port = 8080
        self.hash = None

    def check(self, ip, port = None):
        """ 
        """

        versions = {
                     "Oracle GlassFish Server 3.0" : "3.0",
                     "GlassFish Server Open Source Edition 3.1" : "3.1",
                     "GlassFish Server Open Source Edition  4.0" : "4.0"
                   }
           
        try:
            rport = self.port if port is None else port
            url = 'http://{0}:{1}'.format(ip, rport)

            response = utility.requests_get(url)
            if 'Server' in response.headers:

                server = response.headers['Server']
                for val in versions.keys():
                    if val in server:
                        self.version = versions[val]
                        return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip,
                                                        rport), LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                         ip, rport), LOG.DEBUG)
        return False
