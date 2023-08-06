from __future__ import annotations  # Without this, the type hint below would not work.

import debugpy
from Scripts.BehaviorTree.BehaviorTree import BehaviorTree
from Scripts.BehaviorTree.Blackboard import Blackboard
from Scripts.BehaviorTree.Nodes.ActionNodes.DebugNode import DebugNode
from Scripts.BehaviorTree.Nodes.ActionNodes.MoveNode import MoveNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.InfiniteRepeatNode import InfiniteRepeatNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.RepeatNode import RepeatNode
from Scripts.BehaviorTree.Nodes.RootNode import RootNode
from Scripts.BehaviorTree.Nodes.SequenceNodes.ParallelNode import ParallelNode
from Scripts.BehaviorTree.Nodes.SequenceNodes.SequenceNode import SequenceNode
from py4godot.classes.generated import *
from py4godot.core.node_path.NodePath import NodePath
from py4godot.pluginscript_api.utils.annotations import *

@gdclass
class Enemy(Spatial):
	target_point_path: NodePath
	_target_point: Spatial
	delta:float 

	def __init__(self):
		# Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
		self.delta = 0

	prop("target_point_path", NodePath, NodePath())

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

		self._target_point = Spatial.cast(self.get_node(self.target_point_path))
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
			self.global_transform.set_origin(
				self.global_transform.get_origin() +
				(self._target_point.global_transform.get_origin() - self.global_transform.get_origin()).normalized() * self.delta)
			print(self.global_transform.get_origin().x)

		except Exception as e:
			print(e)

	@gdmethod
	def _process(self, delta):
		self.enemy_tree.run()
		self.delta = delta
