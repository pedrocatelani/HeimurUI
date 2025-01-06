class Spells:

    spells_known = ["-None-"]
    spells_equiped = {
        "slot_1": ("-None-", "No Description", 0),
        "slot_2": ("-None-", "No Description", 0),
    }

    spells = [
        ["-None-", 0, "No Description"],
        ["Fast Trigger", 2, "Atire duas vezes seguidas!"],
        ["Charge", 3.5, "Perfome um ataque com bônus."],
        ["Zap", 6, "Pule o turno do inimigo, eletrucutando-o"],
        ["Fireworks", 10, "Um último 'tchau tchau'!"],
        ["Rebuke", 10, "Cure-se um pouco enquanto ataca."],
        ["Heal", 15, "Revitalizar-se."],
    ]

    def read_spells(self) -> str:
        spells_string = ""
        for spell in self.spells_known:
            spells_string += f"{spell} \n"

        return spells_string

    def get_desc(self, spell_name: str) -> str:
        for spell in self.spells:
            if spell[0] == spell_name:
                return spell[2]

    def get_cost(self, spell_name: str) -> float:
        for spell in self.spells:
            if spell[0] == spell_name:
                return spell[1]

    def check_mana(self, game: object, cost: float) -> bool:
        if game.status["current_mana"] >= cost:
            return True
        else:
            return False
