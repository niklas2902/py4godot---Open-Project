from enum import Enum, auto

from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

RIGHT = 2
MARGIN_RIGHT=30

class ZoomState(Enum):
	ZOOMED_IN = auto(),
	ZOOMED_OUT = auto()
@gdclass
class ZoomButton(Button):
	register_signal("zoom_in")
	register_signal("zoom_out")
	def __init__(self)->None:
		super().__init__()
		self.zoom_state:ZoomState = ZoomState.ZOOMED_IN
	@gdmethod
	def _pressed(self)->None:
		print("Zoom Button pressed")
		Button.cast(self.get_parent()).set_disabled(True)
		print(self.disabled)
		if (self.zoom_state == ZoomState.ZOOMED_IN):
			self.zoom_state = ZoomState.ZOOMED_OUT
			self.emit_signal("zoom_out")
			print("zoom_out")
		else:
			self.zoom_state = ZoomState.ZOOMED_IN
			self.emit_signal("zoom_in")

	def _on_Camera_finished_animation(self)->None:
		print("finished_animation")
		Button.cast(self.get_parent()).disabled = False



