
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
import math

DEFAULT_MAX_DIST = 10
DEFAULT_SPRINT_DIST = 200
DEFAULT_MIN_SPRINT_VEL = 0.1
DEFAULT_WEIGHT = 60
@gdclass
class CharHandler(KinematicBody):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
		self.rotation_angle = 0
		self._weight = 0
		self.is_grounded = True
	
	@gdproperty(NodePath, NodePath())
	def node(self):
		return self._node
	@node.setter
	def node(self, value):
		self._node = value
	
	@gdproperty(float, DEFAULT_MAX_DIST)
	def max_dist(self):
		return self._max_dist
	@max_dist.setter
	def max_dist(self, value):
		self._max_dist= value
	
	@gdproperty(float, DEFAULT_WEIGHT)
	def weight(self):
		return self._weight
	@weight.setter
	def weight(self, value):
		self._weight = value
	
	@gdproperty(float, DEFAULT_SPRINT_DIST)
	def sprint_dist(self):
		return self._sprint_dist
	@sprint_dist.setter
	def sprint_dist(self, value):
		self._sprint_dist= value
	
	@gdproperty(float, DEFAULT_MIN_SPRINT_VEL)
	def min_sprint_vel(self):
		return self._min_sprint_vel
	@min_sprint_vel.setter
	def min_sprint_vel(self, value):
		self._min_sprint_vel= value
	
	@gdmethod
	def _ready(self):
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
		
		#Setting the min velocity
		if(self._max_dist == None):
			self._max_dist = DEFAULT_MAX_DIST
		if self._sprint_dist == None:
			self._sprint_dist = DEFAULT_SPRINT_DIST
		if self._min_sprint_vel == None:
			self._min_sprint_vel = DEFAULT_MIN_SPRINT_VEL
	
	@gdmethod
	def set_grounded(self, val):
		self.grounded = val
	
	@gdmethod
	def _physics_process(self, delta):
		mouse_angle = self.mouse_angle()
		self.apply_root_motion(delta, mouse_angle)
		self.set_key_pressed()
		self.transform.set_origin(self.transform.get_origin() - Vector3(0,1,0)*delta)
		
		print(self.is_on_floor())
		self.animation_tree.set("parameters/Movement/blend_position", Variant(min(1,self.get_speed())))
		if(mouse_angle != None):
			self.orientation.set_basis(Basis.new_with_axis_and_angle(Vector3(0,1,0),mouse_angle))	
		
	def mouse_angle(self):
		"""Getting the angle of the mouse to be able to move to a position"""
		if self.input.is_action_pressed("mouse_action"):
			mouse_pos = self.get_viewport().get_mouse_position()
			object_pos = self.get_viewport().get_camera().unproject_position(self.transform.get_origin())
			if (mouse_pos - object_pos).length() <= self.max_dist:
				return
				
			return math.atan2(object_pos.get_x() - mouse_pos.get_x(),
			object_pos.get_y() - mouse_pos.get_y())
		return
		
	def get_speed(self):
		"""Getting the speed of the player depending on the current mouse position relative to the player"""
		if self.input.is_action_pressed("mouse_action"):
			mouse_pos = self.get_viewport().get_mouse_position()
			object_pos = self.get_viewport().get_camera().unproject_position(self.transform.get_origin())
			if (mouse_pos - object_pos).length() <= self.max_dist:
				# if player arrived at place, stop
				return 0
			return max(self.min_sprint_vel,(mouse_pos - object_pos).length() / self.sprint_dist)
		return 0
	
	def apply_root_motion(self, delta, angle):
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
	
	def set_key_pressed(self):
		"""Function for setting pressed keys"""
		self.left_pressed = self.input.is_key_pressed(GlobalConstants.KEY_A)
		self.right_pressed = self.input.is_key_pressed(GlobalConstants.KEY_D)
		self.up_pressed = self.input.is_key_pressed(GlobalConstants.KEY_W)
		self.down_pressed = self.input.is_key_pressed(GlobalConstants.KEY_S)
