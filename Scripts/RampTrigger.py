from py4godot.classes.Area3D.Area3D import Area3D
from py4godot.pluginscript_api.utils.annotations import gdclass

from submodules.py4godot.py4godot.pluginscript_api.utils.annotations import gdmethod


@gdclass
class RampTrigger(Area3D):

    def __init__(self):
        # Don't call any godot-methods here
        super().__init__()

    @gdmethod
    def _on_Area_body_entered(self, body):
        print("body entered", body)

    @gdmethod
    def _on_Area_area_entered(self, area):
        print("area entered", area)

    @gdmethod
    def _on_Area_ready(self):
        print("ready")
