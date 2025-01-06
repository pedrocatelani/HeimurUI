import random as rd
from configparser import ConfigParser


class Game:
    regions_value = [["plains", 1], ["viribus", 2]]

    settings = ConfigParser()
    settings.read("_internal/config.ini")
    monsters = ConfigParser()
    monsters.read("_internal/monsters.ini")

    region = "plains"
    regions_to_travel = ["plains"]
    boss_next = False
    boss_status = {
        "plains": 0,
        "viribus": 0,
        "prljav": 0,
        "east": 0,
        "auribus": 0,
        "nekrigi": 0,
    }

    path = ""
    spell = None
    atributes = {"for": 0, "des": 0, "con": 0, "int": 0, "current_points": 12}
    status = {
        "max_xp": 0,
        "current_xp": 0,
        "max_hp": 0,
        "current_hp": 0,
        "max_mana": 0,
        "current_mana": 0,
        "level": 1,
        "atq": 0,
        "def": 0,
        "base_dmg": 0,
    }
    inventory = {
        "money": 0,
        "shard": 0,
        "potion": 5,
        "elixir": 2,
        "revive": 1,
        "eq_weapon": "",
        "boss_signal": 0,
    }
    materials = {
        "sticks": 0,
        "wood": 0,
        "iron": 0,
        "stone": 0,
        "green_herb": 0,
        "blue_herb": 0,
        "berries": 0,
        "strawberries": 0,
    }
    bonus = {"harvest": 1, "healing": 1, "atq": 0, "def": 0, "money": 0}
    monster = {
        "name": "",
        "max_hp": 0,
        "current_hp": 0,
        "def": 0,
        "atq": 0,
        "dmg": 0,
        "level": 0,
        "special": 0,
        "super_special": 0,
        "mult_money": 0,
        "mult_xp": 0,
        "mult_shard": 0,
        "danger_level": 0,
        "title": "",
    }

    users_cheats = ["commando_11", "beta_tester"]
    weapons = []

    from .saves import write_save, read_save

    def pathdesc(self) -> str:
        if self.path == "Ranger":
            return "Bonûs de colheita"
        elif self.path == "Guerreiro":
            return "Cura HP pós batalhas"
        elif self.path == "Mago":
            return "Cura MP pós batalhas"

    def refresh_status(self):
        self.status["max_xp"] = 11 + (self.status["level"] * 3)
        self.status["max_hp"] = 2 * (self.atributes["con"]) + self.status["level"]
        self.status["current_hp"] = self.status["max_hp"]
        self.status["max_mana"] = 2 * (self.atributes["int"]) + self.status["level"]
        self.status["current_mana"] = self.status["max_mana"]

    def check_points(self, str, des, con, intel):
        atr_for = int(str)
        atr_des = int(des)
        atr_con = int(con)
        atr_int = int(intel)
        soma = atr_for + atr_des + atr_con + atr_int

        if soma == self.atributes["current_points"]:
            return True
        else:
            return False

    def add_points(self, str, des, con, intel):
        self.atributes["for"] += int(str)
        self.atributes["des"] += int(des)
        self.atributes["con"] += int(con)
        self.atributes["int"] += int(intel)
        self.atributes["current_points"] = 0
        self.refresh_status()

    def roll_harvest_chance(self):
        chance = rd.randint(1, 100)
        if chance <= (
            self.atributes["for"]
            + self.atributes["des"]
            + self.atributes["con"]
            + self.atributes["int"]
        ):
            return True
        else:
            return False

    def get_resources(self, type: str) -> list:
        if type == "mine":
            resource = rd.choice(["stone", "iron"])
        if type == "gather":
            resource = rd.choice(["sticks", "wood"])
        if type == "search":
            resource = rd.choice(["green_herb", "blue_herb", "berries", "strawberries"])

        qnt = rd.randint(1, self.status["level"]) * self.bonus["harvest"]
        if self.path == "Ranger":
            qnt += self.status["level"]

        self.materials[f"{resource}"] += qnt
        return [resource, qnt]

    def get_monster_level(self) -> int:
        monster_level = rd.randint(
            (self.status["level"] - 3), (self.status["level"] + 3)
        )
        if monster_level < 1 or self.status["level"] == 1:
            monster_level = 1
        return monster_level

    def get_monster(self, local: str):
        mst = rd.choice(self.monsters["LIST"][f"{local}"].split("|"))
        if self.boss_next:
            mst = f"{self.region.capitalize()}Boss"
            self.boss_next = False

        self.monster["name"] = mst
        self.monster["level"] = self.get_monster_level()
        self.monster["danger_level"] = int(self.monsters[f"{mst}"]["danger"])
        self.monster["max_hp"] = (
            int(self.monsters[f"{mst}"]["hp"]) * self.monster["level"]
        )
        self.monster["current_hp"] = self.monster["max_hp"]
        self.monster["def"] = float(self.monsters[f"{mst}"]["def"]) + (
            self.monster["level"] / 2 + self.monster["danger_level"]
        )
        self.monster["atq"] = float(self.monsters[f"{mst}"]["atq"]) + (
            self.monster["level"] / 2 + self.monster["danger_level"]
        )
        self.monster["dmg"] = int(self.monsters[f"{mst}"]["dmg"])
        self.monster["special"] = int(self.monsters[f"{mst}"]["sp"])
        self.monster["super_special"] = int(self.monsters[f"{mst}"]["xsp"])
        self.monster["mult_money"] = float(self.monsters[f"{mst}"]["din"])
        self.monster["mult_xp"] = float(self.monsters[f"{mst}"]["exp"])
        self.monster["mult_shard"] = float(self.monsters[f"{mst}"]["shard"])
        self.monster["title"] = self.monsters[f"{mst}"]["title"]
        print(self.monster)

    def get_hp_percent(self, current, total) -> float:
        percent = int(current) / int(total)
        percent *= 100
        percent = round(percent, 2)
        return percent

    def roll(self, dice: int):
        return rd.randint(1, dice)

    def scape(self, object: object) -> bool:
        bonus = 0
        if object.status["level"] < 10:
            bonus = 15 * object.monster["danger_level"]

        rolagem = object.roll(100)

        print("Rolagem: ", rolagem + bonus)
        print(f'Meta: {95-object.atributes["des"]}')
        if (rolagem + bonus) >= (95 - object.atributes["des"]):
            return True
        else:
            return False

    def init_weapon(self, classe: str):
        if classe == "Guerreiro":
            weapons = ("Sword", "Lance")
        elif classe == "Ranger":
            weapons = ("Bow", "Revolver")
        elif classe == "Mago":
            weapons = ("Staff", "Orb")

        return rd.choice(weapons)

    def weapon_status(self, weapon: str):

        # Basic Weapons

        if weapon == "Sword":
            self.status["atq"] = (self.atributes["des"] / 2) + (
                self.status["level"] / 4
            )
            self.status["def"] = self.atributes["con"] / 2
            self.status["base_dmg"] = self.atributes["for"] / 2
        elif weapon == "Lance":
            self.status["atq"] = self.atributes["des"] / 2
            self.status["def"] = (self.atributes["con"] / 4) + (
                self.atributes["des"] / 4
            )
            self.status["base_dmg"] = (
                (self.atributes["for"] / 4)
                + (self.atributes["des"] / 4)
                + (self.status["level"] / 2)
            )
        elif weapon == "Bow":
            self.status["atq"] = (self.atributes["des"] / 4) + (
                self.status["level"] / 4
            )
            self.status["def"] = (self.atributes["con"] / 4) + (
                self.atributes["des"] / 4
            )
            self.status["base_dmg"] = (self.atributes["des"] / 2) + (
                self.status["level"] / 4
            )
        elif weapon == "Revolver":
            self.status["atq"] = (self.atributes["des"] / 2) + (
                self.status["level"] / 4
            )
            self.status["def"] = (self.atributes["con"] / 4) + (
                self.atributes["des"] / 4
            )
            self.status["base_dmg"] = self.atributes["des"] / 2
        elif weapon == "Staff":
            self.status["atq"] = self.atributes["des"] / 2
            self.status["def"] = self.atributes["con"] / 2
            self.status["base_dmg"] = self.atributes["int"] / 2
        elif weapon == "Orb":
            self.status["atq"] = (self.atributes["des"] / 4) + (
                self.atributes["int"] / 4
            )
            self.status["def"] = self.atributes["con"] / 4
            self.status["base_dmg"] = (self.atributes["int"] / 2) + (
                self.status["level"] / 4
            )

        # Plain Weapons

        elif weapon == "Great Sword":
            self.status["atq"] = self.atributes["for"] / 2
            self.status["def"] = (self.atributes["con"] / 4) + (
                self.atributes["for"] / 2
            )
            self.status["base_dmg"] = self.atributes["for"] / 2
        elif weapon == "Riffle":
            self.status["atq"] = (self.atributes["des"] / 2) + (
                self.status["level"] / 4
            )
            self.status["def"] = (self.atributes["con"] / 2) + (
                self.atributes["des"] / 4
            )
            self.status["base_dmg"] = (self.atributes["des"] / 2) + (
                self.status["level"] / 4
            )
        elif weapon == "Wand":
            self.status["atq"] = self.atributes["des"] / 2
            self.status["def"] = self.atributes["con"] / 2
            self.status["base_dmg"] = (self.atributes["int"] / 2) + (
                self.status["level"] / 4
            )

    def read_weapons(self) -> str:
        weapons_string = ""
        for w in self.weapons:
            weapons_string += f"{w} \n"

        return weapons_string

    def check_barriers(self) -> bool:
        if self.status["level"] == 15 and self.boss_status["plains"] == 0:
            return True
        elif self.status["level"] == 50 and self.boss_status["viribus"] == 0:
            return True
        elif self.status["level"] == 70 and self.boss_status["prljav"] == 0:
            return True
        elif self.status["level"] == 125 and self.boss_status["east"] == 0:
            return True
        elif self.status["level"] == 150 and self.boss_status["auribus"] == 0:
            return True
        elif self.status["level"] == 160 and self.boss_status["nekrigi"] == 0:
            return True

    def get_loot(self) -> tuple:
        shard = 0
        money = (rd.randint(1, 16) + self.bonus["money"]) * self.monster["mult_money"]
        exp = (rd.randint(1, 10) + self.monster["level"]) * self.monster["mult_xp"]
        rol = rd.randint(1, 100)

        if self.monster["title"] == "Mini Boss":
            bonus = 0
            for region in self.regions_value:
                if region[0] == self.region:
                    if region[1] < len(self.regions_to_travel):
                        bonus = 30

            print("Mini Boss Killed")
            signal = rd.randint(1, 100)
            print(signal)
            if signal <= 60 + bonus:
                self.inventory["boss_signal"] += 1

        if self.monster["title"] == "Boss":
            self.boss_status[self.region] += 1

        print("Shard drop % :", rol)
        if rol <= 20:
            shard = rd.randint(1, 5) * self.monster["mult_shard"]
            round(shard, 2)

        if self.check_barriers():
            exp = 0

        # Travas de nivel
        if self.status["level"] >= 15 and self.boss_status["plains"] == 0:
            exp = 0

        self.inventory["money"] += money
        self.inventory["shard"] += shard
        self.status["current_xp"] += exp

        # Passivas de classe:
        if self.path == "Mago":
            self.heal("mana")
        if self.path == "Guerreiro":
            self.heal("hp")

        return (money, exp, shard)

    def get_boss_drop(self, name: str) -> str:
        drop_pool = []
        ctrl = True
        self.ranger_drops = {"spell": ["Fireworks"], "weapon": ["Riffle"]}
        self.warrior_drops = {"spell": ["Rebuke"], "weapon": ["Great Sword"]}
        self.mage_drops = {"spell": ["Heal"], "weapon": ["Wand"]}

        if name == "PlainsBoss":
            boss = "plains"
            drop_pool = ["Fireworks", "Rebuke", "Heal", "Great Sword", "Riffle", "Wand"]
            if "viribus" not in self.regions_to_travel:
                self.regions_to_travel.append("viribus")
        elif name == "ViribusBoss":
            boss = "viribus"
            drop_pool = []
            if "prljav" not in self.regions_to_travel:
                self.regions_to_travel.append("prljav")

        loot = rd.choice(drop_pool)
        drops = getattr(self, f"{self.path.lower()}_drops")
        print("CHEGUEI AQUI")
        while ctrl:
            print(drops)
            print(loot)
            if self.boss_status[boss] >= 3 and (
                loot not in drops["spell"] and loot not in drops["weapon"]
            ):
                loot = rd.choice(drop_pool)
            else:
                ctrl = False

        if self.path == "Ranger" and loot in self.ranger_drops["spell"]:
            if loot not in self.spell.spells_known:
                self.spell.spells_known.append(loot)
        elif self.path == "Ranger" and loot in self.ranger_drops["weapon"]:
            if loot not in self.weapons:
                self.weapons.append(loot)
        if self.path == "Mago" and loot in self.mage_drops["spell"]:
            if loot not in self.spell.spells_known:
                self.spell.spells_known.append(loot)
        elif self.path == "Mago" and loot in self.mage_drops["weapon"]:
            if loot not in self.weapons:
                self.weapons.append(loot)
        if self.path == "Guerreiro" and loot in self.warrior_drops["spell"]:
            if loot not in self.spell.spells_known:
                self.spell.spells_known.append(loot)
        elif self.path == "Guerreiro" and loot in self.warrior_drops["weapon"]:
            if loot not in self.weapons:
                self.weapons.append(loot)

        return loot

    def check_xp(self) -> bool:
        if self.status["current_xp"] >= self.status["max_xp"]:
            return True
        else:
            return False

    def comput_xp(self):
        self.status["current_xp"] -= self.status["max_xp"]
        self.status["level"] += 1
        self.atributes["current_points"] += 3
        self.status["max_xp"] = 11 + (self.status["level"] * 3)

    def heal(self, type: str, mod: float = None):
        if not mod:
            mod = (rd.randint(1, 7) * self.bonus["healing"]) + self.status["level"]
        self.status[f"current_{type}"] += mod
        if self.status[f"current_{type}"] > self.status[f"max_{type}"]:
            self.status[f"current_{type}"] = self.status[f"max_{type}"]

    def check_materials(self, item: str, qnt: str):
        qnt = int(qnt)

        if item == "potion":
            if (
                self.materials["green_herb"] >= 15 * qnt
                and self.materials["blue_herb"] >= 5 * qnt
                and self.materials["berries"] >= 2 * qnt
            ):
                self.materials["green_herb"] -= 15 * qnt
                self.materials["blue_herb"] -= 5 * qnt
                self.materials["berries"] -= 2 * qnt
                return True
            else:
                return False

        elif item == "elixir":
            if (
                self.materials["green_herb"] >= 7 * qnt
                and self.materials["blue_herb"] >= 20 * qnt
                and self.materials["strawberries"] >= 3 * qnt
            ):
                self.materials["green_herb"] -= 7 * qnt
                self.materials["blue_herb"] -= 20 * qnt
                self.materials["strawberries"] -= 3 * qnt
                return True
            else:
                return False
