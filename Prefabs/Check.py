
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

NORTH = 0b0001
SOTH = 0b0010
EAST = 0b0100
WEST = 0b1000

RADIUS:float = 0.5

@gdclass
class Check(Spatial):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self._dir:str = None
		self._orientation:int = 0
		
		self._bool_val:bool = False
	@gdproperty(str, "", hint=EnumHint("north", "south", "east", "west"))
	def direction(self):
		return self._dir
	@direction.setter
	def dir(self, value):
		self._dir = value
		
	
	@gdproperty(int, 0, FlagsHint("north","south", "east", "west"))
	def orientation(self)->int:
		return self._orientation
	@orientation.setter
	def orientation(self, value:int)->None:
		self._orientation = value

	@gdproperty(type(True), False)
	def bool_val(self)->bool:
		return self._bool_val
	@bool_val.setter
	def bool_val(self, value:bool)->None:
		self._bool_val = value
	
	@gdmethod
	def check_collision(self, other:KinematicBody):
		shape:SphereShape = PhysicsServer.instance().create_shape(1)
		shape.set_radius(RADIUS)
		
		params:PhysicsShapeQueryParameters = PhysicsShapeQueryParameters._new()
		params.set_shape(shape)
		print("shape:", shape)
		print("shape_rid:", params.shape_rid.get_id())
		params.set_transform(self.get_transform()) # same transform as parent, just translate
		#params.set_exclude(Array())
		#res = self.get_world().direct_space_state.intersect_shape(params, 1)
		res = self.get_world().direct_space_state.cast_motion(params, Vector3(1,0,0))
		print("res:",res)
		return res.size() > 0
		
	@gdmethod
	def is_north(self):
		return bool(self._orientation & NORTH)
	
	@gdmethod
	def is_south(self):
		return bool(self._orientation & NORTH)
	
	@gdmethod
	def is_east(self):
		return bool(self._orientation & EAST)
	
	@gdmethod
	def is_west(self):
		return bool(self._orientation & WEST)
