from src.platform.jboss.authenticate import checkAuth
from src.platform.jboss.interfaces import JINTERFACES
from src.module.deploy_utils import parse_war_path
from collections import OrderedDict
from log import LOG
from re import findall
import utility

titles = [JINTERFACES.JMX, JINTERFACES.MM]
def undeploy(fingerengine, fingerprint):
    """
    """

    if fingerprint.title is JINTERFACES.JMX:
        return jmx_undeploy(fingerengine, fingerprint)
    elif fingerprint.title is JINTERFACES.MM:
        return manage_undeploy(fingerengine, fingerprint)
    else:
        utility.Msg("JBoss interfaces %s does not yet support undeploying" %\
                                                fingerprint.title, LOG.ERROR)


def jmx_undeploy(fingerengine, fingerprint):
    """
    """

    context = fingerengine.options.undeploy
    # ensure leading / is stripped
    context = context if not '/' in context else context[1:]
    # check for trailing war
    context = context if '.war' in context else context + '.war'

    url = "http://{0}:{1}/jmx-console/HtmlAdaptor".format(
                    fingerengine.options.ip, fingerprint.port)

    wid = fetchId(context, url)
    if not wid:
        utility.Msg("Could not find ID for WAR {0}".format(context), LOG.ERROR)
        return

    data = OrderedDict([
                    ('action', 'invokeOp'),
                    ('name', 'jboss.web.deployment:war={0},id={1}'.format(context, wid)),
                    ('methodIndex', 0)
                    ])

    response = utility.requests_post(url, data=data)
    if response.status_code == 401:

        utility.Msg("Host %s:%s requires auth, checking..." %
                        (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

        if cookies:
            response = utility.requests_post(url, data=data, cookies=cookies[0],
                                            auth=cookies[1])
        else:
            utility.Msg("Could not get auth for %s:%s" %
                            (fingerengine.options.ip, fingerprint.port), LOG.ERROR)

    if response.status_code == 200:
        utility.Msg("{0} undeployed.  WAR may still show under list".format(context)) 


def fetchId(context, url):
    """ Undeployments require a CSRF token
    """

    response = utility.requests_get(url)
    data = findall("id=(.*?),war={0}".format(context), response.content)
    if len(data) > 0:
        return data[0]


def manage_undeploy(fingerengine, fingerprint):
    """ This is used to undeploy from JBoss 7.x and 8.x
    """

    context = fingerengine.options.undeploy
    context = parse_war_path(context)

    url = 'http://{0}:{1}/management'.format(fingerengine.options.ip,
                                             fingerprint.port)

    undeploy = '{{"operation":"remove", "address":{{"deployment":"{0}"}}}}'\
                                                            .format(context)
    headers = {'Content-Type':"application/json"}
    
    response = utility.requests_post(url, headers=headers, data=undeploy)
    if response.status_code == 401:

        utility.Msg("Host %s:%s requires auth, checking..." %
                            (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookie = checkAuth(fingerengine.options.ip, fingerprint.port,
                           fingerprint.title, fingerprint.version)
        if cookie:
            response = utility.requests_post(url, headers=headers, data=undeploy,
                                            cookies=cookie[0], auth=cookie[1])
        else:
            utility.Msg("Could not get auth for %s:%s" %
                            (fingerengine.options.ip, fingerprint.port), LOG.ERROR)

    if response.status_code == 200:
        utility.Msg("{0} successfully undeployed".format(context), LOG.SUCCESS)
    else:
        utility.Msg("Failed to undeploy", LOG.ERROR)
