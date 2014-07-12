from src.platform.glassfish.authenticate import checkAuth
from src.platform.glassfish.interfaces import GINTERFACES
from src.module.deploy_utils import parse_war_path
from log import LOG
import state
import utility

titles = [GINTERFACES.GAD]
def undeploy(fingerengine, fingerprint):
    """ Undeploying is quite simple via the exposed REST API
    """

    if fingerprint.version in ['3.1', '4.0']:
        state.ssl = True

    base = 'http://{0}:{1}'.format(fingerengine.options.ip,
                                    fingerprint.port)
    context = parse_war_path(fingerengine.options.undeploy)
    cookie = checkAuth(fingerengine.options.ip, fingerprint.port,
                       fingerprint.title)
    headers = {
            "Accept" : "application/json",
            "X-Requested-By" : "requests"
    }

    if not cookie:
        utility.Msg("Could not get auth for %s:%s" %
                       (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
        return

    utility.Msg("Preparing to undeploy %s..." % context)
    uri = '/management/domain/applications/application/%s' % context

    if fingerprint.version in ['3.0']:

        # GF 3.0 doesnt appear to support the DELETE verb
        data = {
                "operation" : "__deleteoperation"
        }

        response = utility.requests_post(base + uri, auth=cookie,
                                         headers=headers,
                                         data=data)
    else:
        response = utility.requests_delete(base + uri, auth=cookie, 
                                         headers=headers)

    if response.status_code is 200:
        utility.Msg("'%s' undeployed successfully" % context, LOG.SUCCESS)
    else:
        utility.Msg("Failed to undeploy %s: %s" % (context, response.content),
                                                  LOG.ERROR)
