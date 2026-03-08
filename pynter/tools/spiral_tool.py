# spiral tool - draws evenly spaced spirals outward from center

import math
import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class SpiralTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        self.spacing = 8.0        # distance between spiral arms
        self.line_width = 1         # spiral line thickness

    def draw(self, surface):
        pass

    def draw_spiral(self, surface):
        cx, cy = self.start_pos
        dx = self.end_pos[0] - cx
        dy = self.end_pos[1] - cy
        max_radius = math.hypot(dx, dy)
        
        if max_radius < 5:
            return
            
        color = g.COLORS[g.color_selected]
        points = []
        
        # archimedes spiral: radius grows linearly with angle
        # a controls how far apart the arms are
        a = self.spacing / (2 * math.pi)
        # 0.1 radians per step (~6 degrees) - smaller = smoother but more points to draw
        angle_step = 0.1
        
        angle = 0
        while True:
            r = a * angle
            if r > max_radius:
                break
                
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            
            # Add all points - let pygame handle clipping
            points.append((int(x), int(y)))
                
            angle += angle_step
        
        # Draw spiral with specified width - pygame will clip automatically
        if len(points) > 1:
            pygame.draw.lines(surface, color, False, points, self.line_width)

    def handle_events(self, event):
        if event is None:
            return
        mx, my = g.mouse_pos

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Ignore clicks outside canvas
            if my < g.TOOLBAR_HEIGHT or mx < g.SIDE_PANEL_WIDTH:
                return
            g.push_undo_snapshot()
            self.is_dragging = True
            self.start_pos = (mx, my)
            self.end_pos = (mx, my)
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.end_pos = (mx, my)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.draw_spiral(g.canvas_surface)
            self.is_dragging = False
        elif event.type == pygame.MOUSEWHEEL:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                # Shift+scroll adjusts line width
                self.line_width += event.y
                self.line_width = max(1, min(20, self.line_width))
            else:
                # Regular scroll adjusts spacing
                self.spacing += event.y * 1.0
                self.spacing = max(3.0, min(20.0, self.spacing))

    def preview(self, screen):
        if self.is_dragging:
            self.draw_spiral(screen)
        else:
            # Show small preview spiral at cursor
            mx, my = g.mouse_pos
            if mx >= g.SIDE_PANEL_WIDTH and my >= g.TOOLBAR_HEIGHT:
                color = g.COLORS[g.color_selected]
                # Mini spiral preview (fixed size to show spacing)
                a = self.spacing / (2 * math.pi)
                angle = 0
                points = []
                while angle <= 4 * math.pi:  # 2 full turns
                    r = a * angle
                    if r > 25:  # limit preview size
                        break
                    x = mx + r * math.cos(angle)
                    y = my + r * math.sin(angle)
                    points.append((int(x), int(y)))
                    angle += 0.2
                if len(points) > 1:
                    pygame.draw.lines(screen, color, False, points, self.line_width)