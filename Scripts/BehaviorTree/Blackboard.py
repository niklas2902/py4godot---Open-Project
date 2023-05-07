from __future__ import annotations  # Without this, the type hint below would not work.

import Scripts.Enemy as enemy


class Blackboard:
    enemy: enemy.Enemy
    def __init__(self, enemy:enemy.Enemy):
        self.enemy = enemy
