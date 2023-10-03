from __future__ import annotations  # Without this, the type hint below would not work.

import math

import debugpy
import typing
from Scripts import CharHandler
from Scripts.BehaviorTree.BehaviorTree import BehaviorTree
from Scripts.BehaviorTree.Blackboard import Blackboard
from Scripts.BehaviorTree.Nodes.ActionNodes.DebugNode import DebugNode
from Scripts.BehaviorTree.Nodes.ActionNodes.FollowNode import FollowNode
from Scripts.BehaviorTree.Nodes.ActionNodes.MoveNode import MoveNode
from Scripts.BehaviorTree.Nodes.ActionNodes.WaitNode import WaitNode
from Scripts.BehaviorTree.Nodes.ActionNodes.WaitNodeSkipFirst import WaitNodeSkipFirst
from Scripts.BehaviorTree.Nodes.BehaviorTreeNode import BehaviorTreeNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.IfElseNode import IfElseNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.InfiniteRepeatNode import InfiniteRepeatNode
from Scripts.BehaviorTree.Nodes.DecoratorNodes.RepeatNode import RepeatNode
from Scripts.BehaviorTree.Nodes.RootNode import RootNode
from Scripts.BehaviorTree.Nodes.SequenceNodes.ParallelNode import ParallelNode
from Scripts.BehaviorTree.Nodes.SequenceNodes.SequenceNode import SequenceNode
from Scripts.CharHandler import DIST_NAVIGATION
from Scripts.Navigation import RouteHolder
from Scripts.Utils import BehaviorTreeVisualizerLogic
from py4godot.classes.generated import *
from py4godot.core.array.Array import Array
from py4godot.core.node_path.NodePath import NodePath
from py4godot.core.vector3.Vector3 import Vector3
from py4godot.pluginscript_api.utils.annotations import *
from Scripts.Navigation.AStar import AStar as NavAstar
from py4godot.pluginscript_api.hints.range_hint.RangeHint import *


@gdclass
class Enemy(KinematicBody):
    route_holder: RouteHolder
    route_holder_path: NodePath

    tree_visualizer: BehaviorTreeVisualizerLogic.BehaviorTreeVisualizerLogic

    delta: float
    route_accept_length: float
    player: typing.Optional[Spatial]
    astar_path: NodePath
    _astar: NavAstar
    current_path_ind: int
    path: typing.Optional[Array]
    last_player_pos: typing.Optional[Vector3]
    speed_modifier: float
    tree_visualizer_initialized: bool
    action_radius: float
    out_of_sight_radius: float
    player_found: bool
    look_direction: Vector3

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()
        self.current_path_ind = 0
        self.velocity = 0
        self.delta = 0
        self.path = None
        self.speed_modifier = 2
        self.tree_visualizer_initialized = False
        self.player_found = False

    prop("route_holder_path", NodePath, NodePath())
    prop("route_accept_length", float, 0.1)
    prop("astar_path", NodePath, NodePath())
    prop("player_path", NodePath, NodePath())
    prop("utils_path", NodePath, NodePath())
    prop("tree_path", NodePath, NodePath())
    prop("action_radius", float, 1, hint=RangeHint(0, 50, 0.1))
    prop("out_of_sight_radius", float, 1, hint=RangeHint(0, 50, 0.1))

    @gdmethod
    def _ready(self):

        self.look_direction = Vector3(1, 0, 1)
        self._astar = typing.cast(NavAstar, self.get_node(self.astar_path).get_pyscript())

        self.route_holder = typing.cast(RouteHolder, self.get_node(self.route_holder_path).get_pyscript())
        self.tree_visualizer = typing.cast(BehaviorTreeVisualizerLogic.BehaviorTreeVisualizerLogic,
                                           self.get_node(self.tree_path).get_pyscript())
        self.player: typing.Optional[Spatial] = Spatial.cast(self.get_node(self.player_path))
        self.last_player_pos: typing.Optional[Vector3] = None
        self.utils = self.get_node(self.utils_path)

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
                            IfElseNode([
                                SequenceNode([
                                    WaitNode(0.1),
                                    FollowNode()
                                ]),
                                SequenceNode([
                                    WaitNodeSkipFirst(2),
                                    MoveNode()])
                            ], lambda: self.should_follow_player())
                        )
                    ])
                ]
            ),
            Blackboard(self, self.tree_visualizer))

    def visualize_nodes(self, parent: BehaviorTreeNode, node: BehaviorTreeNode):
        self.tree_visualizer.add_item(parent, node)
        for child in node.children:
            self.visualize_nodes(node, child)

    def move(self) -> None:
        try:
            if self.path is None:
                self.path = self._astar.get_way_points(self.global_transform.get_origin(),
                                                       self.route_holder.get_current_route_point())

            self.follow_path()

        except Exception as e:
            print(e)

    def follow_path(self) -> None:
        if self.path == None:
            return

        if self.current_path_ind >= self.path.size():
            self.path = None
            self.current_path_ind = 0
            self.route_holder.increase_point()
            return

        dist_vector = self.path[self.current_path_ind] - self.transform.get_origin()
        dist: float = dist_vector.length()
        vel: Vector3 = (self.path[self.current_path_ind] - self.transform.get_origin())
        vel.y = 0
        self.look_direction = vel.normalized()

        new_pos: Vector3 = self.global_transform.get_origin() + vel.normalized() * self.delta * self.speed_modifier
        self.global_transform.set_origin(new_pos)

        if dist < DIST_NAVIGATION:
            self.current_path_ind += 1

    def follow_player(self) -> None:
        if self.path == None or self.player.global_transform.get_origin() != self.last_player_pos:
            self.path = self._astar.get_way_points(self.global_transform.get_origin(),
                                                   self.player.global_transform.get_origin())
        dist_vector = self.path[self.current_path_ind] - self.transform.get_origin()
        dist: float = dist_vector.length()
        vel: Vector3 = (self.path[self.current_path_ind] - self.transform.get_origin())
        vel.y = 0
        self.look_direction = vel.normalized()

        new_pos: Vector3 = self.global_transform.get_origin() + vel.normalized() * self.delta * self.speed_modifier
        self.global_transform.set_origin(new_pos)

        if dist < DIST_NAVIGATION:
            self.current_path_ind += 1
            self.current_path_ind = min(self.current_path_ind, self.path.size() - 1)

        self.last_player_pos = self.player.global_transform.get_origin()

    @gdmethod
    def _process(self, delta: float) -> None:
        if not self.tree_visualizer_initialized:
            self.init_tree_visualizer()

        self.enemy_tree.update_states()
        self.enemy_tree.run()
        self.delta = delta

    def player_in_sight(self) -> bool:
        res = self.utils.callv("sphere_cast",
                               Array(self.global_transform.get_origin(), self.action_radius, Array(),
                                     1)).get_converted_value()
        number_of_hits = res.size()
        return number_of_hits != 0

    def player_out_of_sight(self) -> bool:
        res = self.utils.callv("sphere_cast",
                               Array(self.global_transform.get_origin(), self.out_of_sight_radius, Array(),
                                     1)).get_converted_value()
        number_of_hits = res.size()
        return number_of_hits != 0

    def should_follow_player(self) -> bool:
        if not self.player_found:
            self.player_found = self.player_in_sight()
        else:
            self.player_found = self.player_out_of_sight()
        return self.player_found

    def init_tree_visualizer(self):
        self.tree_visualizer.init_tree(self.enemy_tree.root_node)
        for child in self.enemy_tree.root_node.children:
            self.visualize_nodes(self.enemy_tree.root_node, child)
        self.tree_visualizer_initialized = True

    def reset(self) -> None:
        self.current_path_ind = 0
        self.path = None
