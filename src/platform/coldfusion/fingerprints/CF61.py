from src.platform.coldfusion.interfaces import AdminInterface


class FPrint(AdminInterface):

    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "6.1"
