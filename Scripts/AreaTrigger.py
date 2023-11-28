from py4godot.classes.CSGMesh3D.CSGMesh3D import CSGMesh3D
from py4godot.classes.CharacterBody3D.CharacterBody3D import CharacterBody3D
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.ResourceLoader.ResourceLoader import ResourceLoader
from py4godot.classes.StandardMaterial3D.StandardMaterial3D import StandardMaterial3D
from py4godot.classes.generated4_core import NodePath, Color
from py4godot.pluginscript_api.utils.annotations import prop, register_signal, gdmethod, gdclass

from py4godot import *
from typing import Optional


@gdclass
class AreaTrigger(Node3D):

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()
        self.velocity = 0
        self.mesh_path: Optional[NodePath] = None
        self.mesh: Optional[CSGMesh3D] = None
        self.connected_obj: Optional[Node3D] = None
        self.activated: bool = False

    prop("mesh_path", NodePath, NodePath())
    register_signal("trigger_entered")
    register_signal("trigger_exited")

    @gdmethod
    def _ready(self):
        self.mesh = CSGMesh3D.cast(self.get_node(self.mesh_path))

    @gdmethod
    def body_entered(self, other: CharacterBody3D):
        self.set_color(Color.new3(0, 1, 0))
        self.activated = True
        self.emit_signal("trigger_entered")

    @gdmethod
    def body_exited(self, other: CharacterBody3D):
        self.set_color(Color(1, 0, 0))
        self.activated = False
        self.emit_signal("trigger_exited")

    def set_color(self, color: Color) -> None:
        material: StandardMaterial3D = StandardMaterial3D.cast(self.mesh.get_material())

        if material == None:
            # print("before new_mat")
            new_mat: StandardMaterial3D = StandardMaterial3D.constructor()
            self.mesh.material = new_mat
            material = StandardMaterial3D.cast(self.mesh.get_material())

        material.albedo_color = color

    def load_finish_mat(self) -> StandardMaterial3D:
        return StandardMaterial3D.cast(ResourceLoader.instance().load("res://Materials/green.mat"))

    def _on_Logic_tree_entered(self) -> None:
        print("----------------------tree entered-----------------")
