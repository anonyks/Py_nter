# Mandala tool - draws with symmetry around a center point.
# Whatever you draw gets copied and rotated around the center.

import math
import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class MandalaTool(Tool):
    def __init__(self):
        self.is_drawing = False
        self.center_pos = (0, 0)
        self.current_stroke = []
        self.symmetry_count = 8  # Number of symmetry axes (3-16)
        self.brush_size = 3      # Size of brush circles (1-20)

    def draw(self, surface):
        # Drawing happens in real-time during mouse motion in handle_events
        pass

    def draw_symmetric_line(self, surface, start, end):
        # Draw a smooth symmetric line between two points.
        color = g.COLORS[g.color_selected]
        cx, cy = self.center_pos
        
        x1, y1 = start
        x2, y2 = end
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if distance < 1:
            return
            
        spacing = max(1, self.brush_size * 0.3)
        steps = max(1, int(distance / spacing))
        
        for i in range(steps + 1):
            if steps > 0:
                t = i / steps
            else:
                t = 0
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            
            # Apply symmetry - rotate each point around the center
            for sym_i in range(self.symmetry_count):
                angle = 2 * math.pi * sym_i / self.symmetry_count
                cos_a = math.cos(angle)
                sin_a = math.sin(angle)

                # Rotation formula: shift point to origin, rotate, shift back
                rel_x = x - cx
                rel_y = y - cy
                new_x = cx + rel_x * cos_a - rel_y * sin_a
                new_y = cy + rel_x * sin_a + rel_y * cos_a
                
                px, py = int(new_x), int(new_y)
                if 0 <= px < surface.get_width() and 0 <= py < surface.get_height():
                    pygame.draw.circle(surface, color, (px, py), self.brush_size // 2)

    def draw_symmetric_stroke(self, surface, stroke_points):
        # Draw a stroke with radial symmetry.
        if len(stroke_points) < 2:
            return
            
        color = g.COLORS[g.color_selected]
        cx, cy = self.center_pos
        
        # Draw lines between consecutive points for each symmetry axis  
        for i in range(len(stroke_points) - 1):
            x1, y1 = stroke_points[i]
            x2, y2 = stroke_points[i + 1]
            
            # Draw rotated segments
            for sym_i in range(self.symmetry_count):
                angle = 2 * math.pi * sym_i / self.symmetry_count
                cos_a = math.cos(angle)
                sin_a = math.sin(angle)
                
                rel_x1 = x1 - cx
                rel_y1 = y1 - cy
                new_x1 = cx + rel_x1 * cos_a - rel_y1 * sin_a
                new_y1 = cy + rel_x1 * sin_a + rel_y1 * cos_a
                
                rel_x2 = x2 - cx
                rel_y2 = y2 - cy
                new_x2 = cx + rel_x2 * cos_a - rel_y2 * sin_a
                new_y2 = cy + rel_x2 * sin_a + rel_y2 * cos_a
                
                # Stamp along path
                distance = ((new_x2 - new_x1) ** 2 + (new_y2 - new_y1) ** 2) ** 0.5
                if distance > 1:
                    spacing = max(1, self.brush_size * 0.3)
                    steps = max(1, int(distance / spacing))
                    for step in range(steps + 1):
                        if steps > 0:
                            t = step / steps
                        else:
                            t = 0
                        x = int(new_x1 + t * (new_x2 - new_x1))
                        y = int(new_y1 + t * (new_y2 - new_y1))
                        if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                            pygame.draw.circle(surface, color, (x, y), self.brush_size // 2)

    def handle_events(self, event):
        if event is None:
            return
        mx, my = g.mouse_pos

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Ignore clicks outside canvas
            if my < g.TOOLBAR_HEIGHT or mx < g.SIDE_PANEL_WIDTH:
                return
            g.push_undo_snapshot()
            self.is_drawing = True
            self.center_pos = (mx, my)
            self.current_stroke = [(mx, my)]
        elif event.type == pygame.MOUSEMOTION and self.is_drawing:
            self.current_stroke.append((mx, my))
            # Draw in real-time to canvas with smooth interpolation
            if len(self.current_stroke) >= 2:
                # Get the last two points for smooth line rendering
                start_point = self.current_stroke[-2]
                end_point = self.current_stroke[-1]
                self.draw_symmetric_line(g.canvas_surface, start_point, end_point)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_drawing and len(self.current_stroke) > 1:
                # Already drawn live
                pass
            self.is_drawing = False
            self.current_stroke = []
        elif event.type == pygame.MOUSEWHEEL:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                # Shift+scroll adjusts brush size
                self.brush_size += event.y
                self.brush_size = max(1, min(20, self.brush_size))
            else:
                # Regular scroll adjusts symmetry count
                self.symmetry_count += event.y
                self.symmetry_count = max(3, min(16, self.symmetry_count))

    def preview(self, screen):
        mx, my = g.mouse_pos
        if mx < g.SIDE_PANEL_WIDTH or my < g.TOOLBAR_HEIGHT:
            return
            
        color = g.COLORS[g.color_selected]
        
        # Show symmetry guide lines from cursor (as center)
        if not self.is_drawing:
            angle_step = 2 * math.pi / self.symmetry_count
            for i in range(self.symmetry_count):
                angle = i * angle_step
                end_x = mx + 50 * math.cos(angle)
                end_y = my + 50 * math.sin(angle)
                pygame.draw.line(screen, (100, 100, 100), (mx, my), (int(end_x), int(end_y)), 1)
        
        # Show current stroke preview with symmetry
        if self.is_drawing and len(self.current_stroke) > 1:
            self.draw_symmetric_stroke(screen, self.current_stroke)
            
        # Show cursor brush size
        pygame.draw.circle(screen, (150, 150, 150), (mx, my), self.brush_size // 2, 1)