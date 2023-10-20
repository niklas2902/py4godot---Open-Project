from py4godot.classes.generated import *
from py4godot.core import *
from py4godot.pluginscript_api.utils.annotations import *
import enum


class State(enum.Enum):
	OUT = enum.auto(),
	IN = enum.auto()


@gdclass
class Spike(Spatial):
	prop("activation_time", float, 2)

	enabled: bool
	activation_time: float
	_current_delta_time: float
	state: State

	def __init__(self) -> None:
		super().__init__()
		self.enabled: bool = True
		self._current_delta_time = 0
		self.state = State.IN

	@gdmethod
	def _ready(self) -> None:
		if not self.enabled:
			self.state = State.IN

	@gdmethod
	def _process(self, delta: float) -> None:
		if self._current_delta_time > self.activation_time:
			self.toggle_state()
			self._current_delta_time = 0
		self._current_delta_time += delta

	def toggle_state(self) -> None:
		self.state = State.IN if self.state == State.OUT else State.OUT
		self.animate_state()

	def animate_state(self) -> None:

		mesh: CSGMesh= CSGMesh.cast(self.get_child(0))
		
		material: SpatialMaterial = SpatialMaterial.cast(mesh.get_material())

		if material == None:
			# print("before new_mat")
			new_mat: SpatialMaterial = SpatialMaterial._new()
			mesh.material = new_mat
			material = SpatialMaterial.cast(mesh.get_material())

		material.albedo_color = Color(1, 0, 0) if self.state == State.IN else Color(0, 1, 0)
