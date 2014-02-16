from src.platform.weblogic.authenticate import checkAuth
from src.platform.weblogic.interfaces import WINTERFACES
from log import LOG
from re import findall
from requests import exceptions
import utility

titles = [WINTERFACES.WLA, WINTERFACES.WLS]
def undeploy(fingerengine, fingerprint):
    """ Undeploy a deployed application from the remote WL server
    """

    app = fingerengine.options.undeploy
    # ensure it ends with war
    app = app if '.war' in app else app + '.war'

    base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
    if fingerprint.title is WINTERFACES.WLS:
        base = base.replace("http", "https")

    uri = "/console/console.portal?AppApplicationUninstallPortletreturnTo="\
          "AppAppApp&AppDeploymentsControlPortlethandler="\
          "com.bea.console.handles.JMXHandle(\"com.bea:Name=mydomain,Type=Domain\")"
    data = { "all" : "on",
            "AppApplicationUninstallPortletchosenContents" : 
                    "com.bea.console.handles.AppDeploymentHandle%28%22com.bea"\
                    "%3AName%3D{0}%2CType%3DAppDeployment%22%29".format(app),
            "_pageLabel" : "AppApplicationUninstallPage",
            "_nfpb" : "true",
            "AppApplicationUninstallPortletfrsc" : None
           }

    utility.Msg("Host %s:%s requires auth, checking.." % 
                    (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
    cookies = checkAuth(fingerengine.options.ip, fingerprint, True)
    
    if cookies[0]:

        data['AppApplicationUninstallPortletfrsc'] = fetchCSRF(base, cookies[0])

        try:
            utility.requests_post(base + uri, data=data, cookies=cookies[0], timeout=1.0)
        except exceptions.Timeout:
            utility.Msg("{0} undeployed.".format(app), LOG.SUCCESS)
        else:
            utility.Msg("Failed to undeploy {0}".format(app), LOG.ERROR)

    else:
        utility.Msg("Could not get auth for %s:%s" % 
                        (fingerengine.options.ip, fingerprint.port), LOG.ERROR)


def fetchCSRF(base, cookie):
    """ WebLogic does awkward CSRF token stuff
    """

    uri = '/console/console.portal?_nfpb=true&_pageLabel=AppApplicationInstallPage'

    response = utility.requests_get(base+uri, cookies=cookie)
    if response.status_code == 200:

        data = findall('AppApplicationInstallPortletfrsc" value="(.*?)"',
                        response.content)
        if len(data) > 0:
            return data[0]


def fetchDomain(base, cookie):
    """ Fetch the remote domain we're undeploying from
    """

    uri = ""
