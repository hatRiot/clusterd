from src.platform.tomcat.authenticate import checkAuth
from src.platform.tomcat.interfaces import TINTERFACES
from auxiliary import Auxiliary
from log import LOG
import utility


class Auxiliary:
    """ The Manager application for Tomcat has a nifty fingerprinting
        app that allows us to retrieve host OS, versioning, arch, etc.
        which may aid in targeting payloads.
    """

    def __init__(self):
        self.name = 'Gather Tomcat info'
        self.versions = ['Any']
        self.show = True
        self.flag = 'tc-info'

    def check(self, fingerprint):
        """
        """

        if fingerprint.title == TINTERFACES.MAN:
            return True

        return False

    def run(self, fingerengine, fingerprint):

        utility.Msg("Attempting to retrieve Tomcat info...")
        base = "http://{0}:{1}".format(fingerengine.options.ip,
                                       fingerprint.port)
        relative = '/manager/serverinfo'

        if fingerprint.version in ["7.0", "8.0"]:
            relative = '/manager/text/serverinfo'

        url = base + relative

        response = utility.requests_get(url)
        if response.status_code == 401:
            utility.Msg("Host %s:%s requires auth, checking..." % 
                            (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
            cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                                fingerprint.title, fingerprint.version)

            if cookies:
                response = utility.requests_get(url, cookies=cookies[0],
                                            auth=cookies[1])
            else:
                utility.Msg("Could not get auth for %s:%s" % 
                                (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
                return

        if response.status_code == 200:

            info = response.content.split('\n')[1:-1]
            for entry in info:
                utility.Msg(entry)
