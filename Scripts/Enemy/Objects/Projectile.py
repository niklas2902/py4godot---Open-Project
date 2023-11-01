from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Scripts.Enemy.Objects.Spawner import Spawner
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *


@gdclass
class Projectile(Spatial):
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
        hitting_wall:bool = self.is_hitting_wall()
        if hitting_wall:
            self.spawner.lifetime_over(self)

    def is_hitting_wall(self):
        res = self.utils.callv("sphere_cast",
                               Array(self.global_transform.get_origin(), 0.1, Array(self.spawner),
                                     4)).get_converted_value()
        print(res.size(), res.size() != 0)
        return res.size() != 0

    def reset_lifetime(self) -> None:
        self._current_lifetime_counter = 0
