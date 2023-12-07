from py4godot.classes.generated4_core import Vector3

from typing import List


class AStarPoint():
    position: Vector3
    id: int
    connected_points: List

    def __init__(self, x: float, y: float, z: float, id: int) -> None:
        self.position = Vector3.new3(x, y, z)
        self.id = id
        self.connected_points = []

    def __str__(self) -> str:
        return f"AStarPoint<{self.position}|{self.id}>"
