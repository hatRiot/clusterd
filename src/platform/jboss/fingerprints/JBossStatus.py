from src.platform.jboss.interfaces import JINTERFACES
from cprint import FingerPrint
from log import LOG
from requests import exceptions
import utility


class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "jboss"
        self.version = "Any"
        self.title = JINTERFACES.STS
        self.uri = "/status?full=true"
        self.port = 8080
        self.hash = None


    def check(self, ip, port = None):
        """
        """

        try:
            rport = self.port if port is None else port
            url = "http://{0}:{1}{2}".format(ip, rport, self.uri)

            response = utility.requests_get(url)
            if response.status_code == 401:
                utility.Msg("Host %s:%s requires auth for %s, checking.." % 
                                        (ip, rport, self.uri), LOG.DEBUG)

                cookies = checkAuth(ip, rport, self.title, self.version)
                if cookies:
                    response = utility.requests_get(url, cookies=cookies[0],
                                                    auth=cookies[1])
                else:
                    utility.Msg("Could not get auth for %s:%s" % (ip, rport), LOG.ERROR)
                    return False

            if response.status_code == 200:
                return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip,
                                                        rport), LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                    ip, rport), LOG.DEBUG)

        return False
