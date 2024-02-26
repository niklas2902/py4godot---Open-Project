from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.generated4_core import Vector3
from py4godot.pluginscript_api.utils.annotations import *


@gdclass
class RouteHolder(Node3D):
	route_points: list[Node3D]
	current_route_index: int

	@gdmethod
	def _ready(self) -> None:
		self.current_route_index = 0
		self.route_points = []
		for child in self.get_children():
			self.route_points.append(child)
		print(len(self.route_points))

	def get_current_route_point(self) -> Vector3:
		return self.route_points[self.current_route_index % len(self.route_points)].global_position

	def increase_point(self) -> None:
		self.current_route_index += 1
		self.current_route_index %= len(self.route_points)
