from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *

@gdclass
class PlayerCam(Camera):
	def __init__(self):
		super().__init__()
		self._player_path = None
	
	@gdproperty(NodePath, NodePath())
	def player_path(self):
		return self._player_path
	@player_path.setter
	def player_path(self, value):
		self._player_path = value
	
	@gdmethod
	def _ready(self):
		print("_init Camera")
		self.player = KinematicBody.cast(self.get_node(self.player_path))
		self.start_pos = self.transform.get_origin() - self.player.transform.get_origin()
		self.start_pos.set_axis(0,0)

	@gdmethod
	def _process(self, delta):
		self.transform.set_origin(self.player.transform.get_origin() + self.start_pos)
