extends Button


var logic
# Called when the node enters the scene tree for the first time.
func _ready():
	logic = get_node(NodePath("HidePlayerLogic"))
	
func _pressed():
	print("pressed")
	logic.call("_pressed")
