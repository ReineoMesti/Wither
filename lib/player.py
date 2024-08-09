import tkinter as tk
from tkinter import ttk

to_import = {'fileio':'fio', 'debug':'dbg', 'display':'disp'}
for module, newname in to_import.items():
    try:
        exec('import '+module+' as '+newname)
    except ModuleNotFoundError:
        exec('import lib.'+module+' as '+newname)

#effect_map = fio.get_effect_map_instruction()

STAMNIA = 'stamnia'
THIRSTY = 'thirsty'
HUNGER = 'hunger'
HEALTH = 'health'
POS = 'pos'

class player_core:
    def __init__(self, stamnia_max, thirsty_max, hunger_max, health_max, pos):
        # POSITION is NOT in use. This attribute actually exist in map module.
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
        self.move_cost_query_command = None
    def consumable(self, attribute, value):
        try:
            val = getattr(self, attribute)
            if val >= value:
                return True
            return False
        except:
            dbg.error('player.py', 'consumability check error')
    def consume(self, attribute, value, atomic=True):
        'Consume given attribute. If `atomic` option is switched on, \
        the operate will be either completely executed or completely failed,\
        otherwise the call will consume all the remain resource if the \
        object doesn\'t have enough.'
        try:
            if atomic:
                if not self.consumable(attribute, value):
                    dbg.error(__name__, 'unchecked call at `consume`')
                    return False
            else:
                value = min(value, getattr(self, attribute))
            setattr(self, attribute, getattr(self, attribute)-value)
        except AttributeError:
            dbg.error(__name__, 'consumption error, attr %s'%attribute)
            return False
        return True
    def replenish(self, attribute, value, atomic=False):
        'Replenish given attribute.'
        try:
            if not atomic or getattr(self, attribute) + value <= getattr(self, attribute+'_max'):
                setattr(self, attribute, min(getattr(self, attribute + '_max'), getattr(self, attribute) + value))
                return True
            else:
                return False
        except:
            dbg.error(__name__, 'replenish process error')
            return False
    def move_consumability_check(self, position, dx, dy):
        assert callable(self.move_cost_query_command)
        cost = self.move_cost_query_command(position, dx, dy)
        for attr in cost.keys():
            if not self.consumable(attr, cost[attr]):
                return False
        return True
    def move_consume(self, position, dx, dy):
        if not self.move_consumability_check(position, dx, dy):
            return
        cost = self.move_cost_query_command(position, dx, dy)
        for attr in cost.keys():
            self.consume(attr, cost[attr])
class status_page(disp.display_page):
    def __init__(self, master, text, stamnia_max, thirsty_max, hunger_max, health_max, position):
        disp.display_page.__init__(self, master, text)
        self.core = player_core(stamnia_max, thirsty_max, hunger_max, health_max, position)
        self.buff_bar = tk.LabelFrame(self.page, text='Effect')
        self.buff_bar.pack(fill=tk.BOTH, padx=5, pady=5)
        self.attr_bar = tk.LabelFrame(self.page, text='Attribute')
        self.attr_bar.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        self.attr_labels = dict()
        self.attr_tuple = ('stamnia', 'thirsty', 'hunger', 'health')
        for attr in self.attr_tuple:
            self.attr_labels[attr] = {'name':tk.Label(self.attr_bar, text=attr),
                                      'value':tk.Label(self.attr_bar,text='0')}
        row = 0
        for pair in self.attr_labels.values():
            pair['name'].grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
            pair['value'].grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)
            row += 1
        self.flush()
    def flush(self):
        for attr in self.attr_tuple:
            self.attr_labels[attr]['value'].config(text=str(getattr(self.core, attr)))
    def affect(self, effect, last):
        raise dbg.UnimplementError()
    def move_consumability_check(self, pos, dx, dy):
        return self.core.move_consumability_check(pos, dx, dy)
    def move_consume(self, pos, dx, dy):
        self.core.move_consume(pos, dx, dy)
        self.flush()
    
