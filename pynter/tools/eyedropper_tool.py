# Eye-dropper tool - click to pick a colour from the canvas.

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class EyeDropperTool(Tool):
    # Click on the canvas to pick the colour under the cursor.

    def __init__(self):
        self.sampled_color = None

    def draw(self, surface):
        pass  # read-only

    def handle_events(self, event):
        if event is None:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = g.mouse_pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOOLBAR_HEIGHT:
                if g.canvas_surface is not None:
                    self.sampled_color = g.canvas_surface.get_at((mx, my))
                    self.match_palette(self.sampled_color)

    def preview(self, screen):
        mx, my = g.mouse_pos
        # Cross-hair cursor
        pygame.draw.line(screen, (0, 0, 0), (mx - 8, my), (mx + 8, my), 1)
        pygame.draw.line(screen, (0, 0, 0), (mx, my - 8), (mx, my + 8), 1)
        # Color preview swatch
        if g.canvas_surface is not None:
            w, h = g.canvas_surface.get_size()
            if 0 <= mx < w and 0 <= my < h:
                col = g.canvas_surface.get_at((mx, my))
                pygame.draw.rect(screen, col, (mx + 12, my - 12, 20, 20))
                pygame.draw.rect(screen, (0, 0, 0), (mx + 12, my - 12, 20, 20), 1)

    @staticmethod
    def match_palette(color):
        # Find the closest palette colour and select it.
        best_idx = 0
        # Start with the biggest possible distance, so any real match beats it
        best_dist = float("inf")
        for i, pc in enumerate(g.COLORS):
            dr = color.r - pc.r
            dg = color.g - pc.g
            db = color.b - pc.b
            dist = dr * dr + dg * dg + db * db
            if dist < best_dist:
                best_dist = dist
                best_idx = i
            if dist == 0:
                break
        g.color_selected = best_idx
