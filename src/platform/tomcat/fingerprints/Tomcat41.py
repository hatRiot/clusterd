from src.platform.tomcat.authenticate import checkAuth
from src.platform.tomcat.interfaces import TINTERFACES
from requests import exceptions
from cprint import FingerPrint
from re import findall
from log import LOG
import utility

class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "tomcat"
        self.version = "4.1"
        self.title = TINTERFACES.APP
        self.uri = "/index.jsp"
        self.port = 8080
        self.hash = None

    def check(self, ip, port=None):
        """
        """

        try:
            rport = self.port if port is None else port
            url = "http://{0}:{1}{2}".format(ip, rport, self.uri)

            response = utility.requests_get(url)
            found = findall("Apache Tomcat/(.*?)\n", response.content)
            if len(found) > 0 and self.version in found[0]: 
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
