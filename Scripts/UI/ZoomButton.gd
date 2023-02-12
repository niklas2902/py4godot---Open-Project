extends Button


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var logic
# Called when the node enters the scene tree for the first time.
func _ready():
	logic = get_node(NodePath("Logic"))
	
func _pressed():
	print("pressed")
	logic.call("_pressed")


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
