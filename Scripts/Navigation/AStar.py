from py4godot import *
from typing import Optional

WALKABLE_GROUP = "walkable"
@gdclass
class AStar(Spatial):

	def __init__(self):
		# Don't call any godot-methods here
		super().__init__()
		self.astar: Optional[AStar] = None
		self.walkables: Optional[Array] = None

	@gdmethod
	def _ready(self):
		self.astar = AStar._new()
		self.walkables = self.get_tree().get_nodes_in_group(WALKABLE_GROUP)
		print("#######################py_script:",self.get_pyscript())
		self.get_pyscript().method()
		self.generate_points()
	
	def method(self):
		print("method")

	def generate_points(self)->None:
		"""Here we are generating all the points we could later use for astar"""
		for walkable in self.walkables:
			mesh: Optional[MeshInstance] = self.get_mesh(walkable)
			if (not mesh):
				continue
			aabb: AABB = mesh.get_transformed_aabb()
			print("Python AABB:", aabb, aabb.has_no_area())

	def get_mesh(self, node:Node) -> Optional[MeshInstance]:
		for child in node.get_children():
			print("Node:", child)
			if isinstance(child, MeshInstance):
				print("return")
				return child

	def generate_point_connections(self)->None:
		"""Here we generate the connections between the points, the player can walk"""
		pass