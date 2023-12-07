from __future__ import annotations  # Without this, the type hint below would not work.

import Scripts.Enemy as enemy
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from Scripts.Utils.BehaviorTreeVisualizerLogic import *


class Blackboard:
    enemy: enemy.Enemy

    def __init__(self, enemy: enemy.Enemy) -> None:
        self.enemy = enemy
