import py4godot.classes.Node3D.Node3D as node
from Scripts.Tools.Draw import Draw
from py4godot.classes.generated4_core import *
from py4godot.pluginscript_api.utils.SignalArg import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.utils.print_tools import print_error


@gdclass
class node_3d2(node.Node3D, Draw):
	prop("test_int", int, 5)
	prop("test_float", float, 5.2)
	prop("test_bool", bool, True)
	prop("test_string", str, String.new0())

	signal("test_signal", [SignalArg("test_arg", int)])

	def __init__(self):
		super().__init__()
		self.test = None

	def _ready(self) -> None:
		self.immediate_geometry_init(self, "test")
		self.immediate_geometry_init(self, "test_line")
		self.immediate_geometry_init(self, "test_ray")
		self.immediate_geometry_init(self, "test_circle")

	def _process(self, time: float) -> None:
		self.test_method()

	def test_method(self) -> None:
		print_error("test_method")
		self.draw_sphere("test", 1, self.global_position + Vector3.new3(-2, 0, 0), Color.new3(1, 0, 0))

		self.draw_cirlce("test_circle", self.global_position, 1, Color.new3(1, 0, 0))
		origin: Vector3 = Vector3.new3(1, 1, 0)
		target: Vector3 = Vector3.new3(0, 0, 1)
		self.draw_line("test_line", origin, target)

		self.draw_ray("test_ray", Vector3.new0(), Vector3.new3(1, 0, 0), 10)
