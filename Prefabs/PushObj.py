from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *
from Scripts.Tools.Draw import Draw

ARROW_RAD = 0.5
PUSHLAYER = 7
@gdtool
class PushObj(StaticBody, Draw):

	@gdproperty(NodePath, NodePath())
	def trigger(self)->NodePath:
		return self._trigger
	@trigger.setter
	def trigger(self, value:NodePath)->None:
		self._trigger = value

	@gdproperty(int, PUSHLAYER)
	def push_layer(self)->int:
		return self._push_layer
	@push_layer.setter
	def push_layer(self, value:int)->None:
		self._push_layer = value


	@gdproperty(NodePath, NodePath())
	def arrows(self)->NodePath:
		return self._arrows
	@arrows.setter
	def arrows(self, value:NodePath):
		self._arrows = value
	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self._arrow_obj = None
		self._push_layer:int = PUSHLAYER
		self._is_pushing:bool = False
		self._delta_pushing:Vector3 = Vector3(0,0,0)
		self._player_path:NodePath = None
		self.player:KinematicBody = None
			
	@gdmethod
	def _ready(self):
		if self._trigger:
			trigger:Node = self.get_node(self._trigger)
			self.trigger_obj:Node = Node.cast(trigger)
		
		print("arrows:", self.arrows)
		if(self._arrows):
			arrows:Node = self.get_node(self.arrows)
			self._arrow_obj:Node = Node.cast(arrows)

		if(not self._arrow_obj):
			return
		for child in self._arrow_obj.get_children():
			self.immediate_geometry_init(self, child.get_name())
			
	@gdmethod
	def _process(self, delta):
		if(not self._arrow_obj):
			return
			
		for child in self._arrow_obj.get_children():
			self.draw_sphere(child.get_name(), ARROW_RAD, child.global_transform.get_origin())
	
	@gdmethod
	def start_pushing(self, other:KinematicBody):
		print("start pushing", other)
		self.set_collision_layer_bit(0, False)
		self.set_collision_layer_bit(1, False)
		self.set_collision_layer_bit(6, True)
		self.set_collision_layer_bit(7, True)
		
		self.set_collision_mask_bit(0, False)
		self.set_collision_mask_bit(1, False)
		self.set_collision_mask_bit(6, True)
		self.set_collision_mask_bit(7, True)
		
		self._delta_pushing = self.global_transform.get_origin() - other.global_transform.get_origin()
		
		print("test_delta_pushing:", self._delta_pushing)
		self._is_pushing = False
		
		print(self.get_collision_layer())
	
	@gdmethod
	def get_triggers(self)->Array:
		return self.trigger_obj.get_children()
	
	@gdmethod
	def get_delta_pushing(self)->Vector3:
		return self._delta_pushing
