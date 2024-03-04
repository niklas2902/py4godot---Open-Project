import math

from py4godot.classes.AnimationTree.AnimationTree import AnimationTree
from py4godot.classes.CPUParticles3D.CPUParticles3D import CPUParticles3D
from py4godot.classes.Camera3D.Camera3D import Camera3D
from py4godot.classes.CharacterBody3D.CharacterBody3D import CharacterBody3D
from py4godot.classes.Input.Input import Input
from py4godot.classes.Node.Node import Node
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.classes.Object.Object import Object
from py4godot.classes.generated4_core import NodePath, Vector3, Vector2, Basis, Dictionary, Array, Transform3D, \
	StringName
from py4godot.classes.typedarrays import RIDTypedArray
from py4godot.pluginscript_api.utils.annotations import gdclass, gdmethod

import typing
from Scripts.InteractionObjects.Lever import Lever
from Scripts.Navigation.AStar import AStar as NavAstar, AStar
from Scripts.PushObj import PushObj
from Scripts.Tools.Draw import Draw
from py4godot.classes.utils import get_viewport

from py4godot.classes.PhysicsRayQueryParameters3D.PhysicsRayQueryParameters3D import PhysicsRayQueryParameters3D
from py4godot.pluginscript_api.utils.experimental import gdproperty
from py4godot.utils.print_tools import print_error
from typing import Optional

DEFAULT_MAX_DIST = 10
DEFAULT_SPRINT_DIST = 200
GRAVITY = 20
SPHERE_HANDLE = "SPHERE"
RAY_HANDLE = "RAY"
DIST_NAVIGATION = 0.2
MOUSE_ACTION = StringName.new2("mouse_action")


@gdclass
class CharHandler(CharacterBody3D, Draw):
	selected_push_obj: Optional[Node3D]
	push_obj_selected: Optional[Node3D]
	lever_obj_selected: Optional[Lever]
	astar_path: NodePath
	_astar: NavAstar

	rotation_angle: float
	y_speed: float
	is_on_ramp: bool
	sound: float
	_push_obj_layer: int
	_clicked_before: bool
	is_pushing: bool
	_max_dist: float
	_sprint_dist: float
	_move_possible: bool
	_particle_system: CPUParticles3D

	# properties
	can_move: bool = gdproperty(bool, True)
	astar_path: NodePath = gdproperty(NodePath, NodePath.new0())
	particle_path: NodePath = gdproperty(NodePath, NodePath.new0())
	animation_tree_path: NodePath = gdproperty(NodePath, NodePath.new0())
	max_dist: float = gdproperty(float, 0)
	sprint_dist: float = gdproperty(float, 0)
	push_obj_layer = gdproperty(int, 0)

	def __init__(self) -> None:
		# Don't call any godot-methods here
		super().__init__()
		self.is_on_ramp = False
		self._clicked_before = False
		self._move_possible = False
		self._max_dist = DEFAULT_MAX_DIST
		self._sprint_dist = DEFAULT_SPRINT_DIST
		self.sound = 0
		self.rotation_angle = 0
		self._move_possible = True
		self.y_speed = 0
		self.is_pushing = False
		self.selected_push_obj = None
		self.lever_obj_selected = None
		self.path = None
		self.current_path_ind = 0

	@gdmethod
	def test_call(self):
		return Array.new0()

	@gdmethod
	def _ready(self):
		self.path: Optional[Array] = None
		self.current_path_ind: int = 0
		self.immediate_geometry_init(self, SPHERE_HANDLE)
		self.immediate_geometry_init(self, RAY_HANDLE)
		self.input: Input = Input.get_instance()
		self.save_rotation: int = 0
		node = self.get_node(self.animation_tree_path)
		self.animation_tree: AnimationTree = AnimationTree.cast(node)

		particle: Node = self.get_node(self.particle_path)
		self._particle_system = CPUParticles3D.cast(particle)

		#        print(self._particle_system.name)
		# Taken from: https://github.com/godotengine/tps-demo/blob/master/player/player.gd
		self.orientation: Transform3D = Transform3D.new1(self.transform)

		vector: Vector3 = Vector3.new3(1, 0, 0)
		vector.x = 1

		origin = self.transform.origin
		self.root_motion = Transform3D.new3(Vector3.new3(0, 0, 0), Vector3.new3(0, 0, 0), Vector3.new3(0, 0, 0),
											origin)
		self.root_motion: Transform3D = Transform3D.new0()
		self.root_motion.origin = self.global_position
		self.root_motion.set_basis(self.transform.basis)

		self.motion: Vector2 = Vector2.new3(0, 0)
		self.velocity: Vector3 = Vector3.new3(0, 0, 0)

		# self.orientation.set_basis(self.orientation.get_basis().rotated(Vector3(0,1,0), math.pi*-self.rotation_angle))
		self.orientation.basis = Basis.new3(Vector3.new3(0, 1, 0), math.pi * -self.rotation_angle)

		if self._max_dist is None:
			self._max_dist = DEFAULT_MAX_DIST
		if self._sprint_dist is None:
			self._sprint_dist = DEFAULT_SPRINT_DIST
		self._astar = typing.cast(AStar, self.get_node(self.astar_path).get_pyscript())

	# TODO:enable self._particle_system.emitting = False

	@gdmethod
	def _process(self, delta: float):
		# debugpy.breakpoint()
		if not self.can_move:
			return
		# TODO:enable self._particle_system.emitting = self.get_speed() > 0.9
		self.emit_sound()

	@gdmethod
	def _physics_process(self, delta: float):

		if not self.can_move or not self._move_possible:
			self.animation_tree.set(StringName.new2("parameters/Movement/blend_position"), 0)
			return
		ignore: bool = False
		self.handle_ray()
		self.draw_sphere(SPHERE_HANDLE, 2, self.transform.get_origin())

		mouse_angle: float = self.follow_path(delta)
		self.apply_gravity(delta)
		path = StringName.new2("parameters/Movement/blend_position")
		self.animation_tree.set(path, 1)

		if self.path is None:
			mouse_angle = self.mouse_angle()
			if mouse_angle is None:
				pass
		self.selected_push_obj = None
		if self.is_pushing and mouse_angle is not None:
			mouse_angle = (round(mouse_angle / (math.pi / 2))) * (math.pi / 2)
		if self.is_pushing:
			if not self.selected_push_obj.callv("is_move_allowed",
												Array(self.get_move_dir())):
				ignore = True
		self.apply_root_motion(delta, mouse_angle)
		self.animation_tree.set(StringName.new2("parameters/Movement/blend_position"),
								(min(1., self.get_speed(ignore))))

		if mouse_angle is not None:
			self.orientation.basis = Basis.new3(Vector3.new3(0, 1, 0), mouse_angle)

		self.sound = min(1., self.get_speed(ignore))

		if self.selected_push_obj is not None:
			self.selected_push_obj.global_transform.set_origin(self.global_transform.get_origin() +
															   self.selected_push_obj.call(
																   "get_delta_pushing"))

	@gdmethod
	def entered_ramp(self) -> None:
		self.is_on_ramp = True and not self.selected_push_obj

	@gdmethod
	def set_can_move(self, value: bool) -> None:
		self.can_move = value

	def exited_ramp(self):
		self.is_on_ramp = False

	def get_move_dir(self) -> Vector2:
		if self.input.is_action_pressed(MOUSE_ACTION):
			mouse_pos: Vector2 = get_viewport(self).get_mouse_position()
			object_pos: Vector2 = get_viewport(self).get_camera_3d().unproject_position(self.transform.get_origin())
			# noinspection PyTypeChecker
			if abs(object_pos.x - mouse_pos.x) > abs(object_pos.y - mouse_pos.y):
				# noinspection PyTypeChecker
				return Vector2.new3((object_pos.x - mouse_pos.x) /
									abs(object_pos.x - mouse_pos.x), 0)
			else:
				# noinspection PyTypeChecker
				return Vector2.new3(0,
									(object_pos.y - mouse_pos.y) / abs(object_pos.y - mouse_pos.y))
		return Vector2.new3(0, 0)

	def apply_gravity(self, delta):
		"""applying gravity to the player"""
		if (not self.is_on_floor()) and not self.is_on_ramp:
			self.y_speed += GRAVITY
			self.set_velocity(Vector3.new3(0, self.y_speed, 0) * -1 * delta)
			self.set_up_direction(Vector3.new3(0, 1, 0))
			self.move_and_slide()
		else:
			self.y_speed = 0

	def mouse_angle(self) -> Optional[float]:
		"""Getting the angle of the mouse to be able to move to a position"""
		if self.input.is_action_just_released(MOUSE_ACTION):
			self._clicked_before = False
			self.reset_pushing()

		if self.input.is_action_pressed(MOUSE_ACTION):
			mouse_pos: Vector2 = get_viewport(self).get_mouse_position()
			object_pos: Vector2 = get_viewport(self).get_camera_3d().unproject_position(self.transform.get_origin())
			if (mouse_pos - object_pos).length() <= self.max_dist:
				return
			self._clicked_before = True
			# noinspection PyTypeChecker
			return math.atan2(object_pos.x - mouse_pos.x,
							  object_pos.y - mouse_pos.y)
		return

	def reset_pushing(self) -> None:
		"""function for resetting push, so that it gets aborted"""
		self.is_pushing = False
		if self.selected_push_obj:
			push_obj_pos: Vector3 = self.selected_push_obj.transform.get_origin()
			self._astar.disable_points(round(push_obj_pos.x), round(push_obj_pos.z), 2, 2)
		self.push_obj_selected = None
		self.selected_push_obj = None

	def get_speed(self, ignore: bool = False) -> float:
		"""Getting the angle of the mouse to be able to move to a position"""
		if self.input.is_action_pressed(MOUSE_ACTION) and not ignore:
			mouse_pos = get_viewport(self).get_mouse_position()
			object_pos = get_viewport(self).get_camera_3d().unproject_position(self.transform.get_origin())

			return (mouse_pos - object_pos).length() / self.sprint_dist
		return 0

	def apply_root_motion(self, delta: float, angle: float):
		# Taken from: https://github.com/godotengine/tps-demo/blob/master/player/player.gd
		# and https://www.youtube.com/watch?v=2AUMMmTNijg&list=LL&index=1
		pos: Vector3 = self.animation_tree.get_root_motion_position()
		accumulator: Vector3 = self.animation_tree.get_root_motion_position_accumulator()
		self.root_motion = Transform3D.new2(Basis.new3(Vector3.new3(0, 1, 0),
													   self.animation_tree.get_root_motion_rotation().get_angle()),
											pos)
		self.orientation *= self.root_motion

		h_velocity: Vector3 = self.orientation.origin

		h_velocity.y = 0
		self.velocity = h_velocity
		# Fix -1 in movement
		self.set_velocity(h_velocity * -1 * (1.0 / delta))
		self.set_up_direction(Vector3.new3(0, 1, 0).normalized())
		# self.velocity = self.get_velocity()
		self.move_and_slide()
		self.orientation.origin = Vector3.new3(0, 0, 0)
		self.orientation = self.orientation.orthonormalized()

		self.global_transform = Transform3D.new2(self.orientation.get_basis(), self.global_transform.get_origin())

	def emit_sound(self):
		pass

	def follow_path(self, delta: float):
		if self.path is None:
			return

		if self.current_path_ind >= self.path.size():
			self.path = None
			self.current_path_ind = 0
			if self.push_obj_selected:
				self.selected_push_obj = self.push_obj_selected
				self.selected_push_obj.callv("start_pushing", Array(self))
				scripts: PushObj = typing.cast(PushObj, self.selected_push_obj.get_pyscript())
				self._astar.enable_points(round(scripts.pos_before.x), round(scripts.pos_before.z), 2, 2)
				self.is_pushing = True

				self.face_push_obj()
			if self.lever_obj_selected:
				self.lever_obj_selected.trigger_connected_object()
				self.lever_obj_selected = None
			return

		dist_vector = self.path[self.current_path_ind] - self.transform.get_origin()
		dist_vector.y = 0
		dist: float = dist_vector.length()
		vel: Vector3 = (self.path[self.current_path_ind] - self.transform.get_origin())
		if dist < DIST_NAVIGATION:
			self.current_path_ind += 1
		vel_z = vel.z
		if vel.z == 0:
			vel_z = 0.001
		# noinspection PyTypeChecker
		self.apply_root_motion(delta, math.atan2(vel.x, vel_z))
		# noinspection PyTypeChecker
		return math.atan2(vel.x, vel_z)

	def face_push_obj(self) -> None:
		angle_to = math.atan2(
			-(self.global_transform.get_origin().x - self.selected_push_obj.global_transform.get_origin().x),
			-(self.global_transform.get_origin().z - self.selected_push_obj.global_transform.get_origin().z))
		self.orientation.basis = Basis.new3(Vector3(0, 1, 0), angle_to)

	def handle_ray(self) -> None:
		"""handling the player clicking on a PushObj here"""
		if self.input.is_action_just_pressed(MOUSE_ACTION):
			if self._clicked_before:
				return

			self.path = None
			self.current_path_ind: int = 0
			ray_length: float = 100000
			mouse_pos: Vector2 = get_viewport(self).get_mouse_position()
			camera: Camera3D = get_viewport(self).get_camera_3d()
			from_: Vector3 = camera.project_ray_origin(mouse_pos)
			to: Vector3 = from_ - camera.project_ray_normal(mouse_pos) * ray_length
			exclude: RIDTypedArray = RIDTypedArray.new0()
			# exclude.append(self)

			params: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.constructor()
			params.from_ = from_
			params.to = from_ + camera.project_ray_normal(mouse_pos) * ray_length
			params.exclude = exclude
			params.collision_mask = self.push_obj_layer
			result = self.get_world_3d().direct_space_state.intersect_ray(params)

			if result["position"] == None:
				return None

			self.interpret_result(result)

	def interpret_result(self, result) -> None:
		collider: Object = result["collider"].get_pyscript()
		# TODO: Check why isinstance is not working
		if collider.__class__.__name__ == PushObj.__name__:
			self.handle_ray_hit_push_obj(result)
		elif collider.__class__.__name__ == Lever.__name__:
			self.handle_ray_hit_lever(result)
		else:
			raise Exception("handled click on unknown class")

	def handle_ray_hit_lever(self, result: Dictionary) -> None:
		point_to_move_to: Vector3 = typing.cast(Vector3, result["position"])
		point_to_move_to = Vector3(point_to_move_to.x, 0, point_to_move_to.z)
		self.draw_sphere(RAY_HANDLE, 0.5, point_to_move_to)
		self.path = Array()
		for path_point in self._astar.get_way_points(self.global_transform.get_origin(),
													 point_to_move_to):
			self.path.append(path_point)
		self.current_path_ind = 1
		self.lever_obj_selected = typing.cast(Node, result["collider"]).get_pyscript()

	def handle_ray_hit_push_obj(self, result: Dictionary) -> None:
		self.push_obj_selected = result["collider"]
		point_to_move_to = self.get_min_point(result["position"],
											  result["collider"].get_node(NodePath("Triggers")).get_children(),
											  result["collider"])
		self.draw_sphere(RAY_HANDLE, 0.5, point_to_move_to.global_transform.get_origin())
		self.path = Array()
		for path_point in self._astar.get_way_points(self.global_transform.get_origin(),
													 point_to_move_to.global_transform.get_origin()):
			self.path.append(path_point)
		self.current_path_ind = 1

	def get_min_point(self, collider: Vector3, points: Array, alt_object: Node3D):
		if (points.size() == 0):
			return alt_object
		return_val: Node3D = points[0]
		# noinspection PyTypeChecker
		min_dist: float = abs((collider - points[0].global_transform.get_origin()).length())

		for point_index in range(1, points.size()):
			point: Node3D = points[point_index]
			# noinspection PyTypeChecker
			length: float = abs((collider - point.global_transform.get_origin()).length())
			if (min_dist > length):
				return_val = point
				min_dist = length
		return return_val

	def _on_Camera_zoomed_out(self) -> None:
		self.can_move = False

	def _on_Camera_zoomed_in(self) -> None:
		self.can_move = True

	@gdmethod
	def move_impossible(self) -> None:
		self._move_possible = False

	@gdmethod
	def move_possible(self) -> None:
		self._move_possible = True

	def lose_life(self):
		print("lose life")
