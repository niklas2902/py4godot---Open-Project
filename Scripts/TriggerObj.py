from py4godot.classes.CSGMesh3D.CSGMesh3D import CSGMesh3D
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.StandardMaterial3D.StandardMaterial3D import StandardMaterial3D
from py4godot.classes.generated4_core import NodePath, Color
from py4godot.pluginscript_api.utils.annotations import gdclass, prop, gdmethod

from typing import Optional


@gdclass
class TriggerObj(Node3D):

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()
        self.velocity = 0
        self.mesh: Optional[CSGMesh3D] = None

    prop("mesh_path", NodePath, NodePath())

    @gdmethod
    def _ready(self) -> None:
        self.mesh = CSGMesh3D.cast(self.get_node(self.mesh_path))

    @gdmethod
    def action(self, is_activated):
        if (is_activated):
            self.set_color(Color.new3(0, 0, 1))
        else:
            self.set_color(Color.new3(1, 0, 0))

    def set_color(self, color: Color) -> None:
        material: StandardMaterial3D = StandardMaterial3D.cast(self.mesh.get_material())

        if material == None:
            new_mat: StandardMaterial3D = StandardMaterial3D.constructor()
            self.mesh.material = new_mat
            material = StandardMaterial3D.cast(self.mesh.get_material())

        material.albedo_color = color
