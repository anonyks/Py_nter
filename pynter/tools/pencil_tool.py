# pencil tool - draws small circles while mouse is held down

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class PencilTool(Tool):
    RADIUS = 5  # dot size in px

    def __init__(self):
        self.stroke_started = False
        self.last_pos = None

    def draw(self, surface):
        if pygame.mouse.get_pressed()[0]:  # [0] = left, [1] = middle, [2] = right
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
        # smooth line between two points using circles
        x1, y1 = start
        x2, y2 = end
        
        # ** 0.5 = square root (same as math.sqrt but shorter)
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if distance < 1:
            return
            
        # stamp circles along the path so theres no gaps
        # smaller step = more overlap = smoother line
        steps = max(1, int(distance / (self.RADIUS * 0.5)))
        for i in range(steps + 1):
            if steps > 0:
                t = i / steps  # t goes from 0.0 to 1.0 (start to end)
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
        if pygame.mouse.get_pressed()[2]:  # right click = outline only preview
            # last arg 1 = outline only (1px thick), 0 would fill the circle
            pygame.draw.circle(screen, (130, 130, 130), (mx, my), self.RADIUS, 1)
        else:
            pygame.draw.circle(
                screen, g.COLORS[g.color_selected], (mx, my), self.RADIUS
            )
