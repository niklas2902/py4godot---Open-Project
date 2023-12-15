import py4godot.classes.Node3D.Node3D as node
from py4godot.classes.generated4_core import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.utils.SignalArg import *
from py4godot.pluginscript_api.hints.BaseHint import *
from py4godot.utils.print_tools import *


@gdclass
class node_3d(node.Node3D):
	prop("test_int", int, 5)
	prop("test_float", float, 5.2)
	prop("test_bool", bool, True)
	prop("test_string", str, String.new0())

	signal("test_signal", [SignalArg("test_arg", int)])

	def __init__(self):
		self.test = None

	def _process(self, time: float):
		pass
		# print_error("Hello from code")
		# print_error("global_position before:", self.global_position.x)
		# v = Vector3.new3(1,2,3)
		# v.x = 1000
		# v2 = Vector3.new0()

		# v_res = v+v2
		# print_error("v_res_x:", v_res.x)

		a = Array.new0()
		a.push_back(1)
		a.push_back(1)
		a.push_back(1)
		print_error("back:")
		b = a.front()
		print_error(b)

		# array = Array.new0()
		# print_error("before push_back")
		# array.push_back(8)
		# print_error("after push_back")
		# back = array.front()
		# print_error("back:", back)
		# print_error("array[0]:", array[0])
		# array[0] = 2
		# print_error("array[0]:", array[0])
		# print_error("x:", v.x)
		# print_error("y:", v.y)
		# self.global_transform.origin.x = 0
		# transform = self.global_transform
		self.global_position.x = 3
		# self.global_transform = transform
		# self.global_position.x = 100
		# self.test_global_transform()
		# scale = self.global_transform.basis.get_scale()
		# print_error("x:", scale.x)
		# print_error("y:", scale.y)
		# print_error("z:", scale.z)
		# print_error("instance_id:",self.get_instance_id())
		# print_error("py_script:",self.get_pyscript())
		# print_error(self.global_transform.origin.y)

		# self.global_position = v
		dict = Dictionary.new0()
		dict["1"] = 2
		# dict.get("1")
		print_error("dict[1]:", dict["1"])
		dict.has("1")

	# print_error(dict.get("1"))

	def test_method(self):
		print_error("test_method")
