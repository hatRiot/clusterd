from src.platform.jboss.authenticate import checkAuth
from src.platform.jboss.interfaces import JINTERFACES
from auxiliary import Auxiliary
from log import LOG
from re import findall
import utility


class Auxiliary:

    def __init__(self):
        self.name = "Dump host information"
        self.versions = ['Any']
        self.show = True
        self.flag = 'jb-info'

    def check(self, fingerprint):
        if fingerprint.title in [JINTERFACES.JMX, JINTERFACES.MM]:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        """ This runs the jboss.system:type=ServerInfo MBean to gather information
        about the host OS.  JBoss 7.x uses the HTTP API instead to query for this
        info, which also happens to give us quite a bit more.
        """

        utility.Msg("Attempting to retrieve JBoss info...")

        if fingerprint.version in ["7.0", "7.1"]:
            # JBoss 7.x uses an HTTP API instead of jmx-console/
            return self.run7(fingerengine, fingerprint)

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        uri = "/jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.system"\
                  ":type=ServerInfo"
        url = base + uri

        response = utility.requests_get(url)
        if response.status_code == 401:

            utility.Msg("Host %s:%s requires auth, checking..." %
                          (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
            cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                                fingerprint.title, fingerprint.version)

            if cookies:
                response = utility.requests_get(url, cookies=cookies[0],
                                                auth=cookies[1])
            else:
                utility.Msg("Could not get auth for %s:%s" %
                            (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
                return

        if response.status_code == 200:

            if fingerprint.version in ["3.0", "3.2"]:
                names = findall("<span class='aname'>(.*?)</span>", response.content.replace('\n',''))[1:]
                data = findall("<pre>(.*?)</pre>", response.content.replace('\n',''))
            
                for (key, value) in zip(names, data):
                    utility.Msg("\t{0}: {1}".format(key, value))

            elif fingerprint.version in ["4.0", "4.2"]:
                data = findall("<td>(.*?)</td>", response.content.replace('\n',''))

                for x in range(9, len(data)-9, 5):
                    utility.Msg("\t{0}: {1}".format(data[x+1].lstrip().rstrip(),
                                      data[x+4].lstrip().rstrip()))

            elif fingerprint.version in ["5.0", "5.1", "6.0", "6.1"]:
                names = findall("<td class='param'>(.*?)</td>", response.content.replace('\n',''))
                data = findall("<pre>(.*?)</pre>", response.content.replace('\n',''))

                for (key, value) in zip(names, data):
                    utility.Msg("\t{0}: {1}".format(key,value.rstrip('').lstrip()))

            else:
                utility.Msg("Version %s is not supported by this module." % 
                                                    fingerprint.version, LOG.ERROR)


    def run7(self, fingerengine, fingerprint):
        """ Runs our OS query using the HTTP API

        NOTE: This does not work against 7.0.0 or 7.0.1 because the platform-mbean 
        was not exposed until 7.0.2 and up. See AS7-340
        """

        url = "http://{0}:{1}/management".format(fingerengine.options.ip,
                                                 fingerprint.port)
        info = '{"operation":"read-resource", "include-runtime":"true", "address":'\
               '[{"core-service":"platform-mbean"},{"type":"runtime"}], "json.pretty":1}'
        headers = {"Content-Type":"application/json"}

        response = utility.requests_post(url, data=info, headers=headers)
        if response.status_code == 401:
                
            utility.Msg("Host %s:%s requires auth, checking..." % 
                            (fingerengine.options.ip, fingerprint.port), LOG.DEBUG)
            cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                                fingerprint.title, fingerprint.version)
            if cookies:
                response = utility.requests_post(url, data=info, cookies=cookies[0],
                                                auth=cookies[1], headers=headers)
            else:
                utility.Msg("Could not get auth for %s:%s" %
                                (fingerengine.options.ip, fingerprint.port), LOG.ERROR)
                return

        if response.status_code == 200:

            result = response.json()['result']
            for key in result.keys():

                if 'system-properties' in key:
                    for skey in result[key].keys():
                        utility.Msg('\t%s: %s' % (skey, result[key][skey]))
                else:
                    utility.Msg('\t%s: %s' % (key, result[key]))

        elif response.status_code == 500:
            utility.Msg("Failed to retrieve system properties, checking if "
                        "this is 7.0.0/7.0.1...")

            info = '{"operation":"read-attribute", "name":"server-state"}'

            response = utility.requests_post(url, data=info, headers=headers)
            if response.status_code == 200:
                utility.Msg("Older version found.  This version is unsupported.")
            else:
                utility.Msg("Failed to retrieve info (HTTP %d)", response.status_code,
                                                                LOG.DEBUG)  
        else:
            utility.Msg("Failed to retrieve info (HTTP %d)" % response.status_code,
                                                              LOG.DEBUG)   
