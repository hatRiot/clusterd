from src.platform.axis2.interfaces import AINTERFACES
from src.platform.axis2.authenticate import checkAuth
from src.module.deploy_utils import parse_war_path
from log import LOG
import utility

titles = [AINTERFACES.DSR]
def undeploy(fingerengine, fingerprint):
    """ Remove a deployed service from the remote Axis2 server
    """

    if fingerprint.version not in ['1.6']:
        utility.Msg("Version %s does not support undeploying via the web interface"
                        % fingerprint.version, LOG.ERROR)
        return

    context = parse_war_path(fingerengine.options.undeploy)
    base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)
    uri = '/axis2/axis2-admin/deleteService?serviceName={0}'.format(context)

    utility.Msg("Preparing to undeploy {0}...".format(context))

    response = utility.requests_get(base + uri)
    if "name=\"password\"" in response.content:
        utility.Msg("Host %s:%s requires auth, checking..." %
                        (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookie = checkAuth(fingerengine.options.ip, fingerprint.port,
                           fingerprint.title, fingerprint.version)

        if cookie:
            response = utility.requests_get(base + uri, cookies=cookie)
        else:
            utility.Msg("Could not get auth for %s:%s" % 
                            (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return

    if "Service doesn't exist" in response.content:
        utility.Msg("Service '%s' not found on server." % context, LOG.ERROR)
    elif 'successfully removed' in response.content: 
        utility.Msg("Successfully undeployed '%s'" % context, LOG.SUCCESS)
    else:
        utility.Msg("Failed to undeploy '%s' (HTTP %d)" % (context, response.status_code),
                                                        LOG.ERROR)
