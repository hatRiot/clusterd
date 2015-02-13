from src.platform.coldfusion.authenticate import checkAuth
from src.platform.coldfusion.interfaces import CINTERFACES
from auxiliary import Auxiliary
from log import LOG
from re import findall
import utility


class Auxiliary:

    def __init__(self):
        self.name = 'Dump host information'
        self.versions = ['5.0', '6.0', '6.1', '7.0', '8.0', '9.0', '10.0',
                         '11.0']
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

        if fingerprint.version in ["5.0", "6.0", "6.1"]:
            return self._run5(fingerengine, fingerprint)

        utility.Msg("Attempting to retrieve Coldfusion info...")

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        uri = "/CFIDE/administrator/reports/index.cfm"

        if fingerprint.version in ["7.0"]:
            uri = '/CFIDE/administrator/settings/version.cfm'

        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)
        if not cookies:
            utility.Msg("Could not get auth for %s:%s" %
                        (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return
        else:
            cookies = cookies[0]

        try:
            response = utility.requests_get(base + uri, cookies=cookies)
        except Exception, e:
            utility.Msg("Failed to fetch info: %s" % e, LOG.ERROR)
            return
            
        if response.status_code == 200:
           
            regex = self.versionRegex(fingerprint.version)
            types = findall(regex[0], response.content.translate(None, "\n\t\r"))
            data = findall(regex[1], response.content.translate(None, "\n\t\r"))

            # pad
            if fingerprint.version in ["8.0", "9.0", "10.0", '11.0']:
                types.insert(0, "Version")

            for (row, data) in zip(types, data)[:26]:
               utility.Msg('  %s: %s' % (row, data[:-7]))

    def versionRegex(self, version):
        """
        """

        if version in ["7.0"]:
            return ["<td nowrap class=\"cell3BlueSides\">(.*?)</td>",
                    "<td nowrap class=\"cellRightAndBottomBlueSide\">(.*?)</td>"]
        else:
            return ["<td scope=row nowrap class=\"cell3BlueSides\">(.*?)</td>",
                    "<td scope=row class=\"cellRightAndBottomBlueSide\">(.*?)</td>"]

    def _run5(self, fingerengine, fingerprint):
        """ Pull sys info from older CF instances; it is quite ugly
        """

        utility.Msg("Attempting to retrieve Coldfusion info...")

        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)[0]
        if not cookies:
            utility.Msg("Could not get auth for %s:%s" %
                         (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return

        base = 'http://{0}:{1}'.format(fingerengine.options.ip,
                                       fingerprint.port)

        if fingerprint.version in ['5.0']:
            uri = '/CFIDE/administrator/server_settings/version.cfm'
        elif fingerprint.version in ['6.0', '6.1']:
            uri = '/CFIDE/administrator/settings/version.cfm'

        response = utility.requests_get(base+uri, cookies=cookies)

        if fingerprint.version in ['5.0']:

            keys = findall("<td height=\".*?\" nowrap>(.*?)</td>", response.content.translate(None, '\r\n'))[1:]
            values = findall("<td>(.*?)</td>", response.content.translate(None, '\r\n'))
            for (key, value) in zip(keys, values[2:]):
                k = findall("class=\"text2\">(.*?)</p>", key)[0].replace("&nbsp;",'').rstrip()
                v = findall(">(.*?)\t", value)[0].replace(' ','')
                utility.Msg("  %s: %s" % (k, v))

        elif fingerprint.version in ['6.0', '6.1']:

            keys = findall("<td height=\"18\" nowrap>(.*?)</td>", 
                            response.content.translate(None, '\r\n'))
            values = findall("<td width=\"100%\" class=\"color-row\">(.*?)</td>",
                            response.content.translate(None, '\r\n'))

            for (key, value) in zip(keys[:-2], values[:-2]):

                k = findall("&nbsp;(.*?)&nbsp;", key)[0].lstrip().rstrip()
                v = findall("&nbsp;(.*?)\t", value)[0].lstrip().rstrip()
                utility.Msg("  %s: %s" % (k, v))
