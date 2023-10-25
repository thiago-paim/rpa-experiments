from functools import partial

import pyautogui
import pyperclip
from PIL import ImageGrab

# To work with multiple monitors/screens, grab all the screens first
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

# -----------------------------------------------------------------------------
# Mouse
# -----------------------------------------------------------------------------

# Get current mouse position
pyautogui.position()


# Move mouse in a square
for i in range(10):
    # Absolute coordinates
    pyautogui.moveTo(100, 100, duration=0.25)
    pyautogui.moveTo(200, 100, duration=0.25)
    pyautogui.moveTo(200, 200, duration=0.25)
    pyautogui.moveTo(100, 200, duration=0.25)

for i in range(10):
    # Relative coordinates
    pyautogui.move(100, 0, duration=0.25)  # right
    pyautogui.move(0, 100, duration=0.25)  # down
    pyautogui.move(-100, 0, duration=0.25)  # left
    pyautogui.move(0, -100, duration=0.25)  # up


# Move mouse to (10, 5) and click.
pyautogui.click(10, 10)

# Move mouse to (10, 5) and click with right button.
pyautogui.click(10, 10, button="right")


# Spiral drag movement
distance = 300
change = 20
while distance > 0:
    pyautogui.drag(distance, 0, duration=0.2)  # Move right.
    distance = distance - change
    pyautogui.drag(0, distance, duration=0.2)  # Move down.
    pyautogui.drag(-distance, 0, duration=0.2)  # Move left.
    distance = distance - change
    pyautogui.drag(0, -distance, duration=0.2)  # Move up.


# Scroll up (positive) or down (negative) by the given amount of pixels
pyautogui.scroll(200)

# Opens helper application for monitoring mouse movement and position
pyautogui.mouseInfo()


# -----------------------------------------------------------------------------
# Keyboard
# -----------------------------------------------------------------------------

# Clicks and write in the position (without prompting an input in between)
pyautogui.click(100, 200)
pyautogui.write("Hello, world!")

# Keys can be passed as list of strings
pyautogui.write(["a", "b", "left", "left", "X", "Y"])

# Shows available keyboard keys
pyautogui.KEYBOARD_KEYS

# Holds a key a press another (manually)
pyautogui.keyDown("shift")
pyautogui.press("4")
pyautogui.keyUp("shift")

# Presses multiple keys at the same time
pyautogui.hotkey("ctrl", "c")
pyautogui.hotkey("alt", "shift", "tab")


# -----------------------------------------------------------------------------
# Screen
# -----------------------------------------------------------------------------

# Obtain the screen resolution (only from primary monitor)
pyautogui.size()

# Takes screenshot and saves it to the current directory
im = pyautogui.screenshot()
im.save("test.png")
# Or
pyautogui.screenshot("test.png")

# Saves screenshot containing only a region of the screen
pyautogui.screenshot("test_region.png", region=(1260, 360, 110, 100))


# Gets RGB from pixel by coordinates
pyautogui.pixel(0, 0)

# Checks if pixel matches RGB
pyautogui.pixelMatchesColor(0, 0, (117, 117, 117))

# Locates the image in the screen
# If a single pixel is a different color, then it won’t find the image
# It also doesn't work with images from Windows snipping tool
pyautogui.locateOnScreen("test_region.png")

# Compares only in grayscale; useful for handling minor color variations
pyautogui.locateOnScreen("test_region.png", grayscale=True)

# Compares the imagem considering possible noise. Requires OpenCV installed
pyautogui.locateOnScreen("test_region.png", confidence=0.9)

# Combines both parameters
pyautogui.locateOnScreen("test_region.png", grayscale=True, confidence=0.9)

# Locate the image in the screen and returns its center coordinates
pyautogui.locateCenterOnScreen("test_region.png")


# -----------------------------------------------------------------------------
# Window
# -----------------------------------------------------------------------------

# Get active window
w = pyautogui.getActiveWindow()

# Returns a list of Window objects for every visible window on the screen.
pyautogui.getAllWindows()

# Returns a list of Window objects for every visible window that includes the point (x, y).
pyautogui.getWindowsAt(10, 10)

# Returns a list of Window object titles for every visible window on the screen.
pyautogui.getAllTitles()

# Returns a list of Window objects for every visible window that includes the string title in its title bar.
pyautogui.getWindowsWithTitle("Program Manager")


# Shows window coordinates
w.left, w.right, w.top, w.bottom

# Shows other info
w.size, w.area, w.center, w.box, w.title

# Resizes the window
w.width = w.width - 100

# Moves the window
w.topleft = (10, 10)

# Other window size manipulations
w.minimize()
w.maximize()
w.restore()
w.isMaximized
w.isMinimized
w.isActive
w.activate()
w.close()


# -----------------------------------------------------------------------------
# Messages
# -----------------------------------------------------------------------------

# Displays text and has a single OK button.
pyautogui.alert("This is a message.", "Important")

# Displays text and has OK and Cancel buttons, returning either 'OK' or 'Cancel' depending on the button clicked
pyautogui.confirm("text", "Title")

# Displays text and has a text field for the user to type in, which it returns as a string.
pyautogui.prompt("text")

# Is the same as prompt(), but displays asterisks so the user can enter sensitive information such as a password.
pyautogui.password("text")


# -----------------------------------------------------------------------------
# Generic
# -----------------------------------------------------------------------------

# Wait time between commands
pyautogui.PAUSE
pyautogui.PAUSE = 0.1


# Exception for ctrl+c; important to handle it for halting programs
KeyboardInterrupt

# Paste what's in the clipboard
pyperclip.paste()
