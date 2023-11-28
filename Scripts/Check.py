from py4godot.classes.CharacterBody3D.CharacterBody3D import CharacterBody3D
from py4godot.classes.Node.Node import Node
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.generated4_core import NodePath
from py4godot.pluginscript_api.utils.annotations import gdclass, prop, gdmethod

from py4godot.classes.generated4_core import Array
from py4godot.pluginscript_api.utils.annotations import gdproperty

NORTH = 0b0001
SOUTH = 0b0010
EAST = 0b0100
WEST = 0b1000

RADIUS: float = 0.5


@gdclass
class Check(Node3D):

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()
        self._dir: str = None
        self._orientation: int = 0

        self._bool_val: bool = False
        self._util_path: NodePath = None
        self.util: Node3D = None
        print("init_trigger")

    prop("direction", int, 0)  # , FlagsHint("north", "south", "east", "west"))
    prop("test", int, 0)

    # @gdproperty(NodePath, NodePath())
    # def util_path(self) -> NodePath:
    #     return self._util_path
    #
    # @util_path.setter
    # def util_path(self, value: NodePath) -> None:
    #     self._util_path = value
    #
    # @gdproperty(int, 0)  # , FlagsHint("north", "south", "east", "west"))
    # def orientation(self) -> int:
    #     return self._orientation
    #
    # @orientation.setter
    # def orientation(self, value: int) -> None:
    #     self._orientation = value
    #
    # @gdproperty(type(True), False)
    # def bool_val(self) -> bool:
    #     return self._bool_val
    #
    # @bool_val.setter
    # def bool_val(self, value: bool) -> None:
    #     self._bool_val = value

    @gdmethod
    def _ready(self):
        if self._util_path:
            util: Node = self.get_node(self._util_path)
            self._util: Node3D = Node3D.cast(util)

    @gdmethod
    def check_collision(self, other: CharacterBody3D):
        res = self._util.callv("sphere_cast",
                               Array(self.global_transform.get_origin(), 0.1, Array(), -1)).get_converted_value()
        return res

    @gdmethod
    def get_direction(self):
        print("orientation:", self._orientation)
        if (self.is_north()):
            return "north"
        if (self.is_south()):
            return "south"
        if (self.is_east()):
            return "east"
        if (self.is_west()):
            return "west"

    @gdmethod
    def is_north(self):
        return bool(self._orientation & NORTH)

    @gdmethod
    def is_south(self):
        return bool(self._orientation & SOUTH)

    @gdmethod
    def is_east(self):
        return bool(self._orientation & EAST)

    @gdmethod
    def is_west(self):
        return bool(self._orientation & WEST)
