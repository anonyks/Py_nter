# Circle tool - drag to set center & radius. Uses midpoint circle algorithm.

import math
import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class CircleTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.initial_pos = (0, 0)
        self.final_pos = (0, 0)
        self.radius = 0

    # Midpoint circle algorithm
    # plots each point as a small square so bigger width = thicker stroke
    def plot_8(self, surface, cx, cy, x, y, color, w=1):
        for px, py in [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x),
        ]:
            if w <= 1:
                surface.set_at((px, py), color)
            else:
                pygame.draw.rect(surface, color, (px - w // 2, py - w // 2, w, w))

    def draw_midpoint_circle(self, surface, cx, cy, r, color, width=1):
        if r <= 0:
            return
        x, y = 0, r
        d = 1 - r
        self.plot_8(surface, cx, cy, x, y, color, width)
        while x < y:
            x += 1
            if d < 0:
                d += 2 * x + 1
            else:
                y -= 1
                d += 2 * (x - y) + 1
            self.plot_8(surface, cx, cy, x, y, color, width)

    def draw(self, surface):
        pass

    def handle_events(self, event):
        if event is None:
            return
        mx, my = g.mouse_pos

        if event.type == pygame.MOUSEWHEEL:
            g.line_width += event.y
            g.line_width = max(1, min(20, g.line_width))
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Ignore clicks outside canvas
            if my < g.TOOLBAR_HEIGHT or mx < g.SIDE_PANEL_WIDTH:
                return
            g.push_undo_snapshot()
            self.is_dragging = True
            self.initial_pos = (mx, my)
            self.final_pos = (mx, my)
            self.radius = 0
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.final_pos = (mx, my)
            dx = self.final_pos[0] - self.initial_pos[0]
            dy = self.final_pos[1] - self.initial_pos[1]
            self.radius = math.hypot(dx, dy)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_dragging:
            self.final_pos = (mx, my)
            dx = self.final_pos[0] - self.initial_pos[0]
            dy = self.final_pos[1] - self.initial_pos[1]
            self.radius = math.hypot(dx, dy)
            if g.canvas_surface is not None:
                self.draw_midpoint_circle(
                    g.canvas_surface,
                    self.initial_pos[0], self.initial_pos[1],
                    int(self.radius), g.COLORS[g.color_selected], g.line_width
                )
                # or just use pygame's built-in:
                # pygame.draw.circle(g.canvas_surface, g.COLORS[g.color_selected],
                #     self.initial_pos, int(self.radius), g.line_width)
            self.is_dragging = False

    def preview(self, screen):
        if self.is_dragging and self.radius > 0:
            self.draw_midpoint_circle(
                screen,
                self.initial_pos[0], self.initial_pos[1],
                int(self.radius), g.COLORS[g.color_selected], g.line_width
            )

