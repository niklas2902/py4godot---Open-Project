
from py4godot import *

@gdclass
class TriggerObj(Spatial):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
		
	@gdmethod
	def trigger_entered(self):
		print("trigger_entered")
	
	@gdmethod
	def trigger_exited(self):
		print("trigger_exited")







