from src.platform.weblogic.interfaces import BEAConsole

class FPrint(BEAConsole):
    
    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "8.1"
