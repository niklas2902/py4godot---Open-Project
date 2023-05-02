from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *


class DebugNode(BehaviorTreeNode):
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message: str = message

    def run(self) -> None:
        self.success()

    def success(self) -> None:
        print("DEBUG:", self.message)
        self.status = NodeStates.SUCCEEDED
