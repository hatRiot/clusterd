from src.platform.axis2.interfaces import DefaultServer

class FPrint(DefaultServer):
    
    def __init__(self):
        super(FPrint, self).__init__()
        self.version = '1.4'
