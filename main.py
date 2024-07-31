from ui import create_settings
from Aspects.game import Game
from Aspects.spells import Spells

game = Game()
spells = Spells()

game.spell = spells

create_settings(game)