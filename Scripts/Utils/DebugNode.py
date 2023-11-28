# import debugpy
from py4godot.classes.Node.Node import Node

from py4godot.pluginscript_api.utils.annotations import *


@gdclass
class DebugNode(Node):

    @gdmethod
    def _enter_tree(self) -> None:
        pass
