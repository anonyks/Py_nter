# Main window - sets up pygame, runs the game loop.

import pygame
from pynter import globals as g
from pynter.canvas import Canvas
from pynter.color_select import ColorSelect
from pynter.tool_select import ToolSelect


class MainWindowGUI:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.color_select = None
        self.tool_select = None
        self.canvas = None
        self.running = False

    def init(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))
        pygame.display.set_caption("Pynter")
        self.clock = pygame.time.Clock()

        self.color_select = ColorSelect()
        self.tool_select = ToolSelect()
        self.canvas = Canvas(self.tool_select)

        self.color_select.init()
        self.tool_select.init()
        self.canvas.init()

    def start_loop(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(120)  # cap at 120 frames per second

    def handle_events(self):
        g.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # Global undo / redo  (Ctrl+Z / Ctrl+Y)
            if event.type == pygame.KEYDOWN:
                mods = event.mod
                if mods & pygame.KMOD_CTRL:
                    if event.key == pygame.K_z:
                        g.undo()
                        continue
                    elif event.key == pygame.K_y:
                        g.redo()
                        continue

            self.canvas.handle_events(event)
            self.color_select.handle_events(event)
            self.tool_select.handle_events(event)

        # Per-frame updates (no specific event)
        self.canvas.handle_events(None)
        self.color_select.update()

    def draw(self):
        self.screen.fill((245, 245, 245))
        self.canvas.draw(self.screen)
        self.color_select.draw(self.screen)
        self.tool_select.draw(self.screen)
        pygame.display.flip()

    def shutdown(self):
        pygame.quit()
