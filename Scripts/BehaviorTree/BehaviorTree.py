from Scripts.BehaviorTree import Blackboard
from Scripts.BehaviorTree.Nodes import RootNode
from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import NodeStates


class BehaviorTree:
    root_node: RootNode
    blackboard: Blackboard

    def __init__(self, root_node: RootNode, blackboard: Blackboard):
        self.root_node: RootNode = root_node
        self.blackboard = blackboard
        root_node.flood_children(blackboard)

    def run(self) -> None:
        if self.root_node.status not in {NodeStates.CANCELLED, NodeStates.SUCCEEDED, NodeStates.FAILED}:
            self.root_node.run()
