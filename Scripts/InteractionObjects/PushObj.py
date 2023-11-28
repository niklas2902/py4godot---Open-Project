from py4godot.classes.CharacterBody3D.CharacterBody3D import CharacterBody3D
from py4godot.classes.Node.Node import Node
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.StaticBody3D.StaticBody3D import StaticBody3D
from py4godot.classes.generated4_core import NodePath, Vector2, Array, Vector3
from py4godot.pluginscript_api.utils.annotations import gdclass, prop, gdproperty, gdmethod

from Scripts.Tools.Draw import Draw
from typing import Optional

ARROW_RAD = 0.5
PUSHLAYER = 7


@gdclass
class PushObj(StaticBody3D, Draw):

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()
        self._arrow_pszh = None
        self._push_layer: int = PUSHLAYER
        self._is_pushing: bool = False
        self._arrow_path: Optional[NodePath] = None
        self._arrows: Optional[Node] = None
        self._trigger: Optional[Node] = None
        self.player: Optional[CharacterBody3D] = None
        self._direction: Optional[str] = None
        self._util: Optional[Node] = None
        self.collision_layer_direction: int = 0
        self.pos_before: Optional[Vector3] = None

    @gdmethod
    def _ready(self):
        self._delta_pushing: Vector3 = Vector3.new3(0, 0, 0)
        self.pos_before = self.global_transform.get_origin()

    prop("collision_layer_direction", int, 64)  # , RangeHint(0,2**16,1))
    prop("util_path", NodePath, NodePath())

    @gdproperty(NodePath, NodePath())
    def trigger(self) -> NodePath:
        return self._trigger

    @trigger.setter
    def trigger(self, value: NodePath) -> None:
        self._trigger = value

    @gdproperty(int, PUSHLAYER)
    def push_layer(self) -> int:
        return self._push_layer

    @push_layer.setter
    def push_layer(self, value: int) -> None:
        self._push_layer = value

    @gdproperty(NodePath, NodePath())
    def arrow_path(self) -> NodePath:
        return self._arrow_path

    @arrow_path.setter
    def arrow_path(self, value: NodePath) -> None:
        self._arrow_path = value

    @gdmethod
    def _ready(self):
        if self._trigger:
            trigger: Node = self.get_node(self._trigger)
            self.trigger_obj: Node = Node.cast(trigger)

        if (self._arrow_path):
            self._arrows = self.get_node(self._arrow_path)
            self._arrows = Node.cast(self._arrows)
        self._util = self.get_node(self.util_path)

        if (not self._arrow_path):
            return

        if (self._arrows and self._arrows.get_children()):
            for child in self._arrows.get_children():
                self.immediate_geometry_init(self, child.get_name())
        self.immediate_geometry_init(self, "push")

    @gdmethod
    def _process(self, delta):
        if (not self._arrows):
            return

    @gdmethod
    def start_pushing(self, other: CharacterBody3D) -> None:
        self.pos_before = self.global_position

        self.set_collision_layer_bit(0, False)
        self.set_collision_layer_bit(1, False)
        self.set_collision_layer_bit(6, True)
        self.set_collision_layer_bit(7, True)

        self.set_collision_mask_bit(0, False)
        self.set_collision_mask_bit(1, False)
        self.set_collision_mask_bit(6, True)
        self.set_collision_mask_bit(7, True)

        self._delta_pushing = self.global_position - other.global_position

        self._is_pushing = False

        self._direction = self.get_direction(other)

    @gdmethod
    def is_move_allowed(self, vector: Vector2) -> bool:
        if (self._direction == "east" or self._direction == "west"):
            if vector.x != 0:
                res = self._util.callv("sphere_cast",
                                       Array(self.global_position +
                                             Vector3(vector.x, 0, 0),
                                             0.02, Array(self), self.collision_layer_direction)).get_converted_value()

                self.draw_sphere("push", 1, self.global_position +
                                 Vector3(vector.x, 0, 0))
                return res.size() == 0
        else:
            if vector.y != 0:
                res = self._util.callv("sphere_cast",
                                       Array(self.global_position + Vector3(0, 0, vector.y),
                                             0.02, Array(self), self.collision_layer_direction)).get_converted_value()
                self.draw_sphere("push", 1, self.global_position +
                                 Vector3(0, 0, vector.y))
                return res.size() == 0
        return False

    def get_direction(self, other: CharacterBody3D) -> None:
        min = 1000000
        min_arrow: Optional[Node3D] = None
        for arrow_index in range(0, self._arrows.get_children().size()):
            arrow: Node3D = Node3D.cast(self._arrows.get_children()[arrow_index])
            if ((arrow.global_position - other.global_position).length() < min):
                min_arrow = arrow
                min = (arrow.global_position - other.global_position).length()

        if min_arrow:
            return min_arrow.call("get_direction").get_converted_value()

    @gdmethod
    def get_triggers(self) -> Array:
        return self.trigger_obj.get_children()

    @gdmethod
    def get_delta_pushing(self) -> Vector3:
        return self._delta_pushing
