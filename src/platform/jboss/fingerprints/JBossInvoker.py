from src.platform.jboss.interfaces import JINTERFACES
from cprint import FingerPrint
from requests import exceptions
from hashlib import md5
from log import LOG
import utility

class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "jboss"
        self.version = "Any"
        self.title = JINTERFACES.IN
        self.uri = "/invoker/JMXInvokerServlet"
        self.port = 8080
        self.hash = "186c0e8a910b87dfd98ae0f746eb4879"

    def check(self, ip, port=None):
        """
        """

        try:
            rport = self.port if port is None else port
            request = utility.requests_get("http://{0}:{1}{2}".format(
                                    ip, rport, self.uri))

            compare_hash = md5(request.content[:44]).hexdigest()
            if compare_hash == self.hash:
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
