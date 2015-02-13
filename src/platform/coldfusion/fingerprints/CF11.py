from src.platform.coldfusion.interfaces import CINTERFACES
from cprint import FingerPrint

class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "coldfusion"
        self.version = "11.0"
        self.title = CINTERFACES.CFM
        self.uri = "/CFIDE/administrator/images/loginbackground.jpg"
        self.port = 80
        self.hash = "457c6f1f26d8a030a9301e975663589d"
