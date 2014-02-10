from src.platform.jboss.interfaces import WebConsoleInterface


class FPrint(WebConsoleInterface):
    
    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "5.0"
