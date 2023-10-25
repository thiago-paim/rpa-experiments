from functools import partial

import pyautogui
from PIL import ImageGrab
from pywinauto.application import Application

# Grabs all screens for pyautogui. Necessary for multi-monitor setups
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


# msg = pyautogui.prompt("Escreva sua mensagem:")
msg = "Oie Goto!"
font_size = "72"
confidence = 0.9
app_command = "mspaint.exe"
window_class_name = "MSPaintApp"

app = Application(backend="uia").start(app_command)

if len(app.windows()) > 1:  # Validates only one main window opened
    raise Exception("More than one window opened")

main_window = app.window(class_name=window_class_name)
if not main_window.exists():  # Validates main window exists
    raise Exception("Main window not found")

# Alert user to confirm the window position before continuing
pyautogui.alert(
    "Certifique-se de que o Paint está aberto e na posição correta antes de continuar",
    "Atenção",
)

# Defines window region to optimize image search
r = main_window.rectangle()
main_window_region = (
    r.left if r.left > 0 else 0,  # Ignore hidden portions of the screen to avoid errors
    r.top if r.top > 0 else 0,  # Ignore hidden portions of the screen to avoid errors
    r.width(),
    r.height(),
)
main_window_center = (r.mid_point().x, r.mid_point().y)

# TODO: Move icons to folder
initial_elements = {
    "text_tool": {
        "icon": "text_tool.png",
        "auto_id": "TextTool",
        "control_type": "Button",
    },
    "pencil_tool": {
        "icon": "pencil_tool.png",
        "auto_id": "PencilTool",
        "control_type": "Button",
    },
    "brush_tool": {
        "icon": "brush_tool.png",
        "auto_id": "BrushesSplitButton",
        "control_type": "RadioButton",
    },
    "file_menu": {
        "icon": "file_menu.png",
        "auto_id": "ContentButton",
        "control_type": "MenuItem",
        "title": "Arquivo",
    },
}

# Only available after clicking on Text Tool
font_size_input_element = {
    "icon": "font_size_input.png",
    "auto_id": "FontSizeComboBox",
    "control_type": "ComboBox",
}


def get_element_center(element):
    if "icon" in element:
        point = pyautogui.locateCenterOnScreen(
            element["icon"], confidence=confidence, region=main_window_region
        )
        if not point:
            raise Exception(f"Element {element['icon']} not found")
        return (point.x, point.y)
    else:
        return None


def validate_and_click(element):
    # TODO: Validate element by `auto_id` and `control_type`
    pyautogui.click(element["center"])


# Get position for starting elements
for element in initial_elements.values():
    element["center"] = get_element_center(element)

# Select Text Tool
validate_and_click(initial_elements["text_tool"])

# Set the correct font size
font_size_input_element["center"] = get_element_center(font_size_input_element)
validate_and_click(font_size_input_element)
pyautogui.write(font_size)

# Write message
pyautogui.click(main_window_center)
pyautogui.write(msg)

# Saves image
pyautogui.hotkey("ctrl", "s")
pyautogui.press("enter")
