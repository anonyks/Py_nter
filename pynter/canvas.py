# canvas - the main surface tools draw onto

import pygame
from pynter import globals as g
from pynter.tool_select import ToolSelect


class Canvas:
    def __init__(self, tool_select):
        self.tool_select = tool_select

    def init(self):
        # Surface = a blank image in memory that we can draw on
        g.canvas_surface = pygame.Surface((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))
        g.canvas_surface.fill((245, 245, 245))  # RAYWHITE

        # clip rect so nothing draws in the margin border
        # m = margin width around the canvas
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
        # set_clip restricts all drawing to inside this rect
        g.canvas_surface.set_clip(self.clip)
        tool.handle_events(event)
        # None = remove the clip so drawing goes back to normal
        g.canvas_surface.set_clip(None)

    def draw(self, screen):
        tool = self.tool_select.get_selected_tool()

        # draw tool strokes
        if tool is not None:
            g.canvas_surface.set_clip(self.clip)
            tool.draw(g.canvas_surface)
            g.canvas_surface.set_clip(None)

        # blit = paste canvas onto the display window
        # (0, 0) = top-left corner
        screen.blit(g.canvas_surface, (0, 0))

        # live preview on screen (not saved to canvas)
        # also clipped so preview doesnt bleed into the border
        if tool is not None:
            mx, my = g.mouse_pos
            # always show preview when tool has uncommitted content (e.g. text being typed)
            has_pending = getattr(tool, 'active', False) and getattr(tool, 'text', '')
            if my > g.TOOLBAR_HEIGHT or has_pending:
                screen.set_clip(self.clip)
                tool.preview(screen)
                screen.set_clip(None)
