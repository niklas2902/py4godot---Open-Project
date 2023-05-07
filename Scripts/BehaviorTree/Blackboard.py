from __future__ import annotations  # Without this, the type hint below would not work.


class Blackboard:
    enemy: object
    def __init__(self, enemy:object):
        self.enemy = enemy
