from src.platform.weblogic.authenticate import checkAuth
from src.platform.weblogic.interfaces import WINTERFACES
from src.module.deploy_utils import parse_war_path
from collections import OrderedDict
from os.path import abspath
from re import findall
from log import LOG
import utility


versions = ["10", "11", "12"]
title = WINTERFACES.WLA
def deploy(fingerengine, fingerprint):
    """ Multistage process of uploading via the web interface; not as neat
    as using the CLI tool, but now we don't need to rely on any enormous
    libraries.
    """
 
    cookies = checkAuth(fingerengine.options.ip, fingerprint)
    war_file = abspath(fingerengine.options.deploy)
    war_name = parse_war_path(war_file, True)

    if not cookies[0]:
        utility.Msg("This module requires valid credentials.", LOG.ERROR)
        return

    utility.Msg("Preparing to deploy {0}..".format(war_name))

    base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
    if fingerprint.title is WINTERFACES.WLS:
        base = base.replace("http", "https")

    # first step is to upload the application
    uri = "/console/console.portal?AppApplicationInstallPortlet_actionOverride="\
          "/com/bea/console/actions/app/install/uploadApp"
    files = OrderedDict([
                    ('AppApplicationInstallPortletuploadAppPath', (war_name, open(war_file, "rb"))),
                    ('AppApplicationInstallPortletuploadPlanPath', (''))
                    ])
    csrf_token = fetchCSRF(cookies, base)

    data = { "AppApplicationInstallPortletfrsc" : csrf_token}
    response = utility.requests_post(base + uri, files=files, cookies=cookies[0],
                                    data = data) 
    if response.status_code is not 200:
        utility.Msg("Failed to upload (HTTP %d)" % response.status_code)
        return


    utility.Msg("Upload successful, deploying...")

    # second step is to select the recently uploaded app and set path
    path = findall('name="AppApplicationInstallPortletselectedAppPath" id="formFC1"'\
                   ' size="64" value="(.*?)">', response.content)[0]

    uri = "/console/console.portal?AppApplicationInstallPortlet_actionOverride"\
          "=/com/bea/console/actions/app/install/appSelected"
    data = { "AppApplicationInstallPortletselectedAppPath" : path,
             "AppApplicationInstallPortletfrsc" : csrf_token
           }

    response = utility.requests_post(base + uri, cookies=cookies[0], data=data)
    if response.status_code is not 200:
        utility.Msg("Failed to set selected path (HTTP %d)" % response.status_code, LOG.ERROR)
        return

    # third step is set the target type, which is by default Application
    uri = "/console/console.portal?AppApplicationInstallPortlet_actionOverride=/com/"\
          "bea/console/actions/app/install/targetStyleSelected"
    data = { "AppApplicationInstallPortlettargetStyle" : "Application",
             "AppApplicationInstallPortletfrsc" : csrf_token
           }

    response = utility.requests_post(base + uri, cookies=cookies[0], data=data)
    if response.status_code is not 200:
        utility.Msg("Failed to set type (HTTP %d)" % response.status_code, LOG.ERROR)
        return

    # final step; deploy it
    uri = "/console/console.portal?AppApplicationInstallPortlet_actionOverride=/com/"\
          "bea/console/actions/app/install/finish"
    data = {"AppApplicationInstallPortletname" : war_name,
            "AppApplicationInstallPortletsecurityModel" : "DDOnly",
            "AppApplicationInstallPortletstagingStyle" : "Default",
            "AppApplicationInstallPortletplanStagingStyle" : "Default",
            "AppApplicationInstallPortletfrsc" : csrf_token
           }

    try:
        response = utility.requests_post(base + uri, cookies=cookies[0], data=data)
    except:
        pass
    else:
        utility.Msg("Failed to finish deploy (HTTP %d)" % response.status_code, LOG.ERROR)
        return

    utility.Msg("{0} deployed at /{0}/".format(war_name), LOG.SUCCESS)


def fetchCSRF(cookies, base):
    """ Each deploy step requires a CSRF, but it doesn't change throughout the
    entire process, so we'll only need to fetch it once.
    """

    uri = '/console/console.portal?_nfpb=true&_pageLabel=AppApplicationInstallPage'

    response = utility.requests_get(base + uri, cookies=cookies[0])
    if response.status_code is 200:

        data = findall('AppApplicationInstallPortletfrsc" value="(.*?)">', response.content)
        if len(data) > 0:
            return data[0]
