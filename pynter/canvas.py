# Drawing canvas - the main surface that tools draw onto.

import pygame
from pynter import globals as g
from pynter.tool_select import ToolSelect


class Canvas:
    def __init__(self, tool_select):
        self.tool_select = tool_select

    def init(self):
        g.canvas_surface = pygame.Surface((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))
        g.canvas_surface.fill((245, 245, 245))  # RAYWHITE

        # clip rect that keeps drawing inside the canvas margin
        m = 6
        self.clip = pygame.Rect(
            g.SIDE_PANEL_WIDTH + m, g.TOOLBAR_HEIGHT + m,
            g.SCREEN_WIDTH - g.SIDE_PANEL_WIDTH - m * 2,
            g.SCREEN_HEIGHT - g.TOOLBAR_HEIGHT - m * 2,
        )

    def handle_events(self, event):
        tool = self.tool_select.get_selected_tool()
        if tool is None:
            return
        g.canvas_surface.set_clip(self.clip)
        tool.handle_events(event)
        g.canvas_surface.set_clip(None)

    def draw(self, screen):
        tool = self.tool_select.get_selected_tool()

        # Draw tool strokes
        if tool is not None:
            g.canvas_surface.set_clip(self.clip)
            tool.draw(g.canvas_surface)
            g.canvas_surface.set_clip(None)

        # Blit canvas
        screen.blit(g.canvas_surface, (0, 0))

        # Draw live preview overlay (not committed)
        if tool is not None:
            mx, my = g.mouse_pos
            if my > g.TOOLBAR_HEIGHT:
                screen.set_clip(self.clip)
                tool.preview(screen)
                screen.set_clip(None)
