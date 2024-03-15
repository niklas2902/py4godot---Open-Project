from py4godot.pluginscript_api.utils.annotations import gdclass
from py4godot.utils.print_tools import print_error

import debugpy
from py4godot.classes.Node3D.Node3D import Node3D


@gdclass
class DebugNode(Node3D):

	def _enter_tree(self)->None:
		print("#####################enter_tree############################")
		try:
			with open("locked_debug", "w"):
				pass
			debugpy.log_to('log.txt')
			debugpy.configure(
				python=r"C:\g\addons\windows64\cpython-3.11.3-windows64\python\install\python.exe")
			debugpy.listen(("localhost", 5678))
			print("before wait for client")
			debugpy.wait_for_client()  # blocks execution until client is attached
		except Exception as e:
			print("Exception:", e)
