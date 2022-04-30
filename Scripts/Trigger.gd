extends Area


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

export var playerPath = NodePath()
var player
# Called when the node enters the scene tree for the first time.
func _ready():
	player = get_node(playerPath)


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


func _on_Area_area_entered(area):
	print("area:", area)
	player.entered_ramp()


func _on_Area_body_entered(body):
	print("body_entered:", body)
	player.entered_ramp()
	pass # Replace with function body.


func _on_Area_body_exited(body):
	player.exited_ramp()
	pass # Replace with function body.
