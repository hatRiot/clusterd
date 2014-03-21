from cprint import FingerPrint
from requests import exceptions
from log import LOG
from re import findall
import utility


class RINTERFACES:
    DSR = "Railo Server"        
    WEB = "Railo Web Administrator"
    SRV = "Railo Server Administrator"
    AJP = "Railo AJP"

class WebAdmin(FingerPrint):
    """ Fingerprint interface for the web admin page
    """

    def __init__(self):            
        self.platform = 'railo'
        self.version = None
        self.title = RINTERFACES.WEB
        self.uri = '/railo-context/admin/web.cfm'
        self.port = 8888
        self.hash = None

    def check(self, ip, port = None):
        """
        """

        try:
            rport = self.port if port is None else port
            url = 'http://{0}:{1}{2}'.format(ip, rport, self.uri)

            response = utility.requests_get(url)
            if response.status_code is 200:
                if checkError(url, self.version):
                    return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip,
                                                        rport), LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error {1}:{2}".format(self.platform, ip,
                                                        rport), LOG.DEBUG)

        return False


class ServerAdmin(FingerPrint):
    """ Fingerprint interface for the server admin page
    """

    def __init__(self):
        self.platform = 'railo'
        self.version = None
        self.title = RINTERFACES.SRV
        self.uri = '/railo-context/admin/server.cfm'
        self.port = 8888
        self.hash = None

    def check(self, ip, port = None):     
        """
        """

        try:
            rport = self.port if port is None else port
            url = 'http://{0}:{1}{2}'.format(ip, rport, self.uri)

            response = utility.requests_get(url)
            if response.status_code is 200:
                if checkError(url, self.version):
                    return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform,
                                                        ip, rport), LOG.DEBUG)
        except exceptions.ConnectionError:            
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                        ip, rport), LOG.DEBUG)

        return False            


class DefaultServer(FingerPrint):
    """ This tests for the default welcome page at /
    """

    def __init__(self):
        self.platform = 'railo'
        self.version = None
        self.title = RINTERFACES.DSR
        self.uri = '/'
        self.port = 8888
        self.hash = None

    def check(self, ip, port = None):
        """
        """

        try:
            rport = self.port if port is None else port
            url = 'http://{0}:{1}{2}'.format(ip, rport, self.uri)

            response = utility.requests_get(url)
            if response.status_code is 200:
                
                data = findall("<title>Welcome to Railo (.*?)</title>", response.content)
                if len(data) > 0 and self.version in data[0]:
                    return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip,
                                                        rport), LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                          ip, rport), LOG.DEBUG)

        return False            


def checkError(url, version):
    """ There isn't any versioning information listed on the web/server admin
    pages, so instead we trigger an error and read the debugging info.  This is on
    by default for all versions of Railo.
    """

    try:
        url += ".cfm"

        response = utility.requests_get(url)
        if response.status_code == 404:

            data = findall("\">Railo \d.\d", response.content)
            if len(data) > 0 and version in data[0]:
                return True

    except exceptions.Timeout:
        utility.Msg("{0} timeout to {1}:{2}".format(self.platform, ip, rport),
                                                    LOG.DEBUG)
    except exceptions.ConnectionError:
        utility.Msg("{0} connection error to {1}:{2}".format(self.platform, 
                                                      ip, rport), LOG.DEBUG)
    return False                
