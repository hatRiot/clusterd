from src.platform.weblogic.interfaces import WINTERFACES
from src.platform.weblogic.authenticate import checkAuth
from src.module.deploy_utils import wlweb_deploy
from os.path import abspath
from log import LOG
import utility

versions = ["10", "11", "12"]
title = WINTERFACES.WLA
def deploy(fingerengine, fingerprint):
    """ Standard deployer over T3 protocol.  The listed versions above
    are the only ones that have been tested, but this likely works back to
    early versions of 10.x, and perhaps even BEA days (8.x/9.x)
    """

    (usr, pswd) = checkAuth(fingerengine.options.ip, fingerprint)
    war_file = abspath(fingerengine.options.deploy)

    if not usr or not pswd:
        utility.Msg("WebLogic deployer requires valid credentials.", LOG.ERROR)
        return

    utility.Msg("Preparing to deploy {0}...".format(war_file))
    
    response = wlweb_deploy(fingerengine.options.ip, fingerprint, war_file,
                            usr, pswd)

    if type(response) is str and "deploy completed on Server" in response:
        utility.Msg("{0} deployed to {1}".format(war_file, 
                                    fingerengine.options.ip), LOG.SUCCESS)
    elif "is already being used" in response.output:
        utility.Msg("{0} appears to already be deployed.".format(war_file),
                                    LOG.ERROR)
    else:
        utility.Msg("Error deploying to server.", LOG.ERROR)
        utility.Msg(response.output, LOG.DEBUG)
