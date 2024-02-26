from py4godot.classes.StaticBody3D.StaticBody3D import StaticBody3D
from py4godot.classes.generated4_core import NodePath
from py4godot.pluginscript_api.utils.annotations import *

import typing
from Scripts.TriggerObj import TriggerObj


@gdclass
class Lever(StaticBody3D):
	_activated: bool
	action_object: TriggerObj
	connected_obj_path: NodePath

	def __init__(self) -> None:
		# Don't call any godot-methods here
		super().__init__()

	prop("activated", int, 0)  # , hint=FlagsHint("on"))
	prop("connected_obj_path", NodePath, NodePath())

	@gdmethod
	def _ready(self) -> None:
		self._activated = bool(self.activated)
		print("Activated:", self._activated)
		self.action_object = typing.cast(TriggerObj, self.get_node(self.connected_obj_path).get_pyscript())

	@gdmethod
	def trigger_connected_object(self) -> None:
		self._activated = not self._activated
		self.action_object.action(self._activated)
