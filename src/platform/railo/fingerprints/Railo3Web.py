from src.platform.railo.interfaces import WebAdmin


class FPrint(WebAdmin):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "3.0"
