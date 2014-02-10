from src.platform.tomcat.interfaces import AppInterface


class FPrint(AppInterface):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "7.0"
