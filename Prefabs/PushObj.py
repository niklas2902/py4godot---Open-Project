from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

@gdclass
class PushObj(StaticBody):

	@gdproperty(NodePath, NodePath())
	def trigger(self):
		return self._trigger
	@trigger.setter
	def trigger(self, value):
		self._trigger = value
	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
	@gdmethod
	def _ready(self):
		if self._trigger:
			trigger = self.get_node(self._trigger)
			self.trigger_obj = Node.cast(trigger)
	
	@gdmethod
	def start_pushing(self):
		print("start pushing")
	
	@gdmethod
	def get_triggers(self):
		return self.trigger_obj.get_children()

