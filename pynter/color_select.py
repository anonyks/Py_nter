# Color palette panel at the top of the window.

import pygame
from pynter import globals as g
from pynter.bitmap import bitmap_to_surface, ICON_FILE_SAVE, ICON_BIN, ICON_COLOR_PICKER


def pick_color_dialog():
    # Open the OS colour picker and return the chosen colour.
    try:
        import tkinter as tk
        from tkinter import colorchooser
        root = tk.Tk()
        root.withdraw()
        result = colorchooser.askcolor(title="Pick a colour")
        root.destroy()
        if result and result[0] is not None:
            r, gr, b = (int(v) for v in result[0])
            return pygame.Color(r, gr, b)
    except Exception:
        pass
    return None


def save_file_dialog():
    # Open a Save-As dialog so the user can pick where to save.
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        path = filedialog.asksaveasfilename(
            title="Save image as",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("All files", "*.*")],
        )
        root.destroy()
        return path if path else None
    except Exception:
        return None


class ColorSelect:
    def __init__(self):
        self.color_rects = []
        self.btn_save_rect = pygame.Rect(950, 5, 40, 40)
        self.btn_clear_rect = pygame.Rect(1000, 5, 40, 40)
        self.btn_rgb_rect = pygame.Rect(1050, 5, 40, 40)
        self.color_mouse_hover = -1
        # Toast notification state
        self.toast_text = ""
        self.toast_timer = 0
        self.toast_duration = 180  # ~3 seconds at 120fps

    def init(self):
        g.color_selected = 0
        self.color_rects = []
        for i in range(g.MAX_COLORS_COUNT):
            x = 210 + 30 * i + 2 * i
            self.color_rects.append(pygame.Rect(x, 10, 30, 30))

    def handle_events(self, event):
        if event is None:
            return

        # Mouse click on colour swatch
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.color_rects):
                if rect.collidepoint(g.mouse_pos):
                    g.color_selected = i
                    break

            # Save button
            if self.btn_save_rect.collidepoint(g.mouse_pos):
                self.save_canvas()

            # Clear button
            if self.btn_clear_rect.collidepoint(g.mouse_pos):
                self.clear_canvas()

            # RGB picker button -> opens native OS colour dialog
            if self.btn_rgb_rect.collidepoint(g.mouse_pos):
                col = pick_color_dialog()
                if col is not None:
                    g.COLORS[0] = col
                    g.color_selected = 0

    def save_canvas(self):
        if g.canvas_surface is None:
            return
        path = save_file_dialog()
        if path:
            pygame.image.save(g.canvas_surface, path)
            # Show short filename in toast
            import os
            name = os.path.basename(path)
            self.show_toast(f"Saved: {name}")

    def clear_canvas(self):
        if g.canvas_surface is not None:
            g.push_undo_snapshot()
            g.canvas_surface.fill((245, 245, 245))  # RAYWHITE

    def show_toast(self, text):
        self.toast_text = text
        self.toast_timer = self.toast_duration

    def update(self):
        # Hover detection (continuous, no event needed)
        self.color_mouse_hover = -1
        for i, rect in enumerate(self.color_rects):
            if rect.collidepoint(g.mouse_pos):
                self.color_mouse_hover = i
                break

        # Toast auto-dismiss countdown
        if self.toast_timer > 0:
            self.toast_timer -= 1

    def draw(self, screen):
        # Top bar background
        pygame.draw.rect(screen, (245, 245, 245), pygame.Rect(0, 0, g.SCREEN_WIDTH, 50))
        pygame.draw.line(screen, (200, 200, 200), (0, 50), (g.SCREEN_WIDTH, 50))

        # Current colour preview (shows the active colour)
        pygame.draw.rect(screen, g.COLORS[g.color_selected], pygame.Rect(11, 11, 28, 28))
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(10, 10, 30, 30), 1)

        # Colour swatches
        for i, rect in enumerate(self.color_rects):
            pygame.draw.rect(screen, g.COLORS[i], rect)

        # Hover highlight
        if self.color_mouse_hover >= 0:
            hover_surf = pygame.Surface(
                (self.color_rects[self.color_mouse_hover].width,
                 self.color_rects[self.color_mouse_hover].height),
                pygame.SRCALPHA,
            )
            hover_surf.fill((255, 255, 255, 153))  # semi-transparent white
            screen.blit(hover_surf, self.color_rects[self.color_mouse_hover].topleft)

        # Selection border
        sel = self.color_rects[g.color_selected]
        pygame.draw.rect(
            screen, (0, 0, 0),
            pygame.Rect(sel.x - 2, sel.y - 2, sel.width + 4, sel.height + 4), 2,
        )

        # Clear button
        if self.btn_clear_rect.collidepoint(g.mouse_pos):
            clr_color = (230, 41, 55)
        else:
            clr_color = (0, 0, 0)
        pygame.draw.rect(screen, clr_color, self.btn_clear_rect, 2)
        clr_icon = bitmap_to_surface(ICON_BIN, clr_color, scale=1)
        screen.blit(
            clr_icon,
            (self.btn_clear_rect.x + (self.btn_clear_rect.width - clr_icon.get_width()) // 2,
             self.btn_clear_rect.y + (self.btn_clear_rect.height - clr_icon.get_height()) // 2),
        )

        # Save button
        if self.btn_save_rect.collidepoint(g.mouse_pos):
            btn_color = (230, 41, 55)
        else:
            btn_color = (0, 0, 0)
        pygame.draw.rect(screen, btn_color, self.btn_save_rect, 2)
        icon_surf = bitmap_to_surface(ICON_FILE_SAVE, btn_color, scale=1)
        screen.blit(
            icon_surf,
            (self.btn_save_rect.x + (self.btn_save_rect.width - icon_surf.get_width()) // 2,
             self.btn_save_rect.y + (self.btn_save_rect.height - icon_surf.get_height()) // 2),
        )

        # RGB picker button (color picker icon)
        if self.btn_rgb_rect.collidepoint(g.mouse_pos):
            rgb_color = (0, 121, 241)
        else:
            rgb_color = (0, 0, 0)
        pygame.draw.rect(screen, rgb_color, self.btn_rgb_rect, 2)
        rgb_icon = bitmap_to_surface(ICON_COLOR_PICKER, rgb_color, scale=1)
        screen.blit(
            rgb_icon,
            (self.btn_rgb_rect.x + (self.btn_rgb_rect.width - rgb_icon.get_width()) // 2,
             self.btn_rgb_rect.y + (self.btn_rgb_rect.height - rgb_icon.get_height()) // 2),
        )

        # Toast notification (bottom-right, fades out)
        if self.toast_timer > 0 and self.toast_text:
            alpha = min(255, self.toast_timer * 6)  # quick fade-out in last ~40 frames
            toast_font = pygame.font.SysFont(None, 22)
            txt_surf = toast_font.render(self.toast_text, True, (255, 255, 255))
            pad_x, pad_y = 16, 10
            tw = txt_surf.get_width() + pad_x * 2
            th = txt_surf.get_height() + pad_y * 2
            tx = g.SCREEN_WIDTH - tw - 20
            ty = g.SCREEN_HEIGHT - th - 20
            bg = pygame.Surface((tw, th), pygame.SRCALPHA)
            bg.fill((40, 40, 40, alpha))
            screen.blit(bg, (tx, ty))
            txt_surf.set_alpha(alpha)
            screen.blit(txt_surf, (tx + pad_x, ty + pad_y))
