from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *


class RepeatNode(BehaviorTreeNode):
    count:int
    current_count_index:int
    def __init__(self, child:BehaviorTreeNode, count: int) -> None:
        super().__init__()
        self.count = count
        self.children = [child]
        self.current_count_index = 0
        assert len(self.children) == 1
    def run(self) -> None:
        self.status = NodeStates.RUNNING
        if self.current_count_index < self.count:
            self.children[0].run()
            self.current_count_index += 1 if self.children[0].status != NodeStates.RUNNING else 0
            if self.children[0].status in {NodeStates.FAILED, NodeStates.CANCELLED}:
                self.fail()
        else:
            self.success()

    def success(self) -> None:
        self.status = NodeStates.SUCCEEDED
        self.current_count_index = 0

    def fail(self) -> None:
        self.status = NodeStates.FAILED

