
from py4godot import *

DEFAULT_OFFSET = 5
@gdclass
class PlayerCam(Camera):
	def __init__(self):
		super().__init__()
		self._player_path = None
		self._y_offset = DEFAULT_OFFSET
	
	@gdproperty(NodePath, NodePath())
	def player_path(self):
		return self._player_path
	@player_path.setter
	def player_path(self, value):
		self._player_path = value
	
	@gdproperty(int, DEFAULT_OFFSET, hint=PropertyHint.GODOT_PROPERTY_HINT_RANGE.value, hint_string="1,20,1,slider")
	def y_offset(self):
		return self._y_offset
	@y_offset.setter
	def y_offset(self, value):
		self._y_offset = value

	@gdmethod
	def _ready(self):
		print("_init Camera")
		self.player = KinematicBody.cast(self.get_node(self.player_path))

	@gdmethod
	def _process(self, delta):
		self.transform.set_origin(self.player.transform.get_origin() + Vector3(0,self.y_offset,0))

