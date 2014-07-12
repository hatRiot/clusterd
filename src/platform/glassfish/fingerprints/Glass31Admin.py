from src.platform.glassfish.interfaces import ManagerInterface


class FPrint(ManagerInterface):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = '3.1'
