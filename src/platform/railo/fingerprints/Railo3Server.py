from src.platform.railo.interfaces import ServerAdmin


class FPrint(ServerAdmin):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "3.0"
