from src.platform.jboss.interfaces import JMXInterface


class FPrint(JMXInterface):
    
    def __init__(self):
        super(FPrint, self).__init__()
        self.version = "4.0"
