
from py4godot import *

@gdclass
class PushObj(StaticBody):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
	@gdproperty(int, 5, hint=PropertyHint.GODOT_PROPERTY_HINT_RANGE.value, hint_string="1,100,5,slider")
	def vel(self):
		return self.velocity
	@vel.setter
	def vel(self, value):
		self.velocity = value

	@gdmethod
	def _ready(self):
		print("_init")

	@gdmethod
	def _process(self, delta):
		print(delta)

