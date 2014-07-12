from requests import exceptions
from cprint import FingerPrint
from log import LOG
from re import findall
import utility


class GINTERFACES:

    GAD = "GlassFish Admin"
    JXR = "GlassFish JMX RMI"
    HD  = "GlassFish HTTP Headers (Unreliable)"


class ManagerInterface(FingerPrint):
    """
    """

    def __init__(self):
        self.platform = "glassfish"
        self.version = None
        self.title = GINTERFACES.GAD
        self.uri = '/'
        self.port = 4848
        self.ssl = True
        self.hash = None

    def check(self, ip, port = None):
        """
        """

        try:
            rport = self.port if port is None else port
            url = "http://{0}:{1}/resource/xx.cs".format(ip, rport)
            main_url = "http://{0}:{1}{2}".format(ip, rport, self.uri)

            response = utility.requests_get(url)
            if response.status_code == 404:

                data = findall("Edition|Server (.*?) *</h3>", response.content)
                if len(data) > 0 and self.version in data[0]:

                    #
                    # The admin interface can be remotely exposed, but not accessible; lets
                    # check for that 
                    #
                    main_r = utility.requests_post(main_url, 
                                    data={"j_username":"admin",
                                          "j_password":"",
                                          "loginButton.DisabledHiddenField":"true"
                                          }
                                    )

                    if 'Secure Admin must be enabled' in main_r.content:
                        utility.Msg("Admin interface version %s discovered, but"
                                    " not remotely accessible." % self.version,
                                    LOG.UPDATE)
                        return False
                
                    return True

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform,
                                                        ip, rport),
                                                        LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                          ip, rport),
                                                          LOG.DEBUG)
        return False
