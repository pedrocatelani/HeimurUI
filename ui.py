from time import sleep
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

def settings_window(settings,game):
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
            main_window(settings,game)
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
            settings_window(settings,game)
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

    harvest_chance = game.atributes['for'] + game.atributes['des'] + game.atributes['con'] + game.atributes['int']

    col_1 = [
        [sg.Button('Minerar',size=15,key='mine')],
        [sg.Text('Pedra:'),sg.Text(f'{game.materials["stone"]}',key='stone')],
        [sg.Text('Ferro'),sg.Text(f'{game.materials["iron"]}',key='iron')],
        [sg.HorizontalSeparator()],
        [sg.Button('Coletar',size=15,key='gather')],
        [sg.Text('Graveto'),sg.Text(f'{game.materials["sticks"]}',key='sticks')],
        [sg.Text('Madeira'),sg.Text(f'{game.materials["wood"]}',key='wood')],
    ]

    col_2 = [
        [sg.Button('Buscar',size=15,key='search')],
        [sg.Text('Fruta:'),sg.Text(f'{game.materials["berries"]}',key='berries')],
        [sg.Text('Morango:'),sg.Text(f'{game.materials["strawberries"]}',key='strawberries')],
        [sg.Text('Erva:'),sg.Text(f'{game.materials["green_herb"]}',key='green_herb')],
        [sg.Text('Erva Azul:'),sg.Text(f'{game.materials["blue_herb"]}',key='blue_herb')],
    ]

    harvest_layout = [
        [sg.Text('Harvest!')],
        [sg.HorizontalSeparator()],
        [sg.Text(f"Chance de Colheita: {harvest_chance}%")],
        [sg.Text('',key='got')],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1),sg.VerticalSeparator(),sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7)],
    ]

    window = sg.Window('',harvest_layout)
    while True:
        event, values = window.read()

        if event in ["mine","gather","search"]:
            if game.roll_harvest_chance():
                rs = game.get_resources(event)
                print(rs)
                window["got"].update(f'Você conseguiu {rs[1]} {rs[0]}!')
                window[f"{rs[0]}"].update(f'{game.materials[f"{rs[0]}"]}')
            else:
                window["got"].update(f'Você não encontrou nada!')

        if event == 'Voltar':
            window.close()
            action_window(settings,game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break

def combat_window(settings,game):

    def turno_player():
        rolagem = game.roll(20)
        window["ROL"].update(rolagem)
        ataque = rolagem + game.status["atq"]
        defesa = game.roll(20) + game.monster["def"]
        pt_crit = defesa + 16
        if ataque > pt_crit:
            sg.popup_no_titlebar('Você Acertou um Crítico!!!')
            dano = 2 * (game.status["level"] + game.status["base_dmg"])
        elif ataque > defesa:
            sg.popup_no_titlebar('Você Acertou o Ataque!')
            dano = game.roll(game.status["level"]) + game.status["base_dmg"]
        else:
            sg.popup_no_titlebar('Você Errou o Ataque!')
            dano = 0
        
        game.monster["current_hp"] -= dano
        window["dmg c"].update(dano)
        window["permonster"].update(f'{game.get_hp_percent(game.monster["current_hp"],game.monster["max_hp"])}%')

    def turno_inimigo():
        rolagem = game.roll(20)
        ataque = rolagem + game.monster["atq"]
        defesa = game.roll(20) + game.status["def"]
        pt_crit = defesa + 16
        if ataque > pt_crit:
            sg.popup_no_titlebar('Você Recebeu um Crítico!!!')
            dano = 2 * (game.monster["level"] + game.monster["dmg"])
        elif ataque > defesa:
            sg.popup_no_titlebar('Você Recebeu um Ataque!')
            dano = game.roll(game.monster["level"]) + game.monster["dmg"]
        else:
            sg.popup_no_titlebar('Você Defendeu o Ataque!')
            dano = 0
        
        game.status["current_hp"] -= dano
        window["dmg r"].update(dano)
        window["perplayer"].update(f'{game.get_hp_percent(game.status["current_hp"],game.status["max_hp"])}%')

    game.get_monster(game.region)

    col_1 = [
        [sg.Text(f'{game.get_hp_percent(game.status["current_hp"],game.status["max_hp"])}%',k="perplayer")],
        [sg.Image('_internal/assets/char.png')],
    ]

    col_2 = [
        [sg.Push(),sg.Text('Ameaça: '),sg.Text(f'{game.monster["danger_level"]}'),sg.Push()],
        [sg.Push(),sg.Text('Rolagem:'),sg.Push()],
        [sg.Push(),sg.Text('0',k="ROL"),sg.Push()],
        [sg.Push(),sg.Text('Dano Causado:'),sg.Push()],
        [sg.Push(),sg.Text('0',k="dmg c"),sg.Push()],
        [sg.Push(),sg.Text('Dano Recebido:'),sg.Push()],
        [sg.Push(),sg.Text('0',k="dmg r"),sg.Push()],
    ]

    col_3 = [
        [sg.Push(),sg.Text(f'{game.get_hp_percent(game.monster["current_hp"],game.monster["max_hp"])}%',k="permonster")],
        [sg.Image(f'_internal/assets/{game.monster['name']}.png')],
    ]

    combat_layout = [
        [sg.Text('Combate!')],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1),sg.VerticalSeparator(),sg.Column(col_2),sg.VerticalSeparator(),sg.Column(col_3)],
        [sg.HorizontalSeparator()],
        [sg.Push(),sg.Button('Lutar',size=10),sg.Button('Itens',size=10),sg.Button('Libra',size=10),sg.Push()],
        [sg.Push(),sg.Button('Magias',size=10),sg.Button('Fugir',size=10),sg.Push()],
        [sg.HorizontalSeparator()],
    ]

    window = sg.Window('',combat_layout)
    while True:
        event, values = window.read()

        if event == 'Lutar':
            turno_player()
            if game.monster["current_hp"] > 0:
                turno_inimigo()

        if event == 'Fugir':
            if game.status["level"] <= 2 or game.scape == True:
                window.close()
                action_window(settings,game)
                break
            else:
                sg.popup_no_titlebar("Você não conseguiu fugir!")

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

        if event == 'Cheats':
            window.close()
            cheats_window(settings,game)
            break

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

def cheats_window(settings,game):

    col_1 = [
        [sg.Button('potion',size=10)],
        [sg.Button('revive',size=10)],
        [sg.Button('materials',size=10)],
    ]

    col_2 = [
        [sg.Button('elixir',size=10)],
        [sg.Button('100 money',size=10)],
        [sg.Button('1000 money',size=10)],
    ]

    cheats_layout = [
        [sg.Text('CHEATS!!!!')],
        [sg.HorizontalSeparator()],
        [sg.Text('Usuário: '),sg.Input(size=11,key='user')],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1),sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar',size=7)],
    ]

    window = sg.Window('',cheats_layout)
    while True:
        event, values = window.read()

        if values["user"] in game.users_cheats:
            print('Usuário Válidado!!!')
            if event in ['potion','elixir','revive']:
                game.inventory[f"{event}"] += 15
            if event == '100 money':
                game.inventory["money"] += 100
            if event == '1000 money':
                game.inventory["money"] += 1000
            if event == 'materials':
                game.materials["sticks"] += 50
                game.materials["wood"] += 50
                game.materials["stone"] += 50
                game.materials["iron"] += 50
                game.materials["green_herb"] += 50
                game.materials["blue_herb"] += 50
                game.materials["berries"] += 50
                game.materials["strawberries"] += 50

        if event == 'Voltar':
            window.close()
            char_window(settings,game)
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

    others_1 = [
        [sg.Text('Vida:')],
        [sg.Text('Exp:')],
        [sg.Text('Level:')],
    ]

    others_2 = [
        [sg.Text(f'{game.status['current_hp']}/{game.status['max_hp']}')],
        [sg.Text(f'{game.status['current_xp']}/{game.status['max_xp']}')],
        [sg.Text(f'{game.status['level']}')],
    ]

    stts_layout = [
        [sg.Text('Estatísticas!')],
        [sg.HorizontalSeparator()],
        [sg.Text("Atributos:")],
        [sg.HorizontalSeparator()],
        [sg.Text("Bônus:")],
        [sg.HorizontalSeparator()],
        [sg.Text("Outros:")],
        [sg.Column(others_1),sg.Column(others_2)],
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