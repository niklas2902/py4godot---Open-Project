
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *
import math

RESOLUTION = 20

class Draw():

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.immediate_geometry_dict = dict()

	def immediate_geometry_init(self, caller, handle):
		immediate_geometry = ImmediateGeometry._new()
		caller.get_tree().get_root().call_deferred("add_child",immediate_geometry)
		self.immediate_geometry_dict[handle] = immediate_geometry
	@gdmethod
	def draw_cirlce(self,handle,pos, rad):
		immediate_geometry = self.immediate_geometry_dict[handle]
		immediate_geometry.clear()
		immediate_geometry.begin(1, ImageTexture._new());
		num_points = RESOLUTION
		alpha = 2*math.pi *(num_points-1) / num_points
		vector_before = Vector3(math.cos(alpha),0, math.sin(alpha)) * rad + Vector3(0,pos.y,0)
		for alpha_part in range(0,num_points):
			alpha = 2*math.pi *alpha_part / num_points
			x = math.cos(alpha)
			y = math.sin(alpha)
			immediate_geometry.add_vertex(Vector3(x,0,y) * rad + Vector3(0,pos.y,0))
			if(vector_before):
				immediate_geometry.add_vertex(vector_before)
			vector_before = Vector3(x,0,y) * rad +  Vector3(0,pos.y,0)
		immediate_geometry.end()

	def draw_sphere(self,handle, rad, position):
		immediate_geometry = self.immediate_geometry_dict[handle]
		immediate_geometry.clear()
		immediate_geometry.begin(1, ImageTexture._new());
		num_points = RESOLUTION
		alpha = 2*math.pi *(num_points-1) / num_points
		vectors = []
		vector_before = Vector3(math.cos(alpha),0, math.sin(alpha)) * rad
		for alpha_part in range(0,num_points):
			alpha = 2*math.pi *alpha_part / num_points
			x = math.cos(alpha)
			y = math.sin(alpha)
			vectors.append(Vector3(x,0,y) * rad )
			if(vector_before):
				vectors.append(vector_before)
			vector_before = Vector3(x,0,y) * rad

		z_rotation = []
		for vector in vectors:
			z_rotation.append(vector.rotated(Vector3.FORWARD, math.pi/2))

		x_rotation = []
		for vector in vectors:
			x_rotation.append(vector.rotated(Vector3.RIGHT, math.pi/2))
		for vector in vectors + z_rotation + x_rotation:
			immediate_geometry.add_vertex(vector + position)
		immediate_geometry.end()

	@gdmethod
	def draw_ray(self,handle, origin, direction, length):
		immediate_geometry = self.immediate_geometry_dict[handle]
		immediate_geometry.clear()
		immediate_geometry.begin(1, ImageTexture._new());
		immediate_geometry.add_vertex(origin)
		immediate_geometry.add_vertex(origin + direction * length)
		immediate_geometry.end()

	@gdmethod
	def draw_line(self,handle, origin, target):
		immediate_geometry = self.immediate_geometry_dict[handle]
		immediate_geometry.clear()
		immediate_geometry.begin(1, ImageTexture._new());
		immediate_geometry.add_vertex(origin)
		immediate_geometry.add_vertex(target)
		immediate_geometry.end()
"""		
	@gdmethod
	def _physics_process(self, delta):
		self.draw_sphere(2)
"""
