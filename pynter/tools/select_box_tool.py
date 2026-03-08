# select box tool - select a region, move it, press enter to commit

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class SelectBoxTool(Tool):
    def __init__(self):
        self.is_dragging = False
        self.selected = False
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        self.selected_surface = None
        self.selected_rect = pygame.Rect(0, 0, 0, 0)

    def get_rect(self):
        sx, sy = self.start_pos
        ex, ey = self.end_pos
        x = min(sx, ex)
        y = min(sy, ey)
        w = abs(sx - ex)
        h = abs(sy - ey)
        return pygame.Rect(x, y, w, h)

    @staticmethod
    def draw_dashed_rect(surface, rect):
        # dashed rectangle outline
        # dash pattern: 4 pixels on, 4 pixels off (step 8, draw first 4)
        color = (0, 0, 0)
        # Top & bottom edges
        for i in range(0, rect.width, 8):
            for j in range(min(4, rect.width - i)):
                px = rect.x + i + j
                if 0 <= px < surface.get_width():
                    if 0 <= rect.y < surface.get_height():
                        surface.set_at((px, rect.y), color)
                    by = rect.y + rect.height - 1
                    if 0 <= by < surface.get_height():
                        surface.set_at((px, by), color)
        # Left & right edges
        for i in range(0, rect.height, 8):
            for j in range(min(4, rect.height - i)):
                py = rect.y + i + j
                if 0 <= py < surface.get_height():
                    if 0 <= rect.x < surface.get_width():
                        surface.set_at((rect.x, py), color)
                    rx = rect.x + rect.width - 1
                    if 0 <= rx < surface.get_width():
                        surface.set_at((rx, py), color)

    def draw(self, surface):
        pass  # committed on enter

    def handle_events(self, event):
        if event is None:
            return

        mx, my = g.mouse_pos

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Ignore clicks outside canvas
            if my < g.TOOLBAR_HEIGHT or mx < g.SIDE_PANEL_WIDTH:
                return
            if self.selected:
                # Already selected -> start moving
                self.is_dragging = False
            else:
                self.is_dragging = True
                self.start_pos = (mx, my)
                self.end_pos = (mx, my)

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.end_pos = (mx, my)
            elif self.selected and pygame.mouse.get_pressed()[0]:
                self.selected_rect.x = mx - self.selected_rect.width // 2
                self.selected_rect.y = my - self.selected_rect.height // 2

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.end_pos = (mx, my)
                self.is_dragging = False
                rect = self.get_rect()
                if rect.width > 0 and rect.height > 0 and g.canvas_surface is not None:
                    g.push_undo_snapshot()
                    # subsurface grabs a rectangular chunk without copying everything
                    # .copy() makes it a separate image so changing canvas doesnt affect it
                    self.selected_surface = g.canvas_surface.subsurface(rect).copy()
                    self.selected_rect = rect.copy()
                    # Clear region on canvas
                    g.canvas_surface.fill((245, 245, 245), rect)
                    self.selected = True

        elif event.type == pygame.KEYDOWN:
            if not self.selected or self.selected_surface is None:
                return

            if event.key == pygame.K_RETURN:
                # Commit selection
                if g.canvas_surface is not None:
                    g.canvas_surface.blit(self.selected_surface, self.selected_rect.topleft)
                self.selected = False
                self.selected_surface = None

            elif event.key == pygame.K_r:
                # Rotate 90 deg CW  (Shift+R = CCW)
                mods = pygame.key.get_mods()  # get_mods() = which modifier keys are held right now
                if mods & pygame.KMOD_SHIFT:
                    self.selected_surface = pygame.transform.rotate(self.selected_surface, 90)
                else:
                    self.selected_surface = pygame.transform.rotate(self.selected_surface, -90)
                self.refit_rect()

            elif event.key == pygame.K_h:
                # flip(True, False) = mirror horizontally (left-right swap)
                self.selected_surface = pygame.transform.flip(self.selected_surface, True, False)

            elif event.key == pygame.K_v:
                # flip(False, True) = mirror vertically (top-bottom swap)
                self.selected_surface = pygame.transform.flip(self.selected_surface, False, True)

            elif event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                # Scale up 2x
                w = self.selected_surface.get_width() * 2
                h = self.selected_surface.get_height() * 2
                self.selected_surface = pygame.transform.scale(self.selected_surface, (w, h))
                self.refit_rect()

            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                # Scale down 0.5x (minimum 1px)
                w = max(1, self.selected_surface.get_width() // 2)
                h = max(1, self.selected_surface.get_height() // 2)
                self.selected_surface = pygame.transform.scale(self.selected_surface, (w, h))
                self.refit_rect()

            elif event.key == pygame.K_ESCAPE:
                # cancel - restore original region
                self.selected = False
                self.selected_surface = None

    def refit_rect(self):
        # keep selection centred after rotating/scaling changes its size
        if self.selected_surface is None:
            return
        cx = self.selected_rect.x + self.selected_rect.width // 2
        cy = self.selected_rect.y + self.selected_rect.height // 2
        nw = self.selected_surface.get_width()
        nh = self.selected_surface.get_height()
        self.selected_rect = pygame.Rect(cx - nw // 2, cy - nh // 2, nw, nh)

    def preview(self, screen):
        if self.is_dragging:
            self.draw_dashed_rect(screen, self.get_rect())
        if self.selected and self.selected_surface is not None:
            screen.blit(self.selected_surface, self.selected_rect.topleft)
            self.draw_dashed_rect(screen, self.selected_rect)
