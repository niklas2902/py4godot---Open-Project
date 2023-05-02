from Scripts.BehaviorTree.Nodes import RootNode
from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import NodeStates


class BehaviorTree:
    def __init__(self, root_node: RootNode):
        self.root_node: RootNode = root_node

    def run(self) -> None:
        if self.root_node.status not in {NodeStates.CANCELLED, NodeStates.SUCCEEDED, NodeStates.FAILED}:
            self.root_node.run()