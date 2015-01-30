from src.platform.glassfish.interfaces import GINTERFACES
from requests import exceptions
from cprint import FingerPrint
from log import LOG
import utility

class FPrint(FingerPrint):

    def __init__(self):
        self.platform = 'glassfish'
        self.version = '4.0'
        self.title = GINTERFACES.JXR
        self.uri = '/'
        self.port = 7676
        self.hash = None

    def check(self, ip, port = None):
        """
        """

        try:
            rport = self.port if port is None else port
            url = 'http://{0}:{1}{2}'.format(ip, rport, self.uri)

            response = utility.requests_get(url)
            if response.status_code is 200 and "glassfish4" in response.content:
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
