from py4godot.classes.generated4_core import NodePath, Color, Vector3
from py4godot.pluginscript_api.utils.annotations import gdclass, prop, gdmethod

import typing
from Scripts.Enemy.Enemy import Enemy
from Scripts.Tools.Draw import Draw
from py4godot.classes.Node3D.Node3D import Node3D

ACTION_RADIUS_HANDLE = "ActionRadius"
OUT_OF_SIGHT_RADIUS_HANDLE = "OutOfSightRadius"
LOOK_DIRECTION_HANDLE = "LookDirection"
MIN_FIELD_OF_VIEW_HANDLE = "MinFieldOfView"
MAX_FIELD_OF_VIEW_HANDLE = "MaxFieldOfView"


@gdclass
class EnemyGizmo(Node3D, Draw):
    enemy: typing.Optional[Enemy]
    enemy_path: NodePath

    def __init__(self) -> None:
        # Don't call any godot-methods here
        super().__init__()
        self.velocity = 0
        self.enemy = None

    prop("enemy_path", NodePath, NodePath())

    @gdmethod
    def _ready(self) -> None:
        if self.enemy_path and self.get_node(self.enemy_path):
            self.enemy = typing.cast(Enemy, self.get_node(self.enemy_path).get_pyscript())
            self.immediate_geometry_init(self, ACTION_RADIUS_HANDLE)
            self.immediate_geometry_init(self, OUT_OF_SIGHT_RADIUS_HANDLE)
            self.immediate_geometry_init(self, LOOK_DIRECTION_HANDLE)
            self.immediate_geometry_init(self, MIN_FIELD_OF_VIEW_HANDLE)
            self.immediate_geometry_init(self, MAX_FIELD_OF_VIEW_HANDLE)

    @gdmethod
    def _process(self, delta: float) -> None:
        if self.enemy:
            self.draw_sphere(ACTION_RADIUS_HANDLE, self.enemy.action_radius, self.global_position,
                             Color.new3(1, 0, 1))
            self.draw_sphere(OUT_OF_SIGHT_RADIUS_HANDLE, self.enemy.out_of_sight_radius,
                             self.global_position,
                             Color.new3(1, 1, 0))
            self.draw_ray(LOOK_DIRECTION_HANDLE, self.global_position, self.enemy.look_direction,
                          self.enemy.action_radius, Color.new3(1, 0, 1))
            self.draw_ray(MIN_FIELD_OF_VIEW_HANDLE, self.global_position,
                          self.enemy.look_direction.rotated(
                              Vector3.new3(0, 1, 0), -self.enemy.field_of_view / 2.), self.enemy.action_radius,
                          Color.new0(1, 0, 1))
            self.draw_ray(MAX_FIELD_OF_VIEW_HANDLE, self.global_position,
                          self.enemy.look_direction.rotated(
                              Vector3.new3(0, 1, 0), self.enemy.field_of_view / 2.), self.enemy.action_radius,
                          Color.new0(1, 0, 1))
