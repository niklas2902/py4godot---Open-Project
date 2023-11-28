from py4godot.classes.Area3D.Area3D import Area3D
from py4godot.pluginscript_api.utils.annotations import gdclass, gdmethod


@gdclass
class TriggerArea(Area3D):

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()

    @gdmethod
    def _ready(self):
        print("I'm alive")

    @gdmethod
    def _process(self, delta):
        print(delta)
