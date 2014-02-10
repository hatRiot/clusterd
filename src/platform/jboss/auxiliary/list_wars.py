from src.platform.jboss.authenticate import checkAuth
from src.platform.jboss.interfaces import JINTERFACES
from auxiliary import Auxiliary
from re import findall
from log import LOG
import utility


class Auxiliary:
    """Obtain deployed WARs through jmx-console
    """

    def __init__(self):
        self.name = "List deployed WARs"
        self.versions = ['Any']
        self.show = True
        self.flag = "jb-list"

    def check(self, fingerprint):
        """
        """

        if fingerprint.title == JINTERFACES.JMX:
            return True
        elif fingerprint.version in ["7.0", "7.1"]:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        """
        """

        utility.Msg("Obtaining deployed applications...")

        if fingerprint.version in ["5.0", "5.1", "6.0", "6.1"] and\
            fingerprint.title == JINTERFACES.JMX:
           url = 'http://{0}:{1}/jmx-console/HtmlAdaptor?action='\
                 'displayMBeans&filter=jboss.web.deployment'.format\
                  (fingerengine.options.ip, fingerprint.port)
        elif fingerprint.version in ["7.0", "7.1"]:
            return self.run7(fingerengine, fingerprint)
        elif fingerprint.title == JINTERFACES.JMX:
            url = 'http://{0}:{1}/jmx-console/'.format(fingerengine.options.ip,
                                               fingerprint.port)
        else:
            # unsupported interface
            utility.Msg("Interface %s version %s is not supported." % \
                            (fingerprint.title, fingerprint.version), LOG.DEBUG)
            return

        response = utility.requests_get(url)
        if response.status_code == 401:
            utility.Msg('Host %s:%s requires auth for JMX, checking...' %
                               (fingerengine.options.ip, fingerprint.port),
                               LOG.DEBUG)
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

            wars = findall("war=(.*?)</a>", response.content)
            if len(wars) > 0:
                for war in wars:
                    utility.Msg("Deployment found: %s" % war)
            else:
                utility.Msg("No deployments found.")


    def run7(self, fingerengine, fingerprint):
        """ JBoss 7.x does not have a jmx-console, and instead uses an 
        HTTP management API that can be queried with JSON.  It's not
        much fun to parse, but it does its job.
        """

        headers = {'Content-Type' : 'application/json'}
        data = '{"operation":"read-resource","address":[{"deployment":"*"}]}'
        url = "http://{0}:{1}/management".format(fingerengine.options.ip,
                                                 fingerprint.port)

        response = utility.requests_post(url, headers=headers, data=data)
        if response.status_code == 401:
            utility.Msg("Host %s:%s requires auth for management, checking..." % 
                                    (fingerengine.options.ip, fingerprint.port),
                                    LOG.DEBUG)

            cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                                fingerprint.title, fingerprint.version)
            if cookies:
                response = utility.requests_post(url, headers=headers, data=data,
                                                 auth=cookies[1])
            else:
                utility.Msg("Could not get auth for %s:%s" % 
                                    (fingerengine.options.ip, fingerprint.port),
                                    LOG.ERROR)
                return

        json_list = response.json()['result']
        for item in json_list:

            item_dict = dict(item)
            if "address" in item_dict.keys():
                utility.Msg("Deployment found: %s" % 
                                    dict(item_dict['address'][0])['deployment'])

        if len(json_list) <= 0:
            utility.Msg("No deployments found.", LOG.INFO)
