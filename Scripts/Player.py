from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

DEFAULT_VEL = 2
DEFAULT_DIST = 50
@gdclass
class Player(KinematicBody):
	def __init__(self):
		super().__init__()
		self.velocity = DEFAULT_VEL
		self.left_pressed = False
		self.right_pressed = False
		self.up_pressed = False
		self.down_pressed = False
		self.current_dist = 0
		self.save_vertical_move = 0
		self.save_horizontal_move = 0
		self._max_dist = 2

	@gdproperty(int, DEFAULT_VEL,hint = RangeHint(1,10))
	def vel(self):
		return self.velocity
	@vel.setter
	def vel(self, value):
		self.velocity = value
	
	@gdproperty(int, DEFAULT_DIST, hint=RangeHint(1,10))
	def max_dist(self):
		return self._max_dist
	@max_dist.setter
	def max_dist(self, value):
		self._max_dist = value

	@gdmethod
	def _ready(self):
		self.input = Input.instance()
	
	@gdmethod
	def _process(self, delta):
		self.set_key_pressed()
		self.reset_move()
		self.move(delta)
	
	def reset_move(self):
		"""Resetting, after player moved a block"""
		if(self.current_dist > self.max_dist):
			self.current_dist = 0
			self.transform.set_origin(self.round_vector(self.transform.get_origin()))
			self.save_horizontal_move = 0
			self.save_vertical_move = 0
			
	def round_vector(self, vector):
		"""Function for rounding the position after arriving"""
		return Vector3(round(vector.get_axis(Vector3_Axis.X.value)), 
		round(vector.get_axis(Vector3_Axis.Y.value)),
		round(vector.get_axis(Vector3_Axis.Z.value)))
	
	def move(self, delta):
		if(self.save_horizontal_move == 0 and self.save_vertical_move == 0):
			vertical_modifier = self.move_vertical_val()
			horizontal_modifier = self.move_horizontal_val()
			if horizontal_modifier and vertical_modifier:
				horizontal_modifier, vertical_modifier = 0,0
			self.save_horizontal_move, self.save_vertical_move = horizontal_modifier, vertical_modifier
		
		move_vector = Vector3(self.save_horizontal_move,0,self.save_vertical_move)
		
		self.move_and_collide(move_vector* delta * self.vel)
		self.current_dist += move_vector.length() * delta * self.vel
		
	
	def move_vertical_val(self):
		val = 0
		if self.up_pressed and self.down_pressed:
			val = 0
		elif not self.up_pressed and self.down_pressed:
			val = 1
		elif self.up_pressed and not self.down_pressed:
			val = -1
		
		return val
	
	def move_horizontal_val(self):
		val = 0
		if self.left_pressed and self.right_pressed:
			val = 0
		elif not self.left_pressed and self.right_pressed:
			val = 1
		elif self.left_pressed and not self.right_pressed:
			val = -1
		
		return val
	def set_key_pressed(self):
		"""Function for setting pressed keys"""
		self.left_pressed = self.input.is_key_pressed(GlobalConstants.KEY_A)
		self.right_pressed = self.input.is_key_pressed(GlobalConstants.KEY_D)
		self.up_pressed = self.input.is_key_pressed(GlobalConstants.KEY_W)
		self.down_pressed = self.input.is_key_pressed(GlobalConstants.KEY_S)
