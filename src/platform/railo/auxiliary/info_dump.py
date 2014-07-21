from src.platform.railo.authenticate import checkAuth
from src.platform.railo.interfaces import RINTERFACES
from auxiliary import Auxiliary
from log import LOG
from re import findall
import utility

class Auxiliary:

    def __init__(self):
        self.name = 'Dump host information'
        self.versions = ['3.0', '3.3', '4.0', '4.1', '4.2']
        self.flag = 'rl-info'

    def check(self, fingerprint):
        if fingerprint.title in [RINTERFACES.WEB] and \
                fingerprint.version in self.versions:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        """ Dump host OS info from a railo server
        """

        utility.Msg("Attempting to retrieve Railo info...")

        base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)

        uri = None
        if fingerprint.title is RINTERFACES.WEB:
            uri = '/railo-context/admin/web.cfm'
        elif fingerprint.title is RINTERFACES.SRV:
            uri = '/railo-context/admin/server.cfm'
        url = base + uri            

        response = utility.requests_get(url)
        if response.status_code is 200 and 'login' in response.content:

            utility.Msg("Host %s:%s requires auth, checking..." %
                            (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
            cookie = checkAuth(fingerengine.options.ip, fingerprint.port, 
                               fingerprint.title)
            
            if cookie:
                response = utility.requests_get(url, cookies=cookie)
            else:
                utility.Msg("Could not get auth for %s:%s" %
                                (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
                return

        if response.status_code is 200 and 'Overview' in response.content:

            (h, d) = self.fetchVersionRegex(fingerprint)
            headers = findall(h, response.content.translate(None, "\n\t\r"))
            data = findall(d, response.content.translate(None, "\n\t\r"))

            # do some version-specific trimming
            if fingerprint.version in ["4.1", '4.2']:
               headers = headers[4:]
               data = data[2:]
            elif fingerprint.version in ["3.0"]:
                headers = headers[:-6]
                data = data[:-6]
            elif fingerprint.version in ["3.3"]:
                headers = headers[:-7]
                data = data[:-7]

            for (th, td) in zip(headers, data):
                utility.Msg("\t%s: %s" % (th, td))                    

    def fetchVersionRegex(self, fingerprint):
        """ Information we need is represented differently, depending on
        the version.  This'll return a regex for matching specific items.
        """

        if fingerprint.version in ["3.0"]:
            return ("150\">(.*?)</td>", "400\">(.*?)</td>")
        elif fingerprint.version in ["3.3"]:            
            return ("150\">(.*?)</td>", "tblContent\">(.*?)</td>")
        elif fingerprint.version in ["4.0", "4.1", '4.2']:
            return ("\"row\">(.*?)</th>", "<td>(.*?)</td>")
