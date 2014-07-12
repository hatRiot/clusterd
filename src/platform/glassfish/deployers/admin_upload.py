from src.platform.glassfish.authenticate import checkAuth
from src.platform.glassfish.interfaces import GINTERFACES
from src.module.deploy_utils import parse_war_path
from os.path import abspath
from log import LOG
import utility
import json


versions = ['4.0']
title = GINTERFACES.GAD
def deploy(fingerengine, fingerprint):
    """ Upload via the exposed REST API
    """
    
    war_file = fingerengine.options.deploy
    war_path = abspath(war_file)
    war_name = parse_war_path(war_file)
    dip = fingerengine.options.ip
    headers = {
            "Accept" : "application/json",
            "X-Requested-By" : "requests"
    }

    cookie = checkAuth(dip, fingerprint.port, title)
    if not cookie:
        utility.Msg("Could not get auth to %s:%s" % (dip, fingerprint.port),
                                                     LOG.ERROR)
        return

    utility.Msg("Preparing to deploy {0}...".format(war_file))
    base = 'https://{0}:{1}/management/domain/applications/application'\
                                        .format(dip, fingerprint.port)

    data = {
            "id" : open(war_path, 'rb'),
            'force' : 'true'
    }

    response = utility.requests_post(base, files=data,
                                    auth=cookie,
                                    headers=headers)
    if response.status_code is 200:
        utility.Msg("Deployed {0} to :8080/{0}".format(war_name), LOG.SUCCESS)
    else:
        utility.Msg("Failed to deploy {0} (HTTP {1})".format(war_name,
                                                 response.status_code),
                                                 LOG.ERROR)
