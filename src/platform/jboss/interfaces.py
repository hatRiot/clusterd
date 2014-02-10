from cprint import FingerPrint
from requests import exceptions
from HTMLParser import HTMLParser
from log import LOG
from re import search
import authenticate
import utility


class JINTERFACES:
    """ JBoss interface 'enums'; exposes a commonality between 
    fingerprints and deployers or auxiliary modules.
    """

    JMX = "JBoss JMX Console"
    WC = "JBoss Web Console"
    WM = "JBoss Web Manager"
    MM = "JBoss Management"
    IN = "JBoss JMX Invoker Servlet"
    RMI = "JBoss RMI Interface"
    STS = "JBoss Status Page"


class WebConsoleInterface(FingerPrint):
    """ This interface defines the Web Console interface for JBoss.
    Only versions 3.x - 5.x have this, and thus will not be available
    or have fingerprints for anything 6.x and up.
    """

    def __init__(self):
        self.platform = 'jboss'
        self.version = None
        self.title = JINTERFACES.WC
        self.uri = "/web-console/ServerInfo.jsp"
        self.port = 8080
        self.hash = None

    def check(self, ip, port = None):
        """ The version string for the web-console is pretty easy to parse out.
        """

        try:
            rport = self.port if port is None else port
            url = "http://{0}:{1}{2}".format(ip, rport, self.uri)

            response = utility.requests_get(url)
            if response.status_code == 401:
                utility.Msg("Host %s:%s requires auth for /web-console, checking.." %
                                    (ip, rport), LOG.DEBUG)

                cookies = authenticate.checkAuth(ip, rport, self.title, self.version)
                if cookies:
                    response = utility.requests_get(url, cookies=cookies[0],
                                                    auth=cookies[1])
                else:
                    utility.Msg("Could not get auth for %s:%s" % (ip, rport), LOG.ERROR)
                    return False

            if "Version: </b>{0}".format(self.version) in response.content:
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


class JMXInterface(FingerPrint):
    """ This interface defines the JMX console fingerprint.  This is only
    available in versions 3.x - 6.x, and is parsed in three different formats.
    """

    def __init__(self):
        self.platform = 'jboss'
        self.version = None
        self.title = JINTERFACES.JMX
        self.uri = "/jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.system%3Atype%3DServer"
        self.port = 8080
        self.hash = None

    def check(self, ip, port = None):
        """ Because the version strings are different across a couple
        different versions, we parse it a little bit different.  Pre-5.x versions
        are simple, as we match a pattern, whereas post-5.x versions require us
        to parse an HTML table for our value.
        """

        re_match = False
        rport = self.port if port is None else port
        url = "http://{0}:{1}{2}".format(ip, rport, self.uri)

        try:

            request = utility.requests_get(url)

            # go check auth
            if request.status_code == 401:
                utility.Msg("Host %s:%s requires auth for JMX, checking..." %
                                                        (ip, rport), LOG.DEBUG)
                cookies = authenticate.checkAuth(ip, rport, self.title, self.version)
                if cookies:
                    request = utility.requests_get(url, cookies=cookies[0],
                                                        auth=cookies[1])
                else:
                    utility.Msg("Could not get auth for %s:%s" % (ip, rport), LOG.ERROR)
                    return False

            if request.status_code != 200:
                return False

            if self.version in ["3.0", "3.2"]:
                match = search("{0}.(.*?)\(".format(self.version), request.content)

                if match and len(match.groups()) > 0:
                    re_match = True

            elif self.version in ["4.0", "4.2"]:
                match = search("{0}.(.*?)GA".format(self.version), request.content)

                if match and len(match.groups()) > 0:
                    re_match = True

            elif self.version in ["5.0", "5.1", "6.0", "6.1"]:
                parser = TableParser()
                parser.feed(request.content)

                if parser.data and self.version in parser.data:
                    re_match = True

            return re_match

        except exceptions.Timeout:
            utility.Msg("{0} timeout to {1}:{2}".format(self.platform,
                                                        ip, rport),
                                                        LOG.DEBUG)
        except exceptions.ConnectionError:
            utility.Msg("{0} connection error to {1}:{2}".format(self.platform,
                                                          ip, rport),
                                                          LOG.DEBUG)
        return re_match


class TableParser(HTMLParser):
    """ Table parser for the jmx-console page; obtains the VersionNumber
    string from the page.  Little bit messy.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = None
        self.in_td = False
        self.vn = False
        self.found = False

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
        elif tag == 'pre' and self.vn:
            self.found = True

    def handle_data(self, data):
        if self.in_td:
            if data == 'VersionNumber':
                self.vn = True

        if self.found:
            self.data = data.rstrip('\r\n ').lstrip('\r\n')
            self.found = False
            self.vn = False

    def handle_endtag(self, tag):
        self.in_td = False
