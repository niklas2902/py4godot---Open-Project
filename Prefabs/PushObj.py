from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

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

