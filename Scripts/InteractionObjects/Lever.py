
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

@gdclass
class Lever(StaticBody):

	def __init__(self)->None:
		#Don't call any godot-methods here
		super().__init__()
		self._activated:bool = False
	
	@gdmethod
	def ready(self)->None:
		self._activated = self.activated
		print("Activated:", self._activated)

	prop("activated",int, 0, hint=FlagsHint("on"))

