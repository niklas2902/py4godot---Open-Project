from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *


@gdclass
class RouteHolder(Spatial):
	route_points: list[Spatial]
	current_route_index: int

	@gdmethod
	def _ready(self) -> None:
		self.current_route_index = 0
		self.route_points = []
		for child in self.get_children():
			self.route_points.append(child)
		print(len(self.route_points))

	def get_current_route_point(self) -> Vector3:
		return self.route_points[self.current_route_index % len(self.route_points)].get_global_transform().get_origin()

	def increase_point(self) -> None:
		self.current_route_index += 1
		self.current_route_index %= len(self.route_points)
