from time import sleep
from pathlib import Path
import PySimpleGUI as sg


def get_theme(root: str) -> str:
    if root == "Alpha":
        return "Dark"
    elif root == "Omega":
        return "DarkBrown4"
    elif root == "Phi":
        return "DarkAmber"
    elif root == "Prljav":
        return "DarkGreen1"
    elif root == "Nekrigi":
        return "DarkPurple"
    elif root == "Azurian":
        return "LightBlue5"
    elif root == "Krymmenos":
        return "DarkRed1"
    elif root == "Dark":
        return "DarkBlack"


def put_points_window(settings, game):

    col_1 = [
        [sg.Text("Força:")],
        [sg.Text("Destreza:")],
        [sg.Text("Constituição:")],
        [sg.Text("Inteligência:")],
    ]

    col_2 = [
        [sg.Input("0", s=3, key="for")],
        [sg.Input("0", s=3, key="des")],
        [sg.Input("0", s=3, key="con")],
        [sg.Input("0", s=3, key="int")],
    ]

    layout_points = [
        [sg.Text("Atribuição de Pontos!!!")],
        [sg.HorizontalSeparator()],
        [sg.Text("Pontos Restantes:"), sg.Text(f'{game.atributes["current_points"]}')],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1), sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Button("Check", size=23)],
    ]

    window = sg.Window("Tabela de Pontos", layout_points)
    while True:
        event, values = window.read()

        if event == "Check":
            if game.check_points(
                values["for"], values["des"], values["con"], values["int"]
            ):
                window.close()
                game.add_points(
                    values["for"], values["des"], values["con"], values["int"]
                )
                game.atributes["current_points"] = 0

                game.weapon_status(game.inventory["eq_weapon"])
                game.refresh_status()
                main_window(settings, game)
                break
            else:
                sg.popup_no_titlebar("VALORES INVÁLIDOS!!!!")

        if event == sg.WIN_CLOSED:
            window.close()
            break


def refresh_window(settings):

    theme = settings["GUI"]["default_theme"]
    font_size = int(settings["GUI"]["font_size"] or 24)
    font_family = settings["GUI"]["font_family"]

    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))


def settings_window(settings, game):
    col_1 = [
        [sg.Text("Tema:")],
        [sg.Text("Tamanho Fonte:")],
    ]

    col_2 = [
        [sg.Combo(settings["GUI"]["theme"].split("|"), s=10, key="-THEME-")],
        [
            sg.Combo(
                settings["GUI"]["sizes"].split("|"),
                default_value=24,
                s=10,
                key="-SIZE-",
            )
        ],
    ]

    col_3 = [[sg.Text("Pasta de Assets:")]]

    col_4 = [
        [
            sg.Input(
                default_text=settings["FILE"]["assets_folder"],
                key="IMAGES",
                size=(10, 10),
            ),
            sg.FolderBrowse(
                key="ASSETS", size=(1, 1), button_text="", enable_events=True
            ),
        ],
    ]

    layout_settings = [
        [sg.Text("CONFIGURAÇÕES")],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1), sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Column(col_3), sg.Column(col_4)],
        [sg.Text("")],
        [sg.Button("Salvar", s=(10, 1))],
    ]

    window = sg.Window("Settings", layout_settings, modal=True, finalize=True)
    while True:
        event, values = window.read()

        if event == "Salvar":
            if values["-THEME-"] != "":
                settings["GUI"]["default_theme"] = get_theme(values["-THEME-"])
            if values["-SIZE-"] in settings["GUI"]["sizes"].split("|"):
                settings["GUI"]["font_size"] = values["-SIZE-"]
            settings["FILE"]["assets_folder"] = values["IMAGES"]
            refresh_window(settings)
            window.close()
            main_window(settings, game)
            break

        if event == sg.WINDOW_CLOSED:
            window.close()
            break


def main_window(settings, game):

    if game.time_refresh():
        game.write_save("auto")
        print("autosave")
            
    menu_bar_definition = [["Menu", ["Configurações", "Sobre", "Save", "Load"]]]

    layout_main = [
        [sg.MenubarCustom(menu_bar_definition)],
        [sg.Text("Bem vindo a Mini Heimur!", justification="center")],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Image(f"_internal/assets/{game.region}.png"), sg.Push()],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Ações", size=(20, 4)),
            sg.Button("Personagem", size=(20, 4)),
            sg.Button("Loja", size=(20, 4)),
        ],
    ]

    window = sg.Window("Heimur Game 3.5", layout_main)
    while True:
        event, values = window.read()

        if event == "Loja":
            window.close()
            shop_window(settings, game)
            break

        if event == "Ações":
            window.close()
            action_window(settings, game)
            break

        if event == "Personagem":
            window.close()
            char_window(settings, game)
            break

        if event == "Sobre":
            window.disappear()
            sg.popup_no_titlebar(
                "Mini Heimur - Versão Simple GUI",
                "Inicio: 14/04/2024",
                "Obrigado por jogar!",
            )
            window.reappear()

        if event == "Configurações":
            window.close()
            settings_window(settings, game)
            break

        if event == "Save":
            window.close()
            save_window(settings, game)
            break

        if event == "Load":
            window.close()
            load_window(settings, game, "main")
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def shop_window(settings, game):

    def check_price(price: int, qnt: int = 1) -> bool:
        if game.inventory["money"] >= (price * qnt):
            game.inventory["money"] -= price * qnt
            window["Money"].update(f'H$: {game.inventory["money"]}')
            return True
        else:
            return False

    def get_price(item: str) -> int:
        if item == "potion":
            return 50
        elif item == "elixir":
            return 70
        elif item == "revive":
            return 500

    column_1 = [
        [sg.Button("Potion", size=(10, 1)), sg.Push(), sg.Text("H$50")],
        [sg.Button("Elixir", size=(10, 1)), sg.Push(), sg.Text("H$70")],
        [sg.Button("Revive", size=(10, 1)), sg.Push(), sg.Text("H$500")],
        [
            sg.Button("+Attack", size=(10, 1)),
            sg.Push(),
            sg.Text(f"H${30+30*game.bonus['atq']}", key="atq"),
        ],
        [
            sg.Button("+Defense", size=(10, 1)),
            sg.Push(),
            sg.Text(f"H${25+25*game.bonus['def']}", key="def"),
        ],
    ]

    column_2 = [
        [sg.Button("Lance", size=(10, 1)), sg.Push(), sg.Text("H$150")],
        [sg.Button("Sword", size=(10, 1)), sg.Push(), sg.Text("H$150")],
        [sg.Button("Bow", size=(10, 1)), sg.Push(), sg.Text("H$150")],
        [sg.Button("Revolver", size=(10, 1)), sg.Push(), sg.Text("H$150")],
        [sg.Button("Staff", size=(10, 1)), sg.Push(), sg.Text("H$150")],
        [sg.Button("Orb", size=(10, 1)), sg.Push(), sg.Text("H$150")],
    ]

    shop_layout = [
        [
            sg.Text("Bem Vindo a Loja do Viajante!"),
            sg.Push(),
            sg.Text(f'H$: {game.inventory["money"]}', key="Money"),
        ],
        [sg.HorizontalSeparator()],
        [sg.Column(column_1), sg.VerticalSeparator(), sg.Column(column_2)],
        [sg.HorizontalSeparator()],
        [
            sg.Text("Qnt:"),
            sg.Input("1", s=(5), key="Qnt"),
            sg.Push(),
            sg.Button("Sair", size=7),
        ],
    ]

    window = sg.Window("", shop_layout)
    while True:
        event, values = window.read()

        if event in ["+Attack", "+Defense"]:
            if event == "+Attack":
                base = 30
                ctrl = "atq"
            else:
                base = 25
                ctrl = "def"

            if check_price(base + base * game.bonus[ctrl]):
                game.bonus[ctrl] += 1
                window[ctrl].update(f"H${base+base*game.bonus[ctrl]}")
            else:
                sg.popup_no_titlebar("EI!", "Você não tem dinheiro suficiente!")

        if event in ["Lance", "Sword", "Revolver", "Bow", "Staff", "Orb"]:
            if event in game.weapons:
                sg.popup_no_titlebar(
                    "Ei, viajante!", "Você não pode carregar duas armas iguais!"
                )
            else:
                if check_price(150):
                    game.weapons.append(event)
                else:
                    sg.popup_no_titlebar("EI!", "Você não tem dinheiro suficiente!")

        if event in ["Potion", "Elixir", "Revive"]:
            item = event.lower()
            qnt = int(values["Qnt"])

            if check_price(get_price(item), qnt):
                game.inventory[item] += qnt
            else:
                sg.popup_no_titlebar("EI!", "Você não tem dinheiro suficiente!")

        if event == "Sair":
            window.close()
            main_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def action_window(settings, game):
    action_layout = [
        [sg.Text("Ações!")],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Descansar", size=(15, 3)),
            sg.Button("Caçar", size=(15, 3)),
            sg.Button("Harvest", size=(15, 3)),
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7), sg.Push(), sg.Button("Viajar", size=7)],
    ]

    window = sg.Window("", action_layout)
    while True:
        event, values = window.read()

        if event == "Descansar":
            ctrl = False
            while True:
                if game.check_xp():
                    print(True)
                    ctrl = True
                    game.comput_xp()
                else:
                    if game.status["level"] == 5 and (
                        "Fast Trigger" not in game.spell.spells_known
                        and "Zap" not in game.spell.spells_known
                        and "Charge" not in game.spell.spells_known
                    ):
                        sg.popup_no_titlebar("Você aprendeu uma magia nova!")
                        if game.path == "Ranger":
                            game.spell.spells_known.append("Fast Trigger")
                        elif game.path == "Guerreiro":
                            game.spell.spells_known.append("Charge")
                        elif game.path == "Mago":
                            game.spell.spells_known.append("Zap")
                    break
            window.close()
            if ctrl:
                put_points_window(settings, game)
            else:
                game.refresh_status()
                main_window(settings, game)
            break

        if event == "Harvest":
            window.close()
            harvest_window(settings, game)
            break

        if event == "Caçar":
            window.close()
            combat_window(settings, game)
            break

        if event == "Viajar":
            window.close()
            travel_window(settings, game)
            break

        if event == "Voltar":
            window.close()
            main_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def travel_window(settings, game):

    travel_layout = [
        [sg.Push(), sg.Text("Regiões de Heimur!"), sg.Push()],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Plains", size=(15, 2)),
            sg.Button("Viribus", size=(15, 2)),
            sg.Button("Prljav", size=(15, 2)),
        ],
        [
            sg.Button("East Land", size=(15, 2)),
            sg.Button("Auribus", size=(15, 2)),
            sg.Button("Nekrigi", size=(15, 2)),
        ],
        [sg.Push(), sg.Button("World's End", size=(20, 2)), sg.Push()],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Text(f'Level Atual: {game.status["level"]}')],
    ]

    window = sg.Window("", travel_layout)
    while True:
        event, values = window.read()

        if event == "Plains":
            window.close()
            game.region = "plains"
            main_window(settings, game)
            break

        if event == "Viribus":
            if game.status["level"] >= 15:
                if "viribus" in game.regions_to_travel:
                    window.close()
                    game.region = "viribus"
                    main_window(settings, game)
                    break
                else:
                    sg.popup_no_titlebar(
                        "Guerreiro!", "Voce necessita matar o Boss anterior!"
                    )
            else:
                sg.popup_no_titlebar(
                    "Ei!", "Você precisa ter nível 15 para acessar essa região!"
                )

        if event == "Prljav":
            if game.status["level"] >= 50:
                if "prljav" in game.regions_to_travel:
                    window.close()
                    game.region = "prljav"
                    main_window(settings, game)
                    break
                else:
                    sg.popup_no_titlebar(
                        "Guerreiro!", "Voce necessita matar o Boss anterior!"
                    )
            else:
                sg.popup_no_titlebar(
                    "Ei!", "Você precisa ter nível 50 para acessar essa região!"
                )

        if event == "East Land":
            if game.status["level"] >= 70:
                if "east" in game.regions_to_travel:
                    window.close()
                    game.region = "east"
                    main_window(settings, game)
                    break
                else:
                    sg.popup_no_titlebar(
                        "Guerreiro!", "Voce necessita matar o Boss anterior!"
                    )
            else:
                sg.popup_no_titlebar(
                    "Ei!", "Você precisa ter nível 70 para acessar essa região!"
                )

        if event == "Auribus":
            if game.status["level"] >= 50:
                if "auribus" in game.regions_to_travel:
                    window.close()
                    game.region = "auribus"
                    main_window(settings, game)
                    break
                else:
                    sg.popup_no_titlebar(
                        "Guerreiro!", "Voce necessita matar o Boss anterior!"
                    )
            else:
                sg.popup_no_titlebar(
                    "Ei!", "Você precisa ter nível 125 para acessar essa região!"
                )

        if event == "Nekrigi":
            if game.status["level"] >= 50:
                if "nekrigi" in game.regions_to_travel:
                    window.close()
                    game.region = "nekrigi"
                    main_window(settings, game)
                    break
                else:
                    sg.popup_no_titlebar(
                        "Guerreiro!", "Voce necessita matar o Boss anterior!"
                    )
            else:
                sg.popup_no_titlebar(
                    "Ei!", "Você precisa ter nível 160 para acessar essa região!"
                )

        if event == sg.WIN_CLOSED:
            window.close()
            break


def harvest_window(settings, game):

    harvest_chance = (
        game.atributes["for"]
        + game.atributes["des"]
        + game.atributes["con"]
        + game.atributes["int"]
    )

    col_1 = [
        [sg.Button("Minerar", size=15, key="mine")],
        [sg.Text("Pedra:"), sg.Text(f'{game.materials["stone"]}', key="stone")],
        [sg.Text("Ferro"), sg.Text(f'{game.materials["iron"]}', key="iron")],
        [sg.HorizontalSeparator()],
        [sg.Button("Coletar", size=15, key="gather")],
        [sg.Text("Graveto"), sg.Text(f'{game.materials["sticks"]}', key="sticks")],
        [sg.Text("Madeira"), sg.Text(f'{game.materials["wood"]}', key="wood")],
    ]

    col_2 = [
        [sg.Button("Buscar", size=15, key="search")],
        [sg.Text("Fruta:"), sg.Text(f'{game.materials["berries"]}', key="berries")],
        [
            sg.Text("Morango:"),
            sg.Text(f'{game.materials["strawberries"]}', key="strawberries"),
        ],
        [
            sg.Text("Erva:"),
            sg.Text(f'{game.materials["green_herb"]}', key="green_herb"),
        ],
        [
            sg.Text("Erva Azul:"),
            sg.Text(f'{game.materials["blue_herb"]}', key="blue_herb"),
        ],
    ]

    harvest_layout = [
        [sg.Text("Harvest!")],
        [sg.HorizontalSeparator()],
        [sg.Text(f"Chance de Colheita: {harvest_chance}%")],
        [sg.Text("", key="got")],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1), sg.VerticalSeparator(), sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7)],
    ]

    window = sg.Window("", harvest_layout)
    while True:
        event, values = window.read()

        if event in ["mine", "gather", "search"]:
            if game.roll_harvest_chance():
                rs = game.get_resources(event)
                print(rs)
                window["got"].update(f"Você conseguiu {rs[1]} {rs[0]}!")
                window[f"{rs[0]}"].update(f'{game.materials[f"{rs[0]}"]}')
            else:
                window["got"].update(f"Você não encontrou nada!")

        if event == "Voltar":
            window.close()
            action_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def combat_window(settings, game):

    def turno_player(temp_atk_bonus=0, temp_dmg_bonus=0):
        rolagem = game.roll(20)
        window["ROL"].update(rolagem)
        ataque = rolagem + game.status["atq"] + game.bonus["atq"] + temp_atk_bonus
        defesa = game.roll(20) + game.monster["def"]
        pt_crit = defesa + 15
        if ataque >= pt_crit:
            sg.popup_no_titlebar("Você Acertou um Crítico!!!")
            dano = 2 * (game.status["level"] + game.status["base_dmg"] + temp_dmg_bonus)
        elif ataque > defesa:
            sg.popup_no_titlebar("Você Acertou o Ataque!")
            dano = game.roll(game.status["level"]) + game.status["base_dmg"] + temp_dmg_bonus
        else:
            sg.popup_no_titlebar("Você Errou o Ataque!")
            dano = 0

        game.monster["current_hp"] -= dano
        window["dmg c"].update(dano)
        window["permonster"].update(
            f'{game.get_hp_percent(game.monster["current_hp"],game.monster["max_hp"])}%'
        )

    def turno_inimigo():
        rolagem = game.roll(20)
        ataque = rolagem + game.monster["atq"]
        defesa = game.roll(20) + game.status["def"] + game.bonus["def"]
        pt_crit = defesa + 16
        if ataque > pt_crit:
            sg.popup_no_titlebar("Você Recebeu um Crítico!!!")
            dano = 2 * (game.monster["level"] + game.monster["dmg"])
        elif ataque > defesa:
            sg.popup_no_titlebar("Você Recebeu um Ataque!")
            dano = game.roll(game.monster["level"]) + game.monster["dmg"]
        else:
            sg.popup_no_titlebar("Você Defendeu o Ataque!")
            dano = 0

        game.status["current_hp"] -= dano
        window["dmg r"].update(dano)
        window["perplayer"].update(
            f'{game.get_hp_percent(game.status["current_hp"],game.status["max_hp"])}%'
        )

    def drop_loot():
        loot = game.get_loot()
        window.close()
        sg.popup_no_titlebar(
            "Você recebeu:", f"{loot[0]} H$", f"{loot[1]} XP", f"{loot[2]} Fragmentos"
        )
        if game.monster["title"] == "Boss":
            boss_loot = game.get_boss_drop(game.monster["name"])
            sg.popup_no_titlebar(
                "Parabéns pela vitória!",
                "Uma nova região foi liberada.",
                f"Você conseguiu: {boss_loot}!!!",
            )
        main_window(settings, game)

    def filter_effects(spell):
        if spell == "Fast Trigger":
            turno_player()
            turno_player()
            if game.monster["current_hp"] > 0:
                turno_inimigo()
            else:
                drop_loot()

        elif spell == "Charge":
            turno_player(game.status["level"] * 2)
            if game.monster["current_hp"] > 0:
                turno_inimigo()
            else:
                drop_loot()

        elif spell == "Rebuke":
            dano = game.status["base_dmg"] * game.roll(4)
            heal = game.status["level"] + game.atributes["int"]
            game.heal("hp", heal)
            window["perplayer"].update(
                f'{game.get_hp_percent(game.status["current_hp"],game.status["max_hp"])}%'
            )
            sg.popup_no_titlebar("Você invocou a Retribuição!",f"{heal} Pontos de vida curados.")

            game.monster["current_hp"] -= dano
            window["dmg c"].update(dano)
            window["permonster"].update(
                f'{game.get_hp_percent(game.monster["current_hp"],game.monster["max_hp"])}%'
            )
            
            if game.monster["current_hp"] > 0:
                turno_inimigo()
            else:
                drop_loot()

        elif spell == "Zap":
            dano = game.status["level"] * game.roll(8)
            sg.popup_no_titlebar("Você conjurou Zap!")

            game.monster["current_hp"] -= dano
            window["dmg c"].update(dano)
            window["permonster"].update(
                f'{game.get_hp_percent(game.monster["current_hp"],game.monster["max_hp"])}%'
            )

        elif spell == "Heal":
            heal = (game.atributes["int"] - game.atributes["con"]) * game.rol(5)
            window["perplayer"].update(
                f'{game.get_hp_percent(game.status["current_hp"],game.status["max_hp"])}%'
            )
            game.heal("hp")
            sg.popup_no_titlebar("Você cura suas feridas utilizando sua magia!",f"{heal} pontos curados!")

        elif spell == "Fireworks":
            turno_player(game.atributes["des"] / 4, 3 * game.roll(10))
            if game.monster["current_hp"] > 0:
                turno_inimigo()
            else:
                drop_loot()

    game.get_monster(game.region)

    col_1 = [
        [
            sg.Text(
                f'{game.get_hp_percent(game.status["current_hp"],game.status["max_hp"])}%',
                k="perplayer",
            )
        ],
        [sg.Image("_internal/assets/char.png")],
        [sg.Text(f'Level {game.status["level"]}')],
    ]

    col_2 = [
        [
            sg.Push(),
            sg.Text("Ameaça: "),
            sg.Text(f'{game.monster["danger_level"]}'),
            sg.Push(),
        ],
        [sg.Push(), sg.Text("Rolagem:"), sg.Push()],
        [sg.Push(), sg.Text("0", k="ROL"), sg.Push()],
        [sg.Push(), sg.Text("Dano Causado:"), sg.Push()],
        [sg.Push(), sg.Text("0", k="dmg c"), sg.Push()],
        [sg.Push(), sg.Text("Dano Recebido:"), sg.Push()],
        [sg.Push(), sg.Text("0", k="dmg r"), sg.Push()],
    ]

    col_3 = [
        [
            sg.Push(),
            sg.Text(
                f'{game.get_hp_percent(game.monster["current_hp"],game.monster["max_hp"])}%',
                k="permonster",
            ),
        ],
        [sg.Image(f"_internal/assets/{game.monster['name']}.png")],
        [sg.Push(), sg.Text(f'Level {game.monster["level"]}')],
    ]

    combat_layout = [
        [sg.Text("Combate!"), sg.Push(), sg.Text(f"{game.monster['title']}")],
        [sg.HorizontalSeparator()],
        [
            sg.Column(col_1),
            sg.VerticalSeparator(),
            sg.Column(col_2),
            sg.VerticalSeparator(),
            sg.Column(col_3),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Push(),
            sg.Button("Lutar", size=10),
            sg.Button("Itens", size=10),
            sg.Button("Libra", size=10),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.Button("Magias", size=10),
            sg.Button("Fugir", size=10),
            sg.Push(),
        ],
        [sg.HorizontalSeparator()],
    ]

    window = sg.Window("", combat_layout)
    while True:
        event, values = window.read()

        if game.status["current_hp"] <= 0:
            sg.popup_no_titlebar("Você foi derrotado!")
            window.close()
            if game.inventory["revive"] > 0:
                game.inventory["revive"] -= 1
                main_window(settings, game)
            break

        if event == "Itens":
            if itens_window(settings, game):
                turno_inimigo()
            window["perplayer"].update(
                f'{game.get_hp_percent(game.status["current_hp"],game.status["max_hp"])}%'
            )

        if event == "Lutar":
            turno_player()
            if game.monster["current_hp"] > 0:
                turno_inimigo()
            else:
                drop_loot()
                break

        if event == "Magias":
            spell = use_spells_window(settings, game)
            if spell:
                filter_effects(spell)

        if event == "Fugir":
            if game.status["level"] <= 2 or game.scape(game):
                window.close()
                action_window(settings, game)
                break
            else:
                sg.popup_no_titlebar("Você não conseguiu fugir!")

        if event == sg.WIN_CLOSED:
            window.close()
            break


def use_spells_window(settings, game) -> str:
    use_spells_layout = [
        [sg.Push(), sg.Text("Magias Equipadas"), sg.Push()],
        [sg.HorizontalSeparator()],
        [
            sg.Button(f"{game.spell.spells_equiped['slot_1'][0]}", size=(15)),
            sg.Button(f"{game.spell.spells_equiped['slot_2'][0]}", size=(15)),
        ],
        [
            sg.Push(),
            sg.Text(f"{game.spell.spells_equiped['slot_1'][2]}MP"),
            sg.Push(),
            sg.Text(f"{game.spell.spells_equiped['slot_2'][2]}MP"),
            sg.Push(),
        ],
        [sg.Text("")],
        [
            sg.Push(),
            sg.Text(
                f'{game.get_hp_percent(game.status["current_mana"],game.status["max_mana"])}%'
            ),
            sg.Push(),
        ],
    ]

    window = sg.Window("", use_spells_layout)
    ctrl = True
    while ctrl:
        event, values = window.read()
        print(event)

        if event == f"{game.spell.spells_equiped['slot_1'][0]}":
            cost = game.spell.spells_equiped["slot_1"][2]
            if game.spell.check_mana(game, cost):
                game.status["current_mana"] -= cost
                window.close()
                ctrl = False
                return event
            else:
                sg.popup_no_titlebar("Ei!", "Você está sem mana para isso!")
                window.close()
                break

        if event == f"{game.spell.spells_equiped['slot_2'][0]}":
            cost = game.spell.spells_equiped["slot_2"][2]
            if game.spell.check_mana(game, cost):
                game.status["current_mana"] -= cost
                window.close()
                ctrl = False
                return event
            else:
                sg.popup_no_titlebar("Ei!", "Você está sem mana para isso!")
                window.close()
                break

        if event == sg.WIN_CLOSED or event == "-None-":
            window.close()
            ctrl = False
            return None


def itens_window(settings, game):
    itens_layout = [
        [sg.Text("Itens na bolsa")],
        [sg.HorizontalSeparator()],
        [sg.Button("Potion", size=(15, 1)), sg.Text(game.inventory["potion"])],
        [sg.Button("Elixir", size=(15, 1)), sg.Text(game.inventory["elixir"])],
        [
            sg.Button("Boss Signal", size=(15, 1)),
            sg.Text(game.inventory["boss_signal"]),
        ],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Button("Fechar", size=(10, 1))],
    ]

    window = sg.Window("", itens_layout)
    while True:
        event, values = window.read()

        if event == "Potion":
            if game.inventory["potion"] <= 0:
                sg.popup_no_titlebar("Sem Poções!")
            else:
                game.inventory["potion"] -= 1
                game.heal("hp")

        if event == "Elixir":
            if game.inventory["elixir"] <= 0:
                sg.popup_no_titlebar("Sem Elixires!")
            else:
                game.inventory["elixir"] -= 1
                game.heal("mana")

        if event == "Boss Signal":
            if game.inventory["boss_signal"] >= 5:
                game.inventory["boss_signal"] -= 5
                game.boss_next = True
                if game.monster["name"] in ["Boar"]:
                    game.special_boss = game.monster["name"]
                sg.popup_no_titlebar(
                    "Você jogou o sinalizador...", "Ele está a caminho."
                )
            else:
                sg.popup_no_titlebar(
                    "É Necessário 5 Sinalizadores",
                    "para convocar o Boss.",
                    "Obtenha mais derrotando Mini Bosses!",
                )
            window.close()
            break

        if event == sg.WINDOW_CLOSED:
            window.close()
            break

        if event:
            window.close()
            if event in ["Elixir"]:
                return True
            else:
                break


def char_window(settings, game):
    char_layout = [
        [sg.Text("Personagem!")],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Text(game.path), sg.Push()],
        [sg.Push(), sg.Text(game.pathdesc()), sg.Push()],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Inventário", size=(15, 3)),
            sg.Button("Status", size=(15, 3)),
            sg.Button("Magias", size=(15, 3)),
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7), sg.Push(), sg.Button("Cheats", size=7)],
    ]

    window = sg.Window("", char_layout)
    while True:
        event, values = window.read()

        if event == "Cheats":
            window.close()
            cheats_window(settings, game)
            break

        if event == "Magias":
            window.close()
            spell_window(settings, game)
            break

        if event == "Status":
            window.close()
            status_window(settings, game)
            break

        if event == "Inventário":
            window.close()
            inventory_window(settings, game)
            break

        if event == "Voltar":
            window.close()
            main_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def cheats_window(settings, game):

    col_1 = [
        [sg.Button("potion", size=10)],
        [sg.Button("revive", size=10)],
        [sg.Button("materials", size=10)],
    ]

    col_2 = [
        [sg.Button("elixir", size=10)],
        [sg.Button("100 money", size=10)],
        [sg.Button("1000 money", size=10)],
        [sg.Button("100 xp", size=10)],
    ]

    cheats_layout = [
        [sg.Text("CHEATS!!!!")],
        [sg.HorizontalSeparator()],
        [sg.Text("Usuário: "), sg.Input(size=11, key="user")],
        [sg.HorizontalSeparator()],
        [sg.Column(col_1), sg.Column(col_2)],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7)],
    ]

    window = sg.Window("", cheats_layout)
    while True:
        event, values = window.read()

        if values["user"] in game.users_cheats:
            print("Usuário Válidado!!!")
            if event == "100 xp":
                game.status["current_xp"] += 99
            if event in ["potion", "elixir", "revive"]:
                game.inventory[f"{event}"] += 15
            if event == "100 money":
                game.inventory["money"] += 100
            if event == "1000 money":
                game.inventory["money"] += 1000
            if event == "materials":
                game.materials["sticks"] += 50
                game.materials["wood"] += 50
                game.materials["stone"] += 50
                game.materials["iron"] += 50
                game.materials["green_herb"] += 50
                game.materials["blue_herb"] += 50
                game.materials["berries"] += 50
                game.materials["strawberries"] += 50

        if event == "Voltar":
            window.close()
            char_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def spell_window(settings, game):
    spell_layout = [
        [sg.Text("Magias!")],
        [sg.HorizontalSeparator()],
        [sg.Text("Spell Slot 01:")],
        [
            sg.Text("Spell Name:"),
            sg.Push(),
            sg.Text(game.spell.spells_equiped["slot_1"][0]),
        ],
        [sg.Text(game.spell.spells_equiped["slot_1"][1])],
        [sg.Text(f"Custo: {game.spell.spells_equiped['slot_1'][2]}")],
        [sg.HorizontalSeparator()],
        [sg.Text("Spell Slot 02:")],
        [
            sg.Text("Spell Name:"),
            sg.Push(),
            sg.Text(game.spell.spells_equiped["slot_2"][0]),
        ],
        [sg.Text(game.spell.spells_equiped["slot_2"][1])],
        [sg.Text(f"Custo: {game.spell.spells_equiped['slot_2'][2]}")],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7), sg.Push(), sg.Button("Trocar", size=7)],
    ]

    window = sg.Window("", spell_layout)
    while True:
        event, values = window.read()

        if event == "Voltar":
            window.close()
            char_window(settings, game)
            break

        if event == "Trocar":
            window.close()
            change_spells_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def change_spells_window(settings, game):
    change_spells_layout = [
        [sg.Text("Magias!")],
        [sg.HorizontalSeparator()],
        [sg.Text("Obtidas:")],
        [sg.Multiline(size=(15, 8), key="Main")],
        [sg.HorizontalSeparator()],
        [sg.Text("Escolha:")],
        [sg.Input(game.spell.spells_equiped["slot_1"][0], key="choice_1", s=15)],
        [sg.Input(game.spell.spells_equiped["slot_2"][0], key="choice_2", s=15)],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7), sg.Button("Trocar", size=7)],
    ]

    window = sg.Window("", change_spells_layout, finalize=True)
    window["Main"].update(game.spell.read_spells())
    while True:
        event, values = window.read()

        if event == "Trocar":
            if values["choice_1"] and values["choice_2"] in game.spell.spells_known:
                game.spell.spells_equiped["slot_1"] = (
                    values["choice_1"],
                    game.spell.get_desc(values["choice_1"]),
                    game.spell.get_cost(values["choice_1"]),
                )
                game.spell.spells_equiped["slot_2"] = (
                    values["choice_2"],
                    game.spell.get_desc(values["choice_2"]),
                    game.spell.get_cost(values["choice_2"]),
                )
                sg.popup_no_titlebar(
                    "Você trocou para:",
                    f'{values["choice_1"]}',
                    f'{values["choice_2"]}',
                )
                window.close()
                main_window(settings, game)
                break
            else:
                sg.popup_no_titlebar("EI!!!", "Você não possui essa magia!")

        if event == "Voltar":
            window.close()
            spell_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def status_window(settings, game):

    atributes_1 = [
        [sg.Text("Força:")],
        [sg.Text("Destreza:")],
        [sg.Text("Constituição:")],
        [sg.Text("Inteligência:")],
    ]

    atributes_2 = [
        [sg.Text(f'{game.atributes["for"]}')],
        [sg.Text(f'{game.atributes["des"]}')],
        [sg.Text(f'{game.atributes["con"]}')],
        [sg.Text(f'{game.atributes["int"]}')],
    ]

    others_1 = [
        [sg.Text("+Ataque:")],
        [sg.Text("+Defesa:")],
        [sg.Text("+Dano:")],
        [sg.Text("Vida:")],
        [sg.Text("Mana:")],
        [sg.Text("Exp:")],
        [sg.Text("Level:")],
    ]

    others_2 = [
        [sg.Text(f"{game.status['atq']}")],
        [sg.Text(f"{game.status['def']}")],
        [sg.Text(f"{game.status['base_dmg']}")],
        [sg.Text(f"{game.status['current_hp']}/{game.status['max_hp']}")],
        [sg.Text(f"{game.status['current_mana']}/{game.status['max_mana']}")],
        [sg.Text(f"{game.status['current_xp']}/{game.status['max_xp']}")],
        [sg.Text(f"{game.status['level']}")],
    ]

    bonus_1 = [
        [sg.Text("Ataque")],
        [sg.Text("Defesa")],
        [sg.Text("Cura")],
        [sg.Text("Colheita")],
    ]

    bonus_2 = [
        [sg.Text(f'{game.bonus["atq"]}(+)')],
        [sg.Text(f'{game.bonus["def"]}(+)')],
        [sg.Text(f'{game.bonus["healing"]}(*)')],
        [sg.Text(f'{game.bonus["harvest"]}(*)')],
    ]

    master_1 = [
        [sg.Push(), sg.Text("Atributos:"), sg.Push()],
        [sg.Column(atributes_1), sg.Column(atributes_2)],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Text("Outros:"), sg.Push()],
        [sg.Column(others_1), sg.Column(others_2)],
    ]

    master_2 = [
        [sg.Push(), sg.Text("Bônus:"), sg.Push()],
        [sg.Column(bonus_1), sg.Column(bonus_2)],
    ]

    stts_layout = [
        [
            sg.Text("Estatísticas!"),
            sg.Push(),
            sg.Text(f'Arma: {game.inventory["eq_weapon"]}'),
        ],
        [sg.HorizontalSeparator()],
        [sg.Column(master_1), sg.VerticalSeparator(), sg.Column(master_2)],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7)],
    ]

    window = sg.Window("", stts_layout)
    while True:
        event, values = window.read()

        if event == "Voltar":
            window.close()
            char_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def inventory_window(settings, game):

    materials_1 = [
        [sg.Text("Pedra")],
        [sg.Text("Ferro")],
        [sg.Text("Graveto")],
        [sg.Text("Madeira")],
        [sg.Text("Erva Verde")],
        [sg.Text("Erva Azul")],
        [sg.Text("Frutinha")],
        [sg.Text("Morangos")],
    ]

    materials_2 = [
        [sg.Text(f'{game.materials["stone"]}')],
        [sg.Text(f'{game.materials["iron"]}')],
        [sg.Text(f'{game.materials["sticks"]}')],
        [sg.Text(f'{game.materials["wood"]}')],
        [sg.Text(f'{game.materials["green_herb"]}')],
        [sg.Text(f'{game.materials["blue_herb"]}')],
        [sg.Text(f'{game.materials["berries"]}')],
        [sg.Text(f'{game.materials["strawberries"]}')],
    ]

    itens_1 = [
        [sg.Text("Fragmentos")],
        [sg.Text("Revives")],
        [sg.Text("Poção")],
        [sg.Text("Elixir")],
        [sg.Text("Boss Signal")],
    ]

    itens_2 = [
        [sg.Text(f'{round(game.inventory["shard"],2)}')],
        [sg.Text(f'{game.inventory["revive"]}')],
        [sg.Text(f'{game.inventory["potion"]}')],
        [sg.Text(f'{game.inventory["elixir"]}')],
        [sg.Text(f'{game.inventory["boss_signal"]}')],
    ]

    master_1 = [
        [sg.Push(), sg.Text("Materiais:"), sg.Push()],
        [sg.Column(materials_1), sg.Column(materials_2)],
    ]

    master_2 = [
        [sg.Push(), sg.Text("Itens:"), sg.Push()],
        [sg.Column(itens_1), sg.Column(itens_2)],
    ]

    inv_layout = [
        [sg.Text("Inventário!"), sg.Push(), sg.Text(f'{game.inventory["money"]} H$')],
        [sg.HorizontalSeparator()],
        [sg.Column(master_1), sg.VerticalSeparator(), sg.Column(master_2)],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Voltar", size=7),
            sg.Push(),
            sg.Button("Armas", size=7),
            sg.Push(),
            sg.Button("Craft", size=7),
        ],
    ]

    window = sg.Window("", inv_layout)
    while True:
        event, values = window.read()

        if event == "Armas":
            window.close()
            weapons_window(settings, game)
            break

        if event == "Craft":
            window.close()
            craft_window(settings, game)
            break

        if event == "Voltar":
            window.close()
            char_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def craft_window(settings, game):
    select = "Potion"

    craft_layout = [
        [sg.Text("Crafting!")],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Potion", size=(7, 1)),
            sg.Push(),
            sg.Text("5 Ervas A, 15 Ervas, 2 Frutas"),
        ],
        [
            sg.Button("Elixir", size=(7, 1)),
            sg.Push(),
            sg.Text("20 Ervas A, 7 Ervas, 3 Morangos"),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Text(f"Item: {select}", key="item"),
            sg.Push(),
            sg.Text("Qnt:"),
            sg.Input("1", s=(5, 1), key="Qnt"),
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7), sg.Push(), sg.Button("Fazer", size=7)],
    ]

    window = sg.Window("", craft_layout)
    while True:
        event, values = window.read()

        if event in ["Potion", "Elixir"]:
            select = event
            window["item"].update(f"Item: {select}")

        if event == "Fazer":
            select = select.lower()
            qnt = values["Qnt"]
            if game.check_materials(select, qnt):
                game.inventory[f"{select}"] += int(qnt)
            else:
                sg.popup_no_titlebar(
                    "Sem Recursos suficientes para fazer",
                    f"{qnt} {select.capitalize()}!!!",
                )

        if event == "Voltar":
            window.close()
            inventory_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def weapons_window(settings, game):
    weapons_layout = [
        [sg.Text("Armas!")],
        [sg.HorizontalSeparator()],
        [sg.Text("Obtidas:")],
        [sg.Multiline(size=(15, 8), key="Main")],
        [sg.HorizontalSeparator()],
        [sg.Text("Escolha:")],
        [sg.Input(game.inventory["eq_weapon"], key="choice", s=15)],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=7), sg.Button("Trocar", size=7)],
    ]

    window = sg.Window("", weapons_layout, finalize=True)
    window["Main"].update(game.read_weapons())
    while True:
        event, values = window.read()

        if event == "Trocar":
            if values["choice"] in game.weapons:
                game.inventory["eq_weapon"] = values["choice"]
                game.weapon_status(values["choice"])
                sg.popup_no_titlebar("Você trocou para:", f'{values["choice"]}')
                window.close()
                main_window(settings, game)
                break
            else:
                sg.popup_no_titlebar("EI!!!", "Você não possui essa arma!")

        if event == "Voltar":
            window.close()
            inventory_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def starter_window(settings, game):
    starter_layout = [
        [sg.Push(), sg.Text("Bem vindo, novo aventureiro!!!"), sg.Push()],
        [sg.Push(), sg.Text("Por favor, escolha um caminho:"), sg.Push()],
        [
            sg.Push(),
            sg.Button("Guerreiro", s=10),
            sg.Push(),
            sg.Button("Ranger", s=10),
            sg.Push(),
            sg.Button("Mago", s=10),
            sg.Push(),
        ],
        [sg.HorizontalSeparator()],
        [sg.Image("_internal/assets/Threeway.png")],
        [sg.HorizontalSeparator()],
    ]

    window = sg.Window("", starter_layout)
    while True:
        event, values = window.read()

        if event in ["Guerreiro", "Ranger", "Mago"]:
            game.path = event
            weapon = game.init_weapon(event)
            game.inventory["eq_weapon"] = weapon
            game.weapons.append(weapon)
            sg.popup_no_titlebar("Sua arma inicial é:", f"{weapon}")
            window.close()
            put_points_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def welcome_window(settings, game):

    def fail_load(num, back):
        window.close()
        sg.popup_no_titlebar(
            "Ei!", "Impossível carregar!", f"Não existe dado salvo no slot {num}"
        )
        if back == "welcome":
            welcome_window(settings, game)
        elif back == "main":
            main_window(settings, game)

    def return_load(num):
        window.close()
        sg.popup_no_titlebar("Certo!", f"Carregando progresso do slot {num}...")
        main_window(settings, game)

    layout_welcome = [
        [
            sg.Push(),
            sg.Text("Heimur RPG", justification="center"),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.Text("Aventura virtual", justification="center"),
            sg.Push(),
        ],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Button("Novo Jogo", size=(20, 2)), sg.Push()],
        [sg.Push(), sg.Button("Carregar Jogo", size=(20, 2)), sg.Push()],
        [sg.Push(), sg.Button("Continuar", size=(20, 2)), sg.Push()],
        [sg.HorizontalSeparator()],
        [sg.Text("@catelanirocha   2024")],
    ]

    window = sg.Window("Primeira vez? Novo jogo!", layout_welcome)
    while True:
        event, values = window.read()

        if event == "Carregar Jogo":
            window.close()
            load_window(settings, game, "welcome")
            break

        if event == "Continuar":
            try:
                game.read_save("auto")
                return_load("automático")
            except:
                fail_load("automático", "welcome")
            break

        elif event == "Novo Jogo":
            window.close()
            starter_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def load_window(settings, game, back: str):

    def fail_load(num, back):
        window.close()
        sg.popup_no_titlebar(
            "Ei!", "Impossível carregar!", f"Não existe dado salvo no slot {num}"
        )
        if back == "welcome":
            welcome_window(settings, game)
        elif back == "main":
            main_window(settings, game)

    def return_load(num):
        window.close()
        sg.popup_no_titlebar("Certo!", f"Carregando progresso do slot {num}...")
        main_window(settings, game)

    save_1_lvl = game.settings["SAVES"].get("save_1_level")
    save_2_lvl = game.settings["SAVES"].get("save_2_level")
    save_3_lvl = game.settings["SAVES"].get("save_3_level")
    save_4_lvl = game.settings["SAVES"].get("save_4_level")

    save_1_path = game.settings["SAVES"].get("save_1_path")
    save_2_path = game.settings["SAVES"].get("save_2_path")
    save_3_path = game.settings["SAVES"].get("save_3_path")
    save_4_path = game.settings["SAVES"].get("save_4_path")

    column_1 = [
        [sg.Push(), sg.Button("Slot 1", size=(7, 1)), sg.Push()],
        [sg.Text(f"Nível:  {save_1_lvl}")],
        [sg.Text(f"Classe: {save_1_path.capitalize()}")],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Button("Slot 2", size=(7, 1)), sg.Push()],
        [sg.Text(f"Nível:  {save_2_lvl}")],
        [sg.Text(f"Classe: {save_2_path.capitalize()}")],
    ]

    column_2 = [
        [sg.Push(), sg.Button("Slot 3", size=(7, 1)), sg.Push()],
        [sg.Text(f"Nível:  {save_3_lvl}")],
        [sg.Text(f"Classe: {save_3_path.capitalize()}")],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Button("Slot 4", size=(7, 1)), sg.Push()],
        [sg.Text(f"Nível:  {save_4_lvl}")],
        [sg.Text(f"Classe: {save_4_path.capitalize()}")],
    ]

    layout_load = [
        [
            sg.Push(),
            sg.Text("Heimur RPG", justification="center"),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.Text("Carregar Jogo", justification="center"),
            sg.Push(),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Push(),
            sg.Column(column_1),
            sg.VerticalSeparator(),
            sg.Column(column_2),
            sg.Push(),
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=(10, 1)), sg.Push()],
    ]

    window = sg.Window("Load Game", layout_load)
    while True:
        event, values = window.read()

        if event in ["Slot 1", "Slot 2", "Slot 3", "Slot 4"]:
            num = int(event[5])
            # try:
            game.read_save(num)
            return_load(num)
            # except:
            #     fail_load(num, back)
            break

        if event == "Voltar":
            window.close()
            if back == "welcome":
                welcome_window(settings, game)
            elif back == "main":
                main_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def save_window(settings, game):

    def return_save(num):
        window.close()
        sg.popup_no_titlebar("Certo!", f"Progresso salvo no slot {num}")
        main_window(settings, game)

    save_1_lvl = game.settings["SAVES"].get("save_1_level")
    save_2_lvl = game.settings["SAVES"].get("save_2_level")
    save_3_lvl = game.settings["SAVES"].get("save_3_level")
    save_4_lvl = game.settings["SAVES"].get("save_4_level")

    save_1_path = game.settings["SAVES"].get("save_1_path")
    save_2_path = game.settings["SAVES"].get("save_2_path")
    save_3_path = game.settings["SAVES"].get("save_3_path")
    save_4_path = game.settings["SAVES"].get("save_4_path")

    column_1 = [
        [sg.Push(), sg.Button("Slot 1", size=(7, 1)), sg.Push()],
        [sg.Text(f"Nível:  {save_1_lvl}")],
        [sg.Text(f"Classe: {save_1_path.capitalize()}")],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Button("Slot 2", size=(7, 1)), sg.Push()],
        [sg.Text(f"Nível:  {save_2_lvl}")],
        [sg.Text(f"Classe: {save_2_path.capitalize()}")],
    ]

    column_2 = [
        [sg.Push(), sg.Button("Slot 3", size=(7, 1)), sg.Push()],
        [sg.Text(f"Nível:  {save_3_lvl}")],
        [sg.Text(f"Classe: {save_3_path.capitalize()}")],
        [sg.HorizontalSeparator()],
        [sg.Push(), sg.Button("Slot 4", size=(7, 1)), sg.Push()],
        [sg.Text(f"Nível:  {save_4_lvl}")],
        [sg.Text(f"Classe: {save_4_path.capitalize()}")],
    ]

    layout_load = [
        [
            sg.Push(),
            sg.Text("Heimur RPG", justification="center"),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.Text("Salvar Jogo", justification="center"),
            sg.Push(),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Push(),
            sg.Column(column_1),
            sg.VerticalSeparator(),
            sg.Column(column_2),
            sg.Push(),
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Voltar", size=(10, 1)), sg.Push()],
    ]

    window = sg.Window("Save Game", layout_load)
    while True:
        event, values = window.read()

        if event in ["Slot 1", "Slot 2", "Slot 3", "Slot 4"]:
            num = int(event[5])
            game.write_save(num)
            return_save(num)
            break

        if event == "Voltar":
            window.close()
            main_window(settings, game)
            break

        if event == sg.WIN_CLOSED:
            window.close()
            break


def create_settings(game: object):
    settings_path = Path.cwd()
    settings = sg.UserSettings(
        path=settings_path,
        filename="_internal/config.ini",
        use_config_file=True,
        convert_bools_and_none=False,
    )

    refresh_window(settings)
    welcome_window(settings, game)