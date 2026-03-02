# Line tool - drawn on mouse release. Uses pygame.draw.line for adjustable width.

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class LineTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)

    # Bresenham line algorithm - draws a pixel-perfect line between two points
    def draw_bresenham_line(self, surface, color):
        sx, sy = self.start_pos
        ex, ey = self.end_pos

        # Make sure we always draw left to right
        if sx > ex:
            sx, sy, ex, ey = ex, ey, sx, sy

        dx = ex - sx
        dy = ey - sy

        xk, yk = sx, sy
        surface.set_at((xk, yk), color)

        if 0 < dy <= dx:
            # Case 1: 0 <= slope <= 1
            adx, ady = abs(dx), abs(dy)
            p = 2 * ady - adx
            for _ in range(sx, ex):
                if p < 0:
                    p += 2 * ady
                else:
                    p += 2 * ady - 2 * adx
                    yk += 1
                xk += 1
                surface.set_at((xk, yk), color)

        elif dy > dx > 0 or (dy > 0 and dx == 0):
            # Case 2: slope > 1
            adx, ady = abs(dx), abs(dy)
            p = 2 * adx - ady
            for _ in range(sy, ey):
                if p < 0:
                    p += 2 * adx
                else:
                    p += 2 * adx - 2 * ady
                    xk += 1
                yk += 1
                surface.set_at((xk, yk), color)

        elif dy >= -dx and dy <= 0:
            # Case 3: -1 <= slope < 0
            adx, ady = abs(dx), abs(dy)
            p = 2 * ady - adx
            for _ in range(sx, ex):
                if p < 0:
                    p += 2 * ady
                else:
                    p += 2 * ady - 2 * adx
                    yk -= 1
                xk += 1
                surface.set_at((xk, yk), color)

        elif dy < -dx:
            # Case 4: slope < -1
            adx, ady = abs(dx), abs(dy)
            p = 2 * adx - ady
            k = sy
            while k > ey:
                if p < 0:
                    p += 2 * adx
                else:
                    p += 2 * adx - 2 * ady
                    xk += 1
                yk -= 1
                surface.set_at((xk, yk), color)
                k -= 1


    def draw(self, surface):
        # Commit line on mouse release (handled via events)
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
                if g.line_width <= 1:
                    self.draw_bresenham_line(
                        g.canvas_surface, g.COLORS[g.color_selected]
                    )
                else:
                    pygame.draw.line(
                        g.canvas_surface, g.COLORS[g.color_selected],
                        self.start_pos, self.end_pos, g.line_width
                    )
            self.is_dragging = False

    def preview(self, screen):
        if self.is_dragging:
            if g.line_width == 1:
                self.draw_bresenham_line(screen, g.COLORS[g.color_selected])
            else:
                pygame.draw.line(
                    screen, g.COLORS[g.color_selected],
                    self.start_pos, self.end_pos, g.line_width
                )

