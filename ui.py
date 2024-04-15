from pathlib import Path
import PySimpleGUI as sg

def get_theme(root:str) -> str:
    if root == 'Alpha':
        return 'Dark'
    elif root == 'Omega':
        return 'DarkBrown4'
    elif root == 'Phi':
        return 'DarkAmber'
    elif root == 'Prljav':
        return 'DarkGreen1'
    elif root == 'Nekrigi':
        return 'DarkPurple'
    elif root == 'Arzurian':
        return 'LightBlue5'
    elif root == 'Krymmenos':
        return 'DarkRed1'
    elif root == 'Dark':
        return 'DarkBlack'

def refresh_window(settings):

    theme = settings["GUI"]["default_theme"]
    font_size = int(settings["GUI"]["font_size"] or 24)
    font_family = settings["GUI"]["font_family"]

    sg.theme(theme)
    sg.set_options(font = (font_family, font_size))

def settings_window(settings):
    col_1 = [
        [sg.Text("Tema:")],
        [sg.Text("Tamanho Fonte:")],
    ]

    col_2 = [
        [sg.Combo(settings["GUI"]["theme"].split("|"),s = 10,key = "-THEME-")],
        [sg.Combo(settings["GUI"]["sizes"].split("|"),default_value = 24,s = 10,key = "-SIZE-")],
    ]

    col_3 = [
        [sg.Text("Pasta de Assets:")]
    ]

    col_4 = [
        [sg.Input(default_text=settings["FILE"]["assets_folder"],key = "IMAGES",size = (10,10)),sg.FolderBrowse(key="ASSETS",size=(1,1),button_text='',enable_events=True)],
    ]

    layout_settings = [
        [sg.Text("CONFIGURAÇÕES")],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1),sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Column(col_3),sg.Column(col_4)],
        [sg.Text("")],
        [sg.Button("Salvar", s = (10,1))]
    ]

    window = sg.Window("Settings", layout_settings, modal = True, finalize = True)
    while True:
        event, values = window.read()

        if event == "Salvar":
            if values["-THEME-"] != '':
                settings["GUI"]["default_theme"] = get_theme(values["-THEME-"])
            if values["-SIZE-"] in settings["GUI"]["sizes"].split("|"):
                settings["GUI"]["font_size"] = values["-SIZE-"]
            settings["FILE"]["assets_folder"] = values["IMAGES"]
            refresh_window(settings)
            window.close()
            main_window(settings)
            break
            
        if event == sg.WINDOW_CLOSED:
            window.close()
            break

def main_window(settings):

    menu_bar_definition = [
        ["Menu",["Configurações","Sobre","Save","Load"]]
    ]

    layout_main = [
        [sg.MenubarCustom(menu_bar_definition)],
        [sg.Text("Bem vindo a Mini Heimur!",justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Button('Ações',size=(20,4)),sg.Button('Personagem',size=(20,4))],
    ]

    window = sg.Window("Heimur Game 3.5", layout_main)
    while True:
        event,values = window.read()

        if event == 'Sobre':
            window.disappear()
            sg.popup_no_titlebar("Mini Heimur - Versão Simple GUI","Inicio: 14/04/2024", "Obrigado por jogar!")
            window.reappear()

        if event == 'Configurações':
            window.close()
            settings_window(settings)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def create_settings():
    settings_path = Path.cwd()
    settings = sg.UserSettings(
        path=settings_path,
        filename = "_internal/config.ini",
        use_config_file = True,
        convert_bools_and_none = False
        )
        
    refresh_window(settings)
    main_window(settings)