from py4godot.classes.Node2D.Node2D import Node2D
from py4godot.classes.Tree.Tree import Tree
from py4godot.classes.TreeItem.TreeItem import TreeItem
from py4godot.classes.generated4_core import NodePath, Color

import Scripts.BehaviorTree.Nodes.BehaviorTreeNode as tree_node
from py4godot.pluginscript_api.utils.annotations import *
from typing import Dict


@gdclass
class BehaviorTreeVisualizerLogic(Node2D):
    tree_path: NodePath
    tree: Tree

    dict_node: Dict[tree_node.BehaviorTreeNode, TreeItem]

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()

    prop("tree_path", NodePath, NodePath())

    @gdmethod
    def _ready(self):
        self.dict_node = dict()
        self.tree = Tree.cast(self.get_node(self.tree_path))
        root = self.tree.create_item()
        self.tree.hide_root = False
        root.set_text(0, "Root")
        child1 = self.tree.create_item(root)
        child2 = self.tree.create_item(root)
        child1.set_text(0, "Child1")
        child2.set_text(0, "Child2")
        subchild1 = self.tree.create_item(child1)
        subchild1.set_custom_color(0, Color.new_rgb(1, 0, 0))
        subchild1.set_text(0, "Subchild1")

    def init_tree(self, node: tree_node.BehaviorTreeNode) -> None:
        self.tree.clear()
        item: TreeItem = self.tree.create_item()
        item.set_text(0, type(node).__name__)
        self.dict_node[node] = item

    def add_item(self, parent: tree_node.BehaviorTreeNode, node: tree_node.BehaviorTreeNode) -> None:
        parent_item: TreeItem = self.dict_node[parent]
        item = self.tree.create_item(parent_item)
        item.set_text(0, type(node).__name__)
        self.dict_node[node] = item

    def update_node_status(self, node: tree_node.BehaviorTreeNode) -> None:
        item = self.dict_node[node]
        if node.status == tree_node.NodeStates.FAILED:
            item.set_custom_color(0, Color.new3(1, 0, 0))

        if node.status == tree_node.NodeStates.SUCCEEDED:
            item.set_custom_color(0, Color.new3(0, 1, 0))

        if node.status == tree_node.NodeStates.RUNNING:
            item.set_custom_color(0, Color.new3(1, 1, 0))

        if node.status == tree_node.NodeStates.CANCELLED:
            item.set_custom_color(0, Color.new3(0.5, 0.5, 0.5))
