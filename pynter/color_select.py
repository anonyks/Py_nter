# color palette panel at the top of the window

import pygame
from pynter import globals as g
from pynter.bitmap import bitmap_to_surface, ICON_FILE_SAVE, ICON_BIN, ICON_COLOR_PICKER


def pick_color_dialog():
    # opens the colour picker dialog
    try:
        import tkinter as tk
        from tkinter import colorchooser
        root = tk.Tk()
        root.withdraw()  # hides the ugly empty tkinter window that pops up
        result = colorchooser.askcolor(title="Pick a colour")
        root.destroy()
        if result and result[0] is not None:
            # unpack rgb floats into ints (gr not g because g is our globals module)
            r, gr, b = (int(v) for v in result[0])
            return pygame.Color(r, gr, b)
    except Exception:
        pass
    return None


def save_file_dialog():
    # opens save-as dialog
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()  # hide the tkinter root window
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
        # toast stuff
        self.toast_text = ""
        self.toast_timer = 0
        self.toast_duration = 180  # ~3 seconds at 60fps

    def init(self):
        g.color_selected = 0
        self.color_rects = []
        for i in range(g.MAX_COLORS_COUNT):
            # 210px offset from left, each swatch is 30px wide + 2px gap between them
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

            # RGB picker -> opens colour picker dialog
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
        # hover check
        self.color_mouse_hover = -1
        for i, rect in enumerate(self.color_rects):
            if rect.collidepoint(g.mouse_pos):
                self.color_mouse_hover = i
                break

        # count down the toast
        if self.toast_timer > 0:
            self.toast_timer -= 1

    def draw(self, screen):
        # top bar bg - beige
        pygame.draw.rect(screen, (236, 233, 216), pygame.Rect(0, 0, g.SCREEN_WIDTH, 50))

        # colour swatches
        for i, rect in enumerate(self.color_rects):
            pygame.draw.rect(screen, g.COLORS[i], rect)

        # hover effect
        if self.color_mouse_hover >= 0:
            # SRCALPHA so we get transparency on this overlay
            hover_surf = pygame.Surface(
                (self.color_rects[self.color_mouse_hover].width,
                 self.color_rects[self.color_mouse_hover].height),
                pygame.SRCALPHA,
            )
            # 4th number = alpha (153/255 ≈ 60% see-through)
            hover_surf.fill((255, 255, 255, 153))
            screen.blit(hover_surf, self.color_rects[self.color_mouse_hover].topleft)

        # dark outline on selected swatch
        # -2 and +4 make the outline 2px bigger on each side
        sel = self.color_rects[g.color_selected]
        pygame.draw.rect(
            screen, (0, 0, 0),
            pygame.Rect(sel.x - 2, sel.y - 2, sel.width + 4, sel.height + 4), 2,  # last 2 = border thickness
        )

        # Clear button
        if self.btn_clear_rect.collidepoint(g.mouse_pos):
            clr_color = (49, 106, 197)  # windows xp selection blue for hover
        else:
            clr_color = (0, 0, 0)
        clr_icon = bitmap_to_surface(ICON_BIN, clr_color, scale=1)
        # center the icon inside the button: (button_size - icon_size) / 2
        screen.blit(
            clr_icon,
            (self.btn_clear_rect.x + (self.btn_clear_rect.width - clr_icon.get_width()) // 2,
             self.btn_clear_rect.y + (self.btn_clear_rect.height - clr_icon.get_height()) // 2),
        )

        # Save button
        if self.btn_save_rect.collidepoint(g.mouse_pos):
            btn_color = (49, 106, 197)  # xp blue on hover
        else:
            btn_color = (0, 0, 0)
        icon_surf = bitmap_to_surface(ICON_FILE_SAVE, btn_color, scale=1)
        screen.blit(
            icon_surf,
            (self.btn_save_rect.x + (self.btn_save_rect.width - icon_surf.get_width()) // 2,
             self.btn_save_rect.y + (self.btn_save_rect.height - icon_surf.get_height()) // 2),
        )

        # color picker button
        if self.btn_rgb_rect.collidepoint(g.mouse_pos):
            rgb_color = (49, 106, 197)  # xp blue on hover
        else:
            rgb_color = (0, 0, 0)
        rgb_icon = bitmap_to_surface(ICON_COLOR_PICKER, rgb_color, scale=1)
        screen.blit(
            rgb_icon,
            (self.btn_rgb_rect.x + (self.btn_rgb_rect.width - rgb_icon.get_width()) // 2,
             self.btn_rgb_rect.y + (self.btn_rgb_rect.height - rgb_icon.get_height()) // 2),
        )

        # toast message
        if self.toast_timer > 0 and self.toast_text:
            alpha = min(255, self.toast_timer * 6)  # fade out near the end
            toast_font = pygame.font.SysFont(None, 22)  # None = default system font
            txt_surf = toast_font.render(self.toast_text, True, (255, 255, 255))
            pad_x, pad_y = 16, 10
            tw = txt_surf.get_width() + pad_x * 2
            th = txt_surf.get_height() + pad_y * 2
            tx = g.SCREEN_WIDTH - tw - 20
            ty = g.SCREEN_HEIGHT - th - 20
            bg = pygame.Surface((tw, th), pygame.SRCALPHA)
            bg.fill((40, 40, 40, alpha))  # dark bg with fading alpha
            screen.blit(bg, (tx, ty))
            txt_surf.set_alpha(alpha)  # fade the text too
            screen.blit(txt_surf, (tx + pad_x, ty + pad_y))
