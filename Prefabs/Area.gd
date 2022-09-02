extends Area

var node_path = NodePath("Logic")
onready	var logic = get_node(node_path)

func _on_Area_body_entered(body):
	print("-----------------------Area_body_entered")
	print(body)
	logic.body_entered(body)

func _on_Area_body_exited(body):
	logic.body_exited(body)


func _on_Area_tree_entered():
	print("tree entered")
