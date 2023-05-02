from __future__ import annotations

from enum import Enum
from typing import Optional, List


# States
class NodeStates(Enum):
    FRESH = 0
    RUNNING = 1
    FAILED = 2
    SUCCEEDED = 3
    CANCELLED = 4

class BehaviorTreeNode:
    def __init__(self) -> None:
        self.control: Optional[BehaviorTreeNode] = None
        self.tree = None
        self.guard = None
        self.children: List[BehaviorTreeNode] = []
        self.status: NodeStates = NodeStates.FRESH

    # Final methods
    def running(self) -> None:
        self.status = NodeStates.RUNNING
        if self.control is not None:
            self.control.child_running()

    def get_children(self) -> List[BehaviorTreeNode]:
        return self.children

    def success(self) -> None:
        self.status = NodeStates.SUCCEEDED
        if self.control is not None:
            self.control.child_success()

    def fail(self) -> None:
        self.status = NodeStates.FAILED
        if self.control is not None:
            self.control.child_fail()

    def cancel(self) -> None:
        if self.status == NodeStates.RUNNING:
            self.status = NodeStates.CANCELLED
            # Cancel child tasks
            for child in self.get_children():
                child.cancel()

    # Abstract methods
    def run(self) -> None:
        # Process the task and call running(), success(), or fail()
        pass

    def child_success(self) -> None:
        pass

    def child_fail(self) -> None:
        pass

    def child_running(self) -> None:
        pass

    # Non-final non-abstract methods
    def start(self) -> None:
        self.status = NodeStates.FRESH
        for child in self.get_children():
            child.control = self
            child.tree = self.tree
            child.start()

    def reset(self) -> None:
        self.cancel()
        self.status = NodeStates.FRESH
