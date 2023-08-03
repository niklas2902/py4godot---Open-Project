from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *


class MoveNode(BehaviorTreeNode):
	def __init__(self) -> None:
		super().__init__()

	def run(self) -> None:
		self.blackboard.enemy.move()

	def success(self) -> None:
		self.status = NodeStates.SUCCEEDED
