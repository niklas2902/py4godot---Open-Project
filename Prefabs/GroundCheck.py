from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *

@gdclass
class GroundCheck(Spatial):
	register_signal("ground_check")

	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self.velocity = 0
	
	@gdmethod
	def _on_area_entered(self):
		print("_on_area_entered")
	
	@gdmethod
	def _on_body_entered(self):
		print("_on_area_entered")
	
	@gdmethod
	def _ready(self):
		print("on_tree entered")
	
	@gdmethod
	def _on_ready(self):
		print("on_ready")








