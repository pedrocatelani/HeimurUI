import random as rd
from configparser import ConfigParser

class Game():

    settings = ConfigParser()
    settings.read('_internal/config.ini')
    monsters = ConfigParser()
    monsters.read('_internal/monsters.ini')

    region = 'plains'
    initialized = settings["GAME"]["init"]
    atributes = {'for': 0,'des': 0,'con': 0,'int': 0,'current_points': 12}
    status = {'max_xp': 0,'current_xp': 0,'max_hp': 0,'current_hp': 0,'max_mana': 0,'current_mana': 0,'level': 1,'atq': 0,'def': 0,'base_dmg': 0}
    inventory = {'money': 0,'shard': 0,'potion': 5,'elixir': 2,'revive': 1,'eq_weapon': ''}
    materials = {'sticks': 0,'wood': 0,'iron': 0,'stone': 0,'green_herb': 0,'blue_herb': 0,'berries': 0,'strawberries': 0}
    bonus = {'harvest': 1,'healing': 1,'atq': 0,'def': 0,'money': 0}
    monster = {'name':'','max_hp': 0,'current_hp': 0,'def': 0,'atq': 0,'dmg': 0,'level': 0,'special': 0,'super_special': 0,'mult_money': 0,'mult_xp': 0,'mult_shard': 0,'danger_level': 0}

    users_cheats = ['commando_11','beta_tester']
    weapons =  []

    def refresh_status(self):
        self.status["max_xp"]  = 11 + (self.status["level"] * 3) 
        self.status["max_hp"] = 2 * (self.atributes["con"]) + self.status["level"]
        self.status["current_hp"] = self.status["max_hp"]
        self.status["max_mana"] = 2 * (self.atributes["int"]) + self.status["level"]
        self.status["current_mana"] = self.status["max_mana"]

    def check_points(self,str,des,con,intel):
        atr_for = int(str)
        atr_des = int(des)
        atr_con = int(con)
        atr_int = int(intel)
        soma = atr_for + atr_des + atr_con + atr_int

        if soma == self.atributes["current_points"]:
            return True
        else:
            return False
        
    def add_points(self,str,des,con,intel):
        self.atributes["for"] += int(str)
        self.atributes["des"] += int(des)
        self.atributes["con"] += int(con)
        self.atributes["int"] += int(intel)
        self.atributes["current_points"] = 0
        self.refresh_status()

    def roll_harvest_chance(self):
        chance = rd.randint(1,100)
        if chance <= (self.atributes["for"] + self.atributes["des"] + self.atributes["con"] + self.atributes["int"]):
            return True
        else:
            return False
        
    def get_resources(self,type:str) -> list:
        if type == 'mine':
            resource = rd.choice(['stone','iron'])
        if type == 'gather':
            resource = rd.choice(['sticks','wood'])
        if type == 'search':
            resource = rd.choice(['green_herb','blue_herb','berries','strawberries'])

        qnt = rd.randint(1,self.status["level"]) * self.bonus['harvest']

        self.materials[f"{resource}"] += qnt
        return [resource,qnt]
    
    def get_monster_level(self):
        monster_level = rd.randint((self.status["level"]- 3),(self.status["level"]+ 3))
        if monster_level < 1 or self.status["level"] == 1:
            monster_level = 1
        return monster_level

    def get_monster(self,local):
        mst = rd.choice(self.monsters["LIST"][f'{local}'].split("|"))
        self.monster["name"] = mst
        self.monster["level"] = self.get_monster_level()
        self.monster["danger_level"] = int(self.monsters[f"{mst}"]["danger"])
        self.monster["max_hp"] = int(self.monsters[f"{mst}"]["hp"]) * self.monster["level"]
        self.monster["current_hp"] = self.monster["max_hp"]
        self.monster["def"] = float(self.monsters[f"{mst}"]["def"]) + (self.monster["level"] / 2 + self.monster["danger_level"])
        self.monster["atq"] = float(self.monsters[f"{mst}"]["atq"]) + (self.monster["level"] / 2 + self.monster["danger_level"])
        self.monster["dmg"] = int(self.monsters[f"{mst}"]["dmg"])
        self.monster["special"] = int(self.monsters[f"{mst}"]["sp"])
        self.monster["super_special"] = int(self.monsters[f"{mst}"]["xsp"])
        self.monster["mult_money"] = float(self.monsters[f"{mst}"]["din"])
        self.monster["mult_xp"] = float(self.monsters[f"{mst}"]["exp"])
        self.monster["mult_shard"] = float(self.monsters[f"{mst}"]["shard"])
        print(self.monster)

    def get_hp_percent(self,current,total):
        percent = int(current) / int(total)
        percent *= 100
        percent = round(percent,2)
        return percent

    def roll(self,dice:int):
        return rd.randint(1,dice)
    
    def scape(self):
        bonus = 0
        if self.status["level"] < 10:
            bonus = 15 * self.monster["danger_level"]
        
        rolagem = self.roll(100)
        if rolagem + bonus >= 90 - self.atributes["des"]:
            return True
        else:
            return False
        
    def init_weapon(self,classe:str):
        if classe == 'Guerreiro':
            weapons = ('Sword','Lance')
        elif classe == 'Ranger':
            weapons = ('Bow','Revolver')
        elif classe == 'Mago':
            weapons = ('Staff','Orb')

        return rd.choice(weapons)

    def weapon_status(self,weapon:str):
        if weapon == 'Sword':
            self.status["atq"] = self.atributes["des"] / 2
            self.status["def"] = self.atributes["con"] / 2
            self.status["base_dmg"] = self.atributes["for"] / 2
        elif weapon == 'Lance':
            self.status["atq"] = self.atributes["des"] / 2
            self.status["def"] = (self.atributes["con"] / 4) + (self.atributes["des"]/4)
            self.status["base_dmg"] = (self.atributes["for"] / 4) + (self.atributes["des"]/4)
        elif weapon == 'Bow':
            self.status["atq"] = (self.atributes["des"] / 4) + (self.status["level"] / 4)
            self.status["def"] = (self.atributes["con"] / 4) + (self.atributes["des"]/4)
            self.status["base_dmg"] = (self.atributes["des"] / 2) + (self.status["level"] / 4)
        elif weapon == 'Revolver':
            self.status["atq"] = (self.atributes["des"] / 2) + (self.status["level"] / 4)
            self.status["def"] = (self.atributes["con"] / 4) + (self.atributes["des"]/4)
            self.status["base_dmg"] = (self.atributes["des"] / 2)
        elif weapon == 'Staff':
            self.status["atq"] = (self.atributes["des"] / 2) 
            self.status["def"] = (self.atributes["con"] / 2) 
            self.status["base_dmg"] = (self.atributes["int"] / 2)
        elif weapon == 'Orb':
            self.status["atq"] = (self.atributes["des"] / 4) + (self.atributes["int"] / 4)
            self.status["def"] = (self.atributes["con"] / 4) 
            self.status["base_dmg"] = (self.atributes["int"] / 2) + (self.status["level"] / 4)

    def read_weapons(self) -> str:
        weapons_string = ''
        for w in self.weapons:
            weapons_string += f'{w} \n'
        
        return weapons_string

    def get_loot(self) -> tuple:
        shard = 0
        money = (rd.randint(1,16) + self.bonus["money"]) * self.monster["mult_money"]
        exp = (rd.randint(1,10) + self.monster["level"]) * self.monster["mult_xp"]
        if rd.randint(1,100) > 17:
            shard = (rd.randint(1,5) * self.monster["mult_shard"])

        self.inventory["money"] += money    
        self.inventory["shard"] += shard   
        self.status["current_xp"] += exp    
        
        return (money,exp,shard)

    def check_xp(self) -> bool:
        if self.status["current_xp"] >= self.status["max_xp"]:
            return True
        else:
            return False

    def comput_xp(self):
        self.status["current_xp"] -= self.status["max_xp"]
        self.status["level"] += 1
        self.atributes["current_points"] += 3
        self.status["max_xp"]  = 11 + (self.status["level"] * 3) 
