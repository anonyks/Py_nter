# Fill (flood-fill / paint bucket) tool.

import pygame
from collections import deque
from pynter.tools.tool import Tool
from pynter import globals as g


class FillTool(Tool):
    # Click anywhere on the canvas to fill the clicked area
    # with the selected colour. Only fills pixels that match
    # the exact colour you clicked on.

    def draw(self, surface):
        pass  # instant commit

    def handle_events(self, event):
        if event is None:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = g.mouse_pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOOLBAR_HEIGHT:
                if g.canvas_surface is not None:
                    g.push_undo_snapshot()
                    self.flood_fill(g.canvas_surface, mx, my)

    def preview(self, screen):
        # Show a small bucket-cursor indicator
        mx, my = g.mouse_pos
        pygame.draw.rect(
            screen, g.COLORS[g.color_selected],
            (mx - 4, my - 4, 8, 8),
        )
        pygame.draw.rect(screen, (0, 0, 0), (mx - 4, my - 4, 8, 8), 1)

    @staticmethod
    def flood_fill(surface, x, y):
        # Fill the area starting from pixel (x, y) outward.
        w, h = surface.get_size()
        if x < 0 or x >= w or y < 0 or y >= h:
            return

        target_color = surface.get_at((x, y))
        fill_color = g.COLORS[g.color_selected]

        if target_color == fill_color:
            return

        # Lock surface for fast pixel access
        surface.lock()
        visited = set()
        queue = deque()
        queue.append((x, y))
        visited.add((x, y))

        while queue:
            cx, cy = queue.popleft()
            surface.set_at((cx, cy), fill_color)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    if surface.get_at((nx, ny)) == target_color:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        surface.unlock()
