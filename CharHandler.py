
from py4godot import *

@gdclass
class CharHandler(KinematicBody):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
	
	@gdproperty(NodePath, NodePath())
	def node(self):
		return self._node
	@node.setter
	def node(self, value):
		self._node = value
	
	@gdmethod
	def _ready(self):
		node = self.get_node(self._node)
		self.animation_tree = AnimationTree.cast(node)
		
		#Taken from: https://github.com/godotengine/tps-demo/blob/master/player/player.gd
		self.orientation =  Transform.new_with_axis_origin(Vector3(1,0,0),Vector3(0,1,0), Vector3(0,0,1), Vector3(0,0,0))
		self.root_motion =  Transform.new_with_axis_origin(Vector3(1,0,0),Vector3(0,1,0), Vector3(0,0,1), Vector3(0,0,0))
		self.motion = Vector2(0,0)
		self.velocity = Vector3(0,0,0)
	
	@gdmethod
	def _physics_process(self, delta):
		
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
