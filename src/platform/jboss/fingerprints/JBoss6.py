from src.platform.jboss.interfaces import JINTERFACES
from cprint import FingerPrint


class FPrint(FingerPrint):
    
    def __init__(self):
        self.platform = "jboss"
        self.version = "6.0"
        self.title = JINTERFACES.WM
        self.uri = "/admin-console/plugins/jopr-hibernate-plugin-3.0.0.jar"
        self.port = 8080
        self.hash = "15dd8fe4f62a63b4ecac3dcbbae0a862" 
