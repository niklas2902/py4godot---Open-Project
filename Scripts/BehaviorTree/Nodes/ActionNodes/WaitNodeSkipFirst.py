from Scripts.BehaviorTree.Nodes.ActionNodes.WaitNode import WaitNode
from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *


class WaitNodeSkipFirst(WaitNode):
    initialized: bool

    def __init__(self, duration: float) -> None:
        super().__init__(duration)
        self.initialized = False

    def run(self) -> None:
        if self.initialized:
            super().run()
        else:
            self.initialized = True
            self.success()
