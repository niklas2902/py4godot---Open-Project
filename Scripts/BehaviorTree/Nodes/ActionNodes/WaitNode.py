from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *


class WaitNode(BehaviorTreeNode):
    _counter: float
    duration: float

    def __init__(self, duration: float) -> None:
        super().__init__()
        self._counter = 0
        self.duration = duration

    def run(self) -> None:
        self.status = NodeStates.RUNNING
        self._counter += self.blackboard.enemy.delta
        if self.duration <= self._counter:
            self.success()

    def success(self) -> None:
        self.status = NodeStates.SUCCEEDED
        self._counter = 0
