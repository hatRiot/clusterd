from requests import exceptions
from cprint import FingerPrint
from re import findall
from log import LOG
import authenticate
import random
import string
import utility


class TINTERFACES:
    APP = "Tomcat"
    MAN = "Tomcat Manager"
    ADM = "Tomcat Admin"

class ManagerInterface(FingerPrint):
    """ This class defines the default management fingerprint for Tomcat.
    The version number is stripped out of the index page.
    """

    def __init__(self):
        self.platform = "tomcat"
        self.version = None
        self.title = TINTERFACES.MAN
        self.uri = "/manager/html"
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
                utility.Msg("Host %s:%s requires auth for manager, checking.."
                                % (ip, rport), LOG.DEBUG)

                cookies = authenticate.checkAuth(ip, rport, self.title, self.version)
                if cookies:
                    response = utility.requests_get(url, cookies=cookies[0],
                                                    auth=cookies[1])
                else:
                    utility.Msg("Could not get auth for %s:%s" % (ip, rport),
                                                                LOG.ERROR)

            if response.status_code == 200:
                found = findall("Apache Tomcat/(.*)<", response.content)
                if len(found) > 0 and self.version in found[0]:
                    return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform,
                                                        ip, rport), LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                        ip, rport), LOG.DEBUG)

        return False

class AppInterface(FingerPrint):
    """ AppInterface defines the default app fingerprint for Tomcat.  This
    pulls the version number from the release notes.
    """

    def __init__(self):
        self.platform = "tomcat"
        self.version = None
        self.title = TINTERFACES.APP
        self.uri = "/RELEASE-NOTES.txt"
        self.port = 8080
        self.hash = None

    def check(self, ip, port = None):
        """
        """

        try:
            rport = self.port if port is None else port
            url = "http://{0}:{1}{2}".format(ip, rport, self.uri)

            response = utility.requests_get(url)
            found = findall("Apache Tomcat Version (.*?)\n", response.content)

            if len(found) > 0 and self.version in found[0]:
                return True
            else:
                return self.check_error(ip, rport)

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform,
                                                        ip, rport),
                                                        LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                          ip, rport),
                                                          LOG.DEBUG)

        return False
        
    def check_error(self, ip, port):
        """
        """

        try:
            fpath = ''.join(random.choice(string.ascii_lowercase) for x in range(4))
            url = "http://{0}:{1}/{2}".format(ip, port, fpath)

            response = utility.requests_get(url)
            if response.status_code == 404:

                data = findall("<h3>(.*?)</h3>", response.content)
                if len(data) > 0 and self.version in data[0]:
                    return True

            else:
                utility.Msg("/%s returned unexpected HTTP code (%d)" %\
                                (fpath, response.status_code), LOG.DEBUG)

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform,
                                                        ip, port), LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                        ip, port), LOG.DEBUG)

        return False

