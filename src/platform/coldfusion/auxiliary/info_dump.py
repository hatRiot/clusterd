from src.platform.coldfusion.authenticate import checkAuth
from src.platform.coldfusion.interfaces import CINTERFACES
from auxiliary import Auxiliary
from log import LOG
from re import findall
import utility


class Auxiliary:

    def __init__(self):
        self.name = 'Dump host information'
        self.versions = ['9.0', '10.0']
        self.show = True
        self.flag = 'cf-info'

    def check(self, fingerprint):
        if fingerprint.title == CINTERFACES.CFM and \
           fingerprint.version in self.versions:
            return True
        return False

    def run(self, fingerengine, fingerprint):
        """ Obtains remote Coldfusion information from the reports index page.
        This pulls the first 26 entries from this report, as there's lots of
        extraneous stuff.  Perhaps if requested I'll prompt to extend to the
        remainder of the settings.
        """

        utility.Msg("Attempting to retrieve Coldfusion info...")

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        uri = "/CFIDE/administrator/reports/index.cfm"

        response = utility.requests_get(base + uri)
        if response.status_code == 200 and "ColdFusion Administrator Login" \
                                 in response.content:

            utility.Msg("Host %s:%s requires auth, checking..." % 
                            (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
            cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                                fingerprint.title, fingerprint.version)
            
            if cookies:
                response = utility.requests_get(base + uri, cookies=cookies[0])
            else:
                utility.Msg("Could not get auth for %s:%s" %
                               (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
                return

        if response.status_code == 200:
            
            types = findall("<td scope=row nowrap class=\"cell3BlueSides\">(.*?)</td>",
                            response.content.translate(None, "\n\t\r"))
            data = findall("<td scope=row class=\"cellRightAndBottomBlueSide\">(.*?)</td>",
                            response.content.translate(None, "\n\t\r"))
 
            # pad 
            types.insert(0, "Version")

            for (row, data) in zip(types, data)[:26]:
               utility.Msg('  %s: %s' % (row, data[:-7]))
