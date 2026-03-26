import pygame
import math
from pynter.tools.tool import Tool
from pynter import globals as g

class PentagonTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)

    def get_pentagon_points(self):
        sx, sy = self.start_pos
        ex, ey = self.end_pos
        x = min(sx, ex)
        y = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)
        cx = x + w / 2
        cy = y + h / 2
        rx = w / 2
        ry = h / 2
        # separate rx/ry to be flexible (stretches to fit the drag rectangle)
        # start at top (-90°), go clockwise
        points = []
        for i in range(5):
            angle = math.radians(-90 + i * 72)
            px = cx + rx * math.cos(angle)
            py = cy + ry * math.sin(angle)
            points.append((px, py))
        return points

    def draw(self, surface):
        pass  # committed on mouse release

    def handle_events(self, event):
        if event is None:
            return
        if event.type == pygame.MOUSEWHEEL:
            g.line_width += event.y
            g.line_width = max(1, min(20, g.line_width))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = g.mouse_pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOOLBAR_HEIGHT:
                g.push_undo_snapshot()
                self.is_dragging = True
                self.start_pos = g.mouse_pos
                self.end_pos = g.mouse_pos
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.end_pos = g.mouse_pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.end_pos = g.mouse_pos
                pts = self.get_pentagon_points()
                if g.canvas_surface is not None and len(pts) == 5:
                    pygame.draw.polygon(
                        g.canvas_surface, g.COLORS[g.color_selected],
                        pts, g.line_width,
                    )
                self.is_dragging = False

    def preview(self, screen):
        if self.is_dragging:
            pts = self.get_pentagon_points()
            if len(pts) == 5:
                pygame.draw.polygon(
                    screen, g.COLORS[g.color_selected], pts, g.line_width,
                )