from src.platform.tomcat.authenticate import checkAuth
from src.platform.tomcat.interfaces import TINTERFACES
from auxiliary import Auxiliary
from log import LOG
import utility


class Auxiliary:
    """ Obtain a list of deployed WARs
    """

    def __init__(self):
        self.name = 'List deployed WARs'
        self.versions = ['Any']
        self.show = True
        self.flag = 'tc-list'

    def check(self, fingerprint):
        """
        """
        
        if fingerprint.title == TINTERFACES.MAN:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        """ Obtain a list of deployed WARs on a remote Tomcat instance
        """

        utility.Msg("Obtaining deployed applications...")
        base = "http://{0}:{1}".format(fingerengine.options.ip,
                                           fingerprint.port)
        relative = '/manager/list'
            
        if fingerprint.version in ["7.0", "8.0"]:
            relative = '/manager/text/list'

        url = base + relative

        response = utility.requests_get(url)
        if response.status_code == 401:
            utility.Msg('Host %s:%s requires auth, checking...' %
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

            apps = response.content.split('\n')[1:-1]
            for app in apps:
                utility.Msg("App found: %s" % app.split(':', 1)[0])

        else:
            utility.Msg("Unable to retrieve %s (HTTP %d)" % (url, 
                                    response.status_code), LOG.DEBUG)
