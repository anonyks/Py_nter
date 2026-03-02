# Eraser tool - draws white rectangles, size adjustable via scroll wheel.

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g

WHITE = pygame.Color(245, 245, 245)  # RAYWHITE equivalent


class EraserTool(Tool):
    def __init__(self):
        self.eraser_size = 20
        self.opacity = 100           # erase strength 10-100%
        self.stroke_started = False
        self.last_pos = None
        self.original_canvas = None  # snapshot before stroke for proper blending

    def draw(self, surface):
        if pygame.mouse.get_pressed()[0]:
            mx, my = g.mouse_pos
            if my > g.TOOLBAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                if not self.stroke_started:
                    g.push_undo_snapshot()
                    self.stroke_started = True
                    self.last_pos = (mx, my)
                    # Save original canvas so opacity blending doesn't compound
                    if self.opacity < 100:
                        self.original_canvas = surface.copy()
                    self.erase_at(surface, mx, my)
                else:
                    if self.last_pos:
                        self.erase_line(surface, self.last_pos, (mx, my))
                    self.last_pos = (mx, my)
        else:
            self.stroke_started = False
            self.last_pos = None
            self.original_canvas = None

    def handle_events(self, event):
        if event is not None and event.type == pygame.MOUSEWHEEL:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                # Shift+scroll changes opacity
                self.opacity += event.y * 10
                self.opacity = max(10, min(100, self.opacity))
            else:
                self.eraser_size += event.y * 5
                self.eraser_size = max(5, min(100, self.eraser_size))

    def erase_at(self, surface, x, y):
        half = self.eraser_size // 2
        if self.opacity >= 100:
            # Full erase - just fill white
            rect = pygame.Rect(x - half, y - half, self.eraser_size, self.eraser_size)
            surface.fill(WHITE, rect)
        else:
            # Blend each pixel from its ORIGINAL color toward white
            # Going over the same pixel twice in one stroke gives same result
            t = self.opacity / 100.0
            sx = max(0, x - half)
            sy = max(0, y - half)
            ex = min(surface.get_width(), x - half + self.eraser_size)
            ey = min(surface.get_height(), y - half + self.eraser_size)
            for px in range(sx, ex):
                for py in range(sy, ey):
                    orig = self.original_canvas.get_at((px, py))
                    r = int(orig.r + (245 - orig.r) * t)
                    gr = int(orig.g + (245 - orig.g) * t)
                    b = int(orig.b + (245 - orig.b) * t)
                    surface.set_at((px, py), (r, gr, b))

    def erase_line(self, surface, start, end):
        # Interpolate between two points for gap-free erasing.
        x0, y0 = start
        x1, y1 = end
        dx = x1 - x0
        dy = y1 - y0
        dist = (dx * dx + dy * dy) ** 0.5
        spacing = max(1, self.eraser_size * 0.25)
        steps = max(1, int(dist / spacing))
        for i in range(steps + 1):
            t = i / steps
            ix = int(x0 + dx * t)
            iy = int(y0 + dy * t)
            self.erase_at(surface, ix, iy)

    def preview(self, screen):
        mx, my = g.mouse_pos
        half = self.eraser_size // 2
        outline = pygame.Rect(mx - half - 2, my - half - 2,
                               self.eraser_size + 4, self.eraser_size + 4)
        inner = pygame.Rect(mx - half, my - half,
                             self.eraser_size, self.eraser_size)
        pygame.draw.rect(screen, (130, 130, 130), outline, 2)
        pygame.draw.rect(screen, (255, 255, 255), inner)
