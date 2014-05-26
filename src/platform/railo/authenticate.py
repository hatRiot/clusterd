from src.platform.railo.interfaces import RINTERFACES
from requests.utils import dict_from_cookiejar
from collections import OrderedDict
from sys import stdout
from log import LOG
import state
import utility


def _auth(pswd, url, title):
    """ Support auth for both the web and server interfaces
    """            

    data = OrderedDict([ 
                ("lang", "en"),
                ("rememberMe", "yyyy"),
                ("submit", "submit")
            ])
    
    if title is RINTERFACES.WEB:            
        data["login_passwordweb"] =  pswd
    elif title is RINTERFACES.SRV:
        data['login_passwordserver'] = pswd

    response = utility.requests_post(url, data=data)
    if response.status_code is 200 and "login.login_password" not in response.content:
        utility.Msg("Successfully authenticated with '%s'" % pswd, LOG.DEBUG)
        return dict_from_cookiejar(response.cookies)


def checkAuth(ip, port, title):
    """ Railo doesn't have usernames, so we only care about passwords
    """

    url = None            
    if title is RINTERFACES.WEB:
        url = "http://{0}:{1}/railo-context/admin/web.cfm".format(ip, port)
    elif title is RINTERFACES.SRV:
        url = "http://{0}:{1}/railo-context/admin/server.cfm".format(ip, port)
    else:
        utility.Msg("Interface %s not supported yet." % title, LOG.DEBUG)
        return

    if state.usr_auth:
        # check with given auth; handle both cases of "default" and ":default"
        if ':' in state.usr_auth:
            (_, pswd) = state.usr_auth.split(":")
        else:
            pswd = state.usr_auth
        return _auth(pswd, url, title)

    if state.bf_wordlist and not state.hasbf:

        state.hasbf = True
        wordlist = []
        with open(state.bf_wordlist, "r") as f:
            wordlist = [x.decode("ascii", "ignore").rstrip() for x in f.readlines()]

        utility.Msg("Brute forcing %s with %d passwords..." % (state.bf_user,
                                len(wordlist)), LOG.DEBUG)

        try:
            for (idx, word) in enumerate(wordlist):
                stdout.flush()
                stdout.write("\r\033[32m [%s] Brute forcing password for %s [%d/%d]\033[0m"
                                % (utility.timestamp(), state.bf_user, idx+1, len(wordlist)))

                cook = _auth(word, url, title)
                if cook:
                    print ''
                    utility.Msg("Successful login with %s" % word, LOG.SUCCESS)
                    return cook

            print ''

        except KeyboardInterrupt:
            pass
