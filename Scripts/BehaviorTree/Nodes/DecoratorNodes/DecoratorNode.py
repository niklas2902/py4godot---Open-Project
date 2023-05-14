from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *


class DecoratorNode(BehaviorTreeNode):
    condition:int
    def __init__(self, child:BehaviorTreeNode, condition: int) -> None:
        super().__init__()
        self.condition = condition
        self.children = [child]
    def run(self) -> None:
        self.success()

    def success(self) -> None:
        if self.condition > 0:
            self.children[0].run()
            self.status = self.children[0].status

