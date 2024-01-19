import debugpy
from enum import Enum
from py4godot.classes.AStar3D.AStar3D import AStar3D
from py4godot.classes.CollisionShape3D.CollisionShape3D import CollisionShape3D
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.PhysicsRayQueryParameters3D.PhysicsRayQueryParameters3D import PhysicsRayQueryParameters3D
from py4godot.classes.PhysicsShapeQueryParameters3D.PhysicsShapeQueryParameters3D import PhysicsShapeQueryParameters3D
from py4godot.classes.SphereShape3D.SphereShape3D import SphereShape3D
from py4godot.classes.generated4_core import Array, NodePath, AABB, PackedVector3Array, Dictionary, Transform3D

from Scripts.Navigation import NavigationUtils
from Scripts.Navigation.AStarPoint import AStarPoint
from Scripts.Tools.Draw import *
from py4godot.classes.constants import VECTOR3_DOWN
from typing import Optional, List, Dict, Set, Tuple, cast

WALKABLE_GROUP = "walkable"
GRIDSIZE = 1
SCALE: float = 1
DRAW_RAD = 0.2
FLOAT_TOLERANCE = 0.1
WEIGHT_SCALE = 1
GROUND_MASK = 2  # 1 | 2 ** 4 | 2 ** 3 | 2 ** 6


class DIRECTION(Enum):
    UNDEFINED = -1
    LEFT = 0
    RIGHT = 1
    FORWARD = 2
    BACKWARDS = 3
    DOWN = 4
    UP = 5


POINT_OFFSET: float = 0.01


def get_mesh(node: Node) -> Optional[CSGMesh3D]:
    """This function is used to get a mesh child from a given Node"""
    for child in node.get_children():
        if isinstance(child, CSGMesh3D):
            return child


@gdclass
class AStar(Node3D, Draw):
    is_initialized: bool

    def __init__(self) -> None:
        # Don't call any godot-methods here
        super().__init__()
        self.astar: Optional[AStar3D] = None
        self.walkables: Optional[Array] = None
        self.points: List = []
        self.dict_points: Dict = dict()
        self.utils_path: Optional[NodePath] = None
        self.utils: Optional[Node3D] = None
        self.push_obj_layer: int = 32
        self.disabled_points: Set[AStarPoint] = set()
        self.already_traced_pos: Set[Tuple[float, float, float]] = set()

    prop("utils_path", NodePath, NodePath())

    prop("push_obj_layer", int, 32)

    def _ready(self) -> None:
        print_error("ready")
        print_error("Name:")
        print_error(self.get_class())
        print_error("Before get_children:")
        print_error(self.get_children())
        print_error("After get_children")

        try:
            with open("locked_debug", "w"):
                pass
            debugpy.log_to('log.txt')
            debugpy.configure(
                python=r"C:\g\addons\windows64\cpython-3.11.3-windows64\python\install\python.exe")
            debugpy.listen(("localhost", 5678))
            debugpy.wait_for_client()  # blocks execution until client is attached
        except Exception as e:
            print_error("Exception:", e)

        self.astar = AStar3D.constructor()
        self.walkables: Array = get_tree(self).get_nodes_in_group(StringName.new2(WALKABLE_GROUP))
        self.utils = self.get_node(self.utils_path)
        self.disable_enable_collision(True)

        # self.generate_points()
        self.generate_points_advanced()
        print_error("before init immediate_geometry")
        for point in self.points:
            self.immediate_geometry_init(self, point.id)
        print_error("after init immediate_geometry")
        self.generate_point_connections()

        self.generate_disabled()
        self.disable_obstacles()
        self.disable_enable_collision(False)
        # self.is_initialized: bool = False
        self.draw_points()

    def disable_enable_collision(self, disable: bool) -> None:
        obstacles: Array = get_tree(self).get_nodes_in_group(StringName.new2("obstacle"))

        for node in obstacles:
            obstacle: Node3D = Node3D.cast(node)

            for child in obstacle.get_children():
                if child.get_class() == "CollisionShape":
                    collider: CollisionShape3D = CollisionShape3D.cast(child)
                    collider.disabled = disable

        for node in get_tree(self).get_nodes_in_group(StringName.new2("obstacle")):
            obstacle: Node3D = Node3D.cast(node)

            for child in obstacle.get_children():
                if child.get_class() == "CollisionShape":
                    collider: CollisionShape3D = CollisionShape3D.cast(child)
                    collider.disabled = disable

    def draw_points(self) -> None:
        offset: Vector3 = Vector3.new3(0, 0.1, 0)
        return
        for point in self.points:
            self.draw_sphere(point.id, DRAW_RAD, point.position + offset,
                             color=Color.new3(1, 0, 0) if point in self.disabled_points else Color.new3(0, 1, 1))

        for point in self.points:
            for connected_point in point.connected_points:
                self.immediate_geometry_init(self, str(point.id) + "|" + str(connected_point.id))
                self.draw_line(str(point.id) + "|" + str(connected_point.id), point.position + offset,
                               connected_point.position + offset)

        for point in self.disabled_points:
            self.draw_sphere(point.id, DRAW_RAD, point.position + offset,
                             color=Color.new3(1, 0, 0) if point in self.disabled_points else Color.new3(1, 1, 1))

    def disable_obstacles(self) -> None:
        for node in get_tree(self).get_nodes_in_group(StringName.new2("obstacle")):
            vector3_node: Node3D = Node3D.cast(node)
            self.disable_points(vector3_node.global_transform.origin.x,
                                vector3_node.global_transform.origin.z,
                                2, 2)

    def generate_points_advanced(self) -> None:
        """Here we use advanced generation to calculate points"""
        self.add_point(Vector3.new3(0, GRIDSIZE / 100., 0), DIRECTION.UNDEFINED)

    def add_point(self, pos: Vector3, current_dir: DIRECTION) -> None:
        """Recursive algorithm to run over all possible points."""
        if not self.point_below(pos) or (pos.x, pos.y, pos.z) in self.already_traced_pos:
            return
        self.already_traced_pos.add((pos.x, pos.y, pos.z))
        point: AStarPoint = AStarPoint(pos.x / SCALE,
                                       pos.y,
                                       pos.z,
                                       NavigationUtils.calc_point_id(int(pos.x / SCALE), int(pos.y / SCALE),
                                                                     int(pos.z // SCALE)))

        if not self.point_inside_ground(pos):
            self.points.append(point)
            self.dict_points[point.id] = point
            self.astar.add_point(point.id, point.position, weight_scale=1.)
        # TODO: convert this to enums
        if current_dir != DIRECTION.LEFT:
            self.add_point(Vector3.new3(pos.x + GRIDSIZE, pos.y, pos.z), DIRECTION.RIGHT)
        if current_dir != DIRECTION.RIGHT:
            self.add_point(Vector3.new3(pos.x - GRIDSIZE, pos.y, pos.z), DIRECTION.LEFT)
        if current_dir != DIRECTION.FORWARD:
            self.add_point(Vector3.new3(pos.x, pos.y, pos.z + GRIDSIZE), DIRECTION.BACKWARDS)
        if current_dir != DIRECTION.BACKWARDS:
            self.add_point(Vector3.new3(pos.x, pos.y, pos.z - GRIDSIZE), DIRECTION.FORWARD)
        if current_dir != DIRECTION.DOWN:
            self.add_point(Vector3.new3(pos.x, pos.y + GRIDSIZE, pos.z), DIRECTION.UP)
        if current_dir != DIRECTION.UP:
            self.add_point(Vector3.new3(pos.x, pos.y - GRIDSIZE, pos.z), DIRECTION.DOWN)

        # TODO add diagonal movement

        self.add_point(Vector3.new3(pos.x + GRIDSIZE, pos.y + GRIDSIZE, pos.z), DIRECTION.UNDEFINED)
        self.add_point(Vector3.new3(pos.x + GRIDSIZE, pos.y - GRIDSIZE, pos.z), DIRECTION.UNDEFINED)
        self.add_point(Vector3.new3(pos.x - GRIDSIZE, pos.y + GRIDSIZE, pos.z), DIRECTION.UNDEFINED)
        self.add_point(Vector3.new3(pos.x - GRIDSIZE, pos.y - GRIDSIZE, pos.z), DIRECTION.UNDEFINED)

        self.add_point(Vector3.new3(pos.x, pos.y + GRIDSIZE, pos.z + GRIDSIZE), DIRECTION.UNDEFINED)
        self.add_point(Vector3.new3(pos.x, pos.y - GRIDSIZE, pos.z + GRIDSIZE), DIRECTION.UNDEFINED)
        self.add_point(Vector3.new3(pos.x, pos.y + GRIDSIZE, pos.z - GRIDSIZE), DIRECTION.UNDEFINED)
        self.add_point(Vector3.new3(pos.x, pos.y - GRIDSIZE, pos.z - GRIDSIZE), DIRECTION.UNDEFINED)

    def point_below(self, pos: Vector3) -> bool:
        """Function for checking point below"""
        query_3d = PhysicsRayQueryParameters3D.constructor()
        query_3d.collision_mask = 1
        query_3d.from_ = pos
        query_3d.to = pos + VECTOR3_DOWN
        result: Dictionary = self.get_world_3d().direct_space_state.intersect_ray(query_3d)

        if result.size() > 0:
            return pos != cast(Vector3, result["position"])
        return False

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

    def point_inside_ground(self, pos: Vector3) -> bool:
        """Checking if is inside ground by casting upwards ray """
        # erg: object = self.utils.callv("sphere_cast", Array(pos + Vector3.new3(0, 0.1, 0),
        #                                                    0.09, Array(self), GROUND_MASK))
        erg: Array = self.sphere_cast(pos + Vector3.new3(0, 0.1, 0), 0.09, GROUND_MASK)
        inside_ground: bool = erg.size() != 0
        if inside_ground:
            pass
        return inside_ground

    def generate_points(self) -> None:
        """Here we are generating all the points we could later use for astar"""
        for walkable in self.walkables:
            print(walkable.get_class())
            mesh: Optional[CSGMesh3D] = get_mesh(Node.cast(walkable))
            if not mesh:
                print_error("no mesh found")
                continue
            aabb: AABB = mesh.get_mesh().get_aabb()
            scale: Vector3 = mesh.get_scale()
            self.generate_squares(aabb, scale)

    def generate_squares(self, box_to_fill: AABB, scale: Vector3) -> None:
        """ Generate objects at matching points """
        size_to_calc_with: Vector3 = Vector3.new3(box_to_fill.size.x * scale.x, box_to_fill.size.y * scale.y,
                                                  box_to_fill.size.z * scale.z)
        for x in range(int((box_to_fill.get_center().x - size_to_calc_with.x / 2) * SCALE),
                       int((box_to_fill.get_center().x + size_to_calc_with.x / 2) * SCALE),
                       int(GRIDSIZE * SCALE)):
            for z in range(int((box_to_fill.get_center().z - size_to_calc_with.x / 2) * SCALE),
                           int((box_to_fill.get_center().z + size_to_calc_with.z) * SCALE),
                           int(GRIDSIZE * SCALE)):
                point: AStarPoint = AStarPoint(x / SCALE,
                                               box_to_fill.get_center().y + size_to_calc_with.y + POINT_OFFSET,
                                               # TODO:remove 1
                                               z / SCALE,
                                               NavigationUtils.calc_point_id(int(x // SCALE),
                                                                             box_to_fill.get_center().y // SCALE,
                                                                             int(z // SCALE)))
                self.points.append(point)
                self.dict_points[point.id] = point
                self.astar.add_point(point.id, point.position, weight_scale=10.)

    def generate_point_connections(self) -> None:
        """Here we generate the connections between the points, the player can walk"""
        for point in self.points:
            for other_point in self.points:
                diff: Vector3 = point.position - other_point.position
                if diff.length() <= math.sqrt(2) * GRIDSIZE + FLOAT_TOLERANCE and other_point.id != point.id:
                    self.astar.connect_points(point.id, other_point.id)
                    point.connected_points.append(other_point)

    def generate_disabled(self) -> None:
        for point in self.points:
            self.set_point_disabled(point)

    def set_point_disabled(self, point: AStarPoint) -> None:
        # erg: object = self.utils.callv("sphere_cast", Array(point.position,
        #                                                    GRIDSIZE * math.sqrt(2), Array(self), self.push_obj_layer))
        #
        # disabled: bool = erg.size() != 0
        # TODO: enable again
        self.sphere_cast(point.position, GRIDSIZE * math.sqrt(2), self.push_obj_layer)
        disabled: bool = False
        self.astar.set_point_disabled(point.id, disabled=disabled)

    def enable_points(self, x_pos: int, z_pos: int, x_size: int, z_size: int) -> None:
        for x in range(round(x_pos - x_size / 2.), round(x_pos + x_size / 2. + 1), GRIDSIZE):
            for z in range(round(z_pos - z_size / 2.), round(z_pos + z_size / 2. + 1), GRIDSIZE):
                # TODO: foor loop for y
                point_id: int = NavigationUtils.calc_point_id(x, 0, z)
                if point_id in self.dict_points.keys():
                    point = self.dict_points[point_id]
                    self.astar.set_point_disabled(point.id, False)
                    if point in self.disabled_points:
                        self.disabled_points.remove(self.dict_points[point_id])
                    else:
                        print("point not in disabled_points")
                    self.draw_sphere(point.id, DRAW_RAD,
                                     Vector3.new3(point.position.x, point.position.y, point.position.z),
                                     color=Color(0, 1, 0))
                else:
                    print("point_to_enable_not_found:", point_id)

    def disable_points(self, x_pos: int, z_pos: int, x_size: int, z_size: int) -> None:
        for x in range(round(x_pos - x_size / 2.), round(x_pos + x_size / 2. + 1), GRIDSIZE):
            for z in range(round(z_pos - z_size / 2.), round(z_pos + z_size / 2. + 1), GRIDSIZE):
                # TODO:for loop for y
                point_id: int = NavigationUtils.calc_point_id(x, 0, z)
                if point_id in self.dict_points.keys():
                    self.astar.set_point_disabled(point_id, True)
                    self.disabled_points.add(self.dict_points[point_id])
                else:
                    print("point_to_disable_not_found:", point_id)

    @gdmethod
    def get_way_points(self, start_position: Vector3, end_position: Vector3) -> PackedVector3Array:
        start = self.astar.get_closest_point(start_position)
        end = self.astar.get_closest_point(end_position)
        point_path: Array = self.astar.get_point_path(start, end)
        id_path:Array = self.astar.get_id_path(start, end)
        result_points:List[Vector3] = []
        for id in id_path:
            print_error("id:", id)
            point:AStarPoint = self.dict_points[id]
            result_points.append(point.position)
            print_error(f"ASTarPoint<{point.position.x}|{point.position.y}|{point.position.z}>")
        for point in point_path:
            print_error(f"point:{point.x}|{point.y}|{point.z}")
        return result_points
