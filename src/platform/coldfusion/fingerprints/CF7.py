from src.platform.coldfusion.interfaces import CINTERFACES
from cprint import FingerPrint

class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "coldfusion"
        self.version = "7.0"
        self.title = CINTERFACES.CFM
        self.uri = "/CFIDE/administrator/images/AdminColdFusionLogo.gif"
        self.port = 80
        self.hash = "620b2523e4680bf031ee4b1538733349"
