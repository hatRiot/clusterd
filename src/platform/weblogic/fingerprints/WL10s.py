from src.platform.weblogic.interfaces import WINTERFACES, WLConsole


class FPrint(WLConsole):
    """ WebLogic 10 is bugged when using Oracle's custom implementation of SSL.
    Only if the default Java implementation is set will this work; otherwise,
    Oracle sends an SSL23_GET_SERVER_HELLO and breaks OpenSSL.
    """
        
    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "10"
        self.title = WINTERFACES.WLS
        self.port = 9002
        self.ssl = True
