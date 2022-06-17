from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *
import math
from Scripts.Tools.Draw import Draw

DEFAULT_MAX_DIST = 10
DEFAULT_SPRINT_DIST = 200
GRAVITY = 9.81
SPHERE_HANDLE = "SPHERE"
RAY_HANDLE = "RAY"
DIST_NAVIGATION = 0.1
@gdclass
class CharHandler(KinematicBody, Draw):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.rotation_angle = 0
		self.y_speed = 0
		self.is_on_ramp=False
		self.sound = 0
		self._push_obj_layer = 0
	
	@gdproperty(NodePath, NodePath())
	def node(self):
		return self._node
	@node.setter
	def node(self, value):
		self._node = value
	
	@gdproperty(NodePath, NodePath())
	def navigation(self):
		return self._navigation
	@navigation.setter
	def navigation(self, value):
		self._navigation = value
	
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
	
	@gdproperty(int, 0, hint = RangeHint(0, 2147483647))
	def push_obj_layer(self):
		return self._push_obj_layer
	@push_obj_layer.setter
	def push_obj_layer(self, value):
		self._push_obj_layer = value
	
	@gdmethod
	def _ready(self):
		self.path = None
		self.current_path_ind = 0
		self.immediate_geometry_init(self, SPHERE_HANDLE)
		self.immediate_geometry_init(self, RAY_HANDLE)
		self.input = Input.instance()
		self.save_rotation = 0
		node = self.get_node(self._node)
		self.animation_tree = AnimationTree.cast(node)
		
		nav = self.get_node(self._navigation)
		self.navigation_obj = Navigation.cast(nav)
		
		#Taken from: https://github.com/godotengine/tps-demo/blob/master/player/player.gd
		self.orientation = self.transform
		self.root_motion =  Transform.new_with_axis_origin(Vector3(1,0,0),Vector3(0,1,0), Vector3(0,0,1), Vector3(0,0,0))
		self.motion = Vector2(0,0)
		self.velocity = Vector3(0,0,0)
		
		#self.orientation.set_basis(self.orientation.get_basis().rotated(Vector3(0,1,0), math.pi*-self.rotation_angle))
		self.orientation.set_basis(Basis.new_with_axis_and_angle(Vector3(0,1,0), math.pi * -self.rotation_angle))
		
		if(self._max_dist == None):
			self._max_dist = DEFAULT_MAX_DIST
		if self._sprint_dist == None:
			self._sprint_dist = DEFAULT_SPRINT_DIST
	
	@gdmethod
	def _process(self, delta):
		self.emit_sound()
	
	@gdmethod
	def _physics_process(self, delta):
		self.handle_ray()
		self.draw_sphere(SPHERE_HANDLE, 2, self.transform.get_origin())
				
		mouse_angle = self.follow_path(delta)
		self.apply_gravity(delta)
		self.animation_tree.set("parameters/Movement/blend_position", Variant(1))
		if(self.path == None):
			mouse_angle = self.mouse_angle()
			self.set_key_pressed()
			self.apply_root_motion(delta, mouse_angle)
			self.animation_tree.set("parameters/Movement/blend_position", Variant(min(1,self.get_speed())))
		
		if(mouse_angle != None):
				self.orientation.set_basis(Basis.new_with_axis_and_angle(Vector3(0,1,0),mouse_angle))	
			
		#print("speed:", self.get_speed())
		self.sound = min(1,self.get_speed())
		
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
		pass
		#print("sound:",self.sound)
		
	def follow_path(self, delta):
		if self.path == None:
			return
		
		if self.current_path_ind >= self.path.size():
			self.path = None
			self.current_path_ind = 0
			return
		pos = self.transform.get_origin()
		dist_vector = self.path[self.current_path_ind] - self.transform.get_origin()
		dist_vector.y = 0
		dist = dist_vector.length()
		print("dist:", dist)
		vel = (self.path[self.current_path_ind] - self.transform.get_origin())
		if dist < DIST_NAVIGATION:
			self.current_path_ind += 1
		print("vel:",vel)
		vel_z = vel.z
		if vel.z == 0:
			vel_z = 0.001
		self.apply_root_motion(delta, math.atan2(vel.x,vel_z))
		return  math.atan2(vel.x,vel_z)
		
	def handle_ray(self):
		self.path = None
		self.current_path_ind = 0
		if self.input.is_action_pressed("mouse_action"):
			ray_length = 100
			mouse_pos = self.get_viewport().get_mouse_position()
			camera = self.get_viewport().get_camera()
			from_ = camera.project_ray_origin(mouse_pos)
			to = from_ - camera.project_ray_normal(mouse_pos) * ray_length
			exclude = Array()
			exclude.append(self)
			
			result = self.get_world().direct_space_state.intersect_ray(from_, 
			from_ + camera.project_ray_normal(mouse_pos) * ray_length,exclude, 
			collision_mask = self.push_obj_layer)
			print("position:", result["position"])
			
			if result["position"] == None:
				return None
			self.draw_sphere(RAY_HANDLE, 0.5, result["position"])
			self.path = self.navigation_obj.get_simple_path(self.get_transform().get_origin(), result["position"])
			self.current_path_ind = 1		
