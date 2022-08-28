from py4godot import *


@gdclass
class AreaTrigger(Spatial):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
		self.mesh_path:Optional[NodePath] = None
		self.mesh:Optional[CSGMesh] = None
		self.connected_obj:Optional[Spatial] = None
	
	prop("mesh_path", NodePath, NodePath())
	register_signal("trigger_entered")
	register_signal("trigger_exited")
	
	@gdmethod
	def _ready(self):
		self.mesh = CSGMesh.cast(self.get_node(self.mesh_path))
		
	@gdmethod
	def body_entered(self, other:KinematicBody):
		print("body_entered", other)
		self.set_color(Color(0,1,0))
		self.emit_signal("trigger_entered")

	@gdmethod
	def body_exited(self, other:KinematicBody):
		print("body_exited", other)
		self.set_color(Color(1,0,0))
		self.emit_signal("trigger_exited")

	def set_color(self, color:Color)->None:
		print("mesh:",self.mesh)
		print(self.mesh.get_class())
		material:SpatialMaterial = SpatialMaterial.cast(self.mesh.get_material())

		if material == None:
			#print("before new_mat")
			new_mat:SpatialMaterial = SpatialMaterial._new()
			self.mesh.material = new_mat
			material = SpatialMaterial.cast(self.mesh.get_material())

		material.albedo_color = color

	def load_finish_mat(self)->SpatialMaterial:
		return SpatialMaterial.cast(ResourceLoader.instance().load("res://Materials/green.mat"))
	
	def _on_Logic_tree_entered(self)->None:
		print("----------------------tree entered-----------------")
