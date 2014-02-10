from src.platform.jboss.interfaces import JINTERFACES
from cprint import FingerPrint


class FPrint(FingerPrint):
    
    def __init__(self):
        self.platform = "jboss"
        self.version = "7.1"
        self.title = JINTERFACES.MM
        self.uri = "/console/app/gwt/chrome/chrome_rtl.css"
        self.port = 9990
        self.hash = "14755bd918908c2703c57bd1a52046b6"
