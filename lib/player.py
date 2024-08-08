import tkinter as tk
from tkinter import ttk

to_import = {'fileio':'fio', 'debug':'dbg'}
for module, newname in to_import.items():
    try:
        exec('import '+module+' as '+newname)
    except ModuleNotFoundError:
        exec('import lib.'+module+' as '+newname)

effect_map = fio.get_effect_map_instruction()

class player_state_core:
    def __init__(self, stamnia_max, thirsty_max, hunger_max,
                 health_max, position):
        self.stamnia_max = stamnia_max
        self.thirsty_max = thirsty_max
        self.hunger_max = hunger_max
        self.health_max = health_max
        self.stamnia = stamnia_max
        self.thirsty = thirsty_max
        self.hunger = hunger_max
        self.health = health_max
        self.buff = dict()
        self.pos = pos
    def consumable(self, option, value):
        try:
            val = getattr(self, option)
            if val >= value:
                return True
            return False
        except:
            dbg.error('player.py', 'consumability check error')
    def consume(self, option, value, atomic=True):
        try:
            assert atomic > 0
            if atomic:
                if not self.consumable(option, value):
                    dbg.error('player.py', 'unchecked call at `consume`')
                    return False
            else:
                value = min(value, getattr(self, option))
            setattr(self, getattr(option)-value)
        except:
            dbg.error('player.py', 'consumption process error')
class player:
    def __init__(self, **kw)
    
