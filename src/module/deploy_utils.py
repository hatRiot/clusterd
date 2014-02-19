from src.platform.weblogic.interfaces import WINTERFACES
from time import sleep
from subprocess import Popen, PIPE, check_output
from signal import SIGINT
from os import kill, system
from sys import stdout
from log import LOG
import importlib
import pkgutil
import state
import utility


def _serve(war_file = None):
    """ Launch a SimpleHTTPServer listener to serve up our WAR file
    to the requesting host.  This is used primarily to serve a WAR
    to JBoss' jmx_deployer.

    If war_file is provided, this will make a copy of this file into
    our temp dir and remove it once its been completed.
    """

    try:
        if war_file:
            system("cp %s %s 2>/dev/null" % (war_file, state.serve_dir))

        proc = Popen(["python", "-m", "SimpleHTTPServer"], stdout=PIPE,
                        stderr=PIPE, cwd=state.serve_dir)

        while 'GET' not in proc.stderr.readline():
            sleep(1.0)

        # this might be too short for huge files
        sleep(3.0)

    except Exception, e:
        utility.Msg(e, LOG.DEBUG)
    finally:
        kill(proc.pid, SIGINT)

    if war_file:
        war_name = war_file.rsplit('/', 1)[1]
        # remove our copied file
        system("rm -f %s/%s" % (war_name, state.serve_dir))


def waitServe(servert):
    """ Small function used to wait for a _serve thread to receive
    a GET request.  See _serve for more information.

    servert should be a running thread.
    """

    timeout = 10
    status = False

    try:
        while servert.is_alive() and timeout > 0:
            stdout.flush()
            stdout.write("\r\033[32m [%s] Waiting for remote server to "
                         "download file [%ds]" % (utility.timestamp(), timeout))
            sleep(1.0)
            timeout -= 1
    except:
        timeout = 0

    if timeout is not 10:
        print ''

    if timeout is 0:
        utility.Msg("Remote server failed to retrieve file.", LOG.ERROR)
    else:
        status = True

    return status


def wc_invoke(url, local_url, usr = None, pswd = None):
    """ Invoke the webconsole deployer
    """

    res = None
    try:
        res = check_output(["./webc_deploy.sh", url, local_url, str(usr),
                            str(pswd)],
                            cwd="./src/lib/jboss/webconsole_deploy")
    except Exception, e:
        utility.Msg(e, LOG.DEBUG)
        res = e

    return res


def invkdeploy(version, url, local_url):
    """
    """

    res = None
    try:
        res = check_output(["./invkdeploy.sh", version, url, local_url],
                            cwd="./src/lib/jboss/jmxinvoke_deploy")
    except Exception, e:
        utility.Msg(e, LOG.DEBUG)
        res = e

    return res


def bsh_deploy(arch, url, version, usr = None, pswd = None):
    """ Invoke the BSHDeployer
    """

    res = None
    try:
        res = check_output(["./bshdeploy.sh", url, arch, version,
                                              str(usr), str(pswd)],
                            cwd="./src/lib/jboss/bsh_deploy")
    except Exception, e:
        utility.Msg(e, LOG.DEBUG)
        res = e

    return res


def deploy_list():
    """ Simple function for dumping all deployers for supported
    platforms.  This lists them in the format INTERFACE (name), where
    name is used for matching.
    """

    for platform in state.supported_platforms:

        utility.Msg("Deployers for '%s'" % platform, LOG.UPDATE)
        load = importlib.import_module('src.platform.%s.deployers' % platform)

        # load all deployers
        modules = list(pkgutil.iter_modules(load.__path__))
        if len(modules) <= 0:
            utility.Msg("\tNo deployers found.")
            continue

        for deployer in modules:

            dp = deployer[0].find_module(deployer[1]).load_module(deployer[1])
            utility.Msg("\t%s (%s [%s])" % (dp.title, deployer[1], '|'.join(dp.versions)))


def auxiliary_list():
    """ Lists all platform auxiliary modules
    """

    for platform in state.supported_platforms:

        utility.Msg("Auxiliarys for '%s'" % platform, LOG.UPDATE)
        load = importlib.import_module('src.platform.%s.auxiliary' % platform)

        modules = list(pkgutil.iter_modules(load.__path__))
        if len(modules) <= 0:
            utility.Msg("\tNo auxiliarys found.")
            continue

        for auxiliary in modules:
            
            try:
                aux = auxiliary[0].find_module(auxiliary[1]).load_module(auxiliary[1]).Auxiliary()
            except:
                utility.Msg("Could not load auxiliary module '%s'" % 
                                            auxiliary[1], LOG.DEBUG)

            if not aux.show:
                utility.Msg("\t%s ([%s] --%s)" % (aux.name,
                                            '|'.join(aux.versions), aux.flag))


def parse_war_path(war, include_war = False):
    """ Parse off the raw WAR name for setting its context
    """

    if '/' in war:
        war = war.rsplit('/', 1)[1]

    if include_war:
        return war
    else:
        return war.split('.')[0]
