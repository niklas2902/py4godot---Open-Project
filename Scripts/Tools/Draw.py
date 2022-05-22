
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *
import math

RESOLUTION = 20
@gdtool
class Draw(ImmediateGeometry):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		
	
	def draw_cirlce(self, rad):
		print("draw")
		self.clear()
		self.begin(1, ImageTexture._new());
		num_points = RESOLUTION
		alpha = 2*math.pi *(num_points-1) / num_points
		vector_before = Vector3(math.cos(alpha),0, math.sin(alpha)) * rad + Vector3(0,self.transform.get_origin().get_axis(Vector3_Axis.Y.value),0)
		for alpha_part in range(0,num_points):
			alpha = 2*math.pi *alpha_part / num_points
			x = math.cos(alpha)
			y = math.sin(alpha)
			self.add_vertex(Vector3(x,0,y) * rad + Vector3(0,self.transform.get_origin().get_axis(Vector3_Axis.Y.value),0))
			if(vector_before):
				self.add_vertex(vector_before)
			vector_before = Vector3(x,0,y) * rad +  Vector3(0,self.transform.get_origin().get_axis(Vector3_Axis.Y.value),0)
		self.end()

	def draw_sphere(self, rad):
		print("draw")
		self.clear()
		self.begin(1, ImageTexture._new());
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
			self.add_vertex(vector + Vector3(0,self.transform.get_origin().get_axis(Vector3_Axis.Y.value),0))

		self.end()

	def draw_ray(self, origin, direction, length):
		self.clear()
		self.begin(1, ImageTexture._new());
		self.add_vertex(origin)
		self.add_vertex(origin + direction * length)
		self.end()

	def draw_line(self, origin, target):
		self.clear()
		self.begin(1, ImageTexture._new());
		self.add_vertex(origin)
		self.add_vertex(target)
		self.end()
		
	@gdmethod
	def _physics_process(self, delta):
		#self.draw_cirlce(2)
		self.draw_sphere(2)

