extends Spatial

func sphere_cast(origin, radius, direction, hit_info, max_distance, exclude):
    var shape = SphereShape()
    shape.set_radius(radius)

    var params = PhysicsShapeQueryParameters()
    params.set_shape(shape)
    params.set_transform(get_transform().translated(origin)) # same transform as parent, just translate
    params.set_motion(direction*max_distance) # is "motion" the sweep distance?
    if exclude != null:
        param.set_exclude(exclude) # here exclude is an array of... RID??
    var res = PhysicsServer.intersect_shape(params, 1)
    return res