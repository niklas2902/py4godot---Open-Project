from typing import Optional

from py4godot import *

@gdclass
class TriggerObj(Spatial):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
		self.mesh:Optional[CSGMesh] = None

	prop("mesh_path", NodePath, NodePath())

	@gdmethod
	def _ready(self) ->None:
		self.mesh = CSGMesh.cast(self.get_node(self.mesh_path))
	@gdmethod
	def action(self):

		self.set_color(Color(0,0,1))
	def set_color(self, color:Color)->None:
		material:SpatialMaterial = SpatialMaterial.cast(self.mesh.get_material())

		if material == None:
			new_mat:SpatialMaterial = SpatialMaterial._new()
			self.mesh.material = new_mat
			material = SpatialMaterial.cast(self.mesh.get_material())

		material.albedo_color = color
	







