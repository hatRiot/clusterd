from src.platform.weblogic.interfaces import WINTERFACES
from src.platform.weblogic.authenticate import checkAuth
from auxiliary import Auxiliary
from log import LOG
from subprocess import check_output
import utility


class Auxiliary:
    """ Obtain a list of the deployed applications
    """

    def __init__(self):
        self.name = 'List deployed apps'
        self.versions = ['Any']
        self.show = True
        self.flag = 'wl-list'

    def check(self, fingerprint):
        return True

    def run(self, fingerengine, fingerprint):

        (usr, pswd) = checkAuth(fingerengine.options.ip, fingerprint)
        if not usr or not pswd:
            utility.Msg("This module requires valid credentials.", LOG.ERROR)
            return

        utility.Msg("Obtaining deployed applications...")

        try:
            args = ["./list_apps.sh", fingerengine.options.ip, 
                    str(fingerprint.port), usr, pswd]
            if fingerprint.title is WINTERFACES.WLS:
                args.append('ssl')

            res = check_output(args, cwd='./src/lib/weblogic/list_apps')
            if type(res) is str:
                if "There is no application to list" in res:
                    utility.Msg("No applications found deployed.")
                else:
                    output = res.split('\n')[1:-2]
                    for app in output:
                        if "<Notice>" in app:
                            continue

                        utility.Msg("App found: %s" % app.lstrip())
            else:
                utility.Msg("Error fetching applications", LOG.ERROR)
                utility.Msg(res.output, LOG.DEBUG)

        except Exception, e:
            utility.Msg(e, LOG.DEBUG)
