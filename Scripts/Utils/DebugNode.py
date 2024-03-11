import debugpy

from py4godot.classes.Node.Node import Node
from py4godot.pluginscript_api.utils.annotations import gdclass


@gdclass
class DebugNode(Node):

	def _enter_tree(self) -> None:
		try:
			with open("locked_debug", "w"):
				pass
			debugpy.log_to('log.txt')
			debugpy.configure(
				python=r"C:\Users\nikla\OneDrive\Dokumente\repositories\py4godot---Open-Project\addons\windows64\cpython-3.9.7-windows64\python\install\python.exe")
			debugpy.listen(("localhost", 5678))
			print("before wait for client")
			debugpy.wait_for_client()  # blocks execution until client is attached
		except Exception as e:
			print("Exception:", e)
