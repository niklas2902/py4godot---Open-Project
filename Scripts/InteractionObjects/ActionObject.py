
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

@gdclass
class ActionObject(Node):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0

	def action(self, val:object)->None:
		print("#############Action#################")
