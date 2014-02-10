from src.platform.coldfusion.interfaces import CINTERFACES
from cprint import FingerPrint

class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "coldfusion"
        self.version = "8.0"
        self.title = CINTERFACES.CFM 
        self.uri = "/CFIDE/administrator/images/loginbackground.jpg"
        self.port = 80
        self.hash = "779efc149954677095446c167344dbfc"
