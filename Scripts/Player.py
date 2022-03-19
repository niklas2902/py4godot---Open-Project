from py4godot import *

DEFAULT_VEL = 5
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
		self._max_dist = DEFAULT_DIST

	@gdproperty(int, DEFAULT_VEL, hint=PropertyHint.GODOT_PROPERTY_HINT_RANGE.value, hint_string="1,10,1,slider")
	def vel(self):
		return self.velocity
	@vel.setter
	def vel(self, value):
		self.velocity = value
	
	@gdproperty(int, DEFAULT_DIST, hint=PropertyHint.GODOT_PROPERTY_HINT_RANGE.value, hint_string="1,10,1,slider")
	def vel(self):
		return self._max_dist
	@vel.setter
	def vel(self, value):
		self._max_dist = value

	@gdmethod
	def _ready(self):
		print("_init")
		self.input = Input.instance()
	
	@gdmethod
	def _process(self, delta):
		self.set_key_pressed()
		self.move(delta)
	
	def move(self, delta):
		vertical_modifier = self.move_vertical_val()
		horizontal_modifier = self.move_horizontal_val()
		if horizontal_modifier and vertical_modifier:
			horizontal_modifier, vertical_modifier = 0,0
		
		self.move_and_collide(Vector3(self.vel * horizontal_modifier,0,self.vel * vertical_modifier) * delta, True, True, False)
	
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
