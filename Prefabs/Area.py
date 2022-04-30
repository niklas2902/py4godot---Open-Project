
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *


@gdclass
class AreaTrigger(Area):

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
	def _on_Area_body_entered(self, area):
		print("AREA_body_entered")
	def _on_Area_area_entered(self, area):
		print("entered:", area)
