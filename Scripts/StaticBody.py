
from py4godot import *

@gdclass
class TriggerArea(Area):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
	
	
	@gdmethod
	def _ready(self):
		print("I'm alive")

	@gdmethod
	def _process(self, delta):
		print(delta)

