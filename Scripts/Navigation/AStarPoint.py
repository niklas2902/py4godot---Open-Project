from py4godot import *
class AStarPoint():
    def __init__(self, x:float, y:float, z:float, id:str):
        self.position:Vector3 = Vector3(x,y,z)
        self.id:str = id