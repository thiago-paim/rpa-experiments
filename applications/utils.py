from datetime import datetime
from functools import partial, wraps

import pyautogui
from PIL import ImageGrab

# Grabs all screens for pyautogui. Necessary for multi-monitor setups
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


def log_action(func):
    """Decorator for loging RPA actions"""

    @wraps(func)
    def wrapper_func(*args, **kwargs):
        print(
            f'{datetime.today().strftime("%Y-%m-%d %H:%M:%S")} | {func.__name__}({kwargs=})'
        )
        return func(*args, **kwargs)

    return wrapper_func


def get_icon_by_bounding_rectangle(rectangle: list, name: str) -> None:
    """Receives an element bounding rectangle (extracted from Accessibility Insights for Windows) and saves its icon."""
    left = rectangle[0]
    top = rectangle[1]
    right = rectangle[2]
    bottom = rectangle[3]
    width = right - left
    height = bottom - top

    region = (left, top, width, height)
    pyautogui.screenshot(f"{name}.png", region=region)


def get_paint_icons():
    """Get icons from Paint."""
    # Coordenadas com Paint aberto ocupando metade direita do monitor
    bounding_rectangles = {
        "file_menu": [1285, 35, 1354, 67],
        "text_tool": [1652, 88, 1684, 120],
        "pencil_tool": [1572, 88, 1604, 120],
        "brush_tool": [1712, 100, 1744, 148],
        # "font_size_input": [1725, 205, 1805, 245],
    }

    for name, rectangle in bounding_rectangles.items():
        get_icon_by_bounding_rectangle(rectangle, name)
