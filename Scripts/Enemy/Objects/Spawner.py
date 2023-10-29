import typing
from Scripts.Enemy.Objects.Projectile import Projectile
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *


@gdclass
class Spawner(StaticBody):
    prop("utils_path", NodePath, NodePath())
    prop("reload_time", float, 0, hint=RangeHint(0, 10, is_slider=True))

    reload_time: float
    _current_time: float = 0

    utils_path: NodePath
    projectile_scene: PackedScene
    demo_projectile: Projectile

    projectiles_list: typing.List[Projectile]
    current_projectile_id = 0

    @gdmethod
    def _ready(self) -> None:
        # ResourceLoader.instance().load("res://Prefabs/Projectile.tscn")
        self.utils = self.get_node(self.utils_path)

        self.projectile_scene: PackedScene = typing.cast(
            PackedScene,
            self.utils.callv("load_resource", Array("res://Prefabs/Projectile.tscn")).get_converted_value())
        self.demo_projectile = typing.cast(Projectile, self.projectile_scene.instance().get_pyscript())
        # self.add_child(self.demo_projectile)

        self.projectiles_list = []
        for i in range(10):
            self.projectiles_list.append(self.demo_projectile.duplicate())
            self.projectiles_list[-1].get_pyscript().lifetime = 10
            self.projectiles_list[-1].get_pyscript().spawner = self

    @gdmethod
    def _physics_process(self, delta: float) -> None:
        self._current_time += delta
        if self._current_time > self.reload_time:
            self._current_time = 0
            self.spawn_projectile()

    @gdmethod
    def _process(self, delta: float) -> None:
        pass
    
    @gdmethod
    def lifetime_over(self, projectile: Object) -> None:
        print("lifetime_over")

    def spawn_projectile(self) -> None:
        if self.current_projectile_id < len(self.projectiles_list):
            #self.projectiles_list[self.current_projectile_id].get_pyscript().connect("lifetime_over", self, "lifetime_over")
            self.add_child(self.projectiles_list[self.current_projectile_id])
            self.current_projectile_id += 1
