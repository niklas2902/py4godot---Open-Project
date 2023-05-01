from Scripts.BehaviorTree.BehaviorTreeNode import BehaviorTreeNode, NodeStates


class DebugNode(BehaviorTreeNode):
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message: str = message

    def run(self) -> None:
        self.success()

    def success(self) -> None:
        print("DEBUG:", self.message)
        self.status = NodeStates.SUCCEEDED
