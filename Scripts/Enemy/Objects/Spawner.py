import typing
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *


@gdclass
class Spawner(StaticBody):
    prop("utils_path", NodePath, NodePath())
    utils_path: NodePath

    @gdmethod
    def _ready(self) -> None:
        # ResourceLoader.instance().load("res://Prefabs/Projectile.tscn")
        self.utils = self.get_node(self.utils_path)

        # args: Array = Array()
        # args.append()
        scene: PackedScene = typing.cast(
            PackedScene,
            self.utils.callv("load_resource", Array("res://Prefabs/Projectile.tscn")).get_converted_value())
        obj = scene.instance()
        self.add_child(obj)
        print("Projectile:", obj)
