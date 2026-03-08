# line tool - drawn on mouse release. uses pygame.draw.line for adjustable width

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class LineTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)

    # bresenham line algorithm - draws a straight line one pixel at a time
    # uses a decision variable p to decide when to step diagonally
    def draw_bresenham_line(self, surface, color):
        sx, sy = self.start_pos
        ex, ey = self.end_pos

        # make sure we always draw left to right
        # tuple swap trick: swaps start and end in one line
        if sx > ex:
            sx, sy, ex, ey = ex, ey, sx, sy

        dx = ex - sx
        dy = ey - sy

        xk, yk = sx, sy
        surface.set_at((xk, yk), color)

        if 0 < dy <= dx:
            # gentle slope going up-right
            adx, ady = abs(dx), abs(dy)
            # bresenham decision variable: decides if next pixel steps diagonally
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
            # steep slope going up-right (or straight up)
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
            # gentle slope going down-right
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
            # steep slope going down-right
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
        pass  # committed on mouse release

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

