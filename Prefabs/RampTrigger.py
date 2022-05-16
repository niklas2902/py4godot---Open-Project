from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

@gdclass
class RampTrigger(Area):

	def __init__(self):
		#Don't call any godot-methods here
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


