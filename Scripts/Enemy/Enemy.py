from __future__ import annotations  # Without this, the type hint below would not work.
from Scripts.BehaviorTree.BehaviorTree import BehaviorTree
from Scripts.BehaviorTree.Nodes.ActionNodes.DebugNode import DebugNode
from Scripts.BehaviorTree.Nodes.RootNode import RootNode
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from Scripts.BehaviorTree.Blackboard import Blackboard
import debugpy, os


@gdclass
class Enemy(Spatial):

	def __init__(self):
		# Don't call any godot-methods here
		super().__init__()
		self.velocity = 0

	@gdmethod
	def _ready(self):
		print("_init")
		try:
			with open("locked_debug", "w"):
				pass
			debugpy.log_to('log.txt')
			debugpy.configure(python = r"C:\Users\nikla\OneDrive\Dokumente\repositories\py4godot---Open-Project\addons\windows64\cpython-3.9.7-windows64\python\install\python.exe")
			debugpy.listen(("localhost", 5678))
			debugpy.wait_for_client()  # blocks execution until client is attached
		except Exception as e:
			print("Exception:", e)
		self.enemy_tree: BehaviorTree = BehaviorTree(RootNode([DebugNode("test")]), Blackboard(self))

	@gdmethod
	def _process(self, delta):
		self.enemy_tree.run()
