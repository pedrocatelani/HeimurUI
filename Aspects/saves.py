import json


def write_save(self, num: int):
    print(f"NUMERO: {num}")
    save = {
        "path": self.path,
        "region": self.region,
        "regions_to_travel": self.regions_to_travel,
        "boss_next": self.boss_next,
        "boss_status": self.boss_status,
        "status": self.status,
        "inventory": self.inventory,
        "atributes": self.atributes,
        "materials": self.materials,
        "bonus": self.bonus,
        "weapons": self.weapons,
        "spells_known": self.spell.spells_known,
        "spells_equiped": self.spell.spells_equiped,
    }

    with open(f"_internal\saves\save{num}.json", "w") as savefile:
        json.dump(save, savefile)

    with open("_internal\config.ini", "w") as configfile:
        lvl = f"save_{num}_level"
        path = f"save_{num}_path"
        self.settings["SAVES"][lvl] = str(self.status["level"])
        self.settings["SAVES"][path] = self.path
        self.settings.write(configfile)


def read_save(self, num: int):
    with open(f"_internal\saves\save{num}.json") as savefile:
        save_data = json.load(savefile)

        self.path = save_data["path"]
        self.region = save_data["region"]
        self.regions_to_travel = save_data["regions_to_travel"]
        self.boss_next = save_data["boss_next"]
        self.boss_status = save_data["boss_status"]
        self.status = save_data["status"]
        self.inventory = save_data["inventory"]
        self.atributes = save_data["atributes"]
        self.materials = save_data["materials"]
        self.bonus = save_data["bonus"]
        self.weapons = save_data["weapons"]
        self.spell.spells_known = save_data["spells_known"]
        self.spell.spells_equiped = save_data["spells_equiped"]
        
    savefile.close()