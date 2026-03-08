# ellipse tool - drag to define bounding box. uses midpoint ellipse algorithm

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class EllipseTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.initial_pos = (0, 0)
        self.final_pos = (0, 0)

    def params(self):
        # returns (center_x, center_y, radius_x, radius_y) from the drag bounding box
        xc = (self.initial_pos[0] + self.final_pos[0]) // 2
        yc = (self.initial_pos[1] + self.final_pos[1]) // 2
        rx = abs(self.final_pos[0] - self.initial_pos[0]) // 2
        ry = abs(self.final_pos[1] - self.initial_pos[1]) // 2
        return xc, yc, rx, ry

    # midpoint ellipse algorithm
    # only computes 1/4 of the ellipse then mirrors it 4 ways
    # each point is a small square for thickness
    def plot_4(self, surface, cx, cy, x, y, color, w=1):
        for px, py in [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
        ]:
            if w <= 1:
                surface.set_at((px, py), color)
            else:
                pygame.draw.rect(surface, color, (px - w // 2, py - w // 2, w, w))

    def draw_midpoint_ellipse(self, surface, cx, cy, rx, ry, color, width=1):
        if rx <= 0 or ry <= 0:
            return
        self.draw_single_ellipse(surface, cx, cy, rx, ry, color, width)

    def draw_single_ellipse(self, surface, cx, cy, rx, ry, color, w=1):
        # first half - step along x until slope gets too steep
        x, y = 0, ry
        rx2 = rx * rx
        ry2 = ry * ry
        # initial decision value for the flatter top region
        d1 = ry2 - rx2 * ry + rx2 // 4
        self.plot_4(surface, cx, cy, x, y, color, w)

        # ry2*x < rx2*y means we're still in the flatter part
        # once slope gets steep we switch to stepping along y
        while ry2 * x < rx2 * y:
            x += 1
            if d1 < 0:
                d1 += 2 * ry2 * x + ry2
            else:
                y -= 1
                d1 += 2 * ry2 * x - 2 * rx2 * y + ry2
            self.plot_4(surface, cx, cy, x, y, color, w)

        # second half - step along y
        # initial decision value for the steeper side region
        d2 = ry2 * (x * 2 + 1) ** 2 // 4 + rx2 * (y - 1) ** 2 - rx2 * ry2
        while y >= 0:
            y -= 1
            if d2 > 0:
                d2 += rx2 - 2 * rx2 * y
            else:
                x += 1
                d2 += 2 * ry2 * x - 2 * rx2 * y + rx2
            self.plot_4(surface, cx, cy, x, y, color, w)

    def draw(self, surface):
        pass

    def handle_events(self, event):
        if event is None:
            return
        mx, my = g.mouse_pos
        if event.type == pygame.MOUSEWHEEL:
            g.line_width += event.y
            g.line_width = max(1, min(20, g.line_width))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Ignore clicks outside canvas
            if my < g.TOOLBAR_HEIGHT or mx < g.SIDE_PANEL_WIDTH:
                return
            g.push_undo_snapshot()
            self.is_dragging = True
            self.initial_pos = (mx, my)
            self.final_pos = (mx, my)
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.final_pos = (mx, my)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_dragging:
            self.final_pos = (mx, my)
            if g.canvas_surface is not None:
                xc, yc, rx, ry = self.params()
                if rx > 0 and ry > 0:
                    self.draw_midpoint_ellipse(
                        g.canvas_surface, xc, yc, rx, ry,
                        g.COLORS[g.color_selected], g.line_width
                    )
                    # or just use pygame's built-in:
                    # rect = pygame.Rect(xc - rx, yc - ry, rx * 2, ry * 2)
                    # pygame.draw.ellipse(g.canvas_surface, g.COLORS[g.color_selected],
                    #     rect, g.line_width)
            self.is_dragging = False

    def preview(self, screen):
        if self.is_dragging:
            xc, yc, rx, ry = self.params()
            if rx > 0 and ry > 0:
                self.draw_midpoint_ellipse(
                    screen, xc, yc, rx, ry,
                    g.COLORS[g.color_selected], g.line_width
                )

