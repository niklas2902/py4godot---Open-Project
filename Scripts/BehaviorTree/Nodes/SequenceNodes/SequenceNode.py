from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates


class SequenceNode(BehaviorTreeNode):
    current_node_index: int

    def __init__(self, children: list) -> None:
        super().__init__()
        self.children = children
        self.current_node_index = 0

    def run(self) -> None:
        if self.current_node_index < len(self.children):
            self.children[self.current_node_index].run()
            if self.children[self.current_node_index].status != NodeStates.RUNNING:
                self.current_node_index += 1
        else:
            self.success()

    def success(self) -> None:
        self.status = NodeStates.SUCCEEDED
