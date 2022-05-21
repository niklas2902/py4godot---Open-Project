
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *
import math

@gdtool
class Draw(ImmediateGeometry):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		
	
	def draw_cirlce(self, rad):
		print("draw")
		self.clear()
		self.begin(1, ImageTexture._new());
		num_points = 50
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
	
	@gdmethod
	def _physics_process(self, delta):
		self.draw_cirlce(2)

