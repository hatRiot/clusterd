from auxiliary import Auxiliary
from log import LOG
from re import findall
import utility


class Auxiliary:

    def __init__(self):
        self.name = 'Dump host information'
        self.versions = ['All']
        self.flag = 'ax-info'

    def check(self, fingerprint):
        return True

    def run(self, fingerengine, fingerprint):
        """ Dump information about the remote Axis2 server
        """

        utility.Msg("Attempting to retrieve Axis2 info...")

        base = "http://{0}:{1}".format(fingerengine.options.ip, fingerprint.port)
        uri = '/axis2/axis2-web/HappyAxis.jsp'

        try:
            response = utility.requests_get(base + uri)
        except Exception, e:
            utility.Msg("Failed to fetch info: %s" % e, LOG.ERROR)
            return

        if response.status_code is 200:

            data = findall("Properties</h2><pre><table(.*?)</table>", 
                                    response.content.translate(None, "\r\n\t"))
            keys = findall("<th style='border: .5px #A3BBFF solid;'>(.*?)</th>", data[0])
            values = findall("<td style='border: .5px #A3BBFF solid;'>(.*?)</td>", data[0])
            for (k,v) in zip(keys,values):
                utility.Msg("\t%s: %s" % (k, v.replace("&nbsp;", "")))
