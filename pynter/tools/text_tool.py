"""Text input tool - click to place text on the canvas."""

import pygame
from pynter.tools.tool import Tool
from pynter import globals as g


class TextTool(Tool):
    """
    Click on the canvas to set a text insertion point, then type.
    Press Enter to commit the text to the canvas.
    Press Escape to cancel.
    Backspace deletes the last character.
    """

    def __init__(self):
        self.active = False
        self.text = ""
        self.pos = (0, 0)
        self.cached_font = None
        self.font_size = 28
        self.font_family = None  # None = default system font
        self.font_families = [None, 'Arial', 'Times New Roman', 'Courier New', 'Comic Sans MS', 'Verdana', 'Helvetica']

    def get_font(self):
        if self.cached_font is None:
            self.cached_font = pygame.font.SysFont(self.font_family, self.font_size)
        return self.cached_font

    def invalidate_font(self):
        """Clear font cache when size or family changes."""
        self.cached_font = None

    def draw(self, surface):
        pass  # committed on Enter via handle_events

    def handle_events(self, event):
        if event is None:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = g.mouse_pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOOLBAR_HEIGHT:
                # If we had pending text, commit it first
                if self.active and self.text:
                    self.commit()
                self.active = True
                self.text = ""
                self.pos = (mx, my)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.commit()
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode and event.unicode.isprintable():
                    self.text += event.unicode

        elif event.type == pygame.MOUSEWHEEL:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                # Shift+scroll changes font family
                if self.font_family in self.font_families:
                    current_index = self.font_families.index(self.font_family)
                else:
                    current_index = 0
                new_index = (current_index + event.y) % len(self.font_families)
                self.font_family = self.font_families[new_index]
                self.invalidate_font()
            else:
                # Regular scroll changes font size
                self.font_size += event.y * 2
                self.font_size = max(8, min(72, self.font_size))
                self.invalidate_font()

    def preview(self, screen):
        if self.active and self.text:
            txt_surface = self.get_font().render(self.text, True, g.COLORS[g.color_selected])
            screen.blit(txt_surface, self.pos)
            # Blinking cursor line
            tw = txt_surface.get_width()
            th = txt_surface.get_height()
            if pygame.time.get_ticks() % 1000 < 500:
                pygame.draw.line(
                    screen, g.COLORS[g.color_selected],
                    (self.pos[0] + tw + 2, self.pos[1]),
                    (self.pos[0] + tw + 2, self.pos[1] + th),
                    1,
                )
        elif not self.active:
            # Show a text cursor at mouse position
            mx, my = g.mouse_pos
            hint = self.get_font().render("T|", True, g.COLORS[g.color_selected])
            screen.blit(hint, (mx + 6, my - 14))

    def commit(self):
        """Render the text onto the canvas surface."""
        if g.canvas_surface is not None and self.text:
            g.push_undo_snapshot()
            txt_surface = self.get_font().render(self.text, True, g.COLORS[g.color_selected])
            g.canvas_surface.blit(txt_surface, self.pos)
        self.active = False
        self.text = ""
