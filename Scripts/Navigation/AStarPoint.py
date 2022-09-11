from py4godot import *
from typing import List
class AStarPoint():
    def __init__(self, x:float, y:float, z:float, id:int):
        self.position:Vector3 = Vector3(x,y,z)
        self.id:int = id
        self.connected_points:List = []

    def __str__(self)->str:
        return f"AStarPoint<{self.position}|{self.id}>"