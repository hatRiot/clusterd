from src.platform.tomcat.authenticate import checkAuth
from src.platform.tomcat.interfaces import TINTERFACES
from src.module.deploy_utils import parse_war_path
from requests.utils import dict_from_cookiejar
from re import findall
from log import LOG
import utility

titles = [TINTERFACES.MAN]
def undeploy(fingerengine, fingerprint):
    """ This module is used to undeploy a context from a remote Tomcat server.
    In general, it is as simple as fetching /manager/html/undeploy?path=CONTEXT
    with an authenticated GET request to perform this action.

    However, Tomcat 6.x proves to not be as nice.  The undeployer in 6.x requires
    a refreshed session ID and a CSRF token.  This requires one more request on
    our part.

    Tomcat 7.x and 8.x expose /manager/text/undeploy which can bypass
    the need for a CSRF token.
    """

    context = parse_war_path(fingerengine.options.undeploy)
    base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)

    cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                        fingerprint.title, fingerprint.version)
    if not cookies:
        utility.Msg("Could not get auth for %s:%s" % 
                        (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
        return


    if fingerprint.version in ["7.0", "8.0"]:
        uri = "/manager/text/undeploy?path=/{0}".format(context)
    elif fingerprint.version in ['4.0', '4.1']:
        uri = '/manager/html/remove?path=/{0}'.format(context)
    else:
        uri = "/manager/html/undeploy?path=/{0}".format(context)

        if fingerprint.version in ['6.0']:
            (csrf, c) = fetchCSRF(base, cookies)
            uri += '&org.apache.catalina.filters.CSRF_NONCE=%s' % csrf 
            # rebuild our auth tuple
            cookies = (c, cookies[1])

    url = base + uri
    utility.Msg("Preparing to undeploy {0}...".format(context))

    response = utility.requests_get(url, cookies=cookies[0],
                                         auth=cookies[1])
    
    if response.status_code == 200 and \
                ('Undeployed application at context' in response.content or\
                 'OK' in response.content):
        utility.Msg("Successfully undeployed %s" % context, LOG.SUCCESS)
    elif 'No context exists for path' in response.content:
        utility.Msg("Could not find a context for %s" % context, LOG.ERROR)
    else:
        utility.Msg("Failed to undeploy (HTTP %s)" % response.status_code, LOG.ERROR)


def fetchCSRF(url, cookies):
    """ Tomcat 6.x is a huge pain; we need the refreshed cookie and CSRF token
    to correctly undeploy

    This will return the CSRF token and new session id
    """

    response = None
    try:
        csrf = None
        uri = '/manager/html'
        response = utility.requests_get(url + uri, cookies=cookies[0],
                                                   auth=cookies[1])

        if response.status_code is 200:
            
            data = findall("CSRF_NONCE=(.*?)\"", response.content)
            if len(data) > 0:
                csrf = data[0]

    except Exception, e:
        utility.Msg("Failed to fetch CSRF token (HTTP %d)" % response.status_code,
                                                             LOG.ERROR)
        csrf = None

    return (csrf, dict_from_cookiejar(response.cookies))
