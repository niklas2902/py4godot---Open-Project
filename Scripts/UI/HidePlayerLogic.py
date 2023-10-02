import typing
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *


@gdclass
class HidePlayerLogic(Node2D):
    player: KinematicBody
    player_path: NodePath

    prop("player_path", NodePath, NodePath())

    @gdmethod
    def _ready(self) -> None:
        self.player = KinematicBody.cast(self.get_node(self.player_path))

    @gdmethod
    def _pressed(self) -> None:
        self.player.global_transform.set_origin(Vector3(10, 10, 10))
