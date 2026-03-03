# Tool selection side-panel.

from enum import IntEnum
import pygame

from pynter import globals as g
from pynter.bitmap import bitmap_to_surface, TOOL_ICON_BITMAPS
from pynter.tools import (
    Tool,
    PencilTool,
    BrushTool,
    EraserTool,
    LineTool,
    CurveTool,
    RectangleTool,
    SquareTool,
    CircleTool,
    EllipseTool,
    SelectBoxTool,
    HypnotiserTool,
    SpiralTool,
    MandalaTool,
    TriangleTool,
    FillTool,
    EyeDropperTool,
    TextTool,
    MagnifierTool,
)

class Tools(IntEnum):
    SELECT_BOX = 0
    TEXT_INPUT = 1
    ERASER = 2
    FILL = 3
    EYE_DROPPER = 4
    MAGNIFIER = 5
    PENCIL = 6
    BRUSH = 7
    LINE = 8
    CURVE = 9
    SQUARE = 10
    RECTANGLE = 11
    CIRCLE = 12
    ELLIPSE = 13
    TRIANGLE = 14
    HYPNOTISER = 15
    SPIRAL = 16
    MANDALA = 17


TOOL_LABELS = [
    "SEL", "TXT", "ERS", "FIL",
    "EYE", "MAG", "PEN", "BRU",
    "LIN", "CRV", "SQR", "REC",
    "CIR", "ELL", "TRI", "HYP",
]



class ToolSelect:
    def __init__(self):
        self.tool_boxes = []
        self.selected_tool = Tools.PENCIL
        self.current_tool = None
        self.icon_cache = []
        self.tool_mouse_hover = -1

    def init(self):
        self.tool_boxes = []
        for i in range(g.TOOL_BOX_ICONS_COUNT):
            x = 20 + 60 * (i % 2)
            y = 60 + 60 * (i // 2)  # Start 40px higher
            self.tool_boxes.append(pygame.Rect(x, y, 40, 40))

        # load icon images
        self.icon_cache = [
            bitmap_to_surface(bmp, (40, 40, 40), scale=1)
            for bmp in TOOL_ICON_BITMAPS
        ]

        # Default tool
        self.select_tool(Tools.PENCIL)

    def select_tool(self, tool):
        self.selected_tool = tool
        factory = {
            Tools.PENCIL: PencilTool,
            Tools.BRUSH: BrushTool,
            Tools.ERASER: EraserTool,
            Tools.LINE: LineTool,
            Tools.CURVE: CurveTool,
            Tools.RECTANGLE: RectangleTool,
            Tools.SQUARE: SquareTool,
            Tools.CIRCLE: CircleTool,
            Tools.ELLIPSE: EllipseTool,
            Tools.SELECT_BOX: SelectBoxTool,
            Tools.HYPNOTISER: HypnotiserTool,
            Tools.SPIRAL: SpiralTool,
            Tools.MANDALA: MandalaTool,
            Tools.TRIANGLE: TriangleTool,
            Tools.FILL: FillTool,
            Tools.EYE_DROPPER: EyeDropperTool,
            Tools.TEXT_INPUT: TextTool,
            Tools.MAGNIFIER: MagnifierTool,
        }
        cls = factory.get(tool)
        if cls is not None:
            self.current_tool = cls()
        else:
            self.current_tool = None

    def get_selected_tool(self):
        return self.current_tool

    def handle_events(self, event):
        if event is None:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, box in enumerate(self.tool_boxes):
                if box.collidepoint(g.mouse_pos):
                    self.select_tool(Tools(i))
                    break

    def update(self):
        # check which tool button the mouse is over
        self.tool_mouse_hover = -1
        for i, box in enumerate(self.tool_boxes):
            if box.collidepoint(g.mouse_pos):
                self.tool_mouse_hover = i
                break

    def draw(self, screen):
        # side panel bg - clean beige
        pygame.draw.rect(screen, (236, 233, 216), pygame.Rect(0, 0, 140, g.SCREEN_HEIGHT))

        font = pygame.font.SysFont(None, 18)
        for i, box in enumerate(self.tool_boxes):
            # button face
            pygame.draw.rect(screen, (236, 233, 216), box)

            # icon centered in button
            if i < len(self.icon_cache) and self.icon_cache[i]:
                icon = self.icon_cache[i]
                ix = box.x + (box.width - icon.get_width()) // 2
                iy = box.y + (box.height - icon.get_height()) // 2
                screen.blit(icon, (ix, iy))
            else:
                # no icon, show text instead
                label = font.render(TOOL_LABELS[i], True, (0, 0, 0))
                screen.blit(
                    label,
                    (box.x + (box.width - label.get_width()) // 2,
                     box.y + (box.height - label.get_height()) // 2),
                )

            # Hover highlight
            if i == self.tool_mouse_hover and self.selected_tool != Tools(i):
                hover_surf = pygame.Surface((box.width, box.height), pygame.SRCALPHA)
                hover_surf.fill((255, 255, 255, 100))
                screen.blit(hover_surf, box.topleft)

        # Info / hint text below the tool buttons
        self.draw_info(screen)

    def draw_info(self, screen):
        # show tool-specific info + hints below the buttons
        info_y = 60 + 60 * ((g.TOOL_BOX_ICONS_COUNT - 1) // 2) + 40 + 10
        info_font = pygame.font.SysFont(None, 22)

        # Show size for brush / eraser
        if self.selected_tool in (Tools.BRUSH, Tools.ERASER) and self.current_tool is not None:
            if self.selected_tool == Tools.BRUSH:
                val = int(getattr(self.current_tool, 'brush_size', 0))
                if hasattr(self.current_tool, 'get_shape_name'):
                    shape_name = self.current_tool.get_shape_name()
                else:
                    shape_name = ''
            else:
                val = int(getattr(self.current_tool, 'eraser_size', 0))
                shape_name = ''
            size_txt = info_font.render(f"Size: {val}", True, (60, 60, 60))
            screen.blit(size_txt, (20, info_y))
            info_y += 20
            if shape_name:
                sh_txt = info_font.render(f"Type: {shape_name}", True, (60, 60, 60))
                screen.blit(sh_txt, (20, info_y))
                info_y += 20
            # Show spray density when spray is active
            if shape_name == "Spray":
                density = int(getattr(self.current_tool, 'spray_density', 0))
                den_txt = info_font.render(f"Density: {density}", True, (60, 60, 60))
                screen.blit(den_txt, (20, info_y))
                info_y += 20
                hint1_txt = pygame.font.SysFont(None, 16).render("Scroll=size  Tab=type", True, (120, 120, 120))
                screen.blit(hint1_txt, (20, info_y))
                info_y += 16
                hint2_txt = pygame.font.SysFont(None, 16).render("Shift+Scroll=density", True, (120, 120, 120))
                screen.blit(hint2_txt, (20, info_y))
            elif shape_name:
                hint1_txt = pygame.font.SysFont(None, 16).render("Scroll=size  Tab=type", True, (120, 120, 120))
                screen.blit(hint1_txt, (20, info_y))
            elif self.selected_tool == Tools.ERASER:
                opacity = int(getattr(self.current_tool, 'opacity', 100))
                op_txt = info_font.render(f"Opacity: {opacity}%", True, (60, 60, 60))
                screen.blit(op_txt, (20, info_y))
                info_y += 20
                hint1_txt = pygame.font.SysFont(None, 16).render("Scroll=size", True, (120, 120, 120))
                screen.blit(hint1_txt, (20, info_y))
                info_y += 16
                hint2_txt = pygame.font.SysFont(None, 16).render("Shift+Scroll=opacity", True, (120, 120, 120))
                screen.blit(hint2_txt, (20, info_y))
            else:
                hint1_txt = pygame.font.SysFont(None, 16).render("Scroll=resize", True, (120, 120, 120))
                screen.blit(hint1_txt, (20, info_y))

        # Show width for shape tools
        elif self.selected_tool in (Tools.LINE, Tools.CURVE, Tools.RECTANGLE, Tools.SQUARE,
                                       Tools.CIRCLE, Tools.ELLIPSE, Tools.TRIANGLE):
            w_txt = info_font.render(f"Width: {g.line_width}", True, (60, 60, 60))
            screen.blit(w_txt, (20, info_y))
            info_y += 20
            hint_txt = pygame.font.SysFont(None, 16).render("Scroll to adjust", True, (120, 120, 120))
            screen.blit(hint_txt, (20, info_y))

        # Show spacing for hypnotiser
        elif self.selected_tool == Tools.HYPNOTISER and self.current_tool is not None:
            s_txt = info_font.render(f"Spacing: {self.current_tool.ring_spacing}", True, (60, 60, 60))
            screen.blit(s_txt, (20, info_y))
            info_y += 20
            m_txt = info_font.render(f"Multiplier: {self.current_tool.multiplier:.2f}", True, (60, 60, 60))
            screen.blit(m_txt, (20, info_y))
            info_y += 20
            hint1_txt = pygame.font.SysFont(None, 16).render("Scroll=spacing", True, (120, 120, 120))
            screen.blit(hint1_txt, (20, info_y))
            info_y += 16
            hint2_txt = pygame.font.SysFont(None, 16).render("Shift+Scroll=growth", True, (120, 120, 120))
            screen.blit(hint2_txt, (20, info_y))

        # Show spacing and width for spiral
        elif self.selected_tool == Tools.SPIRAL and self.current_tool is not None:
            s_txt = info_font.render(f"Spacing: {self.current_tool.spacing:.1f}", True, (60, 60, 60))
            screen.blit(s_txt, (20, info_y))
            info_y += 20
            w_txt = info_font.render(f"Width: {self.current_tool.line_width}", True, (60, 60, 60))
            screen.blit(w_txt, (20, info_y))
            info_y += 20
            hint1_txt = pygame.font.SysFont(None, 16).render("Scroll=spacing", True, (120, 120, 120))
            screen.blit(hint1_txt, (20, info_y))
            info_y += 16
            hint2_txt = pygame.font.SysFont(None, 16).render("Shift+Scroll=width", True, (120, 120, 120))
            screen.blit(hint2_txt, (20, info_y))

        # Show symmetry and brush size for mandala
        elif self.selected_tool == Tools.MANDALA and self.current_tool is not None:
            s_txt = info_font.render(f"Symmetry: {self.current_tool.symmetry_count}", True, (60, 60, 60))
            screen.blit(s_txt, (20, info_y))
            info_y += 20
            b_txt = info_font.render(f"Brush: {self.current_tool.brush_size}", True, (60, 60, 60))
            screen.blit(b_txt, (20, info_y))
            info_y += 20
            hint1_txt = pygame.font.SysFont(None, 16).render("Scroll=symmetry", True, (120, 120, 120))
            screen.blit(hint1_txt, (20, info_y))
            info_y += 16
            hint2_txt = pygame.font.SysFont(None, 16).render("Shift+Scroll=brush", True, (120, 120, 120))
            screen.blit(hint2_txt, (20, info_y))
        # Show font size and family for text tool
        elif self.selected_tool == Tools.TEXT_INPUT and self.current_tool is not None:
            size_txt = info_font.render(f"Size: {self.current_tool.font_size}", True, (60, 60, 60))
            screen.blit(size_txt, (20, info_y))
            info_y += 20
            font_name = self.current_tool.font_family or "Default"
            font_txt = pygame.font.SysFont(None, 18).render(f"Font: {font_name}", True, (60, 60, 60))
            screen.blit(font_txt, (20, info_y))
            info_y += 20
            hint1_txt = pygame.font.SysFont(None, 16).render("Scroll=size", True, (120, 120, 120))
            screen.blit(hint1_txt, (20, info_y))
            info_y += 16
            hint2_txt = pygame.font.SysFont(None, 16).render("Shift+Scroll=font", True, (120, 120, 120))
            screen.blit(hint2_txt, (20, info_y))

        # Show RGB values for fill tool
        elif self.selected_tool == Tools.FILL:
            current_color = g.COLORS[g.color_selected]
            rgb_txt = pygame.font.SysFont(None, 18).render(f"RGB: ({current_color.r}, {current_color.g}, {current_color.b})", True, (60, 60, 60))
            screen.blit(rgb_txt, (20, info_y))
            info_y += 20
            hex_color = f"#{current_color.r:02x}{current_color.g:02x}{current_color.b:02x}".upper()
            hex_txt = pygame.font.SysFont(None, 18).render(f"Hex: {hex_color}", True, (60, 60, 60))
            screen.blit(hex_txt, (20, info_y))
            info_y += 20
            hint_txt = pygame.font.SysFont(None, 16).render("Click to flood fill", True, (120, 120, 120))
            screen.blit(hint_txt, (20, info_y))

        # Show RGB values for eyedropper tool
        elif self.selected_tool == Tools.EYE_DROPPER:
            current_color = g.COLORS[g.color_selected]
            rgb_txt = pygame.font.SysFont(None, 18).render(f"RGB: ({current_color.r}, {current_color.g}, {current_color.b})", True, (60, 60, 60))
            screen.blit(rgb_txt, (20, info_y))
            info_y += 20
            hex_color = f"#{current_color.r:02x}{current_color.g:02x}{current_color.b:02x}".upper()
            hex_txt = pygame.font.SysFont(None, 18).render(f"Hex: {hex_color}", True, (60, 60, 60))
            screen.blit(hex_txt, (20, info_y))
            info_y += 20
            hint_txt = pygame.font.SysFont(None, 16).render("Click to sample color", True, (120, 120, 120))
            screen.blit(hint_txt, (20, info_y))

        # Show zoom info for magnifier tool
        elif self.selected_tool == Tools.MAGNIFIER:
            if self.current_tool:
                zoom_val = int(getattr(self.current_tool, 'zoom', 4))
            else:
                zoom_val = 4
            zoom_txt = info_font.render(f"Zoom: {zoom_val}x", True, (60, 60, 60))
            screen.blit(zoom_txt, (20, info_y))
            info_y += 20
            hint_txt = pygame.font.SysFont(None, 16).render("Scroll = zoom", True, (120, 120, 120))
            screen.blit(hint_txt, (20, info_y))

        # Show transform hints for select-box
        elif self.selected_tool == Tools.SELECT_BOX:
            tiny = pygame.font.SysFont(None, 16)
            hints = [
                "R=Rotate CW",
                "Shift+R=CCW",
                "H=Flip Horiz",
                "V=Flip Vert",
                "+/- = Scale",
                "Esc=Cancel",
            ]
            for line in hints:
                txt = tiny.render(line, True, (100, 100, 100))
                screen.blit(txt, (20, info_y))
                info_y += 16

        # Credits (shown when no tool-specific info)
        else:
            self.draw_credits(screen, info_y)

    def draw_credits(self, screen, y):
        # credit logo at the bottom
        if not hasattr(self, 'credit_img'):
            try:
                img = pygame.image.load("pynter/credit.png").convert_alpha()
                w = g.SIDE_PANEL_WIDTH - 20
                h = int(img.get_height() * (w / img.get_width()))
                self.credit_img = pygame.transform.smoothscale(img, (w, h))
            except:
                self.credit_img = None
        if self.credit_img:
            x = (g.SIDE_PANEL_WIDTH - self.credit_img.get_width()) // 2
            screen.blit(self.credit_img, (x, y))


