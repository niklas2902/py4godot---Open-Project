from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *


@gdclass
class Projectile(Spatial):
	velocity: Vector3

	def __init__(self):
		# Don't call any godot-methods here
		super().__init__()

	@gdmethod
	def _ready(self) -> None:
		self.velocity = Vector3(1, 0, 0)

	@gdmethod
	def _process(self, delta: float) -> None:
		self.global_transform.set_origin(self.global_transform.get_origin() + self.velocity * delta)
