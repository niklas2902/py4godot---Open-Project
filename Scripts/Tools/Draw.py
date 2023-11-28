import math

from py4godot.classes.BaseMaterial3D.BaseMaterial3D import BaseMaterial3D
from py4godot.classes.CSGMesh3D.CSGMesh3D import CSGMesh3D
from py4godot.classes.ImageTexture.ImageTexture import ImageTexture
from py4godot.classes.ImmediateMesh.ImmediateMesh import ImmediateMesh
from py4godot.classes.MeshInstance3D.MeshInstance3D import MeshInstance3D
from py4godot.classes.ORMMaterial3D.ORMMaterial3D import ORMMaterial3D
from py4godot.classes.ShaderMaterial.ShaderMaterial import ShaderMaterial
from py4godot.classes.StandardMaterial3D.StandardMaterial3D import StandardMaterial3D
from py4godot.classes.generated4_core import Color, Vector3
from py4godot.classes.Node.Node import Node
from py4godot.classes.utils import *
from py4godot.pluginscript_api.utils.annotations import *
import py4godot.classes.constants as constants
from py4godot.utils.print_tools import print_error

RESOLUTION = 20


class Draw():
    caller: Node
    initialized: dict[str, bool]

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()
        self.immediate_geometry_dict = dict()

        self.initialized = dict()

    def immediate_geometry_init(self, caller, handle):
        self.initialized[handle] = False
        instance: MeshInstance3D = MeshInstance3D.constructor()
        immediate_geometry = ImmediateMesh.constructor()
        self.immediate_geometry_dict[handle] = immediate_geometry
        mymesh: CSGMesh3D = CSGMesh3D.constructor()
        my_mat: StandardMaterial3D = StandardMaterial3D.constructor()
        immediate_geometry.surface_begin(0, my_mat)
        new_mat: StandardMaterial3D = StandardMaterial3D.constructor()
        new_mat.albedo_color = Color.new3(1, 1, 1)
        immediate_geometry.surface_set_material(0, new_mat)
        immediate_geometry.surface_end()
        instance.set_mesh(immediate_geometry)
        get_tree(caller).get_root().add_child(instance)
        self.caller = caller

        vector: Vector3 = Vector3.new0()
        vector.x = 2.1

        vector_z: Vector3 = Vector3.new0()
        vector_z.z = 1
        vector_rotated: Vector3 = vector.rotated(vector_z, math.pi / 2)

    @gdmethod
    def draw_cirlce(self, handle: str, pos: Vector3, rad: float, color=Color.new3(1, 1, 1)):

        immediate_geometry: ImmediateMesh = self.immediate_geometry_dict[handle]
        immediate_geometry.clear_surfaces()
        my_mat: StandardMaterial3D = StandardMaterial3D.constructor()
        immediate_geometry.surface_begin(1, my_mat)
        immediate_geometry.surface_set_color(color)

        num_points = RESOLUTION
        alpha = 2 * math.pi * (num_points - 1) / num_points
        vector_before = Vector3.new3(math.cos(alpha), 0, math.sin(alpha)) * rad + Vector3.new3(0, pos.y, 0)
        for alpha_part in range(0, num_points):
            alpha = 2 * math.pi * alpha_part / num_points
            x = math.cos(alpha)
            y = math.sin(alpha)
            immediate_geometry.surface_add_vertex(Vector3.new3(x * rad, 0, y * rad) + Vector3(0, pos.y, 0))
            if (vector_before):
                immediate_geometry.surface_add_vertex(vector_before)
            vector_before = Vector3.new3(x * rad, 0, y * rad) + Vector3.new3(0, pos.y, 0)
        immediate_geometry.surface_end()
        self.finish_initialization(handle, immediate_geometry)

    def draw_sphere(self, handle, rad, position, color=Color.new3(1, 1, 1)):
        immediate_geometry: ImmediateMesh = self.immediate_geometry_dict[handle]
        immediate_geometry.clear_surfaces()
        my_mat: StandardMaterial3D = StandardMaterial3D.constructor()
        immediate_geometry.surface_begin(1, my_mat)
        immediate_geometry.surface_set_color(color)
        num_points = RESOLUTION
        alpha = 2 * math.pi * (num_points - 1) / num_points
        vectors = []

        vector_before = Vector3.new3(math.cos(alpha), math.sin(alpha), 0) * rad

        for alpha_part in range(0, num_points):
            alpha = 2 * math.pi * alpha_part / num_points
            x = math.cos(alpha)
            y = math.sin(alpha)
            vector: Vector3 = Vector3.new3(x, y, 0) * rad
            vectors.append(vector)
            if (vector_before):
                vectors.append(vector_before)

            vector_before = Vector3.new3(vector.x, vector.y, 0)

        vector_x: Vector3 = Vector3.new3(1, 0, 0)

        z_rotation = []
        for vector in vectors:
            z_rotation.append(vector.rotated(constants.VECTOR3_Y_AXIS, math.pi / 2))

        x_rotation = []
        for vector in vectors:
            x_rotation.append(vector.rotated(constants.VECTOR3_X_AXIS, math.pi / 2))

        for vector in vectors + z_rotation + x_rotation:
            vector_to_add: Vector3 = vector + position
            immediate_geometry.surface_add_vertex(vector_to_add)

        immediate_geometry.surface_end()
        self.finish_initialization(handle, immediate_geometry)

    def finish_initialization(self, handle: str, immediate_geometry: ImmediateMesh) -> None:
        if not self.initialized[handle]:
            instance: MeshInstance3D = MeshInstance3D.constructor()
            instance.set_mesh(immediate_geometry)
            get_tree(self.caller).get_root().add_child(instance)
            self.initialized[handle] = True

    @gdmethod
    def draw_ray(self, handle, origin: Vector3, direction: Vector3, length: float,
                 color: Color = Color.new3(1, 1, 1)) -> None:
        immediate_geometry: ImmediateMesh = self.immediate_geometry_dict[handle]
        immediate_geometry.clear_surfaces()
        my_mat: StandardMaterial3D = StandardMaterial3D.constructor()
        immediate_geometry.surface_begin(1, my_mat)
        immediate_geometry.surface_set_color(color)
        immediate_geometry.surface_add_vertex(origin)
        immediate_geometry.surface_add_vertex(origin + direction * length)
        immediate_geometry.surface_end()
        self.finish_initialization(handle, immediate_geometry)

    @gdmethod
    def draw_line(self, handle: str, origin: Vector3, target: Vector3, color: Color = Color.new0()) -> None:
        immediate_geometry: ImmediateMesh = self.immediate_geometry_dict[handle]
        immediate_geometry.clear_surfaces()
        my_mat: StandardMaterial3D = StandardMaterial3D.constructor()
        immediate_geometry.surface_begin(1, my_mat)
        immediate_geometry.surface_set_color(color)
        immediate_geometry.surface_add_vertex(origin)
        immediate_geometry.surface_add_vertex(target)
        immediate_geometry.surface_end()
        self.finish_initialization(handle, immediate_geometry)
