from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *


class InfiniteRepeatNode(BehaviorTreeNode):
    def __init__(self, child:BehaviorTreeNode) -> None:
        super().__init__()
        self.children = [child]
        assert len(self.children) == 1
    def run(self) -> None:
        self.status = NodeStates.RUNNING
        self.children[0].run()