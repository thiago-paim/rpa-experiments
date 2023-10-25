from functools import partial

import pyautogui
from PIL import ImageGrab
from pywinauto.application import Application
from utils import log_action

# Grabs all screens for pyautogui. Necessary for multi-monitor setups
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# Pause between actions
pyautogui.PAUSE = 0.1


class BaseRPAApp:
    backend = None
    app = None
    main_window = None
    elements = {}

    @log_action
    def __init__(self) -> None:
        """Starts Paint application and validates the main window"""
        self.app = Application(backend=self.backend).start(self.app_command)
        if len(self.app.windows()) > 1:  # Validates only one main window opened
            raise Exception("More than one window opened")

        self.main_window = self.app.window(class_name=self.window_class_name)
        if not self.main_window.exists():  # Validates main window exists
            raise Exception("Main window not found")

    def click_element(self, element: dict) -> None:
        """
        Clicks on an instance element. Since only some elements have an `auto_id` (and even among them some are not clickable),
        it's safer to check for the icon center first.
        """

        if "center" in element:
            pyautogui.click(element["center"])
            return

        if "auto_id" in element:
            self.main_window.child_window(auto_id=element["auto_id"]).click()
            return
