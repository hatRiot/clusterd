from auxengine import build_platform_flags
from argparse import ArgumentParser
from random import choice
from log import LOG
import state
import utility
import sys


def parse(arguments):
    """ Parse command line options
    """
    parser = ArgumentParser(usage='./clusterd.py [options]')

    #
    # Connection related command line arguments
    #
    connection = parser.add_argument_group("Connection",
                    description = 'Options for configuring the connection')
    connection.add_argument("-i", help='Server address', action='store',
                            dest='ip', metavar='[ip address]')
    connection.add_argument("-iL", help='Server list', action='store',
                            dest='input_list', metavar='[file]')
    connection.add_argument('-p', help='Server port', action='store',
                            dest='port', type=int, metavar='[port]')
    connection.add_argument('--proxy', help='Connect through proxy [http|https]',
                            action='store', dest='proxy',
                            metavar="[proxy://server:port]")
    connection.add_argument('--proxy-auth', help='Proxy credentials',
                               action='store', dest='proxy_auth',
                           metavar='[username:password]')
    connection.add_argument('--timeout', help='Connection timeout [%ds]' % state.timeout,
                               action='store', dest='timeout',
                               default=state.timeout, metavar='[seconds]')
    connection.add_argument("--random-agent", help='Use a random User-Agent for'\
                            ' requests', action='store_true', dest='random_agent',
                            default=False)
    connection.add_argument("--ssl", help='Force SSL', action='store_true',
                            dest='ssl', default=False)

    #
    # Remote host command line arguments
    #
    remote = parser.add_argument_group('Remote Host',
                        description = 'Settings specific to the remote host')
    remote.add_argument('-a', help='Hint at remote host service',
                    action='store', dest='remote_service',
                    metavar='[%s]' % ('|'.join(state.supported_platforms)))
    remote.add_argument('-o', help='Hint at remote host OS',
                    action='store', dest='remote_os',
                    metavar='[windows|linux]', default='windows')
    remote.add_argument('-v', help='Specific version to test', action='store',
                    dest='version', metavar='[version]', default=None)
    remote.add_argument('--usr-auth', help='Login credentials for service',
                    action='store', dest='usr_auth',
                    metavar='[username:password]')
    remote.add_argument('--fingerprint', help='Fingerprint the remote system',
                    action='store_true', dest='fp', default=False)
    remote.add_argument("--arch", help='Specify remote OS architecture',
                    action='store', dest='arch', default='x86',
                    metavar='[x86|x64]')

    #
    # deploy options
    #
    deploy = parser.add_argument_group("Deploy",
                      description = 'Deployment flags and settings')
    deploy.add_argument("--deploy", help='Deploy to the discovered service',
                    action='store', dest='deploy', metavar='[file]')
    deploy.add_argument("--deployer", help="Specify a deployer to use",
                    action='store', dest='deployer', default=None,
                    metavar='[deployer]')
    deploy.add_argument("--invoke", help="Invoke payload after deployment",
                    action='store_true', dest='invoke_payload', default=False)
    deploy.add_argument("-b", help="Brute force credentials for user [admin]", action='store',
                    dest='bf_user', metavar='[user]', default='admin')
    deploy.add_argument('--wordlist', help='Wordlist for brute forcing passwords',
                    action='store', dest='wordlist', default=None,
                    metavar='[path]')

    #
    # iterate over our supported platforms and build their
    # auxiliary modules
    #
    for platform in state.supported_platforms:

        group = parser.add_argument_group(platform + " modules")
        group = build_platform_flags(platform, group)


    other = parser.add_argument_group("Other",
                            description='Miscellaneous flags')
    other.add_argument("--deploy-list", help="List all available deployers",
                    action='store_true', dest='deploy_list', default=False)
    other.add_argument("--aux-list", help="List all available exploits",
                    action='store_true', dest='aux_list', default=False)
    other.add_argument("--gen-payload", help='Generate a reverse shell payload',
                     action='store', dest='generate_payload',
                     metavar='[host:port] for reverse connection')
    other.add_argument("-d", help='Enable debug output', action='store_true',
                    dest='debug', default=False)
    other.add_argument("-l", help='Log output to file [$time$_log.log]',
                    dest='flog', action='store_true', default=False)

    # parse cli options
    options = parser.parse_args(arguments)

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    #
    # Setup state variables from given flags
    #
    if options.proxy:
        state.proxy = options.proxy

    if options.proxy_auth:
        state.proxy_auth = options.proxy_auth

    if options.debug:
        state.isdebug = True

    if options.usr_auth:
        state.usr_auth = options.usr_auth

    if options.wordlist:
        state.bf_wordlist = options.wordlist

    if options.random_agent:
        # select a random user-agent from the list
        state.random_agent = choice(list(open('./src/lib/user-agents.txt'))).rstrip()
        utility.Msg("Random user agent '%s' selected" % (state.random_agent), LOG.DEBUG)

    state.ssl = options.ssl
    state.bf_user = options.bf_user
    state.flog = ("%s_log.log" % utility.timestamp().replace(' ', '_') if options.flog else None)

    try:
        state.timeout = float(options.timeout)
    except:
        utility.Msg("Timeout value must be an integer.  Defaulting to %d."
                        % state.timeout, LOG.ERROR)

    return options
