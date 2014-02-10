from src.platform.weblogic.authenticate import checkAuth
from src.platform.weblogic.interfaces import WINTERFACES
from auxiliary import Auxiliary
from subprocess import check_output
from log import LOG
from copy import copy
import utility


class Auxiliary:
    """ This module uses weblogic.Admin to query a list of MBeans for 
    specific sets of data.  We currently pull all properties in the MBean as
    it is much much quicker, then parse up the list based on ranges.  This will
    hopefully be made a bit neater once I figure out how to pull specific 
    MBean properties.  Right now this should dump all relevant host and JVM
    information on a remote WebLogic server
    """

    def __init__(self):
        self.name = 'Gather WebLogic info'
        self.versions = ['Any']
        self.show = True
        self.flag = 'wl-info'

    def check(self, fingerprint):
        return True

    def run(self, fingerengine, fingerprint):

        # MBean types; tuples of (type, (start,end)) where start/end are
        # list values to start/stop parsing at.  Temporary hack until I
        # can figure out if i can pull multiple properties in a single
        # request
        mbeans = [("JVMRuntime", (2,15)), ("ServerRuntime", (2,18))]

        (usr, pswd) = checkAuth(fingerengine.options.ip, fingerprint)
        if not usr or not pswd:
            utility.Msg("This module requires valid credentials.", LOG.ERROR)
            return

        utility.Msg("Attempting to retrieve WebLogic info...")

        try:
        
            args = ["./gettype.sh", fingerengine.options.ip, 
                    str(fingerprint.port), usr, pswd]

            for mbean in mbeans:

                targs = copy(args)
                targs.append(mbean[0])

                if fingerprint.title is WINTERFACES.WLS:
                    targs.append("ssl")

                res = check_output(targs, cwd="./src/lib/weblogic/getinfo")

                if "<Notice>" in res:
                    # get around some buggy output in WL with SSL
                    res = '\n'.join(res.split('\n')[1:])

                if type(res) is str and len(res) > 1:
                    for entry in res.split('\n')[mbean[1][0]:mbean[1][1]]:
                        utility.Msg(entry)
                else:
                    utility.Msg("Error fetching info (%s)" % jvmr, LOG.ERROR)
                    utility.Msg(res.output, LOG.DEBUG)

        except Exception, e:
            utility.Msg(e, LOG.DEBUG)
