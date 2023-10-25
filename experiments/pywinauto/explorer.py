import os

from pywinauto import Application, Desktop

script_path = os.getcwd()
script_folder = script_path.split("\\")[-1]

# Shows current windows
Desktop(backend="uia").children()

# Starts File Explorer in the script folder
Application().start(f'explorer.exe "{script_path}"')

# connect to another process spawned by explorer.exe
# Note: make sure the script is running as Administrator!
app = Application(backend="uia").connect(path="explorer.exe")
window = app.window(class_name="CabinetWClass")

window.set_focus()
window.right_click_input()
window.child_window(auto_id="properties").invoke()

# this dialog is open in another process (Desktop object doesn't rely on any process id)
Properties = Desktop(backend="uia")[f"Propriedades de {script_folder}"]
Properties.print_control_identifiers()
Properties.Cancel.click()
Properties.wait_not("visible")  # make sure the dialog is closed
