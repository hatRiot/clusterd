from src.platform.weblogic.interfaces import WLConsole


class FPrint(WLConsole):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "12"
