import typing
from typing import cast

from py4godot import *

MOUSE_ACTION = "mouse_action"

@gdclass
class PlayerCam(Camera):
	def __init__(self):
		super().__init__()
		print("__init__camera")
		self._player_path:NodePath = None
		self._y_offset:float = 0
		self._z_offset:float = 0
		self.scale_multiply:float = 1
		self.is_zooming_in:bool = False
		self.is_key_down:bool = False
		print("end_init_camera")

	prop("scale_multipy", int, 1)
	register_signal("zoomed_out")
	register_signal("zoomed_in")
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

		self.start:Variant = Variant(1)
		self.end:Variant = Variant(10)
		self.duration = 10
		print("end_ready_camera")
		
		self.tween = self.create_tween()
	@gdmethod
	def _process(self, delta:float):
		self.transform.set_origin(self.player.transform.get_origin() + Vector3(0,self._y_offset,self._z_offset) * self.scale_multiply)
		self.handle_zoom_input()
	@gdmethod
	def handle_zoom_input(self):
		input = Input.instance()
		if(input.is_action_pressed(MOUSE_ACTION)):
			print("action_pressed")
			self.is_key_down = False
	@gdmethod
	def toggle_zoom(self)->None:
		print("toggle_zoom")

	@gdmethod
	def tween_method(self, value):
		self.scale_multiply = value
		if(self.is_zooming_in and value == 1):
			self.emit_signal("zoomed_in")

	def _on_zoom_in(self)->None:
		print("on_zoom_in")
		print("#############hallo################")
		child:Node = Node.cast(typing.cast(Node,self.get_children()[0]))
		child.call("start_zoom_anim_in")
		self.is_zooming_in = True

	def _on_zoom_out(self)->None:
		child:Node = Node.cast(typing.cast(Node,self.get_children()[0]))
		print(child)
		child.call("start_zoom_anim_out")
		self.emit_signal("zoomed_out")
		self.is_zooming_in = False

