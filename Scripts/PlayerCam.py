from typing import *
import copy

from py4godot import *

MOUSE_ACTION = "mouse_action"
ROTATION_SCALE = 100.

@gdclass
class PlayerCam(Camera):
	def __init__(self):
		super().__init__()
		self.start_origin:Optional[Vector3] = None
		self.start_pos:Optional[Vector3] = None
		print("__init__camera")
		self._player_path:NodePath = None
		self._y_offset:float = 0
		self._z_offset:float = 0
		self.scale_multiply:float = 1
		self.is_zooming_in:bool = False
		self.is_key_down:bool = False
		self.last_mouse_pos: Optional[Vector2] = None
		self.start_mouse_pos: Optional[Vector2] = None
		self.is_zoomed_in:bool = True
		self.is_animating:bool = False
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
		self.player:KinematicBody = KinematicBody.cast(self.get_node(self.player_path))
		self._z_offset = -(self.player.transform.get_origin().get_axis(2) - self.transform.get_origin().get_axis(2))
		self._y_offset = -(self.player.transform.get_origin().get_axis(1) - self.transform.get_origin().get_axis(1))

		self.start:Variant = Variant(1)
		self.end:Variant = Variant(10)
		self.duration = 10

		self.rotate_cam_to_player()
	@gdmethod
	def _process(self, delta:float):
		if not self.is_key_down:
			self.transform.set_origin(self.player.transform.get_origin() + Vector3(0,self._y_offset,self._z_offset) * self.scale_multiply)
		self.handle_zoom_input()
	@gdmethod
	def handle_zoom_input(self):
		input = Input.instance()
		if self.is_zoomed_in or self.is_animating:
			self.is_key_down = False
			return
		if(input.is_action_just_pressed(MOUSE_ACTION)):
			self.init_move_around_cam()

		elif(input.is_action_just_released(MOUSE_ACTION) and self.scale_multiply == 7):
			self.finish_move_around_cam()

		if (input.is_action_pressed(MOUSE_ACTION)):
			self.set_position_of_cam()

			self.rotate_cam_to_player()

	def rotate_cam_to_player(self):
		self.look_at(self.player.global_transform.get_origin(), Vector3(0, 1, 0))

	def set_position_of_cam(self):
		self.last_mouse_pos = self.get_viewport().get_mouse_position()
		self.global_transform.set_origin(self.start_origin)
		self.global_transform.set_origin(self.global_transform.get_origin().rotated(Vector3(0, 1, 0), (
					self.start_mouse_pos.get_x() - self.last_mouse_pos.get_x()) / 100.))
		forward_vector: Vector3 = Vector3(self.global_transform.get_origin().get_axis(0), 0,
										  self.global_transform.get_origin().get_axis(2)).normalized()
		self.global_transform.set_origin(self.global_transform.get_origin().rotated(forward_vector, (
				self.start_mouse_pos.get_y() - self.last_mouse_pos.get_y()) / ROTATION_SCALE))

	def finish_move_around_cam(self):
		self.is_key_down = False
		self.last_mouse_pos = None
		self.global_transform.set_origin(self.start_pos)
		self.rotate_cam_to_player()

	def init_move_around_cam(self):
		self.start_origin = self.global_transform.get_origin()
		self.is_key_down = True
		self.start_mouse_pos = self.get_viewport().get_mouse_position()
		self.start_pos = self.global_transform.get_origin()

	@gdmethod
	def toggle_zoom(self)->None:
		print("toggle_zoom")

	@gdmethod
	def tween_method(self, value):
		self.scale_multiply = value
		if(self.is_zooming_in and value == 1):
			self.emit_signal("zoomed_in")
			self.is_zoomed_in = True

	def _on_zoom_in(self)->None:
		print("on_zoom_in")
		print("#############hallo################")
		child:Node = Node.cast(cast(Node,self.get_children()[0]))
		child.call("start_zoom_anim_in")
		self.is_zooming_in = True
		self.is_animating = True

	def _on_zoom_out(self)->None:
		child:Node = Node.cast(cast(Node,self.get_children()[0]))
		print(child)
		child.call("start_zoom_anim_out")
		self.emit_signal("zoomed_out")
		self.is_zooming_in = False
		self.is_zoomed_in = False
		self.is_animating = True

	def finished_animation(self)->None:
		print("#############finished_zoom###########")
		self.is_animating = False





