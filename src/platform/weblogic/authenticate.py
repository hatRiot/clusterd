from src.platform.weblogic.interfaces import WINTERFACES
from subprocess import check_output, CalledProcessError
from requests.utils import dict_from_cookiejar
from sys import stdout
from log import LOG
import utility
import state


default_credentials = [('weblogic', 'weblogic'),
                       ('weblogic', 'weblogic1')
                      ]

def _authCookie(usr, pswd, ip, fingerprint):
    """ Authenticate to j_security_check and return the cookie
    """

    try:
        base = "http://{0}:{1}".format(ip, fingerprint.port)
        uri = "/console/j_security_check"

        data = { "j_username" : usr,
                 "j_password" : pswd,
                 "j_character_encoding" : "UTF-8"
               }

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


def _auth(usr, pswd, ip, fingerprint):
    """ Runs our checkauth.sh script in order to determine whether or not
    the given credentials are valid.  This simply runs the VERSION command
    using weblogic.Admin.

    Return is True for success or False for fail.
    """

    result = False

    try:
        args = ["./checkauth.sh", ip, str(fingerprint.port), usr, pswd]
        if fingerprint.title is WINTERFACES.WLS:
            args.append("ssl")

        res = check_output(args, cwd="./src/lib/weblogic/checkauth")
        if type(res) is str and "WebLogic" in res:
            result = True

    except CalledProcessError, e:
        if "BAD_CERTIFICATE" in e.output:
            utility.Msg("BAD_CERTIFICATE error", LOG.DEBUG)    
        result = False
    except Exception, e:
        utility.Msg(e, LOG.DEBUG)
        result = False

    return result


def checkAuth(ip, fingerprint, returnCookie = False):
    """ Default behavior is to simply return True/False based on
    whether or not authentication with the credentials was successful.
    If returnCookie is set to true, we return the required auth cookie.

    Returns a tuple of (usr, pswd) in the event of a success, otherwise
    (None, None) is returned.
    """

    rauth = _auth
    if returnCookie:
       rauth = _authCookie

    # check with given auth
    if state.usr_auth:
        (usr, pswd) = state.usr_auth.split(':')
        auth = rauth(usr, pswd, ip, fingerprint)
        if auth:
            return auth if returnCookie else (usr, pswd) 

    # else try default credentials
    for (usr, pswd) in default_credentials:

        auth = rauth(usr, pswd, ip, fingerprint)
        if auth:
            return auth if returnCookie else (usr, pswd)

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

                auth = rauth(state.bf_user, word, ip, fingerprint)
                if auth:
                    print ''

                    # insert creds into default cred list
                    if not (state.bf_user, word) in default_credentials:
                        default_credentials.insert(0, (state.bf_user, word))

                    utility.Msg("Successful login %s:%s" % 
                                    (state.bf_user, word), LOG.SUCCESS)
                    return auth if returnCookie else (state.bf_user, word)

            print ''

        except KeyboardInterrupt:
            pass

    return (None, None)
