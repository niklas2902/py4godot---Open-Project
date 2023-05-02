from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from typing import List

class RootNode(BehaviorTreeNode):
    def __init__(self, children: List[BehaviorTreeNode]) -> None:
        super().__init__()
        self.children = children

    def run(self) -> None:
        self.status = NodeStates.RUNNING
        is_child_running: bool = False

        for child in self.get_children():
            child.run()
            if child.status == NodeStates.RUNNING:
                is_child_running = True

            if child.status == NodeStates.SUCCEEDED and self.status != NodeStates.FAILED:
                self.status = NodeStates.SUCCEEDED

            if child.status == NodeStates.CANCELLED and self.status != NodeStates.FAILED:
                self.status = NodeStates.CANCELLED

            if child.status == NodeStates.FAILED:
                self.status = NodeStates.FAILED

        if not is_child_running:
            if self.status == NodeStates.FAILED:
                self.fail()
            elif self.status == NodeStates.SUCCEEDED:
                self.success()
