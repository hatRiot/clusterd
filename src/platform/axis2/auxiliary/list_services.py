from src.platform.axis2.authenticate import checkAuth
from src.platform.axis2.interfaces import AINTERFACES
from auxiliary import Auxiliary
from log import LOG
from re import findall
import utility

class Auxiliary:
    """ Obtain a list of deployed services
    """

    def __init__(self):
        self.name = 'List deployed services'
        self.versions = ['Any']
        self.flag = 'ax-list'

    def check(self, fingerprint):
        """
        """

        if fingerprint.title == AINTERFACES.DSR:
            return True
        return False

    def run(self, fingerengine, fingerprint):
        """
        """

        utility.Msg("Obtaining deployed services...")
        base = 'http://{0}:{1}'.format(fingerengine.options.ip,
                                       fingerprint.port)

        uri = '/axis2/axis2-admin/listService'

        cookie = checkAuth(fingerengine.options.ip, fingerprint.port,
                           fingerprint.title, fingerprint.version)
        if not cookie:
            utility.Msg("Could not get auth for %s:%s" %
                            (fingerengine.options.ip, fingerprint.port),LOG.ERROR)
            return

        response = utility.requests_get(base + uri, cookies=cookie)
        if response.status_code is 200:

           data = findall("\?wsdl\">(.*?)<", response.content)
           if len(data) > 0:
               for v in data:
                   utility.Msg("\tService found: %s" % v)
           else:
               utility.Msg("No services found.")
