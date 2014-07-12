from src.platform.glassfish.authenticate import checkAuth
from src.platform.glassfish.interfaces import GINTERFACES
from src.module.deploy_utils import parse_war_path
from os.path import abspath
from log import LOG
import state
import utility
import json


versions = ['3.0', '3.1', '4.0']
title = GINTERFACES.GAD
def deploy(fingerengine, fingerprint):
    """ Upload via the exposed REST API
    """
    
    if fingerprint.version in ['3.1', '4.0']:
        state.ssl = True

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
    base = 'http://{0}:{1}'.format(dip, fingerprint.port)
    uri = '/management/domain/applications/application'

    data = {
            'id' : open(war_path, 'rb'),
            'force' : 'true'
    }

    response = utility.requests_post(base + uri, files=data,
                                    auth=cookie,
                                    headers=headers)
    if response.status_code is 200:

        if fingerprint.version in ['3.0']:

            # GF 3.0 ignores context-root and appends a random character string to
            # the name.  We need to fetch it, then set it as our random_int for
            # invoke support.  There's also no list-wars in here...
            url = base + '/management/domain/applications/application'
            response = utility.requests_get(url, auth=cookie, headers=headers)
            if response.status_code is 200:

                data = json.loads(response.content)
                for entry in data[u"Child Resources"]:
                    if war_name in entry:
                        rand = entry.rsplit('/', 1)[1]
                        rand = rand.split(war_name)[1]
                        fingerengine.random_int = str(rand)

                utility.Msg("Deployed {0} to :8080/{0}{1}".format(war_name, rand),
                                                                     LOG.SUCCESS)
        else:
            utility.Msg("Deployed {0} to :8080/{0}".format(war_name), LOG.SUCCESS)
    else:
        utility.Msg("Failed to deploy {0} (HTTP {1})".format(war_name,
                                                 response.status_code),
                                                 LOG.ERROR)
