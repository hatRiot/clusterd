from src.platform.tomcat.interfaces import ManagerInterface


class FPrint(ManagerInterface):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "4.0"
