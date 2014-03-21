from src.platform.railo.interfaces import DefaultServer


class FPrint(DefaultServer):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "4.0"
