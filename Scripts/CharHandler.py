from py4godot import *
import math
from Scripts.Tools.Draw import Draw
from Scripts.Navigation.AStar import AStar as NavAstar
from typing import Optional

DEFAULT_MAX_DIST = 10
DEFAULT_SPRINT_DIST = 200
GRAVITY = 20
SPHERE_HANDLE = "SPHERE"
RAY_HANDLE = "RAY"
DIST_NAVIGATION = 0.1
MOUSE_ACTION = "mouse_action"


@gdclass
class CharHandler(KinematicBody, Draw):

	def __init__(self):
		# Don't call any godot-methods here
		super().__init__()
		self.rotation_angle: float = 0
		self.y_speed: float = 0
		self.is_on_ramp: bool = False
		self.sound: float = 0
		self._push_obj_layer: int = 0
		self._clicked_before: bool = False
		self.selected_push_obj: Optional[KinematicBody] = None
		self.push_obj_selected: Optional[Object] = None
		self.is_pushing: bool = False
		self._max_dist: float = DEFAULT_MAX_DIST
		self._sprint_dist: float = DEFAULT_SPRINT_DIST
		self.test = None
		self.astar_path:Optional[NodePath] = None
		self._astar:Optional[NavAstar] = None

		print("init CharHandler")

	prop("test", NodePath, NodePath())
	prop("astar_path", NodePath, NodePath())

	@gdproperty(NodePath, NodePath())
	def node(self) -> NodePath:
		return self._node

	@node.setter
	def node(self, value: NodePath):
		self._node = value

	@gdproperty(NodePath, NodePath())
	def navigation(self) -> NodePath:
		return self._navigation

	@navigation.setter
	def navigation(self, value: NodePath):
		self._navigation = value

	@gdproperty(float, DEFAULT_MAX_DIST)
	def max_dist(self) -> float:
		return self._max_dist

	@max_dist.setter
	def max_dist(self, value: float):
		self._max_dist = value

	@gdproperty(float, DEFAULT_SPRINT_DIST)
	def sprint_dist(self) -> float:
		return self._sprint_dist

	@sprint_dist.setter
	def sprint_dist(self, value: float):
		self._sprint_dist = value

	@gdproperty(int, 0, hint=RangeHint(0, 2147483647))
	def push_obj_layer(self) -> int:
		return self._push_obj_layer

	@push_obj_layer.setter
	def push_obj_layer(self, value):
		self._push_obj_layer = value

	@gdmethod
	def test_call(self):
		return Array()

	@gdmethod
	def _ready(self):
		print("ready_Char Handler")
		self.path: Optional[Array] = None
		self.current_path_ind: int = 0
		self.immediate_geometry_init(self, SPHERE_HANDLE)
		self.immediate_geometry_init(self, RAY_HANDLE)
		self.input: Input = Input.instance()
		self.save_rotation: int = 0
		node = self.get_node(self._node)
		self.animation_tree: AnimationTree = AnimationTree.cast(node)

		nav: Node = self.get_node(self._navigation)
		self.navigation_obj: Navigation = Navigation.cast(nav)

		# Taken from: https://github.com/godotengine/tps-demo/blob/master/player/player.gd
		self.orientation: Transform = self.transform
		self.root_motion: Transform = Transform.new_with_axis_origin(Vector3(1, 0, 0), Vector3(0, 1, 0),
																	 Vector3(0, 0, 1), Vector3(0, 0, 0))
		self.motion: Vector2 = Vector2(0, 0)
		self.velocity: Vector3 = Vector3(0, 0, 0)
		print("end_ ready_Char Handler")

		# self.orientation.set_basis(self.orientation.get_basis().rotated(Vector3(0,1,0), math.pi*-self.rotation_angle))
		self.orientation.set_basis(Basis.new_with_axis_and_angle(Vector3(0, 1, 0), math.pi * -self.rotation_angle))

		if (self._max_dist == None):
			self._max_dist = DEFAULT_MAX_DIST
		if self._sprint_dist == None:
			self._sprint_dist = DEFAULT_SPRINT_DIST
		a = NavigationMeshInstance._new()
		self._astar = self.get_node(self.astar_path).get_pyscript()

	@gdmethod
	def _process(self, delta: float):
		self.emit_sound()

	@gdmethod
	def _physics_process(self, delta: float):
		ignore: bool = False
		self.handle_ray()
		self.draw_sphere(SPHERE_HANDLE, 2, self.transform.get_origin())

		mouse_angle: float = self.follow_path(delta)
		self.apply_gravity(delta)
		self.animation_tree.set("parameters/Movement/blend_position", Variant(1))
		if (self.path == None):
			mouse_angle = self.mouse_angle()
			if (mouse_angle != None):
				pass
			# self.selected_push_obj = None
			if (self.is_pushing and mouse_angle != None):
				mouse_angle = (round(mouse_angle / (math.pi / 2))) * (math.pi / 2)
			self.set_key_pressed()
			if self.is_pushing:
				if not self.selected_push_obj.callv("is_move_allowed",
													Array(self.get_move_dir())).get_converted_value():
					ignore = True
			self.apply_root_motion(delta, mouse_angle)
			self.animation_tree.set("parameters/Movement/blend_position", Variant(min(1, self.get_speed(ignore))))

		if (mouse_angle != None):
			self.orientation.set_basis(Basis.new_with_axis_and_angle(Vector3(0, 1, 0), mouse_angle))

		self.sound = min(1, self.get_speed(ignore))

		if (self.selected_push_obj != None):
			# print("delta_pushing:",self.selected_push_obj.call("get_delta_pushing").get_converted_value())
			self.selected_push_obj.global_transform.set_origin(self.global_transform.get_origin() + \
															   self.selected_push_obj.call(
																   "get_delta_pushing").get_converted_value())

	@gdmethod
	def entered_ramp(self):
		self.is_on_ramp = True

	def exited_ramp(self):
		self.is_on_ramp = False

	def get_move_dir(self) -> Vector2:
		if self.input.is_action_pressed(MOUSE_ACTION):
			mouse_pos: Vector2 = self.get_viewport().get_mouse_position()
			object_pos: Vector2 = self.get_viewport().get_camera().unproject_position(self.transform.get_origin())
			if (abs(object_pos.get_x() - mouse_pos.get_x()) > abs(object_pos.get_y() - mouse_pos.get_y())):
				return Vector2((object_pos.get_x() - mouse_pos.get_x()) /
							   abs(object_pos.get_x() - mouse_pos.get_x()), 0)
			else:
				return Vector2(0,
							   (object_pos.get_y() - mouse_pos.get_y()) / abs(object_pos.get_y() - mouse_pos.get_y()))
		return Vector2(0, 0)

	def apply_gravity(self, delta):
		"""applying gravity to the player"""
		if (not self.is_on_floor()) and not self.is_on_ramp:
			self.y_speed += GRAVITY
			self.move_and_slide(Vector3(0, self.y_speed, 0) * -1 * delta, Vector3(0, 1, 0))
		else:
			self.y_speed = 0

	def mouse_angle(self) -> Optional[float]:
		"""Getting the angle of the mouse to be able to move to a position"""
		if (self.input.is_action_just_released(MOUSE_ACTION)):
			self._clicked_before = False
			self.reset_pushing()

		if self.input.is_action_pressed(MOUSE_ACTION):
			mouse_pos: Vector2 = self.get_viewport().get_mouse_position()
			object_pos: Vector2 = self.get_viewport().get_camera().unproject_position(self.transform.get_origin())
			if (mouse_pos - object_pos).length() <= self.max_dist:
				return
			self._clicked_before = True
			return math.atan2(object_pos.get_x() - mouse_pos.get_x(),
							  object_pos.get_y() - mouse_pos.get_y())
		return

	def reset_pushing(self) -> None:
		"""function for resetting push, so that it gets aborted"""
		self.is_pushing = False
		self.push_obj_selected = None
		self.selected_push_obj = None

	def get_speed(self, ignore: bool = False) -> float:
		"""Getting the angle of the mouse to be able to move to a position"""
		if self.input.is_action_pressed(MOUSE_ACTION) and not ignore:
			mouse_pos = self.get_viewport().get_mouse_position()
			object_pos = self.get_viewport().get_camera().unproject_position(self.transform.get_origin())

			return (mouse_pos - object_pos).length() / self.sprint_dist
		return 0

	def apply_root_motion(self, delta: float, angle: float):
		# Taken from: https://github.com/godotengine/tps-demo/blob/master/player/player.gd
		# and https://www.youtube.com/watch?v=2AUMMmTNijg&list=LL&index=1

		self.root_motion = self.animation_tree.get_root_motion_transform()
		self.orientation *= self.root_motion

		h_velocity: Vector3 = self.orientation.get_origin() / delta
		self.velocity.set_axis(0, h_velocity.get_axis(0))
		self.velocity.set_axis(2, h_velocity.get_axis(2))
		# Fix -1 in movement
		self.velocity = self.move_and_slide(self.velocity * -1 * delta, Vector3(0, 1, 0))
		self.orientation.set_origin(Vector3(0, 0, 0))
		self.orientation = self.orientation.orthonormalized()

		trans: Transform = Transform(self.orientation.get_basis(), self.global_transform.get_origin())
		self.global_transform = trans

	def set_key_pressed(self):
		"""Function for setting pressed keys"""
		self.left_pressed = self.input.is_key_pressed(GlobalConstants.KEY_A)
		self.right_pressed = self.input.is_key_pressed(GlobalConstants.KEY_D)
		self.up_pressed = self.input.is_key_pressed(GlobalConstants.KEY_W)
		self.down_pressed = self.input.is_key_pressed(GlobalConstants.KEY_S)

	def emit_sound(self):
		pass

	# print("sound:",self.sound)

	def follow_path(self, delta: float):
		if self.path == None:
			return

		if self.current_path_ind >= self.path.size():
			self.path = None
			self.current_path_ind = 0
			self.selected_push_obj = self.push_obj_selected
			self.selected_push_obj.callv("start_pushing", Array(self))
			self.is_pushing = True
			return

		pos: Vector3 = self.transform.get_origin()
		dist_vector = self.path[self.current_path_ind] - self.transform.get_origin()
		dist_vector.y = 0
		dist: float = dist_vector.length()
		vel: float = (self.path[self.current_path_ind] - self.transform.get_origin())
		if dist < DIST_NAVIGATION:
			self.current_path_ind += 1
		vel_z = vel.z
		if vel.z == 0:
			vel_z = 0.001
		self.apply_root_motion(delta, math.atan2(vel.x, vel_z))
		return math.atan2(vel.x, vel_z)

	def handle_ray(self):
		"""handling the player clicking on a PushObj here"""
		if self.input.is_action_just_pressed(MOUSE_ACTION):
			if (self._clicked_before):
				return

			self.path: Array = None
			self.current_path_ind: int = 0
			ray_length: float = 100000
			mouse_pos: Vector2 = self.get_viewport().get_mouse_position()
			camera: Camera = self.get_viewport().get_camera()
			from_: Vector3 = camera.project_ray_origin(mouse_pos)
			to: Vector3 = from_ - camera.project_ray_normal(mouse_pos) * ray_length
			exclude: Array = Array()
			exclude.append(self)

			result = self.get_world().direct_space_state.intersect_ray(from_,
																	   from_ + camera.project_ray_normal(
																		   mouse_pos) * ray_length, exclude,
																	   collision_mask=self.push_obj_layer)
			print("result:", result["name"])

			if result["position"] == None:
				return None

			self.push_obj_selected = result["collider"]
			point_to_move_to = self.get_min_point(result["position"],
												  result["collider"].get_node(NodePath("Triggers")).get_children(),
												  result["collider"])

			self.draw_sphere(RAY_HANDLE, 0.5, point_to_move_to.global_transform.get_origin())
			#self.path = self.navigation_obj.get_simple_path(self.global_transform.get_origin(),
			#												point_to_move_to.global_transform.get_origin())
			self.path = Array()
			for path_point in self._astar.get_way_points(self.global_transform.get_origin(),
												   point_to_move_to.global_transform.get_origin()):
				self.path.append(path_point)
			for point in self.path:
				print(point)
			self.current_path_ind = 1

	def get_min_point(self, collider: Spatial, points: Array, alt_object: Spatial):
		if (points.size() == 0):
			return alt_object
		return_val: Spatial = points[0]
		min_dist: float = abs((collider - points[0].global_transform.get_origin()).length())

		for point_index in range(1, points.size()):
			point: Spatial = points[point_index]
			length: float = abs((collider - point.global_transform.get_origin()).length())
			if (min_dist > length):
				return_val = point
				min_dist = length
		return return_val
