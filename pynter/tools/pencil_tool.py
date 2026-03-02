# Pencil tool - draws small filled circles while the mouse is held down.

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class PencilTool(Tool):
    RADIUS = 5

    def __init__(self):
        self.stroke_started = False
        self.last_pos = None

    def draw(self, surface):
        if pygame.mouse.get_pressed()[0]:  # left button
            mx, my = g.mouse_pos
            if my > g.TOOLBAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                if not self.stroke_started:
                    g.push_undo_snapshot()
                    self.stroke_started = True
                    self.last_pos = (mx, my)
                    pygame.draw.circle(
                        surface, g.COLORS[g.color_selected], (mx, my), self.RADIUS
                    )
                else:
                    # Smooth line to current pos
                    if self.last_pos:
                        self.draw_line(surface, self.last_pos, (mx, my))
                    self.last_pos = (mx, my)
        else:
            self.stroke_started = False
            self.last_pos = None

    def draw_line(self, surface, start, end):
        # Draw a smooth line between two points using circles.
        x1, y1 = start
        x2, y2 = end
        
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if distance < 1:
            return
            
        # Stamp circles along path
        steps = max(1, int(distance / (self.RADIUS * 0.5)))
        for i in range(steps + 1):
            if steps > 0:
                t = i / steps
            else:
                t = 0
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            pygame.draw.circle(
                surface, g.COLORS[g.color_selected], (x, y), self.RADIUS
            )

    def handle_events(self, event):
        pass

    def preview(self, screen):
        mx, my = g.mouse_pos
        if pygame.mouse.get_pressed()[2]:  # right button -> outline
            pygame.draw.circle(screen, (130, 130, 130), (mx, my), self.RADIUS, 1)
        else:
            pygame.draw.circle(
                screen, g.COLORS[g.color_selected], (mx, my), self.RADIUS
            )
