# tetsuo.ai 
# generated with Grok3 
# $TETSUO on Solana
# CA: 8i51XNNpGaKaj4G4nDdmQh95v4FKAxw8mhtaRoKd9tE8

import pygame
import sys
import colorsys
import math
import os
import random
from pygame import gfxdraw
from datetime import datetime

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grok3 Mogs")
icon = pygame.Surface((32, 32))
icon.fill((50, 50, 150))
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# UI Colors
UI_BG = (30, 30, 40)
UI_ACCENT = (60, 100, 170)
UI_HIGHLIGHT = (80, 120, 200)
UI_TEXT = (240, 240, 240)
UI_BUTTON = (50, 60, 80)
UI_BUTTON_HOVER = (70, 80, 100)
UI_PANEL = (40, 45, 55)
UI_BORDER = (80, 85, 95)

# UI Layout Constants
SIDEBAR_WIDTH = 280
TOOLBAR_HEIGHT = 50
BOTTOM_HEIGHT = 70
PADDING = 10
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 30
SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT = 60, 25
COLOR_PANEL_HEIGHT = 180

# Initial settings
current_color = BLACK
secondary_color = WHITE
brush_size = 5
opacity = 255
tool = "brush"
drawing = False
start_pos = None
last_pos = None
canvas_size = (WIDTH - SIDEBAR_WIDTH - 20, HEIGHT -
               TOOLBAR_HEIGHT - BOTTOM_HEIGHT - 20)
canvas = pygame.Surface(canvas_size)
canvas.fill(WHITE)
layers = [canvas.copy()]
current_layer = 0
undo_stack = [layers.copy()]
redo_stack = []
grid_snap = False
grid_size = 20
show_rulers = True
zoom_level = 1.0
canvas_offset = [0, 0]
canvas_drag = False
canvas_drag_start = None
selection = None
selection_surface = None
selection_start = None
symmetry_enabled = False
symmetry_points = []
symmetry_mode = "horizontal"  # horizontal, vertical, radial
brush_hardness = 1.0  # 0.0 to 1.0
texture_brush = None
custom_brushes = []
custom_patterns = []
color_history = []
autosave_enabled = True
autosave_interval = 300  # seconds
last_autosave_time = pygame.time.get_ticks()
project_name = "Untitled"
filters = {"grayscale": False, "invert": False, "blur": False}
shape_points = []
preview_surface = None

# Create directories if they don't exist
for directory in ["brushes", "patterns", "projects"]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create custom brush


def create_custom_brush(size, hardness, shape="circle"):
    brush = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    if shape == "circle":
        for x in range(size * 2):
            for y in range(size * 2):
                distance = math.sqrt((x - size) ** 2 + (y - size) ** 2)
                if distance <= size:
                    alpha = 255 * (1 - distance /
                                   size) ** hardness if distance > 0 else 255
                    brush.set_at((x, y), (255, 255, 255, int(alpha)))
    elif shape == "square":
        square_size = size * 2 * hardness
        offset = (size * 2 - square_size) // 2
        pygame.draw.rect(brush, (255, 255, 255, 255),
                         (offset, offset, square_size, square_size))
    return brush


# Fonts
font = pygame.font.SysFont("Arial", 16, bold=True)
small_font = pygame.font.SysFont("Arial", 12)
large_font = pygame.font.SysFont("Arial", 24, bold=True)
title_font = pygame.font.SysFont("Arial", 18, bold=True)

# UI Elements
canvas_view_rect = pygame.Rect(SIDEBAR_WIDTH + 10, TOOLBAR_HEIGHT + 10,
                               WIDTH - SIDEBAR_WIDTH - 20, HEIGHT - TOOLBAR_HEIGHT - BOTTOM_HEIGHT - 20)
canvas_rect = pygame.Rect(0, 0, canvas_size[0], canvas_size[1])
sidebar_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, HEIGHT)
toolbar_rect = pygame.Rect(SIDEBAR_WIDTH, 0, WIDTH -
                           SIDEBAR_WIDTH, TOOLBAR_HEIGHT)
bottom_rect = pygame.Rect(0, HEIGHT - BOTTOM_HEIGHT, WIDTH, BOTTOM_HEIGHT)
color_panel_rect = pygame.Rect(
    PADDING, PADDING, SIDEBAR_WIDTH - 2 * PADDING, COLOR_PANEL_HEIGHT)
color_picker = pygame.Rect(PADDING * 2, PADDING *
                           3 + 30, SIDEBAR_WIDTH - 4 * PADDING, 120)
color_preview_primary = pygame.Rect(PADDING * 2, PADDING * 4 + 160, 40, 40)
color_preview_secondary = pygame.Rect(
    PADDING * 2 + 45, PADDING * 4 + 160, 40, 40)
color_history_rect = pygame.Rect(
    PADDING * 2 + 90, PADDING * 4 + 160, SIDEBAR_WIDTH - PADDING * 4 - 90, 40)

# Tool panels
panels = {
    "tools": {
        "rect": pygame.Rect(PADDING, COLOR_PANEL_HEIGHT + PADDING * 2 + 30, SIDEBAR_WIDTH - 2 * PADDING, 200),
        "title": "Drawing Tools",
        "buttons": {}
    },
    "shapes": {
        "rect": pygame.Rect(PADDING, COLOR_PANEL_HEIGHT + PADDING * 3 + 240, SIDEBAR_WIDTH - 2 * PADDING, 160),
        "title": "Shapes",
        "buttons": {}
    },
    "effects": {
        "rect": pygame.Rect(PADDING, COLOR_PANEL_HEIGHT + PADDING * 4 + 410, SIDEBAR_WIDTH - 2 * PADDING, 160),
        "title": "Effects & Filters",
        "buttons": {}
    }
}

# Ensure panels fit within the sidebar height
total_panels_height = (COLOR_PANEL_HEIGHT + PADDING * 5 + 30 + 240 + 160 + 410)
if total_panels_height > HEIGHT:
    # Adjust panel heights to fit
    excess_height = total_panels_height - HEIGHT + PADDING
    panels["tools"]["rect"].height -= excess_height // 3
    panels["shapes"]["rect"].height -= excess_height // 3
    panels["effects"]["rect"].height -= excess_height // 3

    # Recalculate positions
    panels["shapes"]["rect"].y = COLOR_PANEL_HEIGHT + \
        PADDING * 3 + 30 + panels["tools"]["rect"].height
    panels["effects"]["rect"].y = panels["shapes"]["rect"].y + \
        panels["shapes"]["rect"].height + PADDING

# Tool buttons
tool_buttons = {
    "brush": {"panel": "tools", "row": 0, "col": 0, "icon": "🖌️"},
    "eraser": {"panel": "tools", "row": 0, "col": 1, "icon": "🧽"},
    "eyedropper": {"panel": "tools", "row": 0, "col": 2, "icon": "👁️"},
    "fill": {"panel": "tools", "row": 1, "col": 0, "icon": "🪣"},
    "line": {"panel": "tools", "row": 1, "col": 1, "icon": "📏"},
    "spray": {"panel": "tools", "row": 1, "col": 2, "icon": "💨"},
    "text": {"panel": "tools", "row": 2, "col": 0, "icon": "🔤"},
    "select": {"panel": "tools", "row": 2, "col": 1, "icon": "✂️"},
    "move": {"panel": "tools", "row": 2, "col": 2, "icon": "👆"},
    "gradient": {"panel": "tools", "row": 3, "col": 0, "icon": "🌈"},
    "stamp": {"panel": "tools", "row": 3, "col": 1, "icon": "🔖"},
    "smudge": {"panel": "tools", "row": 3, "col": 2, "icon": "👋"},
}

# Shape buttons
shape_buttons = {
    "rect": {"panel": "shapes", "row": 0, "col": 0, "icon": "▭"},
    "filled_rect": {"panel": "shapes", "row": 0, "col": 1, "icon": "■"},
    "ellipse": {"panel": "shapes", "row": 0, "col": 2, "icon": "⬭"},
    "filled_ellipse": {"panel": "shapes", "row": 1, "col": 0, "icon": "●"},
    "polygon": {"panel": "shapes", "row": 1, "col": 1, "icon": "⬡"},
    "filled_polygon": {"panel": "shapes", "row": 1, "col": 2, "icon": "⬢"},
    "star": {"panel": "shapes", "row": 2, "col": 0, "icon": "★"},
    "heart": {"panel": "shapes", "row": 2, "col": 1, "icon": "♥"},
    "arrow": {"panel": "shapes", "row": 2, "col": 2, "icon": "➜"},
}

# Effect buttons
effect_buttons = {
    "blur": {"panel": "effects", "row": 0, "col": 0, "icon": "🌫️"},
    "sharpen": {"panel": "effects", "row": 0, "col": 1, "icon": "✨"},
    "grayscale": {"panel": "effects", "row": 0, "col": 2, "icon": "⚪"},
    "invert": {"panel": "effects", "row": 1, "col": 0, "icon": "🔄"},
    "pixelate": {"panel": "effects", "row": 1, "col": 1, "icon": "🔲"},
    "symmetry": {"panel": "effects", "row": 1, "col": 2, "icon": "📐"},
    "grid": {"panel": "effects", "row": 2, "col": 0, "icon": "🔳"},
    "rulers": {"panel": "effects", "row": 2, "col": 1, "icon": "📊"},
    "snap": {"panel": "effects", "row": 2, "col": 2, "icon": "🧲"},
}

# Toolbar buttons (spaced evenly across the toolbar)
button_spacing = (WIDTH - SIDEBAR_WIDTH -
                  (5 * BUTTON_WIDTH + 3 * SMALL_BUTTON_WIDTH)) // 10
toolbar_buttons = {
    "new": pygame.Rect(SIDEBAR_WIDTH + button_spacing, PADDING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "open": pygame.Rect(SIDEBAR_WIDTH + button_spacing * 2 + BUTTON_WIDTH, PADDING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "save": pygame.Rect(SIDEBAR_WIDTH + button_spacing * 3 + BUTTON_WIDTH * 2, PADDING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "export": pygame.Rect(SIDEBAR_WIDTH + button_spacing * 4 + BUTTON_WIDTH * 3, PADDING, BUTTON_WIDTH, BUTTON_HEIGHT),
    "undo": pygame.Rect(SIDEBAR_WIDTH + button_spacing * 5 + BUTTON_WIDTH * 4, PADDING, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT),
    "redo": pygame.Rect(SIDEBAR_WIDTH + button_spacing * 6 + BUTTON_WIDTH * 4 + SMALL_BUTTON_WIDTH, PADDING, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT),
    "zoom_in": pygame.Rect(WIDTH - button_spacing * 3 - SMALL_BUTTON_WIDTH * 3, PADDING, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT),
    "zoom_out": pygame.Rect(WIDTH - button_spacing * 2 - SMALL_BUTTON_WIDTH * 2, PADDING, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT),
    "zoom_reset": pygame.Rect(WIDTH - button_spacing - SMALL_BUTTON_WIDTH, PADDING, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Bottom bar - layer controls and sliders (evenly distributed)
layer_button_spacing = PADDING
layer_buttons = {
    "new": pygame.Rect(PADDING, HEIGHT - BOTTOM_HEIGHT + PADDING, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT),
    "delete": pygame.Rect(PADDING * 2 + SMALL_BUTTON_WIDTH, HEIGHT - BOTTOM_HEIGHT + PADDING, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT),
    "up": pygame.Rect(PADDING * 3 + SMALL_BUTTON_WIDTH * 2, HEIGHT - BOTTOM_HEIGHT + PADDING, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT),
    "down": pygame.Rect(PADDING * 4 + SMALL_BUTTON_WIDTH * 3, HEIGHT - BOTTOM_HEIGHT + PADDING, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT),
    "merge": pygame.Rect(PADDING * 5 + SMALL_BUTTON_WIDTH * 4, HEIGHT - BOTTOM_HEIGHT + PADDING, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT),
    "duplicate": pygame.Rect(PADDING * 6 + SMALL_BUTTON_WIDTH * 5, HEIGHT - BOTTOM_HEIGHT + PADDING, SMALL_BUTTON_WIDTH, SMALL_BUTTON_HEIGHT),
}

# Evenly space sliders in the remaining width
slider_width = (WIDTH - SIDEBAR_WIDTH - PADDING * 7) // 3
sliders = {
    "size": pygame.Rect(SIDEBAR_WIDTH + PADDING, HEIGHT - BOTTOM_HEIGHT + PADDING, slider_width, 20),
    "opacity": pygame.Rect(SIDEBAR_WIDTH + PADDING * 3 + slider_width, HEIGHT - BOTTOM_HEIGHT + PADDING, slider_width, 20),
    "hardness": pygame.Rect(SIDEBAR_WIDTH + PADDING * 5 + slider_width * 2, HEIGHT - BOTTOM_HEIGHT + PADDING, slider_width, 20),
}

# Initialize button rects for tools, shapes, and effects


def init_button_rects():
    for panel_name, panel_info in panels.items():
        panel_rect = panel_info["rect"]
        button_width = (panel_rect.width - PADDING * 4) // 3
        button_height = 40

        # Determine how many rows can fit in the panel
        max_rows = (panel_rect.height - PADDING * 2 -
                    20) // (button_height + PADDING)

        # Assign buttons to the panel
        button_dict = {}
        if panel_name == "tools":
            button_dict = tool_buttons
        elif panel_name == "shapes":
            button_dict = shape_buttons
        elif panel_name == "effects":
            button_dict = effect_buttons

        # Position each button
        for button_name, button_info in button_dict.items():
            if button_info["panel"] == panel_name:
                row, col = button_info["row"], button_info["col"]

                # Skip if the row doesn't fit
                if row >= max_rows:
                    continue

                x = panel_rect.x + PADDING + col * (button_width + PADDING)
                y = panel_rect.y + PADDING * 2 + 20 + \
                    row * (button_height + PADDING)
                button_dict[button_name]["rect"] = pygame.Rect(
                    x, y, button_width, button_height)


init_button_rects()

# Functions


def add_to_color_history(color):
    if color not in color_history:
        color_history.insert(0, color)
        if len(color_history) > 10:
            color_history.pop()


def draw_gradient(surface, rect, color1, color2, vertical=True):
    for i in range(rect.height if vertical else rect.width):
        ratio = i / (rect.height if vertical else rect.width)
        color = tuple(int(c1 + (c2 - c1) * ratio)
                      for c1, c2 in zip(color1, color2))
        if vertical:
            pygame.draw.line(surface, color, (rect.x, rect.y + i),
                             (rect.x + rect.width, rect.y + i))
        else:
            pygame.draw.line(surface, color, (rect.x + i, rect.y),
                             (rect.x + i, rect.y + rect.height))


def draw_rounded_rect(surface, rect, color, radius=10, border=0, border_color=None):
    if border_color is None:
        border_color = color

    if border > 0:
        pygame.draw.rect(surface, border_color, rect, border_radius=radius)
        inner_rect = pygame.Rect(
            rect.x + border, rect.y + border, rect.width - 2*border, rect.height - 2*border)
        pygame.draw.rect(surface, color, inner_rect,
                         border_radius=radius-border)
    else:
        pygame.draw.rect(surface, color, rect, border_radius=radius)


def apply_filters(surface, filters):
    # Handle individual filter application
    if "grayscale" in filters and filters["grayscale"]:
        try:
            pixels = pygame.surfarray.pixels3d(surface)
            avg = pixels.mean(axis=2)
            pixels[:, :, 0] = avg
            pixels[:, :, 1] = avg
            pixels[:, :, 2] = avg
            del pixels
        except ValueError:
            # Surface is likely empty or has an unsupported format
            pass

    if "invert" in filters and filters["invert"]:
        try:
            pixels = pygame.surfarray.pixels3d(surface)
            pixels[:, :] = 255 - pixels
            del pixels
        except ValueError:
            pass

    if "blur" in filters and filters["blur"]:
        # Simple box blur
        blurred = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        blur_size = 3
        for x in range(blur_size, surface.get_width() - blur_size):
            for y in range(blur_size, surface.get_height() - blur_size):
                r, g, b, a = 0, 0, 0, 0
                count = 0
                for bx in range(-blur_size, blur_size + 1):
                    for by in range(-blur_size, blur_size + 1):
                        try:
                            pixel = surface.get_at((x + bx, y + by))
                            r += pixel[0]
                            g += pixel[1]
                            b += pixel[2]
                            a += pixel[3]
                            count += 1
                        except:
                            pass
                if count > 0:  # Avoid division by zero
                    blurred.set_at(
                        (x, y), (r // count, g // count, b // count, a // count))
        surface.blit(blurred, (0, 0))

    # Handle "sharpen" filter if it exists
    if "sharpen" in filters and filters["sharpen"]:
        # Simple sharpening filter
        try:
            kernel = [[-1, -1, -1],
                      [-1,  9, -1],
                      [-1, -1, -1]]

            original = surface.copy()
            for x in range(1, surface.get_width() - 1):
                for y in range(1, surface.get_height() - 1):
                    r, g, b, a = 0, 0, 0, 0
                    for ky in range(3):
                        for kx in range(3):
                            try:
                                pixel = original.get_at(
                                    (x + kx - 1, y + ky - 1))
                                r += pixel[0] * kernel[ky][kx]
                                g += pixel[1] * kernel[ky][kx]
                                b += pixel[2] * kernel[ky][kx]
                                a += pixel[3]
                            except:
                                pass
                    r = max(0, min(255, r))
                    g = max(0, min(255, g))
                    b = max(0, min(255, b))
                    a = a // 9  # Average alpha
                    surface.set_at((x, y), (r, g, b, a))
        except Exception as e:
            print(f"Error applying sharpen filter: {e}")

    # Handle "pixelate" filter if it exists
    if "pixelate" in filters and filters["pixelate"]:
        try:
            pixel_size = 8
            width, height = surface.get_size()

            # Create a smaller surface
            small_surface = pygame.transform.scale(
                surface,
                (width // pixel_size, height // pixel_size)
            )

            # Scale it back up
            pixelated = pygame.transform.scale(
                small_surface,
                (width, height)
            )

            # Replace the content
            surface.blit(pixelated, (0, 0))
        except Exception as e:
            print(f"Error applying pixelate filter: {e}")


def fill_area(surface, pos, fill_color, target_color, tolerance=10):
    width, height = surface.get_size()
    stack = [pos]
    processed = set()

    while stack:
        x, y = stack.pop()
        if (x, y) in processed or x < 0 or y < 0 or x >= width or y >= height:
            continue

        try:
            current_color = surface.get_at((x, y))
            color_diff = sum(abs(a - b)
                             for a, b in zip(current_color[:3], target_color[:3]))

            if color_diff > tolerance:
                continue

            surface.set_at((x, y), fill_color)
            processed.add((x, y))

            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))
        except IndexError:
            # Skip invalid coordinates
            continue


def spray_paint(surface, pos, color, size, density):
    x, y = pos
    points = []
    for _ in range(density):
        angle = random.random() * 2 * math.pi
        distance = random.random() * size
        px = int(x + math.cos(angle) * distance)
        py = int(y + math.sin(angle) * distance)
        if 0 <= px < surface.get_width() and 0 <= py < surface.get_height():
            points.append((px, py))

    for point in points:
        surface.set_at(point, color)


def draw_with_symmetry(surface, pos, start_pos, tool, color, size, symmetry_mode):
    width, height = surface.get_size()
    center_x, center_y = width // 2, height // 2

    if symmetry_mode == "horizontal":
        mirror_y = pos[1]
        mirror_x = 2 * center_x - pos[0]
        mirror_start_y = start_pos[1] if start_pos else mirror_y
        mirror_start_x = 2 * center_x - start_pos[0] if start_pos else mirror_x

        if tool == "brush":
            pygame.draw.line(surface, color, pos,
                             start_pos if start_pos else pos, size)
            pygame.draw.line(surface, color, (mirror_x, mirror_y),
                             (mirror_start_x, mirror_start_y), size)

    elif symmetry_mode == "vertical":
        mirror_x = pos[0]
        mirror_y = 2 * center_y - pos[1]
        mirror_start_x = start_pos[0] if start_pos else mirror_x
        mirror_start_y = 2 * center_y - start_pos[1] if start_pos else mirror_y

        if tool == "brush":
            pygame.draw.line(surface, color, pos,
                             start_pos if start_pos else pos, size)
            pygame.draw.line(surface, color, (mirror_x, mirror_y),
                             (mirror_start_x, mirror_start_y), size)

    elif symmetry_mode == "radial":
        # Calculate angle and distance from center
        dx, dy = pos[0] - center_x, pos[1] - center_y
        distance = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)

        # Draw multiple points in a circular pattern
        num_points = 8
        for i in range(num_points):
            new_angle = angle + (2 * math.pi * i / num_points)
            x = center_x + math.cos(new_angle) * distance
            y = center_y + math.sin(new_angle) * distance

            if start_pos:
                start_dx, start_dy = start_pos[0] - \
                    center_x, start_pos[1] - center_y
                start_distance = math.sqrt(
                    start_dx*start_dx + start_dy*start_dy)
                start_angle = math.atan2(start_dy, start_dx)
                start_x = center_x + \
                    math.cos(start_angle + (2 * math.pi *
                             i / num_points)) * start_distance
                start_y = center_y + \
                    math.sin(start_angle + (2 * math.pi *
                             i / num_points)) * start_distance
            else:
                start_x, start_y = x, y

            if tool == "brush":
                pygame.draw.line(surface, color, (int(x), int(y)),
                                 (int(start_x), int(start_y)), size)


def draw_polygon(surface, points, color, filled=False, width=1):
    if len(points) < 3:
        return

    if filled:
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.polygon(surface, color, points, width)


def draw_star(surface, center, outer_radius, inner_radius, points, color, filled=False, width=1):
    angle = -math.pi / 2  # Start at top
    step = math.pi / points
    vertices = []

    for i in range(points * 2):
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
        angle += step

    if filled:
        pygame.draw.polygon(surface, color, vertices)
    else:
        pygame.draw.polygon(surface, color, vertices, width)


def draw_heart(surface, center, size, color, filled=False, width=1):
    x, y = center
    points = []

    for angle in range(0, 360, 5):
        rad = math.radians(angle)
        # Heart curve formula
        px = x + size * 16 * math.sin(rad) ** 3
        py = y - size * (13 * math.cos(rad) - 5 * math.cos(2 *
                         rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad))
        points.append((px, py))

    if filled:
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.polygon(surface, color, points, width)


def draw_arrow(surface, start, end, color, width=1, arrow_size=10):
    pygame.draw.line(surface, color, start, end, width)

    # Calculate the arrow head
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    x1 = end[0] - arrow_size * math.cos(angle - math.pi/6)
    y1 = end[1] - arrow_size * math.sin(angle - math.pi/6)
    x2 = end[0] - arrow_size * math.cos(angle + math.pi/6)
    y2 = end[1] - arrow_size * math.sin(angle + math.pi/6)

    pygame.draw.polygon(
        surface, color, [(end[0], end[1]), (int(x1), int(y1)), (int(x2), int(y2))])


def save_project(filename, layers, canvas_size):
    # Create a directory for this project
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_dir = f"projects/{project_name}_{timestamp}"

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    # Save each layer as a separate image
    project_data = {
        "layers": [],
        "canvas_size": canvas_size
    }

    for i, layer in enumerate(layers):
        layer_filename = f"{project_dir}/layer_{i}.png"
        pygame.image.save(layer, layer_filename)
        project_data["layers"].append(layer_filename)

    # Save project metadata
    with open(f"{project_dir}/project.txt", "w") as f:
        f.write(f"canvas_size: {canvas_size[0]},{canvas_size[1]}\n")
        f.write(f"layers: {len(layers)}\n")
        for i, layer_file in enumerate(project_data["layers"]):
            f.write(f"layer_{i}: {layer_file}\n")

    return f"{project_dir}/project.txt"


def load_project(filename):
    layers = []
    canvas_size = None

    try:
        if not os.path.exists(filename):
            print(f"Project file does not exist: {filename}")
            return None, None

        with open(filename, "r") as f:
            lines = f.readlines()

            for line in lines:
                if line.startswith("canvas_size:"):
                    size_str = line.split(":")[1].strip()
                    width, height = map(int, size_str.split(","))
                    canvas_size = (width, height)
                elif line.startswith("layer_"):
                    layer_file = line.split(":")[1].strip()
                    if os.path.exists(layer_file):
                        layer = pygame.image.load(layer_file).convert_alpha()
                        layers.append(layer)

        if not layers or not canvas_size:
            print("Invalid project file: missing layers or canvas size")
            return None, None

        return layers, canvas_size
    except Exception as e:
        print(f"Error loading project: {e}")
        return None, None


def export_image(layers, filename, format="png"):
    # Create a composite image from all layers
    composite = pygame.Surface(layers[0].get_size(), pygame.SRCALPHA)
    for layer in layers:
        composite.blit(layer, (0, 0))

    # Save in the specified format
    pygame.image.save(composite, f"{filename}.{format}")
    print(f"Exported as '{filename}.{format}'")


def autosave():
    global last_autosave_time
    current_time = pygame.time.get_ticks()
    if autosave_enabled and (current_time - last_autosave_time) > autosave_interval * 1000:
        save_project(f"projects/autosave_{project_name}", layers, canvas_size)
        last_autosave_time = current_time
        print(f"Auto-saved at {datetime.now().strftime('%H:%M:%S')}")


# Main game loop
running = True
clock = pygame.time.Clock()
hover_button = None
text_input = ""
text_active = False
drawing_shape = False
current_shape = None

# Create custom brushes
custom_brush = create_custom_brush(brush_size, brush_hardness)

# Add initial color to history
add_to_color_history(current_color)

while running:
    mouse_pos = pygame.mouse.get_pos()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if we're clicking in the canvas view area
            if canvas_view_rect.collidepoint(mouse_pos):
                # Convert mouse position to canvas coordinates with zoom
                canvas_x = (mouse_pos[0] - canvas_view_rect.x) / \
                    zoom_level - canvas_offset[0]
                canvas_y = (mouse_pos[1] - canvas_view_rect.y) / \
                    zoom_level - canvas_offset[1]
                canvas_mouse_pos = (int(canvas_x), int(canvas_y))

                # Middle mouse button for panning
                if event.button == 2:
                    canvas_drag = True
                    canvas_drag_start = mouse_pos
                # Left mouse button for drawing
                elif event.button == 1:
                    if 0 <= canvas_x < canvas_size[0] and 0 <= canvas_y < canvas_size[1]:
                        if tool == "eyedropper":
                            # Create a composite of all layers up to the current one
                            composite = pygame.Surface(
                                canvas_size, pygame.SRCALPHA)
                            for i, layer in enumerate(layers):
                                if i <= current_layer:
                                    composite.blit(layer, (0, 0))

                            # Get the color at the mouse position
                            try:
                                picked_color = composite.get_at(
                                    (int(canvas_x), int(canvas_y)))
                                current_color = picked_color[:3]
                                add_to_color_history(current_color)
                            except IndexError:
                                pass
                        elif tool == "select":
                            # Start selection
                            selection_start = (int(canvas_x), int(canvas_y))
                            selection = None
                            drawing = True
                        elif tool == "fill":
                            # Get the target color
                            target_color = layers[current_layer].get_at(
                                (int(canvas_x), int(canvas_y)))
                            fill_color = current_color + (opacity,)
                            fill_area(layers[current_layer], (int(canvas_x), int(
                                canvas_y)), fill_color, target_color)
                        elif tool in shape_buttons or current_shape is not None:
                            # Start drawing a shape
                            start_pos = (int(canvas_x), int(canvas_y))
                            if grid_snap:
                                start_pos = (start_pos[0] - start_pos[0] % grid_size,
                                             start_pos[1] - start_pos[1] % grid_size)
                            drawing = True
                            drawing_shape = True
                            if tool in shape_buttons:
                                current_shape = tool
                            shape_points = [start_pos]
                            preview_surface = pygame.Surface(
                                canvas_size, pygame.SRCALPHA)
                        elif tool == "text":
                            # Start text input
                            start_pos = (int(canvas_x), int(canvas_y))
                            text_active = True
                            text_input = ""
                        else:
                            # Start drawing with other tools
                            drawing = True
                            start_pos = last_pos = (
                                int(canvas_x), int(canvas_y))
                            if grid_snap:
                                start_pos = last_pos = (start_pos[0] - start_pos[0] % grid_size,
                                                        start_pos[1] - start_pos[1] % grid_size)

                # Right click to cancel current action or use secondary color
                elif event.button == 3:
                    if drawing_shape and (tool == "polygon" or tool == "filled_polygon"):
                        # Complete polygon with right click
                        if len(shape_points) >= 3:
                            color_with_opacity = current_color + (opacity,)
                            if tool == "polygon":
                                pygame.draw.polygon(
                                    layers[current_layer], color_with_opacity, shape_points, brush_size)
                            else:  # filled_polygon
                                pygame.draw.polygon(
                                    layers[current_layer], color_with_opacity, shape_points)
                        drawing_shape = False
                        current_shape = None
                        shape_points = []
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []
                    else:
                        # Swap primary and secondary colors
                        current_color, secondary_color = secondary_color, current_color

            # Color picker click
            elif color_picker.collidepoint(mouse_pos):
                rel_x, rel_y = mouse_pos[0] - \
                    color_picker.x, mouse_pos[1] - color_picker.y
                hue = rel_x / color_picker.width
                sat = 1 - rel_y / color_picker.height
                rgb = colorsys.hsv_to_rgb(hue, sat, 1)
                current_color = tuple(int(c * 255) for c in rgb)
                add_to_color_history(current_color)

            # Color history click
            elif color_history_rect.collidepoint(mouse_pos):
                rel_x = mouse_pos[0] - color_history_rect.x
                if len(color_history) > 0:  # Make sure color history is not empty
                    idx = min(int(rel_x // (color_history_rect.width /
                              min(10, len(color_history)))), len(color_history) - 1)
                    if 0 <= idx < len(color_history):
                        if event.button == 1:  # Left click - set primary color
                            current_color = color_history[idx]
                        elif event.button == 3:  # Right click - set secondary color
                            secondary_color = color_history[idx]

            # Color preview clicks
            elif color_preview_primary.collidepoint(mouse_pos):
                if event.button == 3:  # Right click - swap colors
                    current_color, secondary_color = secondary_color, current_color
            elif color_preview_secondary.collidepoint(mouse_pos):
                if event.button == 1:  # Left click - swap colors
                    current_color, secondary_color = secondary_color, current_color

            # Tool and shape buttons
            for name, info in tool_buttons.items():
                if "rect" in info and info["rect"].collidepoint(mouse_pos):
                    tool = name
                    current_shape = None
                    drawing_shape = False
                    # If eyedropper is selected, change cursor
                    if tool == "eyedropper":
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for name, info in shape_buttons.items():
                if "rect" in info and info["rect"].collidepoint(mouse_pos):
                    tool = name
                    current_shape = name
                    drawing_shape = False

            for name, info in effect_buttons.items():
                if "rect" in info and info["rect"].collidepoint(mouse_pos):
                    if name in filters:
                        filters[name] = not filters[name]
                    elif name == "symmetry":
                        symmetry_enabled = not symmetry_enabled
                        if symmetry_enabled:
                            # Cycle through symmetry modes
                            if symmetry_mode == "horizontal":
                                symmetry_mode = "vertical"
                            elif symmetry_mode == "vertical":
                                symmetry_mode = "radial"
                            else:
                                symmetry_mode = "horizontal"
                    elif name == "grid":
                        grid_snap = not grid_snap
                    elif name == "rulers":
                        show_rulers = not show_rulers
                    # Apply effects
                    if name in ["blur", "sharpen", "grayscale", "invert", "pixelate"]:
                        apply_filters(layers[current_layer], {name: True})
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []

            # Layer buttons
            for name, rect in layer_buttons.items():
                if rect.collidepoint(mouse_pos):
                    if name == "new":
                        new_layer = pygame.Surface(
                            canvas_size, pygame.SRCALPHA)
                        new_layer.fill((0, 0, 0, 0))
                        layers.append(new_layer)
                        current_layer = len(layers) - 1
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []
                    elif name == "delete" and len(layers) > 1:
                        layers.pop(current_layer)
                        current_layer = max(0, current_layer - 1)
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []
                    elif name == "up" and current_layer < len(layers) - 1:
                        layers[current_layer], layers[current_layer +
                                                      1] = layers[current_layer + 1], layers[current_layer]
                        current_layer += 1
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []
                    elif name == "down" and current_layer > 0:
                        layers[current_layer], layers[current_layer -
                                                      1] = layers[current_layer - 1], layers[current_layer]
                        current_layer -= 1
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []
                    elif name == "merge" and current_layer > 0:
                        layers[current_layer -
                               1].blit(layers[current_layer], (0, 0))
                        layers.pop(current_layer)
                        current_layer -= 1
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []
                    elif name == "duplicate":
                        layers.insert(current_layer + 1,
                                      layers[current_layer].copy())
                        current_layer += 1
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []

            # Toolbar buttons
            for name, rect in toolbar_buttons.items():
                if rect.collidepoint(mouse_pos):
                    if name == "new":
                        for i in range(len(layers)):
                            layers[i] = pygame.Surface(
                                canvas_size, pygame.SRCALPHA)
                        layers[0].fill(WHITE)
                        for i in range(1, len(layers)):
                            layers[i].fill((0, 0, 0, 0))
                        undo_stack = [[l.copy() for l in layers]]
                        redo_stack = []
                    elif name == "open":
                        # Placeholder for file dialog - would use tkinter or similar in a real app
                        loaded_layers, loaded_size = load_project(
                            "projects/last_project.txt")
                        if loaded_layers and loaded_size:
                            layers = loaded_layers
                            canvas_size = loaded_size
                            canvas = pygame.Surface(canvas_size)
                            canvas_rect = pygame.Rect(
                                0, 0, canvas_size[0], canvas_size[1])
                            current_layer = 0
                            undo_stack = [[l.copy() for l in layers]]
                            redo_stack = []
                    elif name == "save":
                        project_file = save_project(
                            f"projects/{project_name}", layers, canvas_size)
                        print(f"Project saved as {project_file}")
                    elif name == "export":
                        export_image(layers, f"projects/{project_name}_export")
                    elif name == "undo" and len(undo_stack) > 1:
                        redo_stack.append([l.copy() for l in layers])
                        undo_stack.pop()
                        layers = [l.copy() for l in undo_stack[-1]]
                    elif name == "redo" and redo_stack:
                        undo_stack.append([l.copy() for l in layers])
                        layers = [l.copy() for l in redo_stack.pop()]
                    elif name == "zoom_in":
                        zoom_level = min(5.0, zoom_level * 1.2)
                    elif name == "zoom_out":
                        zoom_level = max(0.2, zoom_level / 1.2)
                    elif name == "zoom_reset":
                        zoom_level = 1.0
                        canvas_offset = [0, 0]

            # Sliders
            for s, rect in sliders.items():
                if rect.collidepoint(mouse_pos):
                    val_ratio = max(
                        0, min(1, (mouse_pos[0] - rect.x) / rect.width))
                    if s == "size":
                        brush_size = int(val_ratio * 100) + \
                            1  # Ensure minimum size of 1
                        # Recreate custom brush with new size
                        custom_brush = create_custom_brush(
                            brush_size, brush_hardness)
                    elif s == "opacity":
                        opacity = int(val_ratio * 255)
                    elif s == "hardness":
                        brush_hardness = val_ratio
                        # Recreate custom brush with new hardness
                        custom_brush = create_custom_brush(
                            brush_size, brush_hardness)

        # Mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False

                # Handle completed shapes
                if drawing_shape and current_shape and current_shape != "polygon" and current_shape != "filled_polygon":
                    drawing_shape = False

                    # Commit the preview to the layer
                    if preview_surface:
                        layers[current_layer].blit(preview_surface, (0, 0))
                        preview_surface = None

                    current_shape = None

                # Finalize selection
                if tool == "select" and selection_start:
                    canvas_x = (
                        mouse_pos[0] - canvas_view_rect.x) / zoom_level - canvas_offset[0]
                    canvas_y = (
                        mouse_pos[1] - canvas_view_rect.y) / zoom_level - canvas_offset[1]
                    end_pos = (int(canvas_x), int(canvas_y))

                    if selection_start != end_pos:
                        x1, y1 = min(selection_start[0], end_pos[0]), min(
                            selection_start[1], end_pos[1])
                        x2, y2 = max(selection_start[0], end_pos[0]), max(
                            selection_start[1], end_pos[1])
                        w, h = x2 - x1, y2 - y1

                        if w > 0 and h > 0:
                            selection = pygame.Rect(x1, y1, w, h)
                            # Create a copy of the selected area
                            selection_surface = pygame.Surface(
                                (w, h), pygame.SRCALPHA)
                            selection_surface.blit(
                                layers[current_layer], (0, 0), selection)

                # Add to undo stack
                undo_stack.append([l.copy() for l in layers])
                redo_stack = []

            # Stop canvas dragging
            elif event.button == 2:
                canvas_drag = False

        # Mouse movement
        elif event.type == pygame.MOUSEMOTION:
            # Pan the canvas with middle mouse button
            if canvas_drag:
                dx, dy = mouse_pos[0] - \
                    canvas_drag_start[0], mouse_pos[1] - canvas_drag_start[1]
                canvas_offset[0] += dx / zoom_level
                canvas_offset[1] += dy / zoom_level
                canvas_drag_start = mouse_pos

        # Key presses
        elif event.type == pygame.KEYDOWN:
            # Text input
            if text_active:
                if event.key == pygame.K_RETURN:
                    # Render text to layer
                    if text_input:
                        color_with_opacity = current_color + (opacity,)
                        text_surface = font.render(
                            text_input, True, color_with_opacity)
                        layers[current_layer].blit(text_surface, start_pos)
                        text_active = False
                        text_input = ""
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_input = ""
                else:
                    text_input += event.unicode
            else:
                # Tool shortcuts
                if event.key == pygame.K_b:
                    tool = "brush"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_g:
                    tool = "gradient"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_t:
                    tool = "text"
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Save with Ctrl+S
                    project_file = save_project(
                        f"projects/{project_name}", layers, canvas_size)
                    print(f"Project saved as {project_file}")
                elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Open with Ctrl+O
                    loaded_layers, loaded_size = load_project(
                        "projects/last_project.txt")
                    if loaded_layers and loaded_size:
                        layers = loaded_layers
                        canvas_size = loaded_size
                        canvas = pygame.Surface(canvas_size)
                        canvas_rect = pygame.Rect(
                            0, 0, canvas_size[0], canvas_size[1])
                        current_layer = 0
                        undo_stack = [[l.copy() for l in layers]]
                        redo_stack = []
                elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Undo with Ctrl+Z
                    if len(undo_stack) > 1:
                        redo_stack.append([l.copy() for l in layers])
                        undo_stack.pop()
                        layers = [l.copy() for l in undo_stack[-1]]
                elif event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Redo with Ctrl+Y
                    if redo_stack:
                        undo_stack.append([l.copy() for l in layers])
                        layers = [l.copy() for l in redo_stack.pop()]
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    # Delete selection
                    if selection:
                        layers[current_layer].fill((0, 0, 0, 0), selection)
                        selection = None
                        selection_surface = None
                        undo_stack.append([l.copy() for l in layers])
                        redo_stack = []
                # Toggle grid with G key
                elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    grid_snap = not grid_snap
                # Layer navigation
                elif event.key == pygame.K_PAGEUP:
                    current_layer = min(current_layer + 1, len(layers) - 1)
                elif event.key == pygame.K_PAGEDOWN:
                    current_layer = max(current_layer - 1, 0)

    # Active drawing
    if drawing and canvas_view_rect.collidepoint(mouse_pos):
        mouse_x, mouse_y = mouse_pos
        canvas_x = (mouse_x - canvas_view_rect.x) / \
            zoom_level - canvas_offset[0]
        canvas_y = (mouse_y - canvas_view_rect.y) / \
            zoom_level - canvas_offset[1]
        mouse_canvas_pos = (int(canvas_x), int(canvas_y))

        # Snap to grid if enabled
        if grid_snap:
            mouse_canvas_pos = (mouse_canvas_pos[0] - mouse_canvas_pos[0] % grid_size,
                                mouse_canvas_pos[1] - mouse_canvas_pos[1] % grid_size)

        # Check if inside canvas bounds
        if 0 <= mouse_canvas_pos[0] < canvas_size[0] and 0 <= mouse_canvas_pos[1] < canvas_size[1]:
            color_with_opacity = current_color + (opacity,)

            # Drawing with various tools
            if tool == "brush":
                if symmetry_enabled:
                    draw_with_symmetry(layers[current_layer], mouse_canvas_pos,
                                       last_pos, tool, color_with_opacity, brush_size, symmetry_mode)
                else:
                    if last_pos:
                        pygame.draw.line(
                            layers[current_layer], color_with_opacity, last_pos, mouse_canvas_pos, brush_size)
                    else:
                        pygame.draw.circle(
                            layers[current_layer], color_with_opacity, mouse_canvas_pos, brush_size // 2)
                last_pos = mouse_canvas_pos

            elif tool == "eraser":
                if last_pos:
                    # Use a transparent "color" for erasing
                    pygame.draw.line(
                        layers[current_layer], (0, 0, 0, 0), last_pos, mouse_canvas_pos, brush_size)
                else:
                    pygame.draw.circle(
                        layers[current_layer], (0, 0, 0, 0), mouse_canvas_pos, brush_size // 2)
                last_pos = mouse_canvas_pos

            elif tool == "line" and start_pos:
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                pygame.draw.line(preview_surface, color_with_opacity,
                                 start_pos, mouse_canvas_pos, brush_size)

            elif tool == "spray":
                spray_paint(layers[current_layer], mouse_canvas_pos,
                            color_with_opacity, brush_size * 2, int(brush_size * 0.8))
                last_pos = mouse_canvas_pos

            elif tool == "smudge" and last_pos:
                # Get the color at the start position and blend with surrounding pixels
                try:
                    base_color = layers[current_layer].get_at(start_pos)
                    for i in range(5):
                        blend_x = int(
                            last_pos[0] + (mouse_canvas_pos[0] - last_pos[0]) * (i / 5))
                        blend_y = int(
                            last_pos[1] + (mouse_canvas_pos[1] - last_pos[1]) * (i / 5))

                        # Add some randomness for a more natural smudge
                        blend_x += random.randint(-2, 2)
                        blend_y += random.randint(-2, 2)

                        if 0 <= blend_x < canvas_size[0] and 0 <= blend_y < canvas_size[1]:
                            try:
                                current_color = layers[current_layer].get_at(
                                    (blend_x, blend_y))
                                # Blend the colors
                                blend_color = tuple(
                                    int(base_color[j] * 0.8 + current_color[j] * 0.2) for j in range(4))
                                pygame.draw.circle(
                                    layers[current_layer], blend_color, (blend_x, blend_y), brush_size // 3)
                            except IndexError:
                                pass
                except IndexError:
                    pass

                last_pos = mouse_canvas_pos

            elif tool == "gradient" and start_pos:
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                rect = pygame.Rect(
                    min(start_pos[0], mouse_canvas_pos[0]),
                    min(start_pos[1], mouse_canvas_pos[1]),
                    abs(mouse_canvas_pos[0] - start_pos[0]),
                    abs(mouse_canvas_pos[1] - start_pos[1])
                )
                draw_gradient(preview_surface, rect, current_color +
                              (opacity,), secondary_color + (opacity,))

            elif tool == "select":
                # Update selection preview
                selection = pygame.Rect(
                    min(selection_start[0], mouse_canvas_pos[0]),
                    min(selection_start[1], mouse_canvas_pos[1]),
                    abs(mouse_canvas_pos[0] - selection_start[0]),
                    abs(mouse_canvas_pos[1] - selection_start[1])
                )

            # Shape tools
            elif tool == "rect" or current_shape == "rect":
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                rect = pygame.Rect(
                    min(start_pos[0], mouse_canvas_pos[0]),
                    min(start_pos[1], mouse_canvas_pos[1]),
                    abs(mouse_canvas_pos[0] - start_pos[0]),
                    abs(mouse_canvas_pos[1] - start_pos[1])
                )
                pygame.draw.rect(
                    preview_surface, color_with_opacity, rect, brush_size)

            elif tool == "filled_rect" or current_shape == "filled_rect":
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                rect = pygame.Rect(
                    min(start_pos[0], mouse_canvas_pos[0]),
                    min(start_pos[1], mouse_canvas_pos[1]),
                    abs(mouse_canvas_pos[0] - start_pos[0]),
                    abs(mouse_canvas_pos[1] - start_pos[1])
                )
                pygame.draw.rect(preview_surface, color_with_opacity, rect)

            elif tool == "ellipse" or current_shape == "ellipse":
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                rect = pygame.Rect(
                    min(start_pos[0], mouse_canvas_pos[0]),
                    min(start_pos[1], mouse_canvas_pos[1]),
                    abs(mouse_canvas_pos[0] - start_pos[0]),
                    abs(mouse_canvas_pos[1] - start_pos[1])
                )
                pygame.draw.ellipse(
                    preview_surface, color_with_opacity, rect, brush_size)

            elif tool == "filled_ellipse" or current_shape == "filled_ellipse":
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                rect = pygame.Rect(
                    min(start_pos[0], mouse_canvas_pos[0]),
                    min(start_pos[1], mouse_canvas_pos[1]),
                    abs(mouse_canvas_pos[0] - start_pos[0]),
                    abs(mouse_canvas_pos[1] - start_pos[1])
                )
                pygame.draw.ellipse(preview_surface, color_with_opacity, rect)

            elif (tool == "polygon" or current_shape == "polygon" or
                  tool == "filled_polygon" or current_shape == "filled_polygon"):
                if drawing_shape:
                    # Preview the polygon
                    preview_surface = pygame.Surface(
                        canvas_size, pygame.SRCALPHA)
                    points_plus_current = shape_points + [mouse_canvas_pos]
                    if len(points_plus_current) > 1:
                        pygame.draw.lines(
                            preview_surface, color_with_opacity, False, points_plus_current, brush_size)

            elif tool == "star" or current_shape == "star":
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                center = ((start_pos[0] + mouse_canvas_pos[0]) // 2,
                          (start_pos[1] + mouse_canvas_pos[1]) // 2)
                radius = int(math.sqrt((mouse_canvas_pos[0] - start_pos[0]) ** 2 +
                                       (mouse_canvas_pos[1] - start_pos[1]) ** 2) / 2)
                draw_star(preview_surface, center, radius, radius//2, 5, color_with_opacity,
                          (tool == "filled_star" or current_shape == "filled_star"), brush_size)

            elif tool == "heart" or current_shape == "heart":
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                center = ((start_pos[0] + mouse_canvas_pos[0]) // 2,
                          (start_pos[1] + mouse_canvas_pos[1]) // 2)
                size = int(math.sqrt((mouse_canvas_pos[0] - start_pos[0]) ** 2 +
                                     (mouse_canvas_pos[1] - start_pos[1]) ** 2) / 10)
                draw_heart(preview_surface, center, size,
                           color_with_opacity, False, brush_size)

            elif tool == "arrow" or current_shape == "arrow":
                # Preview on a temporary surface
                preview_surface = pygame.Surface(canvas_size, pygame.SRCALPHA)
                draw_arrow(preview_surface, start_pos,
                           mouse_canvas_pos, color_with_opacity, brush_size)

            # Move the selection if we have one
            elif tool == "move" and selection and selection_surface:
                # Move the selection
                selection.x = mouse_canvas_pos[0] - selection.width // 2
                selection.y = mouse_canvas_pos[1] - selection.height // 2
        else:
            last_pos = None
    else:
        last_pos = None

    # Finalize shape drawing when mouse button is released
    if not drawing and drawing_shape and tool != "polygon" and tool != "filled_polygon" and preview_surface:
        # Copy the preview to the layer
        layers[current_layer].blit(preview_surface, (0, 0))
        preview_surface = None

        # Add to undo stack
        undo_stack.append([l.copy() for l in layers])
        redo_stack = []

        drawing_shape = False

    # Autosave (check every frame but save only at interval)
    autosave()

    # Drawing the UI
    screen.fill(UI_BG)

    # Draw the canvas view with current zoom level
    zoomed_size = (int(canvas_size[0] * zoom_level),
                   int(canvas_size[1] * zoom_level))
    zoomed_pos = (canvas_view_rect.x + canvas_offset[0] * zoom_level,
                  canvas_view_rect.y + canvas_offset[1] * zoom_level)

    # Create a composite of all layers
    composite = pygame.Surface(canvas_size, pygame.SRCALPHA)
    for i, layer in enumerate(layers):
        # Draw a special border for the current layer
        if i == current_layer:
            # Just blend the layer
            composite.blit(layer, (0, 0))
        else:
            # Regular blend
            composite.blit(layer, (0, 0))

    # Add preview if applicable
    if drawing and preview_surface:
        composite.blit(preview_surface, (0, 0))

    # Draw selection outline
    if selection:
        pygame.draw.rect(composite, (255, 0, 0), selection, 1)

    # Show text input preview
    if text_active and text_input:
        text_surface = font.render(
            text_input, True, current_color + (opacity,))
        composite.blit(text_surface, start_pos)

    # Apply filters for preview
    if any(filters.values()):
        filter_preview = composite.copy()
        apply_filters(filter_preview, filters)
        composite = filter_preview

    # Draw checkerboard background for transparency
    for y in range(0, canvas_view_rect.height, 20):
        for x in range(0, canvas_view_rect.width, 20):
            color = LIGHT_GRAY if (x // 20 + y // 20) % 2 == 0 else WHITE
            pygame.draw.rect(
                screen, color, (canvas_view_rect.x + x, canvas_view_rect.y + y, 20, 20))

    # Create zoomed version of the composite
    try:
        zoomed_canvas = pygame.transform.scale(composite, zoomed_size)
        # Draw the zoomed canvas
        screen.blit(zoomed_canvas, zoomed_pos)
    except ValueError:
        # Handle error if canvas scaling fails
        print("Error scaling canvas - check canvas dimensions")

    # Draw canvas border
    pygame.draw.rect(screen, UI_BORDER, pygame.Rect(
        zoomed_pos[0], zoomed_pos[1], zoomed_size[0], zoomed_size[1]), 1)

    # Draw grid if enabled
    if grid_snap:
        grid_color = (100, 100, 120, 150)
        for x in range(0, canvas_size[0], grid_size):
            x_pos = int(zoomed_pos[0] + x * zoom_level)
            pygame.draw.line(screen, grid_color, (x_pos, zoomed_pos[1]),
                             (x_pos, zoomed_pos[1] + zoomed_size[1]), 1)
        for y in range(0, canvas_size[1], grid_size):
            y_pos = int(zoomed_pos[1] + y * zoom_level)
            pygame.draw.line(screen, grid_color, (zoomed_pos[0], y_pos),
                             (zoomed_pos[0] + zoomed_size[0], y_pos), 1)

    # Draw rulers if enabled
    if show_rulers:
        ruler_color = (80, 80, 100)
        ruler_size = 20

        # Horizontal ruler
        pygame.draw.rect(screen, UI_PANEL, (canvas_view_rect.x,
                         canvas_view_rect.y - ruler_size, zoomed_size[0], ruler_size))
        for x in range(0, canvas_size[0], 50):
            x_pos = int(zoomed_pos[0] + x * zoom_level)
            if x % 100 == 0:  # Major tick
                pygame.draw.line(screen, ruler_color, (x_pos, canvas_view_rect.y - ruler_size),
                                 (x_pos, canvas_view_rect.y), 1)
                text = small_font.render(str(x), True, UI_TEXT)
                screen.blit(
                    text, (x_pos + 2, canvas_view_rect.y - ruler_size + 2))
            else:  # Minor tick
                pygame.draw.line(screen, ruler_color, (x_pos, canvas_view_rect.y - ruler_size // 2),
                                 (x_pos, canvas_view_rect.y), 1)

        # Vertical ruler
        pygame.draw.rect(screen, UI_PANEL, (canvas_view_rect.x -
                         ruler_size, canvas_view_rect.y, ruler_size, zoomed_size[1]))
        for y in range(0, canvas_size[1], 50):
            y_pos = int(zoomed_pos[1] + y * zoom_level)
            if y % 100 == 0:  # Major tick
                pygame.draw.line(screen, ruler_color, (canvas_view_rect.x - ruler_size, y_pos),
                                 (canvas_view_rect.x, y_pos), 1)
                text = small_font.render(str(y), True, UI_TEXT)
                screen.blit(text, (canvas_view_rect.x -
                            ruler_size + 2, y_pos + 2))
            else:  # Minor tick
                pygame.draw.line(screen, ruler_color, (canvas_view_rect.x - ruler_size // 2, y_pos),
                                 (canvas_view_rect.x, y_pos), 1)

        # Ruler corner
        pygame.draw.rect(screen, UI_PANEL, (canvas_view_rect.x - ruler_size,
                         canvas_view_rect.y - ruler_size, ruler_size, ruler_size))

    # Draw symmetry guide if enabled
    if symmetry_enabled:
        sym_color = (255, 128, 0, 150)
        if symmetry_mode == "horizontal":
            center_x = int(zoomed_pos[0] + (zoomed_size[0] // 2))
            pygame.draw.line(screen, sym_color, (center_x, zoomed_pos[1]),
                             (center_x, zoomed_pos[1] + zoomed_size[1]), 1)
        elif symmetry_mode == "vertical":
            center_y = int(zoomed_pos[1] + (zoomed_size[1] // 2))
            pygame.draw.line(screen, sym_color, (zoomed_pos[0], center_y),
                             (zoomed_pos[0] + zoomed_size[0], center_y), 1)
        elif symmetry_mode == "radial":
            center_x = int(zoomed_pos[0] + (zoomed_size[0] // 2))
            center_y = int(zoomed_pos[1] + (zoomed_size[1] // 2))
            for i in range(8):
                angle = math.pi * i / 4
                end_x = center_x + \
                    math.cos(angle) * max(zoomed_size[0], zoomed_size[1])
                end_y = center_y + \
                    math.sin(angle) * max(zoomed_size[0], zoomed_size[1])
                pygame.draw.line(screen, sym_color, (center_x,
                                 center_y), (int(end_x), int(end_y)), 1)
            pygame.draw.circle(screen, sym_color, (center_x, center_y), 5, 1)

    # Draw panels
    # Sidebar
    pygame.draw.rect(screen, UI_PANEL, sidebar_rect)
    pygame.draw.line(screen, UI_BORDER, (sidebar_rect.right, 0),
                     (sidebar_rect.right, HEIGHT), 1)

    # Toolbar
    pygame.draw.rect(screen, UI_PANEL, toolbar_rect)
    pygame.draw.line(screen, UI_BORDER, (toolbar_rect.left,
                     toolbar_rect.bottom), (WIDTH, toolbar_rect.bottom), 1)

    # Bottom bar
    pygame.draw.rect(screen, UI_PANEL, bottom_rect)
    pygame.draw.line(screen, UI_BORDER, (0, bottom_rect.top),
                     (WIDTH, bottom_rect.top), 1)

    # Color panel
    pygame.draw.rect(screen, UI_BG, color_panel_rect, border_radius=5)
    pygame.draw.rect(screen, UI_BORDER, color_panel_rect, 1, border_radius=5)
    color_title = title_font.render("Color Picker", True, UI_TEXT)
    screen.blit(color_title, (color_panel_rect.x + 10, color_panel_rect.y + 5))

    # Draw color picker gradient
    for x in range(color_picker.width):
        for y in range(color_picker.height):
            hue = x / color_picker.width
            sat = 1 - y / color_picker.height
            rgb = colorsys.hsv_to_rgb(hue, sat, 1)
            color = tuple(int(c * 255) for c in rgb)
            try:
                pygame.gfxdraw.pixel(
                    screen, color_picker.x + x, color_picker.y + y, color)
            except:
                # Fall back to simple rect if gfxdraw fails
                pygame.draw.rect(
                    screen, color, (color_picker.x + x, color_picker.y + y, 1, 1))
    pygame.draw.rect(screen, UI_BORDER, color_picker, 1, border_radius=3)

    # Color previews
    pygame.draw.rect(screen, current_color, color_preview_primary)
    pygame.draw.rect(screen, UI_BORDER, color_preview_primary, 1)
    pygame.draw.rect(screen, secondary_color, color_preview_secondary)
    pygame.draw.rect(screen, UI_BORDER, color_preview_secondary, 1)

    # Color history
    if color_history:
        swatch_width = max(5, color_history_rect.width //
                           min(10, len(color_history)))
        for i, color in enumerate(color_history):
            if i < 10:  # Show up to 10 color swatches
                rect = pygame.Rect(color_history_rect.x + i * swatch_width, color_history_rect.y,
                                   swatch_width, color_history_rect.height)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, UI_BORDER, rect, 1)

    # Tool panels
    for panel_name, panel_info in panels.items():
        panel_rect = panel_info["rect"]
        pygame.draw.rect(screen, UI_BG, panel_rect, border_radius=5)
        pygame.draw.rect(screen, UI_BORDER, panel_rect, 1, border_radius=5)
        panel_title = title_font.render(panel_info["title"], True, UI_TEXT)
        screen.blit(panel_title, (panel_rect.x + 10, panel_rect.y + 5))

    # Tool buttons
    for name, info in tool_buttons.items():
        if "rect" in info:
            button_color = UI_ACCENT if tool == name else UI_BUTTON
            if info["rect"].collidepoint(mouse_pos):
                button_color = UI_HIGHLIGHT
            draw_rounded_rect(screen, info["rect"], button_color, radius=5)
            pygame.draw.rect(screen, UI_BORDER,
                             info["rect"], 1, border_radius=5)

            # Draw button text/icon
            text = small_font.render(
                f"{info['icon']} {name.capitalize()}", True, UI_TEXT)
            text_pos = (info["rect"].x + (info["rect"].width - text.get_width()) // 2,
                        info["rect"].y + (info["rect"].height - text.get_height()) // 2)
            screen.blit(text, text_pos)

    # Shape buttons
    for name, info in shape_buttons.items():
        if "rect" in info:
            button_color = UI_ACCENT if tool == name else UI_BUTTON
            if info["rect"].collidepoint(mouse_pos):
                button_color = UI_HIGHLIGHT
            draw_rounded_rect(screen, info["rect"], button_color, radius=5)
            pygame.draw.rect(screen, UI_BORDER,
                             info["rect"], 1, border_radius=5)

            # Draw button text/icon
            text = small_font.render(
                f"{info['icon']} {name.replace('_', ' ').capitalize()}", True, UI_TEXT)
            text_pos = (info["rect"].x + (info["rect"].width - text.get_width()) // 2,
                        info["rect"].y + (info["rect"].height - text.get_height()) // 2)
            screen.blit(text, text_pos)

    # Effect buttons
    for name, info in effect_buttons.items():
        if "rect" in info:
            # Special handling for toggle buttons
            if name in filters:
                button_color = UI_ACCENT if filters[name] else UI_BUTTON
            elif name == "symmetry":
                button_color = UI_ACCENT if symmetry_enabled else UI_BUTTON
            elif name == "grid":
                button_color = UI_ACCENT if grid_snap else UI_BUTTON
            elif name == "rulers":
                button_color = UI_ACCENT if show_rulers else UI_BUTTON
            else:
                button_color = UI_BUTTON

            if info["rect"].collidepoint(mouse_pos):
                button_color = UI_HIGHLIGHT
            draw_rounded_rect(screen, info["rect"], button_color, radius=5)
            pygame.draw.rect(screen, UI_BORDER,
                             info["rect"], 1, border_radius=5)

            # Draw button text/icon
            text = small_font.render(
                f"{info['icon']} {name.capitalize()}", True, UI_TEXT)
            text_pos = (info["rect"].x + (info["rect"].width - text.get_width()) // 2,
                        info["rect"].y + (info["rect"].height - text.get_height()) // 2)
            screen.blit(text, text_pos)

    # Toolbar buttons
    for name, rect in toolbar_buttons.items():
        button_color = UI_BUTTON
        if rect.collidepoint(mouse_pos):
            button_color = UI_HIGHLIGHT
        draw_rounded_rect(screen, rect, button_color, radius=5)
        pygame.draw.rect(screen, UI_BORDER, rect, 1, border_radius=5)

        # Draw button text
        text = small_font.render(name.capitalize(), True, UI_TEXT)
        text_pos = (rect.x + (rect.width - text.get_width()) // 2,
                    rect.y + (rect.height - text.get_height()) // 2)
        screen.blit(text, text_pos)

    # Layer buttons
    for name, rect in layer_buttons.items():
        button_color = UI_BUTTON
        if rect.collidepoint(mouse_pos):
            button_color = UI_HIGHLIGHT
        draw_rounded_rect(screen, rect, button_color, radius=5)
        pygame.draw.rect(screen, UI_BORDER, rect, 1, border_radius=5)

        # Create simple icons for layer buttons
        icon = ""
        if name == "new":
            icon = "+"
        elif name == "delete":
            icon = "-"
        elif name == "up":
            icon = "↑"
        elif name == "down":
            icon = "↓"
        elif name == "merge":
            icon = "⊕"
        elif name == "duplicate":
            icon = "⧉"

        text = small_font.render(icon, True, UI_TEXT)
        text_pos = (rect.x + (rect.width - text.get_width()) // 2,
                    rect.y + (rect.height - text.get_height()) // 2)
        screen.blit(text, text_pos)

    # Layer info
    layer_text = font.render(
        f"Layer: {current_layer + 1}/{len(layers)}", True, UI_TEXT)
    screen.blit(layer_text, (PADDING * 7 + SMALL_BUTTON_WIDTH *
                6, HEIGHT - BOTTOM_HEIGHT + PADDING + 5))

    # Sliders
    for s, rect in sliders.items():
        # Draw slider background
        pygame.draw.rect(screen, UI_BG, rect, border_radius=5)

        # Draw slider value
        val = brush_size if s == "size" else opacity if s == "opacity" else brush_hardness * 100
        max_val = 100 if s == "size" else 255 if s == "opacity" else 100
        ratio = val / max_val
        value_width = int(rect.width * ratio)
        value_rect = pygame.Rect(rect.x, rect.y, value_width, rect.height)
        pygame.draw.rect(screen, UI_ACCENT, value_rect, border_radius=5)

        # Draw slider border
        pygame.draw.rect(screen, UI_BORDER, rect, 1, border_radius=5)

        # Draw slider handle
        handle_pos = (rect.x + value_width, rect.y + rect.height // 2)
        pygame.draw.circle(screen, UI_TEXT, handle_pos, 5)

        # Draw slider label
        label = f"{s.capitalize()}: {int(val)}"
        if s == "hardness":
            label = f"Hardness: {int(val)}%"
        elif s == "opacity":
            label = f"Opacity: {int(val/2.55)}%"

        label_text = small_font.render(label, True, UI_TEXT)
        screen.blit(label_text, (rect.x, rect.y - 20))

    # Status bar
    status_text = f"Tool: {tool.capitalize()} | Zoom: {int(zoom_level * 100)}% | Canvas: {canvas_size[0]}x{canvas_size[1]} | Project: {project_name}"
    status = small_font.render(status_text, True, UI_TEXT)
    screen.blit(status, (WIDTH - status.get_width() - PADDING,
                HEIGHT - status.get_height() - PADDING))

    # Tool info based on current tool
    tool_info = ""
    if tool == "brush":
        tool_info = "Click and drag to draw. Use Size/Opacity/Hardness sliders to adjust."
    elif tool == "eraser":
        tool_info = "Click and drag to erase. Use Size slider to adjust eraser size."
    elif tool == "select":
        tool_info = "Click and drag to select an area. Use Move tool to move selection."
    elif tool == "fill":
        tool_info = "Click to fill an area with current color."
    elif tool == "eyedropper":
        tool_info = "Click to pick a color from the canvas."
    elif tool == "line":
        tool_info = "Click and drag to draw a line."
    elif tool == "polygon" or tool == "filled_polygon":
        tool_info = "Click to add points. Right-click to complete polygon."
    elif tool == "text":
        tool_info = "Click to place text. Type and press Enter when done."

    info_text = small_font.render(tool_info, True, UI_TEXT)
    screen.blit(info_text, (SIDEBAR_WIDTH + PADDING,
                HEIGHT - info_text.get_height() - PADDING))

    # Mouse coordinates
    if canvas_view_rect.collidepoint(mouse_pos):
        mouse_x, mouse_y = mouse_pos
        canvas_x = int((mouse_x - canvas_view_rect.x) /
                       zoom_level - canvas_offset[0])
        canvas_y = int((mouse_y - canvas_view_rect.y) /
                       zoom_level - canvas_offset[1])

        if 0 <= canvas_x < canvas_size[0] and 0 <= canvas_y < canvas_size[1]:
            coord_text = f"X: {canvas_x}, Y: {canvas_y}"
            coords = small_font.render(coord_text, True, UI_TEXT)
            screen.blit(coords, (WIDTH - coords.get_width() -
                        PADDING, HEIGHT - BOTTOM_HEIGHT + PADDING))

    # Display current shape being drawn
    if drawing_shape and (tool == "polygon" or tool == "filled_polygon") and len(shape_points) > 0:
        shape_text = f"Drawing polygon: {len(shape_points)} points (Right-click to complete)"
        shape_info = small_font.render(shape_text, True, UI_TEXT)
        screen.blit(shape_info, (SIDEBAR_WIDTH + PADDING,
                    HEIGHT - BOTTOM_HEIGHT + PADDING * 3 + 20))

    # Text input indicator
    if text_active:
        text_prompt = f"Enter text: {text_input}"
        text_info = font.render(text_prompt, True, UI_TEXT)
        screen.blit(text_info, (SIDEBAR_WIDTH + PADDING,
                    HEIGHT - BOTTOM_HEIGHT + PADDING * 3 + 20))

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

# Save project before exit if autosave is enabled
if autosave_enabled:
    save_project(f"projects/{project_name}_final", layers, canvas_size)
    print(f"Final project saved as projects/{project_name}_final")

# Quit
pygame.quit()
sys.exit()
