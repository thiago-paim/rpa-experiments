import win32api
from pywinauto.application import Application

msg = "OIE GOTO"

app = Application(backend="uia").start("mspaint.exe")
main_window = app.window(class_name="MSPaintApp")

# Identifica elementos e posições
window_mid_pos = main_window.rectangle().mid_point()

text_tool = main_window.child_window(auto_id="TextTool")
text_tool_pos = text_tool.rectangle().mid_point()

brush_tool = main_window.child_window(auto_id="BrushesSplitButton")
brush_tool_pos = brush_tool.rectangle().mid_point()

file_menu = main_window.child_window(title="Arquivo", control_type="MenuItem")
file_menu_pos = file_menu.rectangle().mid_point()

main_window.from_point(file_menu_pos.x, file_menu_pos.y).click_input()
save_menu = main_window.child_window(auto_id="FileSave")
save_menu_pos = save_menu.rectangle().mid_point()
main_window.from_point(file_menu_pos.x, file_menu_pos.y).click_input()


# Seleciona a ferramenta de texto
text_tool.click_input()

# Seleciona o wrapper do canvas e escreve o texto
group_wrapper = main_window.from_point(window_mid_pos.x, window_mid_pos.y)
group_wrapper.click_input()
group_wrapper.type_keys(msg)

# Des-seleciona a ferramenta de texto para o Paint voltar a estrutura normal
main_window.from_point(brush_tool_pos.x, brush_tool_pos.y).click_input()

# Abre o menu de Arquivo e clica pra salvar
file_menu.click_input()
save_menu.click_input()

save_as_dialog = main_window.child_window(title="Save As", control_type="Window")
save_as_dialog.wait("ready")  # Espera o dialog aparecer; não sei se é necessário

# Define o nome do arquivo e salva
name_input = save_as_dialog.child_window(
    title="Nome:", control_type="Edit", auto_id="1001"
)
name_input.set_text(f"{msg}.png")
save_button = save_as_dialog.child_window(
    title="Salvar", control_type="Button", auto_id="1"
)
save_button.click()


# ------------------------------------------
# DEBUG

# Printa informações de todos os controles descendentes da janela
main_window.print_control_identifiers()

# Maximiza e minimza a janela
main_window.maximize()
main_window.minimize()

# Checa se o controle existe
text_tool.exists()

# Exibe informações sobre o controle
text_tool.element_info

# Exibe as propriedades do controle
text_tool.get_properties()

# Traça um retangulo verde ao redor da janela, para identificação (DEBUG)
text_tool.draw_outline()

# Exibe as coordenadas X,Y do controle
text_tool.rectangle()

# Pega a posição central da janela
main_window.rectangle().mid_point()

# Pega o wrapper que está no ponto passado
main_window.from_point(window_mid_pos.x, window_mid_pos.y)

# Pega o wrapper do elemento raiz do que está no ponto passado
main_window.top_from_point(window_mid_pos.x, window_mid_pos.y)

# Salva screenshot da tela
main_window.capture_as_image().save("screenshot.png")

# Pega posição atual do cursor do mouse


win32api.GetCursorPos()


# ---------------------------------------
# Testes

main_window.menu_select("Arquivo -> Salvar")
"""
Não funciona
O método `menu_select` busca por menus organizados dentro de um controle `Menu`,
e o Paint não faz isso
"""
