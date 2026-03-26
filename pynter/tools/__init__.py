# import all tools so other files can just do: from pynter.tools import PencilTool etc

from pynter.tools.tool import Tool
from pynter.tools.pencil_tool import PencilTool
from pynter.tools.brush_tool import BrushTool
from pynter.tools.eraser_tool import EraserTool
from pynter.tools.line_tool import LineTool
from pynter.tools.curve_tool import CurveTool
from pynter.tools.rectangle_tool import RectangleTool
from pynter.tools.square_tool import SquareTool
from pynter.tools.circle_tool import CircleTool
from pynter.tools.ellipse_tool import EllipseTool
from pynter.tools.select_box_tool import SelectBoxTool
from pynter.tools.hypnotiser_tool import HypnotiserTool
from pynter.tools.spiral_tool import SpiralTool
from pynter.tools.mandala_tool import MandalaTool
from pynter.tools.triangle_tool import TriangleTool
from pynter.tools.fill_tool import FillTool
from pynter.tools.eyedropper_tool import EyeDropperTool
from pynter.tools.text_tool import TextTool
from pynter.tools.magnifier_tool import MagnifierTool
from pynter.tools.pentagon_tool import PentagonTool

# __all__ tells python which names to export when someone does "from pynter.tools import *"
__all__ = [
    "Tool",
    "PencilTool",
    "BrushTool",
    "EraserTool",
    "LineTool",
    "CurveTool",
    "RectangleTool",
    "SquareTool",
    "CircleTool",
    "EllipseTool",
    "SelectBoxTool",
    "HypnotiserTool",
    "SpiralTool",
    "MandalaTool",
    "TriangleTool",
    "FillTool",
    "EyeDropperTool",
    "TextTool",
    "MagnifierTool",
    "PentagonTool",
]
