# Bezier curve tool - add control points by clicking, press Enter to commit.

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


# Math helpers for bezier curve calculation
def factorial(n):
    if n <= 0:
        return 1
    product = 1
    for i in range(1, n + 1):
        product *= i
    return product


def n_cr(n, r):
    # Calculate how many ways to choose r items from n (combination formula).
    return factorial(n) // (factorial(r) * factorial(n - r))


class CurveTool(Tool):
    def __init__(self):
        self.control_points = []
        self.curve_points = []
        self.is_enter_pressed = False
        self.is_changing_control_point = False
        self.changing_point_index = -1

    # Bezier helpers
    @staticmethod
    def bezier_point(
        control_points, t
    ):
        n = len(control_points)
        x, y = 0.0, 0.0
        for i in range(n):
            bin_coeff = n_cr(n - 1, i)
            term = bin_coeff * ((1 - t) ** (n - 1 - i)) * (t ** i)
            x += term * control_points[i][0]
            y += term * control_points[i][1]
        return (x, y)

    def compute_bezier_curve(self):
        pts = []
        t = 0.0
        while t <= 1.0:
            pts.append(self.bezier_point(self.control_points, t))
            t += 0.0005
        return pts


    def draw(self, surface):
        if self.is_enter_pressed:
            g.push_undo_snapshot()
            color = g.COLORS[g.color_selected]
            if len(self.curve_points) > 1:
                int_points = []
                for pt in self.curve_points:
                    int_points.append((int(pt[0]), int(pt[1])))
                # Filter out invalid points
                valid_points = []
                for x, y in int_points:
                    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                        valid_points.append((x, y))
                if len(valid_points) > 1:
                    pygame.draw.lines(surface, color, False, valid_points, g.line_width)
                    # Round off the endpoints so they don't look jagged
                    if g.line_width > 1:
                        r = g.line_width // 2
                        pygame.draw.circle(surface, color, valid_points[0], r)
                        pygame.draw.circle(surface, color, valid_points[-1], r)
            self.control_points.clear()
            self.curve_points.clear()
            self.is_enter_pressed = False

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
            if mx < g.SIDE_PANEL_WIDTH or my < g.TOOLBAR_HEIGHT:
                return
            # Check if clicking an existing control point
            for i, pt in enumerate(self.control_points):
                r = pygame.Rect(pt[0] - 4, pt[1] - 4, 8, 8)
                if r.collidepoint(mx, my):
                    self.is_changing_control_point = True
                    self.changing_point_index = i
                    break

            if not self.is_changing_control_point:
                self.control_points.append((mx, my))
                self.curve_points = self.compute_bezier_curve()

        elif event.type == pygame.MOUSEMOTION:
            if self.is_changing_control_point and pygame.mouse.get_pressed()[0]:
                self.control_points[self.changing_point_index] = (mx, my)
                self.curve_points = self.compute_bezier_curve()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_changing_control_point = False
            self.changing_point_index = -1

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.is_enter_pressed = True

    def preview(self, screen):
        if self.is_enter_pressed:
            return
        color = g.COLORS[g.color_selected]
        # Draw control points as red circles
        for pt in self.control_points:
            pygame.draw.circle(screen, (230, 41, 55), (int(pt[0]), int(pt[1])), 8)
        # Draw curve preview with proper line width
        if len(self.curve_points) > 1:
            int_points = []
            for pt in self.curve_points:
                int_points.append((int(pt[0]), int(pt[1])))
            valid_points = []
            for x, y in int_points:
                if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
                    valid_points.append((x, y))
            if len(valid_points) > 1:
                pygame.draw.lines(screen, color, False, valid_points, g.line_width)
                # Round off the endpoints so they don't look jagged
                if g.line_width > 1:
                    r = g.line_width // 2
                    pygame.draw.circle(screen, color, valid_points[0], r)
                    pygame.draw.circle(screen, color, valid_points[-1], r)
