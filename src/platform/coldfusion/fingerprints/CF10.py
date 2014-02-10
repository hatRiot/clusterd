from src.platform.coldfusion.interfaces import CINTERFACES
from cprint import FingerPrint

class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "coldfusion"
        self.version = "10.0"
        self.title = CINTERFACES.CFM
        self.uri = "/CFIDE/administrator/images/loginbackground.jpg"
        self.port = 80
        self.hash = "a4c81b7a6289b2fc9b36848fa0cae83c"
