from cprint import FingerPrint
from requests import exceptions
from re import findall
from log import LOG
import utility

class AINTERFACES:
    DSR = "Axis2 Server"


class DefaultServer(FingerPrint):
    """
    """

    def __init__(self):
        self.platform = 'axis2'
        self.version = None
        self.title = AINTERFACES.DSR
        self.uri = '/axis2/services/Version/getVersion'
        self.port = 8080
        self.hash = None

    def check(self, ip, port = None):
        """ Snags the version off the default getVersion
        method.
        """
        
        try:
            rport = self.port if port is None else port
            url = 'http://{0}:{1}{2}'.format(ip, rport, self.uri)

            response = utility.requests_get(url)
            if response.status_code is 200:

                data = findall("version is (.*?)</", 
                                    response.content.translate(None,'\n'))
                if len(data) > 0 and self.version in data[0]:
                    return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip,
                                                rport), LOG.DEBUG)

        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                         ip, rport), LOG.DEBUG)

        return False
