import pyautogui


def main():
    # Prints two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
    print(pyautogui.size())

    # Prints the x and y of the mouse cursor's current position.
    print(pyautogui.position())

    # Sets the amount of seconds to wait after each PyAutoGUI call.
    pyautogui.PAUSE = 2.5

    # Opens Chrome
    pyautogui.hotkey("win")
    pyautogui.typewrite("chrome")
    pyautogui.hotkey("enter")

    pyautogui.typewrite("https://web.whatsapp.com/")
    pyautogui.hotkey("enter")

    pyautogui.alert(
        text="Clique em OK quando o Whatsapp Web terminar de carregar",
        title="",
        button="OK",
    )

    whatsapp_search_position = (1400, 200)
    pyautogui.click(whatsapp_search_position)

    # whatsapp_user = "Goto"
    # whatsapp_user = "Notas"
    whatsapp_user = pyautogui.prompt(
        text="Escreva o nome do usuário para mandar a mensagem", title="", default=""
    )
    pyautogui.typewrite(whatsapp_user)

    whatsapp_first_result_position = (1500, 330)
    pyautogui.click(whatsapp_first_result_position)

    whatsapp_msg_position = (1960, 1000)
    pyautogui.click(whatsapp_msg_position)

    # whatsapp_msg = "Oee, tudo bom? Esta é uma mensagem automatizada enviada com PyAutoGUI. Novidades sobre a vaga? :D"
    whatsapp_msg = pyautogui.prompt(
        text=f"Escreva a mensagem a ser enviada para {whatsapp_user}",
        title="",
        default="",
    )
    pyautogui.write(whatsapp_msg)
    pyautogui.hotkey("enter")

    # PyAutoGUI doesn't handle special characters outside of US keyboard layout: https://stackoverflow.com/questions/51902824/pyautogui-cannot-write-the-symbol


if __name__ == "__main__":
    main()
