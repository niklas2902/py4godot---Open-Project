
from py4godot import *

@gdclass
class MotionHandler(Spatial):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
		self._turn = 0
		self._node = None
	@gdmethod
	def _ready(self):
		if(self.turn == None):
			self.turn = 0
			
		node = self.get_node(self._node)
		animationTree = AnimationTree.cast(node)
		print(self.vel, self.turn)
		animationTree.set("parameters/Movement/blend_position", Variant(Vector2(self.vel,self.turn)))
		print("get_value",animationTree.get("parameters/Movement/blend_position").get_converted_value())
			
	
	@gdproperty(NodePath, NodePath())
	def node(self):
		return self._node
	@node.setter
	def node(self, value):
		self._node = value
		
	@gdproperty(int, 0)
	def vel(self):
		return self.velocity
	@vel.setter
	def vel(self, value):
		self.velocity = value
	
	@gdproperty(int, 0)
	def turn(self):
		return self._turn
	@turn.setter
	def turn(self, value):
		self._turn = value
