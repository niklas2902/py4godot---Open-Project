import typing
from Scripts.TriggerObj import TriggerObj
from typing import Optional

from Scripts.InteractionObjects.ActionObject import ActionObject
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
		self.action_object:Optional[TriggerObj] = None
		self.connected_obj_path:Optional[NodePath] = None

	prop("activated",int, 0, hint=FlagsHint("on"))
	prop("connected_obj_path", NodePath, NodePath())
	
	@gdmethod
	def _ready(self)->None:
		self._activated = bool(self.activated)
		print("Activated:", self._activated)
		self.action_object = typing.cast(TriggerObj, self.get_node(self.connected_obj_path).get_pyscript())

	@gdmethod
	def trigger_connected_object(self)->None:
		self._activated = not self._activated
		self.action_object.action(self._activated)

