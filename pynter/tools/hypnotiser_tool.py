# Hypnotiser tool - draws expanding rings that look like a hypnotic spiral.

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class HypnotiserTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.initial_pos = (0, 0)
        self.ring_spacing = 14      # base distance between ring centres
        self.multiplier = 1.15    # each ring gap gets this much bigger than the last
        self.grow_radius = 0     # how far the rings have expanded so far
        self.next_ring = 0       # radius where next ring should appear
        self.cur_gap = 0         # current gap 
        self.growth_rate = 1.15   # px per frame

    def draw(self, surface):
        mx, my = g.mouse_pos
        if mx < g.SIDE_PANEL_WIDTH or my < g.TOOLBAR_HEIGHT:
            return
        if not (self.is_dragging and pygame.mouse.get_pressed()[0]):
            return

        self.grow_radius += self.growth_rate
        color = g.COLORS[g.color_selected]

        # Draw rings as expansion front reaches them; gap grows by multiplier each ring
        while self.next_ring <= self.grow_radius:
            r = int(self.next_ring)
            band = max(1, int(self.cur_gap) // 2)
            if r > 0:
                pygame.draw.circle(
                    surface, color, self.initial_pos, r, band
                )
            self.cur_gap *= self.multiplier
            self.next_ring += self.cur_gap

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
            self.initial_pos = (mx, my)
            self.grow_radius = 0
            self.cur_gap = float(self.ring_spacing)
            self.next_ring = self.cur_gap
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        elif event.type == pygame.MOUSEWHEEL:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                # Shift+scroll adjusts multiplier
                self.multiplier += event.y * 0.05
                self.multiplier = max(1.05, min(3.0, self.multiplier))
            else:
                # Regular scroll adjusts spacing
                self.ring_spacing += event.y * 2
                self.ring_spacing = max(4, min(40, self.ring_spacing))

    def preview(self, screen):
        mx, my = g.mouse_pos
        color = g.COLORS[g.color_selected]
        # Show a small preview at cursor (3 rings only)
        gap = float(self.ring_spacing)
        r = gap * 0.5
        for _ in range(3):
            band = max(1, int(gap) // 3)
            pygame.draw.circle(screen, color, (mx, my), int(r), band)
            gap *= self.multiplier
            r += gap * 0.5
