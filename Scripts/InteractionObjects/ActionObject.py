from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.pluginscript_api.utils.annotations import *


@gdclass
class ActionObject(Node3D):

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()
        self.velocity = 0

    def action(self, val: object) -> None:
        print("#############Action#################")
