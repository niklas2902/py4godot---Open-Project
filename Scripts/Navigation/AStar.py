from py4godot import *
from typing import Optional

WALKABLE_GROUP = "walkable"
GRIDSIZE	   = 0.1
SCALE 		   = 1000

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
			self.generate_squares(aabb)
			print("Python AABB:", aabb, aabb.has_no_area())

	def generate_squares(self, box_to_fill:AABB) -> None:
		""" Generate objects at matching points """
		print(box_to_fill)
		print(box_to_fill.get_size())
		print(box_to_fill.get_position())
		for x in range(int(box_to_fill.get_position().x * SCALE),
					   int((box_to_fill.get_position().x + box_to_fill.get_size().x)*SCALE),
					   int(GRIDSIZE * SCALE)):
			for z in range(int(box_to_fill.get_position().z * SCALE),
						   int((box_to_fill.get_position().z + box_to_fill.get_size().z)*SCALE),
						   int(GRIDSIZE * SCALE)):
				print("x:",x/SCALE, "|", "z:", z/SCALE)
	def get_mesh(self, node:Node) -> Optional[MeshInstance]:
		for child in node.get_children():
			print("Node:", child)
			if isinstance(child, MeshInstance):
				print("return")
				return child

	def generate_point_connections(self)->None:
		"""Here we generate the connections between the points, the player can walk"""
		pass
