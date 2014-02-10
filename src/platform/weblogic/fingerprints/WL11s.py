from src.platform.weblogic.interfaces import WINTERFACES, WLConsole

class FPrint(WLConsole):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "11"
        self.title = WINTERFACES.WLS
        self.port = 9002
        self.ssl = True
