from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *
from Scripts.Tools.Draw import Draw

ARROW_RAD = 0.5
@gdtool
class PushObj(StaticBody, Draw):

	@gdproperty(NodePath, NodePath())
	def trigger(self)->NodePath:
		return self._trigger
	@trigger.setter
	def trigger(self, value:NodePath)->None:
		self._trigger = value


	@gdproperty(NodePath, NodePath())
	def arrows(self)->NodePath:
		return self._arrows
	@arrows.setter
	def arrows(self, value:NodePath):
		self._arrows = value
	def __init__(self):
		#Don't call any godot-methods here
		super().__init__()
		self._arrow_obj = None
		
	@gdmethod
	def _ready(self):
		if self._trigger:
			trigger:Node = self.get_node(self._trigger)
			self.trigger_obj:Node = Node.cast(trigger)
		
		print("arrows:", self.arrows)
		if(self._arrows):
			arrows:Node = self.get_node(self.arrows)
			self._arrow_obj:Node = Node.cast(arrows)
		
		if(not self._arrow_obj):
			return
		for child in self._arrow_obj.get_children():
			self.immediate_geometry_init(self, child.get_name())
			
	@gdmethod
	def _process(self, delta):
		if(not self._arrow_obj):
			return
			
		for child in self._arrow_obj.get_children():
			self.draw_sphere(child.get_name(), ARROW_RAD, child.global_transform.get_origin())
	
	@gdmethod
	def start_pushing(self):
		print("start pushing")
	
	@gdmethod
	def get_triggers(self):
		return self.trigger_obj.get_children()

