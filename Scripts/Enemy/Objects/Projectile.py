from __future__ import annotations

from py4godot.classes.Node.Node import Node
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.generated4_core import Vector3, NodePath, Array

from Scripts.CharHandler import CharHandler
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Scripts.Enemy.Objects.Spawner import Spawner
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *


@gdclass
class Projectile(Node3D):
    velocity: Vector3

    lifetime: float
    _current_lifetime_counter: float
    spawner: Spawner
    stopped: bool

    utils: Node
    utils_path: NodePath

    prop("lifetime", float, 10)
    prop("utils_path", NodePath, NodePath())
    register_signal("lifetime_over")

    @gdmethod
    def _ready(self) -> None:
        self._current_lifetime_counter = 0
        self.velocity = Vector3(1, 0, 0)

    # self.utils = self.get_node(self.utils_path)

    @gdmethod
    def _process(self, delta: float) -> None:
        if self.is_inside_tree():
            self._current_lifetime_counter += delta
            if (self._current_lifetime_counter > self.lifetime):
                self.spawner.lifetime_over(self)
            else:
                self.global_transform.set_origin(self.global_transform.get_origin() + self.velocity * delta)

    @gdmethod
    def _physics_process(self, delta: float) -> None:
        hitting_wall: bool = self.is_hitting_wall()
        if hitting_wall:
            self.spawner.lifetime_over(self)

        hitting_player: bool = self.is_hitting_player()
        if hitting_player:
            player: CharHandler = self.extract_player_from_collision()
            print("res:", player)
            player.lose_life()
            self.spawner.lifetime_over(self)
            # self.spawner.get_tree().reload_current_scene()

    def extract_player_from_collision(self) -> CharHandler:
        return self.utils.callv("sphere_cast",
                                Array(self.get_global_position(), 0.1, Array(self.spawner),
                                      1))[0]["collider"].get_pyscript()

    def is_hitting_wall(self) -> bool:
        res = self.utils.callv("sphere_cast",
                               Array(self.global_transform.get_origin(), 0.1, Array(self.spawner),
                                     4)).get_converted_value()
        return res.size() != 0

    def is_hitting_player(self) -> bool:
        res = self.utils.callv("sphere_cast",
                               Array(self.global_transform.get_origin(), 0.1, Array(self.spawner),
                                     1)).get_converted_value()
        return res.size() != 0

    def reset_lifetime(self) -> None:
        self._current_lifetime_counter = 0
