from src.platform.glassfish.authenticate import checkAuth
from src.platform.glassfish.interfaces import GINTERFACES
from auxiliary import Auxiliary
from re import findall
from log import LOG
import json
import utility

class Auxiliary:

    def __init__(self):
        self.name = 'List deployed applications'
        self.versions = ['Any']
        self.flag = 'gf-list'

    def check(self, fingerprint):
        """
        """

        if fingerprint.title == GINTERFACES.GAD:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        """
        """

        utility.Msg("Obtaining deployed applications...")
        base = 'https://{0}:{1}'.format(fingerengine.options.ip,
                                        fingerprint.port)
        uri = '/management/domain/applications/list-applications'
        headers = { "Accept" : "application/json" }
        
        cookie = checkAuth(fingerengine.options.ip, fingerprint.port,
                           fingerprint.title)
        if not cookie:
            utility.Msg("Could not get auth on %s:%s" % (fingerengine.options.ip,
                                                         fingerprint.port),
                                                        LOG.ERROR)
            return

        if fingerprint.version in ['3.0']:
            base = base.replace('https', 'http')
            uri = '/management/domain/applications/application'
            return self._parse_old(base + uri, cookie)


        response = utility.requests_get(base+uri, auth=cookie, headers=headers)
        if response.status_code is 200:

            data = json.loads(response.content)
            if not 'properties' in data.keys():
                utility.Msg("No applications found.")
                return

            utility.Msg("Discovered %d deployed apps" % len(data['properties']))
            for entry in data['properties'].keys():
                utility.Msg('  /%s' % entry)

    def _parse_old(self, url, cookie):
        """ Of course 3.0 doesn't expose list-applications ...
        """

        headers = {
                "Accept" : "application/json",
                "X-Requested-By" : "requests"
        }

        response = utility.requests_get(url, auth=cookie, headers=headers)
        if response.status_code is 200:

            data = json.loads(response.content)
            if not u"Child Resources" in data.keys():
                utility.Msg("No apps found")
                return

            for entry in data[u"Child Resources"]:
                splt = entry.rsplit('/',1 )[1]
                utility.Msg("  /%s" % splt)
