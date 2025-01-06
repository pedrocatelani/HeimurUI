class Spells:

    spells_known = ["-None-"]
    spells_equiped = {
        "slot_1": ("-None-", "No Description", 0),
        "slot_2": ("-None-", "No Description", 0),
    }

    def read_spells(self) -> str:
        spells_string = ""
        for spell in self.spells_known:
            spells_string += f"{spell} \n"

        return spells_string

    def get_desc(self, spell_name: str) -> str:
        if spell_name == "-None-":
            return "No Description"
        elif spell_name == "Fast Trigger":
            return "Atire duas vezes seguidas!"
        elif spell_name == "Charge":
            return "Performe um ataque com bônus."
        elif spell_name == "Zap":
            return "Pule o turno do inimigo, eletrucutando-o"

    def get_cost(self, spell_name: str) -> float:
        if spell_name == "-None-":
            return 0
        elif spell_name == "Fast Trigger":
            return 2
        elif spell_name == "Charge":
            return 3.5
        elif spell_name == "Zap":
            return 5

    def check_mana(self, game: object, cost: float) -> bool:
        if game.status["current_mana"] >= cost:
            return True
        else:
            return False
