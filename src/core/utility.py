from datetime import date, datetime
from commands import getoutput
from socket import gethostbyname
from log import LOG
import state
import requests

""" Utility functions
"""

def Msg(string, level=LOG.INFO):
    """ Output a formatted message dictated by the level.  The levels are:
            INFO - Informational message, i.e. progress
            SUCCESS - Action successfully executed/completed, i.e. WAR deployed
            ERROR - An error of some sort has occured
            DEBUG - Debugging output
            UPDATE - Status updates, i.e. host fingerprinting completed

    Currently we only support color output on Linux systems.
    """

    output = "[%s] %s" % (timestamp(), string)
    if state.platform == 'linux':
       
        if level is LOG.INFO:
            output = "%s%s%s" % ("\033[32m", output, "\033[0m")
        elif level is LOG.SUCCESS:
            output = "%s%s%s" % ("\033[1;32m", output, "\033[0m")
        elif level is LOG.ERROR:
            output = "%s%s%s" % ("\033[31m", output, "\033[0m")
        elif level is LOG.DEBUG:
            if state.isdebug:
                output = "%s%s%s" % ("\033[34m", output, "\033[0m")
            else:
                output = None
        elif level is LOG.UPDATE:
            output = "%s%s%s" % ("\033[33m", output, "\033[0m")

    if level is LOG.DEBUG and not state.isdebug:
        return

    if output: print output
    log(string)


def log(string):
    """ Logs a string to the state log file.
    """

    if state.flog:
        with open(state.flog, 'a+') as f:
            f.write('[%s] %s\n' % (timestamp(), string))


def header():
    """ Dumps the application header, printed once at startup.
    """

    print '\033[32m\n\t\tclusterd/%s - clustered attack toolkit\033[0m' % version()
    print '\t\t\t\033[33m[Supporting %d platforms]\033[0m' % (len(state.supported_platforms)) 
    print ''


def version():
    """ clusterd version string, which is printed in the header and will
    be used when checking for updates.
    """

    return "0.5"


def timestamp():
    """ Returns a timestamp in the format year-month-day time
    """

    return '%s %s' % (date.today().isoformat(),
                            datetime.now().strftime('%I:%M%p'))


def local_address():
    """ Return local adapter's IP address.  If a specific adapter
    is specified, we grab that one, else we grab the first adapter's
    IP address in the list.

    If this turns out to cause issues for other platforms, we may
    want to look into third party modules, such as netinet
    """
    
    adapter = None        
    ifconfig = getoutput("/sbin/ifconfig")
    if state.listener:
        ifconfig = ifconfig.split("\n")
        for idx in xrange(len(ifconfig)):
            if state.listener in ifconfig[idx]:
                adapter = ifconfig[idx+1].split()[1][5:]
    else:
        adapter = ifconfig.split("\n")[1].split()[1][5:]

    if not adapter:
        Msg("Unable to find adapter %s" % state.listener, LOG.ERROR)

    return adapter


def check_admin():
    """ Check whether the running user has sufficient
    privileges to execute "privileged" actions; this equates to
    root on linux and administrator on windows
    """

    isAdmin = False
    import ctypes, os
    try:
        isAdmin = os.getuid() == 0
    except AttributeError:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return isAdmin


def build_request(args, kwargs):
    """ This function is used for building requests' objects by adding
    state-wide arguments, such as proxy settings, user agents, and more.
    All requests are built using this function.
    """

    if state.proxy:
        (proxy, server, port) = state.proxy.split(":")
        connection = "{0}:{1}:{2}".format(proxy, server, port)
        if state.proxy_auth:
            (usr, pswd) = state.proxy_auth.split(":")
            connection = "{0}://{1}:{2}@{3}:{4}".format(proxy, usr, pswd, server, port)
        kwargs['proxies'] = dict({proxy:connection})

    if state.random_agent:
        ua = {'User-Agent' : state.random_agent}
        if 'headers' in kwargs:
            kwargs['headers'].update(ua)
        else:
            kwargs['headers'] = ua

    # enable https connections; it's kind of a transparent way of upgrading all
    # existing URL strings, and may not be the best solution.  TODO?
    if state.ssl:
        if "http" in args[0] and "https" not in args[0]:
            args = (args[0].replace("http", "https", 1), )

    if not 'timeout' in kwargs.keys():
        kwargs['timeout'] = state.timeout

    kwargs['verify'] = False
    return (args, kwargs)


def requests_get(*args, **kwargs):
    """ Generate a GET request
    """

    (args, kwargs) = build_request(args, kwargs)
    Msg("Making GET request to {0} with arguments {1}".format(args[0], kwargs),
                                                       LOG.DEBUG)
    return requests.get(*args, **kwargs)


def requests_post(*args, **kwargs):
    """ Generate a POST request
    """

    (args, kwargs) = build_request(args, kwargs)
    Msg("Making POST request to {0} with arguments {1}".format(args[0], kwargs),
                                                        LOG.DEBUG)
    return requests.post(*args, **kwargs)


def requests_head(*args, **kwargs):
    """ Generate a HEAD request
    """

    (args, kwargs) = build_request(args, kwargs)
    Msg("Making HEAD request to {0} with args {1}".format(args[0], kwargs),
                                                   LOG.DEBUG)
    return requests.head(*args, **kwargs)


def requests_put(*args, **kwargs):
    """ Generate a PUT request
    """

    (args, kwargs) = build_request(args, kwargs)
    Msg("Making PUT request to {0} with args {1}".format(args[0], kwargs),
                                                  LOG.DEBUG)
    return requests.put(*args, **kwargs)


def requests_delete(*args, **kwargs):
    """ Generate a DELETE request
    """

    (args, kwargs) = build_request(args, kwargs)
    Msg("Making DELETE request to {0} with args {1}".format(args[0], kwargs),
                                                     LOG.DEBUG)
    return requests.delete(*args, **kwargs)


def capture_input(output_string):
    """ Capture and return user input
    """

    try:
        tmp = raw_input(' \033[1;37m[%s] %s > \033[0m' % (timestamp(), output_string))
    except KeyboardInterrupt:
        return ''
    return tmp


def resolve_host(hostname):
    """ Attempts to resolve a hostname into an IP address
    """

    try:
        ip = gethostbyname(hostname)
    except:
        ip = None
    return ip
