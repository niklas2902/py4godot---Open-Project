from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *


@gdclass
class MotionHandler(Spatial):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity:float = 0
		self._turn:float = 0
		self._node:Node = None
	@gdmethod
	def _ready(self):
		print("####################ready####################")
		if(self.turn == None):
			self.turn = 0
		if(self. vel == None):
			self.vel = 0
			
		node = self.get_node(self._node)
		self.animation_tree = AnimationTree.cast(node)
		self.animation_tree.set("parameters/Movement/blend_position", Variant(Vector2(self.vel,self.turn)))
		
	
	@gdproperty(NodePath, NodePath(), hint_string = "AnimationTree")
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
