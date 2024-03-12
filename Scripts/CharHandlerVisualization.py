from py4godot.classes.generated4_core import NodePath
from py4godot.pluginscript_api.utils.annotations import gdclass, gdmethod, gdtool

import typing
from Scripts.CharHandler import CharHandler
from Scripts.Tools.Draw import Draw
from py4godot.classes.Node3D.Node3D import Node3D
from py4godot.pluginscript_api.utils.experimental import gdproperty

PLAYER_HANDLE: str = "Player"


@gdtool
class CharHandlerVisualization(Node3D, Draw):
    player: CharHandler
    player_path: NodePath = gdproperty(NodePath, NodePath.new0())

    @gdmethod
    def _ready(self):
        self.immediate_geometry_init(self, PLAYER_HANDLE)
        self.player = typing.cast(CharHandler, self.get_node(self.player_path).get_pyscript())

    def _process(self, delta: float):
        self.draw_sphere(PLAYER_HANDLE, self.player.max_dist, self.player.global_position)
