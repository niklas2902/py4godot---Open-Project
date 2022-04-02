
from py4godot import *
import math

@gdclass
class CharHandler(KinematicBody):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
		self.rotation_angle = 0
	
	@gdproperty(NodePath, NodePath())
	def node(self):
		return self._node
	@node.setter
	def node(self, value):
		self._node = value
	
	@gdmethod
	def _ready(self):
		self.left_pressed = False
		self.right_pressed = False
		self.up_pressed = False
		self.down_pressed = False
		self.save_rotation = 0
		
		node = self.get_node(self._node)
		self.animation_tree = AnimationTree.cast(node)
		
		#Taken from: https://github.com/godotengine/tps-demo/blob/master/player/player.gd
		self.orientation = self.transform
		self.root_motion =  Transform.new_with_axis_origin(Vector3(1,0,0),Vector3(0,1,0), Vector3(0,0,1), Vector3(0,0,0))
		self.motion = Vector2(0,0)
		self.velocity = Vector3(0,0,0)
		
		#self.orientation.set_basis(self.orientation.get_basis().rotated(Vector3(0,1,0), math.pi*-self.rotation_angle))
		self.orientation.set_basis(Basis.new_with_axis_and_angle(Vector3(0,1,0), math.pi * -self.rotation_angle))
		
		self.input = Input.instance()
	
	@gdmethod
	def _physics_process(self, delta):
		self.apply_root_motion(delta)
		self.set_key_pressed()
		
		is_moving = False
		horizontal_val = self.move_horizontal_val()
		is_moving = is_moving or horizontal_val
		if horizontal_val == -1:
			horizontal_val = 0.5
		elif horizontal_val == 1:
			horizontal_val = -0.5
		
		vertical_val = self.move_vertical_val()
		is_moving = is_moving or vertical_val
		if vertical_val == -1:
			vertical_val = 0
		elif vertical_val == 1:
			vertical_val = 1
		
		self.animation_tree.set("parameters/Movement/blend_position", Variant(Vector2(int(is_moving),0)))
		if(is_moving):
			self.save_rotation = math.pi * (horizontal_val + vertical_val)
		self.orientation.set_basis(Basis.new_with_axis_and_angle(Vector3(0,1,0),self.save_rotation))	
		
	def apply_root_motion(self, delta):
		# Taken from: https://github.com/godotengine/tps-demo/blob/master/player/player.gd
		# and https://www.youtube.com/watch?v=2AUMMmTNijg&list=LL&index=1
		
		self.root_motion = self.animation_tree.get_root_motion_transform()
		self.orientation *= self.root_motion
		
		h_velocity = self.orientation.get_origin()/delta
		self.velocity.set_axis(0,h_velocity.get_axis(0))
		self.velocity.set_axis(2,h_velocity.get_axis(2))
		# Fix -1 in movement
		self.velocity = self.move_and_slide(self.velocity*-1*delta,Vector3(0,1,0))		
		self.orientation.set_origin(Vector3(0,0,0))
		self.orientation = self.orientation.orthonormalized()
		
		trans = Transform(self.orientation.get_basis(), self.global_transform.get_origin())
		self.global_transform = trans
	
	def move_vertical_val(self):
		val = 0
		if self.up_pressed and self.down_pressed:
			val = 0
		elif not self.up_pressed and self.down_pressed:
			val = 1
		elif self.up_pressed and not self.down_pressed:
			val = -1
		
		return val
	
	def move_horizontal_val(self):
		val = 0
		if self.left_pressed and self.right_pressed:
			val = 0
		elif not self.left_pressed and self.right_pressed:
			val = 1
		elif self.left_pressed and not self.right_pressed:
			val = -1
		
		return val
	def set_key_pressed(self):
		"""Function for setting pressed keys"""
		self.left_pressed = self.input.is_key_pressed(GlobalConstants.KEY_A)
		self.right_pressed = self.input.is_key_pressed(GlobalConstants.KEY_D)
		self.up_pressed = self.input.is_key_pressed(GlobalConstants.KEY_W)
		self.down_pressed = self.input.is_key_pressed(GlobalConstants.KEY_S)
