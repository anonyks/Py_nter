# Magnifier tool - shows a zoomed-in view around the cursor.

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class MagnifierTool(Tool):
    # Hover over the canvas to see a zoomed-in view around the cursor.
    # Scroll wheel adjusts zoom level. Doesn't change the canvas.

    def __init__(self):
        self.zoom = 4          # magnification factor (2x-10x)
        self.src_size = 30     # fixed number of canvas pixels to capture

    def draw(self, surface):
        pass  # read-only

    def handle_events(self, event):
        if event is None:
            return
        if event.type == pygame.MOUSEWHEEL:
            self.zoom += event.y
            self.zoom = max(2, min(10, self.zoom))

    def preview(self, screen):
        if g.canvas_surface is None:
            return
        mx, my = g.mouse_pos
        cw, ch = g.canvas_surface.get_size()

        # Always capture src_size x src_size canvas pixels centred on cursor
        half = self.src_size // 2
        src_x = max(0, min(mx - half, cw - self.src_size))
        src_y = max(0, min(my - half, ch - self.src_size))
        src_w = min(self.src_size, cw - src_x)
        src_h = min(self.src_size, ch - src_y)
        if src_w <= 0 or src_h <= 0:
            return

        src_rect = pygame.Rect(src_x, src_y, src_w, src_h)
        # subsurface grabs a rectangular chunk of the canvas without copying the whole thing
        snippet = g.canvas_surface.subsurface(src_rect).copy()

        # Scale up -- box size = src_size * zoom (grows with zoom)
        out_w = src_w * self.zoom
        out_h = src_h * self.zoom
        zoomed = pygame.transform.scale(snippet, (out_w, out_h))

        # Draw zoomed view offset from cursor
        dest_x = mx + 20
        dest_y = my + 20
        # Keep on screen
        sw, sh = screen.get_size()
        if dest_x + zoomed.get_width() > sw:
            dest_x = mx - 20 - zoomed.get_width()
        if dest_y + zoomed.get_height() > sh:
            dest_y = my - 20 - zoomed.get_height()

        screen.blit(zoomed, (dest_x, dest_y))
        pygame.draw.rect(
            screen, (0, 0, 0),
            (dest_x, dest_y, zoomed.get_width(), zoomed.get_height()), 2,
        )

        # Zoom info
        font = pygame.font.SysFont(None, 16)
        zt = font.render(f"{self.zoom}x", True, (0, 0, 0))
        screen.blit(zt, (dest_x + 4, dest_y + 4))
