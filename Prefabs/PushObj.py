
from py4godot import *

@gdclass
class PushObj(StaticBody):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
	@gdmethod
	def _ready(self):
		print("_init")

	@gdmethod
	def _process(self, delta):
		print(delta)

