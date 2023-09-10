from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode
from py4godot.classes.generated import *
from py4godot.core.color.Color import Color
from py4godot.core.node_path.NodePath import NodePath
from py4godot.pluginscript_api.utils.annotations import *
from typing import Dict


@gdclass
class BehaviorTreeVisualizerLogic(Node2D):
	tree_path: NodePath
	tree: Tree

	dict_node: Dict[BehaviorTreeNode, TreeItem]

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

	def init_tree(self, node: BehaviorTreeNode) -> None:
		self.tree.clear()
		item: TreeItem = self.tree.create_item()
		item.set_text(0, type(node).__name__)
		self.dict_node[node] = item

	def add_item(self, parent: BehaviorTreeNode, node: BehaviorTreeNode) -> None:
		parent_item: TreeItem = self.dict_node[parent]
		item = self.tree.create_item(parent_item)
		item.set_text(0, type(node).__name__)
		self.dict_node[node] = item
