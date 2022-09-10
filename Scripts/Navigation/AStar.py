from py4godot import *
import py4godot
from Scripts.Tools.Draw import *
from Scripts.Navigation.AStarPoint import AStarPoint
from typing import Optional, List, Dict

WALKABLE_GROUP     = "walkable"
GRIDSIZE	       = 1
SCALE 		       = 1
DRAW_RAD 	       = 0.2
FLOAT_TOLERANCE	   = 0.1
WEIGHT_SCALE	   = 1

@gdclass
class AStar(Spatial, Draw):

	def __init__(self):
		# Don't call any godot-methods here
		super().__init__()
		self.astar: Optional[py4godot.AStar] = None
		self.walkables: Optional[Array] = None
		self.points:List = []
		self.dict_points:Dict = dict()

	@gdmethod
	def _ready(self):
		self.astar = py4godot.AStar._new()
		self.walkables = self.get_tree().get_nodes_in_group(WALKABLE_GROUP)
		print("#######################py_script:",self.get_pyscript())
		self.get_pyscript().method()
		self.generate_points()

		self.immediate_geometry_init(self, "test")
		self.draw_sphere("test", 5, Vector3(0,0,0))

		print("len_points:", len(self.points))
		for point in self.points:
			print("point_position:",point.id,"|", point.position)
			self.draw_sphere(point.id, DRAW_RAD, point.position)

		print("points:", point)
		for point in self.astar.get_points():
			print(point)
		self.generate_point_connections()
		a = self.astar.get_closest_point(Vector3(0,0,0))
		b = self.astar.get_closest_point(Vector3(0,0,5))
		print("a:", a)
		print("b:", b)

		path:Array = self.astar.get_point_path(a,b)
		print("path:", path)
		for point in path:
			print("Path:", point)
	def method(self):
		print("method")

	def generate_points(self)->None:
		"""Here we are generating all the points we could later use for astar"""
		print("generate_points")
		for walkable in self.walkables:
			mesh: Optional[MeshInstance] = self.get_mesh(walkable)
			print("walkable:", walkable)
			if (not mesh):
				continue
			print("found_mesh")
			aabb: AABB = mesh.get_transformed_aabb()
			self.generate_squares(aabb)
			print("Python AABB:", aabb, aabb.has_no_area())

	def generate_squares(self, box_to_fill:AABB) -> None:
		""" Generate objects at matching points """
		print("#################generate_squares########################")
		print(box_to_fill)
		print(box_to_fill.get_size())
		print(box_to_fill.get_position())
		id_counter:int = 0
		print("range_values:",int(box_to_fill.get_position().x * SCALE),int((box_to_fill.get_position().x + box_to_fill.get_size().x)*SCALE),int(GRIDSIZE * SCALE))
		for x in range(int(box_to_fill.get_position().x * SCALE),
					   int((box_to_fill.get_position().x + box_to_fill.get_size().x)*SCALE),
					   int(GRIDSIZE * SCALE)):
			print("x:", x)
			for z in range(int(box_to_fill.get_position().z * SCALE),
						   int((box_to_fill.get_position().z + box_to_fill.get_size().z)*SCALE),
						   int(GRIDSIZE * SCALE)):
				print("x:",x/SCALE, "|", "z:", z/SCALE)
				point:AStarPoint = AStarPoint(x / SCALE,
								   			  box_to_fill.get_position().y + box_to_fill.get_size().y,
											  z/SCALE,
								   			  id_counter)
				self.points.append(point)
				self.dict_points[point.id] = point
				self.astar.add_point(point.id, point.position, weight_scale=10.)
				id_counter += 1

		for point in self.points:
			self.immediate_geometry_init(self, point.id)
	def get_mesh(self, node:Node) -> Optional[MeshInstance]:
		"""This function is used to get a mesh child from a given Node"""
		for child in node.get_children():
			print("Node:", child)
			if isinstance(child, MeshInstance):
				print("return")
				return child


	def generate_point_connections(self)->None:
		"""Here we generate the connections between the points, the player can walk"""
		for point in self.points:
			for other_point in self.points:
				diff:Vector3 = point.position- other_point.position
				if diff.length() <= math.sqrt(2) * GRIDSIZE + FLOAT_TOLERANCE and other_point != point:
					self.astar.connect_points(point.id, other_point.id)
