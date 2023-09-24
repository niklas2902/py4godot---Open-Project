import typing
from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode, NodeStates
from py4godot import *
from typing import List, Callable


class IfElseNode(BehaviorTreeNode):
    func_to_eval: typing.Callable

    def __init__(self, children: typing.Tuple[BehaviorTreeNode, BehaviorTreeNode],
                 func_to_eval: typing.Callable) -> None:
        super().__init__()
        self.children = children
        assert len(children) == 2

        self.func_to_eval: Callable = func_to_eval

    def run(self) -> None:
        self.status = NodeStates.RUNNING
        if (self.func_to_eval()):
            self.status = self.children[0].run()
        else:
            self.status = self.children[1].run()
