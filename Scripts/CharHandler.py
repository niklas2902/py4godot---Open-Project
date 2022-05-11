
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
import math

DEFAULT_MAX_DIST = 10
DEFAULT_SPRINT_DIST = 200
GRAVITY = 9.81
@gdclass
class CharHandler(KinematicBody):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = Vector3(0,0,0)
		self.rotation_angle = 0
		self.y_speed = 0
		self.is_on_ramp=False
		self.sound = 0
	
	@gdproperty(NodePath, NodePath())
	def node(self):
		return self._node
	@node.setter
	def node(self, value):
		self._node = value

	@gdproperty(NodePath, NodePath())
	def raycast(self):
		return self._raycast
	@node.setter
	def raycast(self, value):
		self._raycast = value

	
	@gdproperty(float, DEFAULT_MAX_DIST)
	def max_dist(self):
		return self._max_dist
	@max_dist.setter
	def max_dist(self, value):
		self._max_dist= value
	
	@gdproperty(float, DEFAULT_SPRINT_DIST)
	def sprint_dist(self):
		return self._sprint_dist
	@sprint_dist.setter
	def sprint_dist(self, value):
		self._sprint_dist= value
	
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
		
		if(self._max_dist == None):
			self._max_dist = DEFAULT_MAX_DIST
		if self._sprint_dist == None:
			self._sprint_dist = DEFAULT_SPRINT_DIST
	
	@gdmethod
	def _process(self, delta):
		self.emit_sound()
		self.handle_ray()
	
	@gdmethod
	def _physics_process(self, delta):
		mouse_angle = self.mouse_angle()
		self.apply_root_motion(delta, mouse_angle)
		self.apply_gravity(delta)
		self.set_key_pressed()
		
		#print("speed:", self.get_speed())
		self.sound = min(1,self.get_speed())
		self.animation_tree.set("parameters/Movement/blend_position", Variant(min(1,self.get_speed())))
		if(mouse_angle != None):
			self.orientation.set_basis(Basis.new_with_axis_and_angle(Vector3(0,1,0),mouse_angle))	
	
	@gdmethod
	def entered_ramp(self):
		self.is_on_ramp=True
	
	def exited_ramp(self):
		self.is_on_ramp=False
	
	def apply_gravity(self, delta):
		"""applying gravity to the player"""
		if(not self.is_on_floor()) and not self.is_on_ramp:
			self.y_speed += GRAVITY
			self.move_and_slide(Vector3(0,self.y_speed,0)*-1*delta,Vector3(0,1,0))
		else:
			self.y_speed = 0
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
		"""Getting the angle of the mouse to be able to move to a position"""
		if self.input.is_action_pressed("mouse_action"):
			mouse_pos = self.get_viewport().get_mouse_position()
			object_pos = self.get_viewport().get_camera().unproject_position(self.transform.get_origin())
				
			return (mouse_pos - object_pos).length() / self.sprint_dist
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
	
	def emit_sound(self):
		print("sound:",self.sound)
		
	
	def handle_ray(self):
		ray_length = 100
		mouse_pos = self.get_viewport().get_mouse_position()
		camera = self.get_viewport().get_camera()
		from_ = camera.project_ray_origin(mouse_pos)
		to = from_ - camera.project_ray_normal(mouse_pos) * ray_length
		exclude = Array()
		#exclude.append(self)
		result = self.get_world().direct_space_state.intersect_ray(from_, self.global_transform.get_origin(),exclude)
		print("result:", result.size())
