from src.platform.jboss.interfaces import JINTERFACES
from requests import exceptions
from cprint import FingerPrint
from log import LOG
import utility


class FPrint(FingerPrint):

    def __init__(self):
        self.platform = "jboss"
        self.version = "8.1"
        self.title = JINTERFACES.MM
        self.uri = "/console/app/community.css"
        self.port = 9990
        self.hash = "1e4a0817a2d5fd8e2eed4afddb8673b1"
