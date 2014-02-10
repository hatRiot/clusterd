from requests import exceptions
from cprint import FingerPrint
from log import LOG
import utility

class WINTERFACES:
    WLA = "WebLogic Admin Console"
    WLS = "WebLogic Admin Console (https)"

class WLConsole(FingerPrint):
    """ Oracle was kind enough to embed the version string right into the 
    default console page.
    """

    def __init__(self):
        self.platform = "weblogic"
        self.version = None
        self.title = WINTERFACES.WLA
        self.uri = "/console"
        self.port = 7001
        self.hash = None

    def check(self, ip, port = None):
        """ Pull the version string out of the page.
        """

        try:
            rport = self.port if port is None else port

            url = "{0}://{1}:{2}{3}".format("https" if "ssl" in dir(self) and self.ssl else "http",
                                            ip, rport, self.uri)
            response = utility.requests_get(url)

            if "WebLogic Server Version: {0}.".format(self.version) in response.content:
                return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip,
                                                        rport), LOG.DEBUG)
        except exceptions.ConnectionError, e:
            utility.Msg("{0} connection error to {1}:{2} ({3})".format(
                                                                self.platform,
                                                                ip, rport, e),
                                                                LOG.DEBUG)

        return False


class BEAConsole(FingerPrint):
    """ Old versions of BEA WebLogic admin console have the version strings
    embedded into the login page.
    """

    def __init__(self):
        self.platform = "weblogic"
        self.version = None
        self.title = WINTERFACES.WLA
        self.uri = "/console"
        self.port = 7001
        self.hash = None

    def check(self, ip, port = None):
        """ Pull the version string out of the page.
        """

        try:
            rport = self.port if port is None else port
            response = utility.requests_get("http://{0}:{1}{2}".format(
                                    ip, rport, self.uri))

            if "BEA WebLogic Server {0}".format(self.version) in response.content:
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
