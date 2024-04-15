import random as rd
from configparser import ConfigParser

class Game():

    settings = ConfigParser()
    settings.read('_internal/config.ini')

    initialized = settings["GAME"]["init"]
    atributes = {'for': 0,'des': 0,'con': 0,'int': 0,'current_points': 12}
    status = {'xp_max': 0,'current_xp': 0,'max_hp': 0,'current_hp': 0,'max_mana': 0,'current_mana': 0,'lvl': 1}
    inventory = {'money': 0,'potion': 5,'elixir': 2,'revive': 1}
    materials = {'sticks': 0,'wood': 0,'iron': 0,'stone': 0,'green_herb': 0,'blue_herb': 0,'berries': 0,'strawberries': 0}
    bonus = {'harvest': 1,'healing': 1}

    users_cheats = ['commando_11','beta_tester']

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

        qnt = rd.randint(1,self.status["lvl"]) * self.bonus['harvest']

        self.materials[f"{resource}"] += qnt
        return [resource,qnt]