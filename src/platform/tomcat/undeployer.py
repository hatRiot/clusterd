from src.platform.tomcat.authenticate import checkAuth
from src.platform.tomcat.interfaces import TINTERFACES
from src.module.deploy_utils import parse_war_path
from log import LOG
import utility

titles = [TINTERFACES.MAN]
def undeploy(fingerengine, fingerprint):
    """
    """

    context = parse_war_path(fingerengine.options.undeploy)
    base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)

    if fingerprint.version in ["7.0", "8.0"]:
        uri = "/manager/text/undeploy?path=/{0}".format(context)
    else:
        uri = "/manager/html/undeploy?path=/{0}".format(context)

    url = base + uri
    utility.Msg("Preparing to undeploy {0}...".format(context))

    response = utility.requests_get(url)
    if response.status_code == 401 or \
               (response.status_code == 405 and fingerprint.version == "8.0"):
        utility.Msg("Host %s:%s requires auth, checking..." % 
                        (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

        if cookies:
            try:
                response = utility.requests_get(url, cookies=cookies[0],
                                                auth=cookies[1])
            except exceptions.Timeout:
                response.status_code = 200

        else:
            utility.Msg("Could not get auth for %s:%s" %
                            (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return

    if response.status_code == 200 and 'Undeployed application at context'\
                                                        in response.content:
        utility.Msg("Successfully undeployed %s" % context, LOG.SUCCESS)
    elif 'No context exists for path' in response.content:
        utility.Msg("Could not find a context for %s" % context, LOG.ERROR)
    else:
        utility.Msg("Failed to undeploy (HTTP %s)" % response.status_code, LOG.ERROR)
