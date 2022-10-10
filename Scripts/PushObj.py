from py4godot import *
from Scripts.Tools.Draw import Draw
from typing import Optional

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
		self._arrow_path:Optional[NodePath] = None
		self._arrows:Optional[Node] = None
		self._trigger:Optional[Node] = None
		self.player:Optional[KinematicBody] = None
		self._direction:Optional[str] = None
		self._util:Optional[Node] = None
		self.collision_layer_direction:int = 0
		self.pos_before:Optional[Vector3] = None
		print("init PushObj")
		
	@gdmethod
	def _ready(self):
		self._delta_pushing:Vector3 = Vector3(0,0,0)
		self.pos_before = self.global_transform.get_origin()

	prop("collision_layer_direction",int, 64, RangeHint(0,2**16,1))
	prop("util_path",NodePath, NodePath())
	
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
		self._util = self.get_node(self.util_path)

		if(not self._arrow_path):
			return
		print("arrows:", self._arrows)
		if(self._arrows and self._arrows.get_children()):
			print("arrows_childs:", self._arrows.get_children(), self._arrows.get_children().size())
			for child in self._arrows.get_children():
				self.immediate_geometry_init(self, child.get_name())
		self.immediate_geometry_init(self, "push")

	@gdmethod
	def _process(self, delta):
		if(not self._arrows):
			return

		#for child in self._arrows.get_children():
		#	self.draw_sphere(child.get_name(), ARROW_RAD, child.global_transform.get_origin())

	@gdmethod
	def start_pushing(self, other:KinematicBody)->None:
		print("start pushing", other)
		self.pos_before = self.global_transform.get_origin()

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
		if(self._direction == "east" or self._direction == "west"):
			if vector.get_x() != 0 :
				res = self._util.callv("sphere_cast", 
				Array(self.global_transform.get_origin() + 
				Vector3(vector.get_x(),0,0),
				0.02,Array(self), self.collision_layer_direction)).get_converted_value()

				self.draw_sphere("push", 1, self.global_transform.get_origin() + 
				Vector3(vector.get_x(),0,0))
				return res.size() == 0
		else:
			if vector.get_y() != 0:
				print("vector_y:",vector.get_y())
				res = self._util.callv("sphere_cast",
				Array(self.global_transform.get_origin() + Vector3(0,0,vector.get_y()),
				0.02,Array(self), self.collision_layer_direction)).get_converted_value()
				self.draw_sphere("push", 1, self.global_transform.get_origin() +
				Vector3(0,0,vector.get_y()))
				return res.size() == 0
		return False

	def get_direction(self, other:KinematicBody)->None:

		print("################1111get_direction:")
		min = 1000000
		min_arrow:Optional[Spatial] = None
		for arrow_index in range(0,self._arrows.get_children().size()):
			arrow:Spatial = Spatial.cast(self._arrows.get_children()[arrow_index])
			if((arrow.global_transform.get_origin() - other.global_transform.get_origin()).length() < min):
				min_arrow = arrow
				min = (arrow.global_transform.get_origin() - other.global_transform.get_origin()).length()

		print("min_arrow:", min_arrow)
		print(min_arrow.get_name())
		if min_arrow:
			return min_arrow.call("get_direction").get_converted_value()

				

	@gdmethod
	def get_triggers(self)->Array:
		return self.trigger_obj.get_children()

	@gdmethod
	def get_delta_pushing(self)->Vector3:
		return self._delta_pushing



