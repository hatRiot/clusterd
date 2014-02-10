from cprint import FingerPrint
from requests import exceptions
from log import LOG
import utility


class CINTERFACES:
    CFM = "ColdFusion Manager"


class AdminInterface(FingerPrint):
    """
    """

    def __init__(self):
        self.platform = "coldfusion"
        self.version = None
        self.title = CINTERFACES.CFM
        self.uri = "/CFIDE/administrator"
        self.port = 80
        self.hash = None

    def check(self, ip, port = None):
        """
        """

        try:
            rport = self.port if port is None else port
            url = "http://{0}:{1}{2}".format(ip, rport, self.uri)

            response = utility.requests_get(url)

            if "Version: {0}".format(self.version.replace('.',',')) in response.content:
                return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip,
                                                        rport), LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                 ip, rport), LOG.DEBUG)

        return False
