
from py4godot.enums.enums import *
from py4godot.core import *
from py4godot.classes.generated import *
from py4godot.pluginscript_api.utils.annotations import *
from py4godot.pluginscript_api.hints import *

@gdclass
class Lever(StaticBody):

    def __init__(self):
        #Don't call any godot-methods here
        super().__init__()
        self._activated = True

    prop("activated",bool, False)

