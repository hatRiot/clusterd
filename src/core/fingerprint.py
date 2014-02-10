from os.path import abspath
from log import LOG
import pkgutil
import state
import utility


class FingerEngine:
    """ Fingerprinting engine.  Based on service definitions, attempt
    to discover what service is listening, and run various fingerprint
    tests against it.

    If the user hints at a specific service, attempt to first load only
    that engine.  If unsuccessful, load the rest and attempt them.
    """

    def __init__(self):
        self.service = None
        self.fingerprints = []
        self.options = None

    def definitions(self, ip, port, service):
        """ Load and fingerprint the remote system.
        """

        fpath = [abspath("./src/platform/%s/fingerprints" % service)]

        match_fps = []
        fingerprints = list(pkgutil.iter_modules(fpath))
        for fingerprint in fingerprints:
            fp = fingerprint[0].find_module(fingerprint[1]).load_module(fingerprint[1])
            fp = fp.FPrint()

            if self.options.version: 
                # we're looking for a specific version
                if fp.version is not "Any" and self.options.version not in fp.version:
                    continue

            utility.Msg("Checking %s version %s %s..." % (fp.platform,
                                    fp.version, fp.title))

            if fp.check(ip, port):

                # set fingerprint port to match fingerengine port if defined
                if vars(self.options)['port']:
                    fp.port = self.options.port
                match_fps.append(fp)

        return match_fps

    def check_service(self, service):
        """ Given a service, this will initiate our fingerprinting engine against
        the remote host and return a list of all matched fingerprints.  Successful
        fingerprints will also be dumped to console.
        """

        utility.Msg("Loading fingerprint engine '%s'" % service, LOG.DEBUG)

        matched_fingerprints = self.definitions(self.options.ip, self.options.port, service)
        if len(matched_fingerprints) > 0:
            utility.Msg("Matched %d fingerprints for service %s" %
                                        (len(matched_fingerprints), service))

            for fp in matched_fingerprints:
                utility.Msg("\t%s (version %s)" % (fp.title, fp.version), LOG.SUCCESS)
        else:
            utility.Msg("No fingerprints found for service %s" % service)

        return matched_fingerprints

    def run(self):
        """ Kicks off the fingerprint engine
        """

        utility.Msg("Fingerprinting host '%s'" % self.options.ip, LOG.UPDATE)
        state.hasbf = False

        if self.options.remote_service:
            if self.options.remote_service.lower() not in \
                                            state.supported_platforms:
                utility.Msg("Service '%s' unknown or not supported." %
                    self.options.remote_service, LOG.ERROR)
                return False

            self.service = self.options.remote_service
            utility.Msg("Server hinted at '%s'" % self.options.remote_service)


        # if a service was hinted at, load and test it
        if self.service:
            self.fingerprints = self.check_service(self.service)
        else:
            # load one after the other, stop once we find a match
            for service in state.supported_platforms:

                state.hasbf = False
                matched_fps = self.check_service(service)

                if len(matched_fps) > 0:
                    self.service = service
                    self.fingerprints = matched_fps
                    break
