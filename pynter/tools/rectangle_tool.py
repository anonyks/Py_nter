# Rectangle tool - drag to draw a rectangle outline.

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class RectangleTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)

    def get_rect(self):
        # Build a rect from the drag start and end positions
        sx, sy = self.start_pos
        ex, ey = self.end_pos
        x = min(sx, ex)
        y = min(sy, ey)
        w = abs(sx - ex)
        h = abs(sy - ey)
        return pygame.Rect(x, y, w, h)

    def draw(self, surface):
        pass  # drawing happens on mouse release

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
                rect = self.get_rect()
                if rect.width > 0 and rect.height > 0:
                    pygame.draw.rect(
                        g.canvas_surface, g.COLORS[g.color_selected], rect, g.line_width
                    )
            self.is_dragging = False

    def preview(self, screen):
        if self.is_dragging:
            rect = self.get_rect()
            if rect.width > 0 and rect.height > 0:
                pygame.draw.rect(
                    screen, g.COLORS[g.color_selected], rect, g.line_width
                )

