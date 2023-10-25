import time
from copy import copy
from pathlib import Path

import pyautogui
from base import BaseRPAApp
from PIL import Image
from utils import log_action

# TODO: Consider using collections.namedtuple (or create another class for elements)
PAINT_STARTING_ELEMENTS = {
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

FONT_SIZE_INPUT_ELEMENT = {
    "icon": "font_size_input.png",
    "auto_id": "EditableText",
    "control_type": "ComboBox",
}


class PaintRPA(BaseRPAApp):
    backend = "uia"
    app_command = "mspaint.exe"
    window_class_name = "MSPaintApp"
    confidence = 0.9

    def __init__(self) -> None:
        super().__init__()
        self._set_starting_elements()

    @log_action
    def _set_starting_elements(self) -> None:
        """Sets the starting elements of the instance and their positions"""
        self.main_window.maximize()

        # Alert user to confirm the window position before continuing
        # input = pyautogui.alert("Certifique-se de que o Paint está aberto e na posição correta antes de continuar.", "Atenção")
        # if input != "OK":
        #     raise Exception("User canceled")

        r = self.main_window.rectangle()
        self.elements["main_window"] = {
            "center": (r.mid_point().x, r.mid_point().y),
            "region": (
                r.left
                if r.left > 0
                else 0,  # Ignore hidden portions of the screen to avoid errors
                r.top
                if r.top > 0
                else 0,  # Ignore hidden portions of the screen to avoid errors
                r.width(),
                r.height(),
            ),
        }

        r = self.main_window.child_window(auto_id="image").rectangle()
        self.elements["canvas"] = {
            "auto_id": "image",
            "center": (r.mid_point().x, r.mid_point().y),
            "region": (
                r.left
                if r.left > 0
                else 0,  # Ignore hidden portions of the screen to avoid errors
                r.top
                if r.top > 0
                else 0,  # Ignore hidden portions of the screen to avoid errors
                r.width(),
                r.height(),
            ),
        }

        for key, element in PAINT_STARTING_ELEMENTS.items():
            e = copy(element)
            e["center"] = self._find_icon_center(element["icon"])
            self.elements[key] = e

    def _find_icon_center(self, icon: str) -> tuple:
        """Searches for the icon in the main window and returns its center coordinates"""
        icon_path = Path(__file__).parent / "icons" / icon
        img = Image.open(icon_path)
        point = pyautogui.locateCenterOnScreen(
            img,
            confidence=self.confidence,
            region=self.elements["main_window"]["region"],
        )
        if not point:
            raise Exception(f"Element {icon} not found")
        return (point.x, point.y)

    def _set_font_size_element(self):
        """Sets the Font Size Input element (not set on start because it's only available when Text Tool is active)"""
        element = copy(FONT_SIZE_INPUT_ELEMENT)
        element["center"] = self._find_icon_center(element["icon"])
        self.elements["font_size_input"] = element

    def set_font_size(self, font_size: int) -> None:
        """Sets the font size on Font Size Input element"""
        if "font_size_input" not in self.elements:
            time.sleep(0.5)
            self._set_font_size_element()

        self.click_element(self.elements["font_size_input"])
        pyautogui.write(str(font_size))

    @log_action
    def write_message(self, msg: str, font_size: int = 72) -> None:
        """Writes a messave on the canvas using the Text Tool. The positioning is slightly above the center of the canvas."""
        self.main_window.set_focus()
        self.click_element(self.elements["text_tool"])
        self.set_font_size(font_size)

        x_gap = (font_size / 3) * len(msg)
        y_gap = (font_size / 2) * 5

        pyautogui.moveTo(self.elements["canvas"]["center"])
        pyautogui.move(-x_gap, -y_gap)
        pyautogui.click()
        pyautogui.typewrite(msg)

        # Return to starting selected tool (avoids changes on Paint GUI structure that might cause issues)
        self.click_element(self.elements["brush_tool"])

    @log_action
    def draw_spiral(
        self, distance: int = 300, change: int = 20, duration: float = 0.2
    ) -> None:
        """Draws a square spiral in the canvas"""

        self.main_window.set_focus()
        pyautogui.moveTo(self.elements["canvas"]["center"])
        pyautogui.move(-distance / 2, 0)

        while distance > change:
            pyautogui.drag(distance, 0, duration=duration)  # Move right
            distance = distance - change
            pyautogui.drag(0, distance, duration=duration)  # Move down.
            pyautogui.drag(-distance, 0, duration=duration)  # Move left.
            distance = distance - change
            pyautogui.drag(0, -distance, duration=duration)  # Move up.

    @log_action
    def save(self, file_name: str) -> None:
        self.main_window.set_focus()
        pyautogui.hotkey("ctrl", "s")

        # TODO: Add save dialog actions
        # save_as_dialog = self.main_window.child_window(title="Save As", control_type="Window")
        # save_as_dialog.wait("ready")  # Espera o dialog aparecer; não sei se é necessário

        # name_input = save_as_dialog.child_window(title="Nome:", control_type="Edit", auto_id="1001")
        # name_input.set_text(file_name)
        # save_button = save_as_dialog.child_window(title="Salvar", control_type="Button", auto_id="1")
        # save_button.click()

        pyautogui.press("enter")


def main():
    paint = PaintRPA()
    paint.write_message(msg="OIE!")
    paint.draw_spiral(distance=300, change=30)
    # paint.save("teste_rpa.png")


if __name__ == "__main__":
    main()
