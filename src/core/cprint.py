from hashlib import md5
from requests import exceptions
from log import LOG
import utility


""" Abstract fingerprint for modules to inherit from.
"""

class FingerPrint(object):

    def __init__(self):
        self.platform = None    # Platform for the fingerprint
        self.title = None       # Title or interface name
        self.uri = None         # Default URI
        self.port = None        # Default port
        self.hash = None        # md5 hash to check for; this can be a single hash or a list
        self.ssl = False        # establish https connection?

    def check(self, ip, port=None):
        """ Pull the specified URI down and compare the content hash
            against the defined hash.
        """
        try:
            rport = self.port if port is None else port

            url = "{0}://{1}:{2}{3}".format("https" if "ssl" in dir(self) and self.ssl else "http",
                                            ip, rport, self.uri)
            response = utility.requests_get(url)

            utility.Msg("Fetching hash from {0}".format(response.url), LOG.DEBUG)
        
            if response.status_code == 200:

                hsh = md5(response.content).hexdigest()
                if type(self.hash) is list and hsh in self.hash:
                    return True
                elif hsh == self.hash:
                    return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform,
                                                        ip, rport),
                                                        LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                          ip, rport),
                                                          LOG.DEBUG)
        return False
