extends Spatial

func sphere_cast(origin, radius, exclude, layer):
	print("call")
	var shape = SphereShape.new()
	shape.set_radius(radius)

	var params = PhysicsShapeQueryParameters.new()
	params.set_shape(shape)
	params.set_transform(get_transform().translated(origin)) # same transform as parent, just translate
	if exclude != null:
		params.set_exclude(exclude) # here exclude is an array of... RID??
	var res = get_world().direct_space_state.intersect_shape(params, 1)
	return res
