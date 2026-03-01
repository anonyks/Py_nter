"""Square tool - drag to draw a square where all sides are equal."""

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class SquareTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)

    def get_square(self):
        # Make height equal to width so it's always a perfect square
        # The square grows from start_pos in the direction you drag
        sx, sy = self.start_pos
        ex, ey = self.end_pos
        dx = ex - sx
        dy = ey - sy
        # Use the larger distance as the side length
        side = max(abs(dx), abs(dy))
        # Figure out which direction to grow
        if dx >= 0:
            x = sx
        else:
            x = sx - side
        if dy >= 0:
            y = sy
        else:
            y = sy - side
        return pygame.Rect(x, y, side, side)

    def draw(self, surface):
        pass

    def handle_events(self, event):
        if event is None:
            return
        if event.type == pygame.MOUSEWHEEL:
            g.line_width += event.y
            g.line_width = max(1, min(20, g.line_width))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = g.mouse_pos
            # Ignore clicks outside canvas
            if my < g.TOOLBAR_HEIGHT or mx < g.SIDE_PANEL_WIDTH:
                return
            g.push_undo_snapshot()
            self.is_dragging = True
            self.start_pos = g.mouse_pos
            self.end_pos = g.mouse_pos
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.end_pos = g.mouse_pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_dragging:
            self.end_pos = g.mouse_pos
            if g.canvas_surface is not None:
                sq = self.get_square()
                if sq.width > 0 and sq.height > 0:
                    pygame.draw.rect(
                        g.canvas_surface, g.COLORS[g.color_selected], sq, g.line_width
                    )
            self.is_dragging = False

    def preview(self, screen):
        if self.is_dragging:
            sq = self.get_square()
            if sq.width > 0 and sq.height > 0:
                pygame.draw.rect(screen, g.COLORS[g.color_selected], sq, g.line_width)

