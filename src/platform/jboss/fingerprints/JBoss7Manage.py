from src.platform.jboss.interfaces import JINTERFACES
from cprint import FingerPrint


class FPrint(FingerPrint):
    
    def __init__(self):
        self.platform = "jboss"
        self.version = "7.0"
        self.title = JINTERFACES.MM
        self.uri = "/console/app/gwt/chrome/chrome_rtl.css"
        self.port = 9990
        self.hash = "bb721162408f5cc1e18cc7a9466ee90c" # tested against 7.0.0 and 7.0.2
