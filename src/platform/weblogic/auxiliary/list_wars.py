from src.platform.weblogic.authenticate import checkAuth
from src.platform.weblogic.interfaces import WINTERFACES
from auxiliary import Auxiliary
from log import LOG
from re import findall
import utility

class Auxiliary:

    def __init__(self):
        self.name = 'List deployed apps'
        self.versions = ["10", "12"]
        self.flag = 'wl-list'

    def check(self, fingerprint):
        return True

    def run(self, fingerengine, fingerprint):
        
        cookies = checkAuth(fingerengine.options.ip, fingerprint)
        if not cookies[0]:
            utility.Msg("This module requires valid credentials.", LOG.ERROR)
            return

        utility.Msg("Obtaining deployed applications...")

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        uri = "/console/console.portal?_nfpb=true&_pageLabel=AppDeploymentsControlPage"

        if fingerprint.title is WINTERFACES.WLS:
            base = base.replace("http", "https")

        response = utility.requests_get(base + uri, cookies=cookies[0])
        if response.status_code == 200:

            data = findall(r"title=\"Select (.*?)\"", response.content)
            if len(data) > 0:
                for entry in data:
                   utility.Msg("App found: %s" % entry)
            else:
                utility.Msg("No applications found.")
