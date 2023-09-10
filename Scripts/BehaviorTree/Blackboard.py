from __future__ import annotations  # Without this, the type hint below would not work.

import Scripts.Enemy as enemy
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
	from Scripts.Utils.BehaviorTreeVisualizerLogic import *


class Blackboard:
	enemy: enemy.Enemy
	tree_visualizer: BehaviorTreeVisualizerLogic

	def __init__(self, enemy: enemy.Enemy, tree_visualizer: BehaviorTreeVisualizerLogic) -> None:
		self.enemy = enemy
		self.tree_visualizer = tree_visualizer
