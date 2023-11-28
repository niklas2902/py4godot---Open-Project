from py4godot.classes.CharacterBody3D.CharacterBody3D import CharacterBody3D
from py4godot.classes.Node2D.Node2D import Node2D
from py4godot.classes.generated4_core import NodePath, Vector3
from py4godot.pluginscript_api.utils.annotations import *


@gdclass
class HidePlayerLogic(Node2D):
    player: CharacterBody3D
    player_path: NodePath

    prop("player_path", NodePath, NodePath())

    @gdmethod
    def _ready(self) -> None:
        self.player = CharacterBody3D.cast(self.get_node(self.player_path))

    @gdmethod
    def _pressed(self) -> None:
        self.player.global_transform.set_origin(Vector3.new3(10, 10, 10))
