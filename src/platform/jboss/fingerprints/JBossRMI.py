from src.platform.jboss.interfaces import JINTERFACES
from cprint import FingerPrint
from log import LOG
import state
import utility
import socket


class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "jboss"
        self.version = "Any"
        self.title = JINTERFACES.RMI
        self.uri = None
        self.port = 4444
        self.hash = None

    def check(self, ip, port = None):
        """
        """

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(state.timeout)
            res = sock.connect_ex((ip, self.port))
            
            if res == 0:
                return True

        except Exception, e:
            utility.Msg(e, LOG.ERROR)

        return False
