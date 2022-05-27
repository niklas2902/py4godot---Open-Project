
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *
import math


list_draws = []
def draw_cirlce(rad):
	#print("draw")
	geometry = ImmediateGeometry._new()
	list_draws.append(geometry)
	geometry.clear()
	geometry.begin(1, ImageTexture._new());
	num_points = RESOLUTION
	alpha = 2*math.pi *(num_points-1) / num_points
	vector_before = Vector3(math.cos(alpha),0, math.sin(alpha)) * rad + Vector3(0,geometry.transform.get_origin().get_axis(Vector3_Axis.Y.value),0)
	for alpha_part in range(0,num_points):
		alpha = 2*math.pi *alpha_part / num_points
		x = math.cos(alpha)
		y = math.sin(alpha)
		geometry.add_vertex(Vector3(x,0,y) * rad + Vector3(0,geometry.transform.get_origin().get_axis(Vector3_Axis.Y.value),0))
		if(vector_before):
			geometry.add_vertex(vector_before)
		vector_before = Vector3(x,0,y) * rad +  Vector3(0,geometry.transform.get_origin().get_axis(Vector3_Axis.Y.value),0)
	geometry.end()

def draw_sphere(rad):
	geometry = ImmediateGeometry._new()
	list_draws.append(geometry)
	geometry.clear()
	geometry.begin(1, ImageTexture._new());
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
		geometry.add_vertex(vector + Vector3(0,geometry.transform.get_origin().get_axis(Vector3_Axis.Y.value),0))

	geometry.end()

def draw_ray(origin, direction, length):
	geometry = ImmediateGeometry._new()
	list_draws.append(geometry)
	geometry.clear()
	geometry.begin(1, ImageTexture._new());
	geometry.add_vertex(origin)
	geometry.add_vertex(origin + direction * length)
	geometry.end()

def draw_line(origin, target):
	geometry = ImmediateGeometry._new()
	list_draws.append(geometry)
	geometry.clear()
	geometry.begin(1, ImageTexture._new());
	geometry.add_vertex(origin)
	geometry.add_vertex(target)
	geometry.end()


RESOLUTION = 20
@gdtool
class Draw(ImmediateGeometry):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()

	@gdmethod
	def _ready(self):	
		VisualServer.instance().connect('frame_post_draw', self, 'frame_post_draw')
	
	@gdmethod
	def frame_post_draw(self):
		print("post render")
		for draw in list_draws:
			draw.queue_free()
			
		self.list_draws = []
