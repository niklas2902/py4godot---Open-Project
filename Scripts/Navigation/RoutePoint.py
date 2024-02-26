from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.generated4_core import Vector3, Color
from py4godot.pluginscript_api.utils.annotations import *

from Scripts.Tools.Draw import Draw


@gdclass
class RoutePoint(Node3D, Draw):
	route_points: list[Node3D]
	current_route_index: int

	@gdmethod
	def _ready(self) -> None:
		self.immediate_geometry_init(self, "sphere")

	def _process(self, delta: float) -> None:
		self.draw_sphere("sphere", 1, self.global_position, Color.new3(1, 0, 0))
