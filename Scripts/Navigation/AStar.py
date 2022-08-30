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

	def generate_points(self)->None:
		"""Here we are generating all the points we could later use for astar"""
		pass

	def generate_point_connections(self)->None:
		"""Here we generate the connections between the points, the player can walk"""
		pass
