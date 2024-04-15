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
    elif root == 'Azurian':
        return 'LightBlue5'
    elif root == 'Krymmenos':
        return 'DarkRed1'
    elif root == 'Dark':
        return 'DarkBlack'

def put_points_window(settings,game):
    
    col_1 = [
        [sg.Text("Força:")] ,
        [sg.Text("Destreza:")],
        [sg.Text("Constituição:")],
        [sg.Text("Inteligência:")],
    ]

    col_2 = [
        [sg.Input('0',s=3,key='for')],
        [sg.Input('0',s=3,key='des')],
        [sg.Input('0',s=3,key='con')],
        [sg.Input('0',s=3,key='int')],
    ]

    layout_points = [
        [sg.Text("Atribuição de Pontos!!!")],
        [sg.HorizontalSeparator()],
        [sg.Text("Pontos Restantes:"),sg.Text(f'{game.atributes["current_points"]}')],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1),sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Button('Check',size=23)],
    ]

    window = sg.Window('Tabela de Pontos', layout_points)
    while True:
        event, values = window.read()

        if event == 'Check':
            if game.check_points(values['for'],values['des'],values['con'],values['int']):
                window.close()
                game.add_points(values['for'],values['des'],values['con'],values['int'])
                settings["GAME"]["init"] = 1
                main_window(settings,game)
                break
            else:
                sg.popup_no_titlebar('VALORES INVÁLIDOS!!!!')

        if event == sg.WIN_CLOSED:
            window.close()
            break

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

def main_window(settings,game):

    menu_bar_definition = [
        ["Menu",["Configurações","Sobre","Save","Load"]]
    ]

    layout_main = [
        [sg.MenubarCustom(menu_bar_definition)],
        [sg.Text("Bem vindo a Mini Heimur!",justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Button('Ações',size=(20,4)),sg.Button('Personagem',size=(20,4)),sg.Button('Loja',size=(20,4))],
    ]

    window = sg.Window("Heimur Game 3.5", layout_main)
    while True:
        event,values = window.read()

        if event == 'Ações':
            window.close()
            action_window(settings,game)
            break

        if event == 'Personagem':
            window.close()
            char_window(settings,game)
            break

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

def action_window(settings,game):
    action_layout = [
        [sg.Text('Ações!')],
        [sg.HorizontalSeparator()],
        [sg.Button('Descansar',size=(15,3)),sg.Button('Caçar',size=(15,3)),sg.Button('Harvest',size=(15,3))],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7)],
    ]

    window = sg.Window('',action_layout)
    while True:
        event, values = window.read()
        
        if event == 'Harvest':
            window.close()
            harvest_window(settings,game)
            break

        if event == 'Caçar':
            window.close()
            combat_window(settings,game)
            break

        if event == 'Voltar':
            window.close()
            main_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def harvest_window(settings,game):
    harvest_layout = [
        [sg.Text('Ações!')],
        [sg.HorizontalSeparator()],
        [],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7)],
    ]

    window = sg.Window('',harvest_layout)
    while True:
        event, values = window.read()

        if event == 'Voltar':
            window.close()
            action_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def combat_window(settings,game):
    combat_layout = [
        [sg.Text('Combate!')],
        [sg.HorizontalSeparator()],
        [sg.Button('Fugir')],
        [sg.HorizontalSeparator()],
    ]

    window = sg.Window('',combat_layout)
    while True:
        event, values = window.read()

        if event == 'Fugir':
            window.close()
            action_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def char_window(settings,game):
    char_layout = [
        [sg.Text('Personagem!')],
        [sg.HorizontalSeparator()],
        [sg.Button('Inventário',size=(15,3)),sg.Button('Status',size=(15,3)),sg.Button('Magias',size=(15,3))],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7),sg.Button('Cheats',size=7)],
    ]

    window = sg.Window('',char_layout)
    while True:
        event, values = window.read()

        if event == 'Magias':
            window.close()
            spell_window(settings,game)
            break

        if event == 'Status':
            window.close()
            status_window(settings,game)
            break

        if event == 'Inventário':
            window.close()
            inventory_window(settings,game)
            break

        if event == 'Voltar':
            window.close()
            main_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def spell_window(settings,game):
    spell_layout = [
        [sg.Text('Magias!')],
        [sg.HorizontalSeparator()],
        [],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7)],
    ]

    window = sg.Window('',spell_layout)
    while True:
        event, values = window.read()

        if event == 'Voltar':
            window.close()
            char_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def status_window(settings,game):
    stts_layout = [
        [sg.Text('Estatísticas!')],
        [sg.HorizontalSeparator()],
        [sg.Text("Atributos:")],
        [sg.HorizontalSeparator()],
        [sg.Text("Bônus:")],
        [sg.HorizontalSeparator()],
        [sg.Text("Outros:")],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7)],
    ]

    window = sg.Window('',stts_layout)
    while True:
        event, values = window.read()

        if event == 'Voltar':
            window.close()
            char_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def inventory_window(settings,game):
    inv_layout = [
        [sg.Text('Inventário!')],
        [sg.HorizontalSeparator()],
        [sg.Text('Materiais:')],
        [],
        [sg.HorizontalSeparator()],
        [sg.Text('Itens:')],
        [],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7),sg.Button('Armas',size=7),sg.Button('Craft',size=7)],
    ]

    window = sg.Window('',inv_layout)
    while True:
        event, values = window.read()

        if event == 'Armas':
            window.close()
            weapons_window(settings,game)
            break

        if event == 'Craft':
            window.close()
            craft_window(settings,game)
            break

        if event == 'Voltar':
            window.close()
            char_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def craft_window(settings,game):
    craft_layout = [
        [sg.Text('Crafting!')],
        [sg.HorizontalSeparator()],
        [],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7),sg.Button('Fazer',size=7)],
    ]

    window = sg.Window('',craft_layout)
    while True:
        event, values = window.read()

        if event == 'Voltar':
            window.close()
            inventory_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def weapons_window(settings,game):
    weapons_layout = [
        [sg.Text('Armas!')],
        [sg.HorizontalSeparator()],
        [sg.Text('Obtidas:')],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7),sg.Button('Trocar',size=7)],
    ]

    window = sg.Window('',weapons_layout)
    while True:
        event, values = window.read()

        if event == 'Voltar':
            window.close()
            inventory_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def create_settings(game:object):
    settings_path = Path.cwd()
    settings = sg.UserSettings(
        path=settings_path,
        filename = "_internal/config.ini",
        use_config_file = True,
        convert_bools_and_none = False
        )
        
    refresh_window(settings)
    if game.initialized == '1':
        main_window(settings,game)
    else:
        put_points_window(settings,game)