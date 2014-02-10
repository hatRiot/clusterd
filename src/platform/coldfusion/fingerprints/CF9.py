from src.platform.coldfusion.interfaces import CINTERFACES
from cprint import FingerPrint

class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "coldfusion"
        self.version = "9.0"
        self.title = CINTERFACES.CFM
        self.uri = "/CFIDE/administrator/images/loginbackground.jpg"
        self.port = 80
        self.hash = "596b3fc4f1a0b818979db1cf94a82220"
