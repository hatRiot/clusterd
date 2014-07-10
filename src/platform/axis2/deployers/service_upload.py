from src.platform.axis2.interfaces import AINTERFACES
from src.platform.axis2.authenticate import checkAuth
from src.module.deploy_utils import parse_war_path
from os.path import abspath
from re import findall
from log import LOG
import utility


title = AINTERFACES.DSR
versions = ['1.2', '1.3', '1.4', '1.5', '1.6']
def deploy(fingerengine, fingerprint):
    """ Upload a service via the administrative interface
    """

    cookie = None
    file_path = abspath(fingerengine.options.deploy)
    file_name = parse_war_path(file_path, True)
    dip = fingerengine.options.ip

    cookie = checkAuth(dip, fingerprint.port, title, fingerprint.version)
    if not cookie:
        utility.Msg("Could not get auth to %s:%s" % (dip, fingerprint.port),
                                                    LOG.ERROR)
        return

    utility.Msg("Preparing to deploy {0}".format(file_name))

    base = 'http://{0}:{1}'.format(dip, fingerprint.port)
    uri = '/axis2/axis2-admin/upload'

    payload = {'filename' : open(file_path, 'rb')}

    response = utility.requests_post(base + uri, files=payload, cookies=cookie)
    if response.status_code is 200:
        if 'The following error occurred' in response.content:
            error = findall("occurred <br/> (.*?)</font>", response.content)
            utility.Msg("Failed to deploy {0}.  Reason: {1}".format(file_name,
                                                        error[0]), LOG.ERROR)
        else:
            utility.Msg("{0} deployed successfully to /axis2/services/{1}".
                                format(file_name, parse_war_path(file_path)),
                                LOG.SUCCESS)
    else:
        utility.Msg("Failed to deploy {0} (HTTP {1})".format(file_name, 
                                        response.status_code), LOG.ERROR)
