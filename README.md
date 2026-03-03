# Pynter

A simple drawing and paint tool made with Python and Pygame.

The name comes from combining "Py" (Python) and "Painter".


## Features

- 18 drawing tools: pencil, brush, eraser, line, curve, rectangle, square, circle, ellipse, triangle, fill, eyedropper, text, magnifier, select box, hypnotiser, spiral, mandala
- Midpoint circle algorithm and midpoint ellipse algorithm for drawing circles and ellipses
- Bresenham's line algorithm for pixel-accurate lines
- Bezier curves with draggable control points
- Undo and redo support
- Save canvas as image file
- Color palette with RGB color picker
- Adjustable brush size, line width, opacity and other tool settings
- Brush tool with circle and spray modes
- Eraser with adjustable opacity (blends toward background)
- Mandala tool with radial symmetry
- Archimedean spiral drawing
- Select box with rotate, flip and scale transforms


## How to Run

Make sure you have Python 3 and Pygame installed.

```
pip install pygame
```

Then run:

```
python pynter.py
```


## Controls

- Scroll wheel to adjust size/width for most tools
- Shift + Scroll for secondary settings (spray density, eraser opacity, etc.)
- Tab to switch brush type (circle/spray)
- Ctrl+Z to undo, Ctrl+Y to redo
- Right click to show a size-preview outline (pencil, brush, eraser)


## Project Structure

```
├── 📁 pynter
│   ├── 📁 tools
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 brush_tool.py
│   │   ├── 🐍 circle_tool.py
│   │   ├── 🐍 curve_tool.py
│   │   ├── 🐍 ellipse_tool.py
│   │   ├── 🐍 eraser_tool.py
│   │   ├── 🐍 eyedropper_tool.py
│   │   ├── 🐍 fill_tool.py
│   │   ├── 🐍 hypnotiser_tool.py
│   │   ├── 🐍 line_tool.py
│   │   ├── 🐍 magnifier_tool.py
│   │   ├── 🐍 mandala_tool.py
│   │   ├── 🐍 pencil_tool.py
│   │   ├── 🐍 rectangle_tool.py
│   │   ├── 🐍 select_box_tool.py
│   │   ├── 🐍 spiral_tool.py
│   │   ├── 🐍 square_tool.py
│   │   ├── 🐍 text_tool.py
│   │   ├── 🐍 tool.py
│   │   └── 🐍 triangle_tool.py
│   ├── 🐍 __init__.py
│   ├── 🐍 bitmap.py
│   ├── 🐍 canvas.py
│   ├── 🐍 color_select.py
│   ├── 🐍 globals.py
│   ├── 📄 icon.ico
│   ├── 🐍 main_window.py
│   └── 🐍 tool_select.py
├── ⚙️ .gitignore
├── 📝 README.md
├── 📄 icon.ico
└── 🐍 pynter.py
```


## Requirements

- Python 3.10+
- Pygame 2.x

---
Based on [Pixel-Craft](https://github.com/Fiesty-Cushion/Pixel-Craft)
