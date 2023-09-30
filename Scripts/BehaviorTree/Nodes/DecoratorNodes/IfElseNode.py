import typing
from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *
from typing import List, Callable, Optional


class IfElseNode(BehaviorTreeNode):
    func_to_eval: typing.Callable
    current_node: Optional[BehaviorTreeNode]

    def __init__(self, children: typing.Tuple[BehaviorTreeNode, BehaviorTreeNode],
                 func_to_eval: typing.Callable) -> None:
        super().__init__()
        self.children = children
        assert len(children) == 2

        self.func_to_eval: Callable = func_to_eval
        self.current_node: Optional[BehaviorTreeNode] = None

    def run(self) -> None:
        self.status = NodeStates.RUNNING
        if (self.func_to_eval()):
            if self.current_node != self.children[0] and self.current_node:
                self.current_node.fail()
            self.status = self.children[0].run()
            self.current_node = self.children[0]
        else:
            if self.current_node != self.children[1] and self.current_node:
                self.current_node.fail()
            self.status = self.children[1].run()
            self.current_node = self.children[1]
