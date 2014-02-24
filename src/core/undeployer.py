from importlib import import_module
from log import LOG
import utility

def run(fingerengine):
    """ Undeploying is much simpler than deploying; we have a single undeploy
    file that supports a list of interfaces.
    """

    try:
        undeployer = import_module("src.platform.%s.undeployer" % fingerengine.service)
    except:
        utility.Msg("No undeployer found for platform %s" % fingerengine.service, LOG.ERROR)
        return

    for fingerprint in fingerengine.fingerprints:

        if fingerprint.title in undeployer.titles:
            undeployer.undeploy(fingerengine, fingerprint)
            return

    utility.Msg("No valid fingerprints were found to undeploy.", LOG.ERROR)
