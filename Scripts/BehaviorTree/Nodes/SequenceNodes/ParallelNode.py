from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from typing import List


class ParallelNode(BehaviorTreeNode):
    children: List[BehaviorTreeNode]

    def __init__(self, children: list) -> None:
        super().__init__()
        self.children = children
        self.current_node_index = 0

    def run(self) -> None:
        state: NodeStates = NodeStates.SUCCEEDED
        for child in self.children:
            if child.status not in {NodeStates.FAILED, NodeStates.CANCELLED, NodeStates.SUCCEEDED}:
                child.run()
                run_state: NodeStates = child.status
                if run_state == NodeStates.SUCCEEDED and state != NodeStates.RUNNING:
                    state = run_state
            if state == NodeStates.FAILED:
                self.fail()
                return
            elif state == NodeStates.CANCELLED:
                self.cancel()
                return

        if state == NodeStates.SUCCEEDED:
            self.success()

    def success(self) -> None:
        super().success()
        self.status = NodeStates.SUCCEEDED
        for child in self.children:
            child.status = NodeStates.FRESH #TODO: Better possibility for resetting is needed
