# Brush tool - circle or spray brush. Tab to switch type, scroll to resize,
# Shift+scroll to change spray density.

import random
import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


# Two brush types
BRUSH_CIRCLE = 0
BRUSH_SPRAY = 1

_TYPE_NAMES = ["Circle", "Spray"]


class BrushTool(Tool):
    def __init__(self):
        self.brush_size = 20.0
        self.brush_type = BRUSH_CIRCLE
        self.spray_density = 30      # how many dots per stamp (10-80)
        self.tip_cache = {}
        self.stroke_started = False
        self.last_pos = None

    # Circle tip - cached since it doesn't change
    def get_circle_tip(self, color):
        key = (int(self.brush_size), (color.r, color.g, color.b))
        if key in self.tip_cache:
            return self.tip_cache[key]

        sz = int(self.brush_size) * 2
        tip = pygame.Surface((sz, sz), pygame.SRCALPHA)
        half = sz // 2
        pygame.draw.circle(tip, color, (half, half), int(self.brush_size))

        self.tip_cache[key] = tip
        return tip

    # Spray tip - random dots each time, never cached
    def make_spray(self, color):
        sz = int(self.brush_size) * 2
        tip = pygame.Surface((sz, sz), pygame.SRCALPHA)
        half = sz // 2
        r = int(self.brush_size)

        # Scale dot count with both radius and density setting
        dot_count = max(5, int(self.spray_density * (r / 10.0)))
        for _ in range(dot_count):
            dx = random.randint(-r, r)
            dy = random.randint(-r, r)
            if dx * dx + dy * dy <= r * r:
                tip.set_at((half + dx, half + dy), color)
        return tip

    def stamp(self, surface, mx, my, color):
        if self.brush_type == BRUSH_SPRAY:
            tip = self.make_spray(color)
        else:
            tip = self.get_circle_tip(color)
        surface.blit(tip, (mx - tip.get_width() // 2,
                           my - tip.get_height() // 2))

    def draw_smooth_line(self, surface, start, end, color):
        # Draw a smooth line between two points using brush stamps.
        x1, y1 = start
        x2, y2 = end

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if distance < 1:
            return

        # Stamp along path
        spacing = max(1, self.brush_size * 0.25)
        steps = max(1, int(distance / spacing))
        for i in range(1, steps + 1):
            t = i / steps
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            self.stamp(surface, x, y, color)

    # Tool interface
    def draw(self, surface):
        if pygame.mouse.get_pressed()[0]:
            mx, my = g.mouse_pos
            if my > g.TOOLBAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                color = g.COLORS[g.color_selected]
                if not self.stroke_started:
                    g.push_undo_snapshot()
                    self.stroke_started = True
                    self.last_pos = (mx, my)
                    self.stamp(surface, mx, my, color)
                else:
                    if self.last_pos:
                        self.draw_smooth_line(surface, self.last_pos, (mx, my), color)
                    self.last_pos = (mx, my)
        else:
            self.stroke_started = False
            self.last_pos = None

    def handle_events(self, event):
        if event is None:
            return
        if event.type == pygame.MOUSEWHEEL:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                # Shift+scroll changes spray density
                self.spray_density += event.y * 5
                self.spray_density = max(10, min(80, self.spray_density))
            else:
                # Regular scroll changes brush size
                self.brush_size += event.y * 5
                self.brush_size = max(2, min(50, self.brush_size))
                self.tip_cache.clear()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            # Toggle between circle and spray
            if self.brush_type == BRUSH_CIRCLE:
                self.brush_type = BRUSH_SPRAY
            else:
                self.brush_type = BRUSH_CIRCLE
            self.tip_cache.clear()

    def preview(self, screen):
        mx, my = g.mouse_pos
        if pygame.mouse.get_pressed()[2]:  # right-click -> outline only
            sz = int(self.brush_size) * 2
            pygame.draw.rect(screen, (130, 130, 130),
                             (mx - sz // 2, my - sz // 2, sz, sz), 1)
        else:
            self.stamp(screen, mx, my, g.COLORS[g.color_selected])

    def get_shape_name(self):
        return _TYPE_NAMES[self.brush_type]
