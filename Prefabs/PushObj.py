from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *
from Scripts.Tools.Draw import Draw

ARROW_RAD = 0.5
PUSHLAYER = 7
@gdclass
class PushObj(StaticBody, Draw):
	
	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self._arrow_pszh = None
		self._push_layer:int = PUSHLAYER
		self._is_pushing:bool = False
		self._delta_pushing:Vector3 = Vector3(0,0,0)
		self._arrow_path:NodePath = None
		self._arrows:Node = None
		self._trigger = None
		self.player:KinematicBody = None
		self._direction:string = None


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
	def arrow_path(self)->NodePath:
		return self._arrow_path
	@arrow_path.setter
	def arrow_path(self, value:NodePath)->None:
		self._arrow_path = value


	@gdmethod
	def _ready(self):
		if self._trigger:
			trigger:Node = self.get_node(self._trigger)
			self.trigger_obj:Node = Node.cast(trigger)

		if(self._arrow_path):
			self._arrows = self.get_node(self._arrow_path)
			self._arrows = Node.cast(self._arrows)

		if(not self._arrow_path):
			return
		print("arrows:", self._arrows)
		for child in self._arrows.get_children():
			self.immediate_geometry_init(self, child.get_name())

	@gdmethod
	def _process(self, delta):
		if(not self._arrows):
			return

		#for child in self._arrows.get_children():
		#	self.draw_sphere(child.get_name(), ARROW_RAD, child.global_transform.get_origin())

	@gdmethod
	def start_pushing(self, other:KinematicBody)->None:
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

		self._is_pushing = False

		print(self.get_collision_layer())

		self._direction = self.get_direction(other)
	
	@gdmethod
	def is_move_allowed(self, vector:Vector2)->bool:
		print(vector.get_x(), vector.get_y())
		if(self._direction == "east" or self._direction == "west"):
			if vector.get_x() != 0 :
				return True
		else:
			if vector.get_y() != 0:
				return True
		return False

	def get_direction(self, other:KinematicBody)->None:
		for arrow in self._arrows.get_children():
			res = arrow.callv("check_collision", Array(other)).get_converted_value()
			if res.size() >0:
				return arrow.call("get_direction").get_converted_value()
			
				

	@gdmethod
	def get_triggers(self)->Array:
		return self.trigger_obj.get_children()

	@gdmethod
	def get_delta_pushing(self)->Vector3:
		return self._delta_pushing



