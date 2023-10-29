from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Scripts.Enemy.Objects.Spawner import Spawner
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *



@gdclass
class Projectile(Spatial):
	velocity: Vector3

	lifetime: float
	_current_lifetime_counter: float
	spawner:Spawner

	prop("lifetime", float, 10)
	register_signal("lifetime_over")

	@gdmethod
	def _ready(self) -> None:
		self._current_lifetime_counter = 0
		self.velocity = Vector3(1,0,0)

	@gdmethod
	def _process(self, delta: float) -> None:
		self._current_lifetime_counter += delta
		if (self._current_lifetime_counter > self.lifetime):
			self.spawner.lifetime_over(self)
		self.global_transform.set_origin(self.global_transform.get_origin() + self.velocity * delta)
