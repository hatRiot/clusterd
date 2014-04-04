from log import LOG
from os.path import abspath
from fingerprint import FingerEngine
import utility
import re
import pkgutil
import state

def detectFileType(inFile):
	#Check to see if file is of type gnmap
	firstLine = inFile.readline()
	secondLine = inFile.readline()
	thirdLine = inFile.readline()

	#Be polite and reset the file pointer
	inFile.seek(0)

	if (firstLine.find('nmap') != -1 and thirdLine.find('Host:') != -1):
		#Looks like a gnmap file - this wont be true for other nmap output types
		#Check to see if -sV flag was used, if not, warn
		if(firstLine.find('-sV') != -1 or firstLine.find('-A') != -1 or firstLine.find('-sSV') != -1):
			return 'gnmap'
		else:
			utility.Msg("Nmap version detection not used! Discovery module may miss some hosts!", LOG.INFO)
			return 'gnmap'
	else:
		return None

'''
Parse a gnmap file into a dictionary. The dictionary key is the ip address or hostname.
Each key item is a list of ports and whether or not that port is https/ssl. For example:
>>> targets
{'127.0.0.1': [[443, True], [8080, False]]}
'''
def parseGnmap(inFile):
	targets = {}
	for hostLine in inFile:
		currentTarget = []
		#Pull out the IP address (or hostnames) and HTTP service ports
		fields = hostLine.split(' ')
		ip = fields[1] #not going to regex match this with ip address b/c could be a hostname
		for item in fields:
			#Make sure we have an open port with an http type service on it
			if item.find('http') != -1 and re.findall('\d+/open',item):
				port = None
				https = False
				'''
				nmap has a bunch of ways to list HTTP like services, for example:
				8089/open/tcp//ssl|http
				8000/closed/tcp//http-alt///
				8008/closed/tcp//http///
				8080/closed/tcp//http-proxy//
				443/open/tcp//ssl|https?///
				8089/open/tcp//ssl|http
				Since we want to detect them all, let's just match on the word http
				and make special cases for things containing https and ssl when we
				construct the URLs.
				'''
				port = item.split('/')[0]

				if item.find('https') != -1 or item.find('ssl') != -1:
					https = True
				#Add the current service item to the currentTarget list for this host
				currentTarget.append([port,https])

		if(len(currentTarget) > 0):
			targets[ip] = currentTarget
	return targets

def doFingerprint(host, port, ssl, service):
	fpath = [abspath("./src/platform/%s/fingerprints" % service)]

	match_fps = []
	fingerprints = list(pkgutil.iter_modules(fpath))
	for fingerprint in fingerprints:
		fp = fingerprint[0].find_module(fingerprint[1]).load_module(fingerprint[1])
		fp = fp.FPrint()
		#Only try to fingerprint if we have a port match
		if fp.check(host, port):
			# set fingerprint port to match fingerengine port if defined
			match_fps.append(fp)

	return match_fps

def runDiscovery(targets,options):
	fingerengine = FingerEngine()
	fingerengine.options = options

	'''Run a fingerprint on each host/port/platform combination'''
	for host in targets:
		utility.Msg("Beginning discovery scan on host %s" % (host))
		for platform in state.supported_platforms: 
			for port in targets[host]:
				for fp in doFingerprint(host,port[0],port[1],platform):
					utility.Msg("\t%s (version %s port %s)" % (fp.title, 
                                                 fp.version, port[0]), LOG.SUCCESS)

def run(options):
	""" 
	This module takes an input file (for now, nmap gnmap output) with host IP addresses
	and ports and runs the clusterd fingerprinting engine on all HTTP/S servers
	identified. All common app server URLs will be checked for each server in order to
	attempt to identify what may be running.
	"""

	"""Read the input file, for now we only support nmap gnmap - should have been run with
	the -sV flag to detect HTTP/S servers on non-standard ports"""
	try:
		targets={}
		inFile = open(options.discovery_file,'r')
		if(detectFileType(inFile) == 'gnmap'):
			targets = parseGnmap(inFile)
		else:
			utility.Msg("Discovery input file does not appear to be in nmap gnmap format", LOG.ERROR)
			return
		inFile.close()
		runDiscovery(targets,options)
	except KeyboardInterrupt:
		pass
	except OSError:
		utility.Msg("Error loading gnmap file for discovery", LOG.ERROR)
