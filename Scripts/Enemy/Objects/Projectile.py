from __future__ import annotations

from py4godot.classes.Node.Node import Node
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.PhysicsShapeQueryParameters3D.PhysicsShapeQueryParameters3D import PhysicsShapeQueryParameters3D
from py4godot.classes.SphereShape3D.SphereShape3D import SphereShape3D
from py4godot.classes.generated4_core import Vector3, NodePath, Array, Transform3D

from Scripts.CharHandler import CharHandler
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Scripts.Enemy.Objects.Spawner import Spawner
from py4godot.pluginscript_api.utils.annotations import *

PUSH_OBJ_MASK: int = 4
GROUND_MASK: int = 1


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
    prop("utils_path", NodePath, NodePath.new0())

    @gdmethod
    def _ready(self) -> None:
        self._current_lifetime_counter = 0
        self.velocity = Vector3.new3(1, 0, 0)

    # self.utils = self.get_node(self.utils_path)

    @gdmethod
    def _process(self, delta: float) -> None:
        if self.is_inside_tree():
            self._current_lifetime_counter += delta
            if (self._current_lifetime_counter > self.lifetime):
                self.spawner.lifetime_over(self)
            else:
                self.global_position = self.global_position + self.velocity * delta

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

    def sphere_cast(self, position, radius, mask=GROUND_MASK) -> Array:
        shape: SphereShape3D = SphereShape3D.constructor()
        shape.set_radius(radius)

        params = PhysicsShapeQueryParameters3D.constructor()
        params.set_shape(shape)
        if mask != -1:
            params.collision_mask = mask
        translated_transform: Transform3D = self.global_transform.translated(position)
        params.set_transform(translated_transform)  # same transform as parent, just translate

        # array: Array = Array.new0()
        # array.push_back(self)
        # params.set_exclude(array)  # here exclude is an array of... RID??
        res: Array = self.get_world_3d().direct_space_state.intersect_shape(params)
        if res.size() > 0:
            pass
        return res

    def is_hitting_wall(self) -> bool:
        res = self.sphere_cast(self.global_position, 0.1, 4)
        return res.size() != 0

    def is_hitting_player(self) -> bool:
        res = self.sphere_cast(self.global_position, 0.1, 1)
        return res.size() != 0

    def reset_lifetime(self) -> None:
        self._current_lifetime_counter = 0
