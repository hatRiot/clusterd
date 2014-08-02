from src.platform.coldfusion.interfaces import CINTERFACES
from cprint import FingerPrint

class FPrint(FingerPrint):

	def __init__(self):
		self.platform = 'coldfusion'
		self.version = "5.0"
		self.title = CINTERFACES.CFM
		self.uri = '/CFIDE/administrator/images/cf50brand.jpg'
		self.port = 80
		self.hash = "589099b3930c65904297d67b609d2154"