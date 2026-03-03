# Shared variables that all parts of the program use.

import pygame

# Constants
MAX_COLORS_COUNT = 23
TOOL_BOX_ICONS_COUNT = 18

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

TOOLBAR_HEIGHT = 50       # top color bar height
SIDE_PANEL_WIDTH = 140    # left tool panel width

# Color palette
COLORS = [
    pygame.Color(245, 245, 245),  # RAYWHITE
    pygame.Color(253, 249, 0),    # YELLOW
    pygame.Color(255, 203, 0),    # GOLD
    pygame.Color(255, 161, 0),    # ORANGE
    pygame.Color(255, 109, 194),  # PINK
    pygame.Color(230, 41, 55),    # RED
    pygame.Color(190, 33, 55),    # MAROON
    pygame.Color(0, 228, 48),     # GREEN
    pygame.Color(0, 158, 47),     # LIME
    pygame.Color(0, 117, 44),     # DARKGREEN
    pygame.Color(102, 191, 255),  # SKYBLUE
    pygame.Color(0, 121, 241),    # BLUE
    pygame.Color(0, 82, 172),     # DARKBLUE
    pygame.Color(200, 122, 255),  # PURPLE
    pygame.Color(135, 60, 190),   # VIOLET
    pygame.Color(112, 31, 126),   # DARKPURPLE
    pygame.Color(211, 176, 131),  # BEIGE
    pygame.Color(127, 106, 79),   # BROWN
    pygame.Color(76, 63, 47),     # DARKBROWN
    pygame.Color(200, 200, 200),  # LIGHTGRAY
    pygame.Color(130, 130, 130),  # GRAY
    pygame.Color(80, 80, 80),     # DARKGRAY
    pygame.Color(0, 0, 0),        # BLACK
]

# Mutable global state
color_selected = 0
mouse_pos = (0, 0)
line_width = 2          # shared stroke width for shape tools (scroll to change)

# The canvas surface (created at runtime by Canvas.init)
canvas_surface = None

# Undo / Redo history
MAX_UNDO = 50
undo_stack = []
redo_stack = []


def push_undo_snapshot():
    # Save a copy of the canvas so we can undo later.
    if canvas_surface is None:
        return
    undo_stack.append(canvas_surface.copy())
    if len(undo_stack) > MAX_UNDO:
        undo_stack.pop(0)
    redo_stack.clear()


def undo():
    # Restore previous canvas state.
    global canvas_surface
    if not undo_stack or canvas_surface is None:
        return
    redo_stack.append(canvas_surface.copy())
    canvas_surface.blit(undo_stack.pop(), (0, 0))


def redo():
    # Re-apply undone canvas state.
    global canvas_surface
    if not redo_stack or canvas_surface is None:
        return
    undo_stack.append(canvas_surface.copy())
    canvas_surface.blit(redo_stack.pop(), (0, 0))

