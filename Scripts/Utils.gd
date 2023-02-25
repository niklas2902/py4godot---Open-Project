extends Spatial

func sphere_cast(origin, radius, exclude, layer):
	var shape = SphereShape.new()
	shape.set_radius(radius)
	
	var params = PhysicsShapeQueryParameters.new()
	params.set_shape(shape)
	if(layer != -1):
		params.collision_mask = layer
	params.set_transform(get_transform().translated(origin)) # same transform as parent, just translate
	
	if exclude != null:
		params.set_exclude(exclude) # here exclude is an array of... RID??
	var res = get_world().direct_space_state.intersect_shape(params, 1)
	return res



func box_cast(origin, x, y, z, exclude, layer):
	var shape = BoxShape.new()
	shape.extents = Vector3(x,y,z)

	var params = PhysicsShapeQueryParameters.new()
	params.set_shape(shape)
	if(layer != -1):
		params.collision_mask = layer
	params.set_transform(get_transform().translated(origin)) # same transform as parent, just translate

	if exclude != null:
		params.set_exclude(exclude) # here exclude is an array of... RID??
	var res = get_world().direct_space_state.intersect_shape(params, 1)
	return res
