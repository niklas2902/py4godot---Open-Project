from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *

@gdclass
class PlayerCam(Camera):
	def __init__(self):
		super().__init__()
		self._player_path = None
		self._y_offset = 0
		self._z_offset = 0
	
	@gdproperty(NodePath, NodePath())
	def player_path(self):
		return self._player_path
	@player_path.setter
	def player_path(self, value):
		self._player_path = value

	@gdmethod
	def _ready(self):
		self.player = KinematicBody.cast(self.get_node(self.player_path))
		self._z_offset = -(self.player.transform.get_origin().get_axis(2) - self.transform.get_origin().get_axis(2))
		self._y_offset = -(self.player.transform.get_origin().get_axis(1) - self.transform.get_origin().get_axis(1))
	@gdmethod
	def _process(self, delta):
		self.transform.set_origin(self.player.transform.get_origin() + Vector3(0,self._y_offset,self._z_offset))



