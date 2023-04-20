extends Node


# Declare member variables here. Examples:
export var node = NodePath(".")
# var b = "text"

signal finished_animation

func tween_method(value):
	print("tween_method", value)


func completed_animation():
	print("completed animation")
	emit_signal("finished_animation")


# Called when the node enters the scene tree for the first time.
func start_zoom_anim_out():
	var tween = create_tween()
	var camera = get_node(node)
	tween.connect("finished",self, "completed_animation")
	#tween.connect("tween_completed", self, "completed")
	tween.set_ease(Tween.EASE_IN_OUT)
	tween.set_trans(Tween.TRANS_QUAD)	
	#tween.tween_property(self,"a",100,100)
	tween.tween_method(camera,"tween_method",1.0,7.0,2)
	#tween.set_speed_scale(1.1)

func start_zoom_anim_in():
	var tween = create_tween()
	var camera = get_node(node)
	tween.connect("finished",self, "completed_animation")
	tween.set_ease(Tween.EASE_IN_OUT)
	tween.set_trans(Tween.TRANS_QUAD)	
	#tween.tween_property(self,"a",100,100)
	tween.tween_method(camera,"tween_method",7.0,1.0,2)
	#tween.set_speed_scale(1.1)


