from py4godot import *

@gdclass
class PlayerCam(Camera):
	def __init__(self):
		super().__init__()
		print("__init__camera")
		self._player_path:NodePath = None
		self._y_offset:float = 0
		self._z_offset:float = 0
		print("end_init_camera")
	
	@gdproperty(NodePath, NodePath())
	def player_path(self):
		return self._player_path
	@player_path.setter
	def player_path(self, value:NodePath):
		self._player_path = value

	@gdmethod
	def _ready(self):
		print("ready_camera")
		self.player:KinematicBody = KinematicBody.cast(self.get_node(self.player_path))
		self._z_offset = -(self.player.transform.get_origin().get_axis(2) - self.transform.get_origin().get_axis(2))
		self._y_offset = -(self.player.transform.get_origin().get_axis(1) - self.transform.get_origin().get_axis(1))
		print("end_ready_camera")
	@gdmethod
	def _process(self, delta:float):
		self.transform.set_origin(self.player.transform.get_origin() + Vector3(0,self._y_offset,self._z_offset))

	@gdmethod
	def toggle_zoom(self)->None:
		print("toggle_zoom")





