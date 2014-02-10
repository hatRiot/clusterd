from src.platform.weblogic.interfaces import WINTERFACES
import src.platform.weblogic.deployers.web_deploy as web_deploy


versions = ["10", "11", "12"]
title = WINTERFACES.WLS
def deploy(fingerengine, fingerprint):
    return web_deploy.deploy(fingerengine, fingerprint)
