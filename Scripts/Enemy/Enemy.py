from __future__ import annotations  # Without this, the type hint below would not work.

import math

import debugpy
import typing
from Scripts.BehaviorTree.BehaviorTree import BehaviorTree
from Scripts.BehaviorTree.Blackboard import Blackboard
from Scripts.BehaviorTree.Nodes.ActionNodes.DebugNode import DebugNode
from Scripts.BehaviorTree.Nodes.ActionNodes.MoveNode import MoveNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.InfiniteRepeatNode import InfiniteRepeatNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.RepeatNode import RepeatNode
from Scripts.BehaviorTree.Nodes.RootNode import RootNode
from Scripts.BehaviorTree.Nodes.SequenceNodes.ParallelNode import ParallelNode
from Scripts.BehaviorTree.Nodes.SequenceNodes.SequenceNode import SequenceNode
from Scripts.CharHandler import DIST_NAVIGATION
from Scripts.Navigation import RouteHolder
from py4godot.classes.generated import *
from py4godot.core.array.Array import Array
from py4godot.core.node_path.NodePath import NodePath
from py4godot.core.vector3.Vector3 import Vector3
from py4godot.pluginscript_api.utils.annotations import *
from Scripts.Navigation.AStar import AStar as NavAstar


@gdclass
class Enemy(Spatial):
	route_holder: RouteHolder
	route_holder_path: NodePath
	delta: float
	route_accept_length: float

	astar_path: NodePath
	_astar: NavAstar
	current_path_ind: int
	path: typing.Optional[Array]

	def __init__(self):
		# Don't call any godot-methods here
		super().__init__()
		self.current_path_ind = 0
		self.velocity = 0
		self.delta = 0
		self.path = None

	prop("route_holder_path", NodePath, NodePath())
	prop("route_accept_length", float, 0.1)
	prop("astar_path", NodePath, NodePath())

	@gdmethod
	def _ready(self):
		print("_init")
		try:
			with open("locked_debug", "w"):
				pass
			debugpy.log_to('log.txt')
			debugpy.configure(
				python=r"C:\Users\nikla\OneDrive\Dokumente\repositories\py4godot---Open-Project\addons\windows64\cpython-3.9.7-windows64\python\install\python.exe")
			debugpy.listen(("localhost", 5678))
			debugpy.wait_for_client()  # blocks execution until client is attached
		except Exception as e:
			print("Exception:", e)

		self._astar = typing.cast(NavAstar, self.get_node(self.astar_path).get_pyscript())

		self.route_holder = typing.cast(RouteHolder, self.get_node(self.route_holder_path).get_pyscript())

		self.enemy_tree: BehaviorTree = BehaviorTree(
			RootNode(
				[SequenceNode(
					[RepeatNode(
						ParallelNode(
							[DebugNode("test_parallel1"),
							 DebugNode("test_parallel2")
							 ]), 5),
						DebugNode("test1"),
						DebugNode("test2"),
						InfiniteRepeatNode(
							MoveNode()
						)
					])
				]
			),
			Blackboard(self))

	def move(self) -> None:
		try:
			"""
			self.global_transform.set_origin(
				self.global_transform.get_origin() +
				(self.route_holder.get_current_route_point() - self.global_transform.get_origin())
				.normalized() * self.delta)
			"""
			if self.path is None:
				self.path = self._astar.get_way_points(self.global_transform.get_origin(),
													   self.route_holder.get_current_route_point())
			print(self.global_transform.get_origin().x)
			#if (
			#		self.route_holder.get_current_route_point() - self.global_transform.get_origin()).length() < self.route_accept_length:
			#	self.route_holder.increase_point()

			self.follow_path()

		except Exception as e:
			print(e)

	def follow_path(self) -> None:
		if self.path == None:
			return
		print(self.current_path_ind, self.path.size())
		if self.current_path_ind >= self.path.size():
			print("path:")
			for element in self.path:
				print(element)
			self.path = None
			self.current_path_ind = 0
			self.route_holder.increase_point()
			return
		point_to_move_to:Vector3 = self.path[self.current_path_ind]
		dist_vector = self.path[self.current_path_ind] - self.transform.get_origin()
		dist: float = dist_vector.length()
		vel: Vector3 = (self.path[self.current_path_ind] - self.transform.get_origin())
		vel.y = 0

		new_pos: Vector3 = self.global_transform.get_origin() + vel.normalized() * self.delta
		self.global_transform.set_origin(new_pos)

		if dist < DIST_NAVIGATION:
			print("current_origin:", self.global_transform.get_origin())
			print("point_origin", self.path[self.current_path_ind])
			self.current_path_ind += 1

	# self.apply_root_motion(delta, math.atan2(vel.x, vel_z))

	@gdmethod
	def _process(self, delta: float) -> None:
		self.enemy_tree.run()
		self.delta = delta
