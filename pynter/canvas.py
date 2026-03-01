"""
Drawing canvas - owns the persistent surface that tools draw onto.
"""

import pygame
from pynter import globals as g
from pynter.tool_select import ToolSelect


class Canvas:
    def __init__(self, tool_select: ToolSelect):
        self.tool_select = tool_select

    def init(self):
        g.canvas_surface = pygame.Surface((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))
        g.canvas_surface.fill((245, 245, 245))  # RAYWHITE

    def handle_events(self, event):
        tool = self.tool_select.get_selected_tool()
        if tool is None:
            return
        tool.handle_events(event)

    def draw(self, screen):
        tool = self.tool_select.get_selected_tool()

        # Draw tool strokes
        if tool is not None:
            tool.draw(g.canvas_surface)

        # Blit canvas
        screen.blit(g.canvas_surface, (0, 0))

        # Draw live preview overlay (not committed)
        if tool is not None:
            mx, my = g.mouse_pos
            if my > g.TOOLBAR_HEIGHT:
                tool.preview(screen)
