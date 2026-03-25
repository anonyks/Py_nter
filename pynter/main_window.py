# main window - the 3D look

import pygame
from pynter import globals as g
from pynter.canvas import Canvas
from pynter.color_select import ColorSelect
from pynter.tool_select import ToolSelect, Tools

# border colours for the 3D buttons
# light on top-left + dark on bottom-right = looks raised (like win95)
btn_light  = (255, 255, 255)
btn_shadow = (172, 168, 153)
btn_dark   = (113, 111, 100)


def draw_3d_border(surface, rect, pressed=False):
    # draws raised or sunken border depending on pressed
    # hi/lo swap = raised vs sunken illusion
    hi, lo = (btn_dark, btn_light) if pressed else (btn_light, btn_shadow)
    # rect.right is 1 past the last pixel so -1 to stay inside
    pygame.draw.line(surface, hi, rect.topleft, (rect.right - 1, rect.top))
    pygame.draw.line(surface, hi, rect.topleft, (rect.left, rect.bottom - 1))
    pygame.draw.line(surface, lo, (rect.left, rect.bottom - 1), (rect.right - 1, rect.bottom - 1))
    pygame.draw.line(surface, lo, (rect.right - 1, rect.top), (rect.right - 1, rect.bottom - 1))


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
        pygame.font.init()  # need this before rendering any text
        # RESIZABLE lets the user drag the window edges to resize
        self.screen = pygame.display.set_mode((g.SCREEN_WIDTH, g.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Pynter")
        # set window icon
        try:
            icon = pygame.image.load(g.resource_path("pynter/icon.ico"))
            pygame.display.set_icon(icon)
        except:
            pass  # no icon file, whatever
        self.clock = pygame.time.Clock()  # used to cap frame rate

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
            self.clock.tick(120)  # cap at 120 fps so it doesnt eat the cpu

    def handle_events(self):
        g.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # VIDEORESIZE fires when user drags the window border
            if event.type == pygame.VIDEORESIZE:
                g.SCREEN_WIDTH = event.w
                g.SCREEN_HEIGHT = event.h
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # save old canvas before making a new one so we keep the drawing
                old = g.canvas_surface
                g.canvas_surface = pygame.Surface((event.w, event.h))
                g.canvas_surface.fill((245, 245, 245))
                g.canvas_surface.blit(old, (0, 0))  # paste old drawing onto new bigger canvas

            if event.type == pygame.KEYDOWN:
                mods = event.mod
                # bitwise AND to check if ctrl is held
                if mods & pygame.KMOD_CTRL:
                    if event.key == pygame.K_z:
                        g.undo()
                        # continue skips canvas/tool handlers so undo doesnt also trigger a tool action
                        continue
                    elif event.key == pygame.K_y:
                        g.redo()
                        continue

            self.canvas.handle_events(event)
            self.color_select.handle_events(event)
            self.tool_select.handle_events(event)

        # None signals "no specific event, just do per-frame stuff like continuous drawing"
        self.canvas.handle_events(None)
        self.color_select.update()
        self.tool_select.update()

    def draw(self):
        m = 6
        self.screen.fill((245, 245, 245))

        self.canvas.draw(self.screen)

        # draw the panels
        self.color_select.draw(self.screen)
        self.tool_select.draw(self.screen)

        # 3d borders on top of everything
        for i, box in enumerate(self.tool_select.tool_boxes):
            # Tools(i) converts loop index to enum so we can compare with selected_tool
            draw_3d_border(self.screen, box, pressed=(self.tool_select.selected_tool == Tools(i)))
        for rect in self.color_select.color_rects:
            draw_3d_border(self.screen, rect, pressed=True)
        for btn in [self.color_select.btn_save_rect,
                     self.color_select.btn_clear_rect,
                     self.color_select.btn_rgb_rect]:
            # collidepoint = True when cursor hovers over button, giving a pressed look
            draw_3d_border(self.screen, btn, pressed=btn.collidepoint(g.mouse_pos))

        # panel dividers
        pygame.draw.line(self.screen, btn_shadow,
            (g.SIDE_PANEL_WIDTH - 1, 0), (g.SIDE_PANEL_WIDTH - 1, g.SCREEN_HEIGHT))
        pygame.draw.line(self.screen, btn_light,
            (g.SIDE_PANEL_WIDTH, 0), (g.SIDE_PANEL_WIDTH, g.SCREEN_HEIGHT))
        pygame.draw.line(self.screen, btn_shadow,
            (g.SIDE_PANEL_WIDTH, g.TOOLBAR_HEIGHT - 1), (g.SCREEN_WIDTH, g.TOOLBAR_HEIGHT - 1))
        pygame.draw.line(self.screen, btn_light,
            (g.SIDE_PANEL_WIDTH, g.TOOLBAR_HEIGHT), (g.SCREEN_WIDTH, g.TOOLBAR_HEIGHT))

        # sunken border around the canvas
        # -2 and +2 nudge the border lines so they slightly overlap the margin edge
        cx, cy = g.SIDE_PANEL_WIDTH + m - 2, g.TOOLBAR_HEIGHT + m - 2
        cw = g.SCREEN_WIDTH - cx - m + 2
        ch = g.SCREEN_HEIGHT - cy - m + 2
        pygame.draw.line(self.screen, btn_shadow, (cx, cy), (cx + cw, cy))
        pygame.draw.line(self.screen, btn_shadow, (cx, cy), (cx, cy + ch))
        pygame.draw.line(self.screen, btn_light, (cx, cy + ch), (cx + cw, cy + ch))
        pygame.draw.line(self.screen, btn_light, (cx + cw, cy), (cx + cw, cy + ch))
        pygame.draw.line(self.screen, btn_dark, (cx + 1, cy + 1), (cx + cw - 1, cy + 1))
        pygame.draw.line(self.screen, btn_dark, (cx + 1, cy + 1), (cx + 1, cy + ch - 1))

        # flip actually pushes everything we drew this frame to the screen
        # without this nothing shows up
        pygame.display.flip()

    def shutdown(self):
        pygame.quit()


