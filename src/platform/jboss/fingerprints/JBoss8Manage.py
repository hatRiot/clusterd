from src.platform.jboss.interfaces import JINTERFACES
from cprint import FingerPrint
from log import LOG
import utility


class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "jboss"
        self.version = "8.0"
        self.title = JINTERFACES.MM
        self.uri = "/error/index_win.html"
        self.port = 9990
        self.hash = None

    def check(self, ip, port = None):
        """ This works for current releases of JBoss 8.0; future
        versions may require us to modify this.
        """

        try:
            rport = self.port if port is None else port
            request = utility.requests_get("http://{0}:{1}{2}".format(
                                    ip, rport, self.uri))

            if request.status_code == 200:
                if "WildFly 8" in request.content:
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
