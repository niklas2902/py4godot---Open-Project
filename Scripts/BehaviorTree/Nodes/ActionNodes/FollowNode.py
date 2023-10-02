from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *


class FollowNode(BehaviorTreeNode):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        self.status = NodeStates.RUNNING
        self.blackboard.enemy.follow_player()

    def success(self) -> None:
        self.status = NodeStates.SUCCEEDED

    def fail(self) -> None:
        self.blackboard.enemy.reset()
        self.status = NodeStates.FAILED
