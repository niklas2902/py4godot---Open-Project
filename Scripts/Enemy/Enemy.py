from __future__ import annotations  # Without this, the type hint below would not work.
from Scripts.BehaviorTree.BehaviorTree import BehaviorTree
from Scripts.BehaviorTree.Nodes.ActionNodes.DebugNode import DebugNode
from Scripts.BehaviorTree.Nodes.ActionNodes.MoveNode import MoveNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.DecoratorNode import DecoratorNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.InfiniteRepeatNode import InfiniteRepeatNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.RepeatNode import RepeatNode
from Scripts.BehaviorTree.Nodes.RootNode import RootNode
from Scripts.BehaviorTree.Nodes.SequenceNodes.ParallelNode import ParallelNode
from Scripts.BehaviorTree.Nodes.SequenceNodes.SequenceNode import SequenceNode
from py4godot.classes.generated import *
from py4godot.core.vector3.Vector3 import Vector3
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
			debugpy.configure(
				python=r"C:\Users\nikla\OneDrive\Dokumente\repositories\py4godot---Open-Project\addons\windows64\cpython-3.9.7-windows64\python\install\python.exe")
			debugpy.listen(("localhost", 5678))
			debugpy.wait_for_client()  # blocks execution until client is attached
		except Exception as e:
			print("Exception:", e)
		self.enemy_tree: BehaviorTree = BehaviorTree(
			RootNode(
				[SequenceNode(
					[RepeatNode(
						ParallelNode(
							[DebugNode("test_parallel1"),
							 DebugNode("test_parallel2")
							 ]), 5),
						DebugNode("test1"),
						DebugNode("test2"),
						InfiniteRepeatNode(
							MoveNode()
						)
					])
				]
			),
			Blackboard(self))

	def move(self) -> None:
		print("move")
		try:
			self.global_transform.set_origin(self.global_transform.get_origin() + Vector3(0.1, 0, 0))
			print(self.global_transform.get_origin().x)

		except Exception as e:
			print(e)

	@gdmethod
	def _process(self, delta):
		self.enemy_tree.run()
