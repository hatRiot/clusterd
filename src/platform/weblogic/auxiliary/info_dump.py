from src.platform.weblogic.authenticate import checkAuth
from src.platform.weblogic.interfaces import WINTERFACES
from auxiliary import Auxiliary
from log import LOG
from re import findall
import utility

class Auxiliary:

    def __init__(self):
        self.name = 'Gather WebLogic info'
        self.versions = ["10", "12"]
        self.flag = 'wl-info'

    def check(self, fingerprint):
        return True

    def run(self, fingerengine, fingerprint):

        cookies = checkAuth(fingerengine.options.ip, fingerprint)
        if not cookies[0]:
            utility.Msg("This module requires valid credentials.", LOG.ERROR)
            return

        utility.Msg("Attempting to retrieve WebLogic info...")

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        if fingerprint.title is WINTERFACES.WLS:
           base = base.replace('http', 'https')

        server_name = self.fetchServerName(base, cookies[0])
        uri = "/console/console.portal?_nfpb=true&_pageLabel=ServerMonitoringTabmonitoringTabPage&"\
              "handle=com.bea.console.handles.JMXHandle%28%22com.bea%3AName%3D{0}"\
              "%2CType%3DServer%22%29".format(server_name)

        response = utility.requests_get(base + uri, cookies=cookies[0])
        if response.status_code == 200:

            tags = findall("class=\"likeLabel\">(.*?):</span>", response.content)
            values = findall("class=\"inputFieldRO\"><div>(.*?)</div>", response.content.replace('\r\n', ''))

            if len(tags) > 0:
               for (key, value) in zip(tags, values):
                   utility.Msg("  %s: %s" % (key, value))

        else:
            utility.Msg("Unable to fetch server '%s' information (HTTP %d)" %
                            (server_name, response.status_code), LOG.ERROR)

    def fetchServerName(self, base, cookie):
        """
        """

        uri = "/console/console.portal?_nfpb=true&_pageLabel=CoreServerServerTablePage"

        response = utility.requests_get(base + uri, cookies=cookie)
        if response.status_code is 200:

            servers = findall("\"Select (.*?)&#40", response.content)
            if len(servers) > 0:
                return servers[0]
