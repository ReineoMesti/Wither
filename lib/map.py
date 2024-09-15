import tkinter as tk
from tkinter import ttk
import copy
'''
to_import = {"display":"disp", "expandrandom":"exrand", "debug":"dbg",
             "fileio":"fio"}
for module, newname in to_import.items():
    try:
        exec('import '+module+' as '+newname)
    except ModuleNotFoundError:
        exec('import lib.'+module+' as '+newname)
'''
import lib.display as disp
import lib.expandrandom as exrand
import lib.debug as dbg
import lib.fileio as fio

type_ascii = {'empty': ' ', 'field': '.', 'forest': '*', 'wall':'#',
              'water': '~', 'shallow': '~', 'beacon':'O', 'obstruction':'x', 'ruin':'%',
              'factory':'F', 'resident': 'H', 'military': 'B', 'storage':'W'}
SELF_SYMBOL = '@'
mapsize = (15,15)
totalsize = (100, 100)

mainmap = []
def movecost(pos, dx, dy):
    return {'stamnia':10}

def reachable(x, y):
    if x<0 or y<0 or x>=totalsize[0] or y>=totalsize[1]:
        return False
    return True

class facility:
    def __init__(self, name):
        self.name = name
class block:
    def __init__(self, tp, name, desc_index, attr_comm, attr_spec):
        self.type = tp
        self.name = name
        self.text_index = desc_index
        self.common = attr_comm
        self.special = attr_spec
        self.content = []
    def spawn_facility(self):
        tp = self.type
        if tp == 'field':
            count = exrand.polynominal_linear(4, 4, 11)
            for i in range(count):
                self.content.append(facility('Grass'))


# -------- Functions controlling blocks' visibility ----------
roundview = lambda x, y: x**2+y**2<=25

# -------- Map Display Part ----------
class map_page(disp.display_page):
    def __init__(self, master, text:str, position:list, viewfunc):
        global totalsize, mapsize
        disp.display_page.__init__(self, master, text)
        self.viewrule = viewfunc
        self.position = position
        self.map = None
        self.map_bar = tk.LabelFrame(self.page)
        self.map_bar.grid(row=0,column=0,padx=5,pady=5)
        self.map_desc_bar = tk.Frame(self.page)
        self.map_desc_bar.grid(row=0,column=1,padx=5,pady=5)
        self.map_content = [[tk.StringVar() for i in range(mapsize[0])] for j in range(mapsize[1])]
        self.map_field = [[tk.Label(self.map_bar, textvariable=self.map_content[i][j], font='fixedsys')
                      for i in range(mapsize[0])] for j in range(mapsize[1])]
        for j in range(mapsize[1]):
            for i in range(mapsize[0]):
                self.map_field[i][j].grid(column=i, row=j,padx=2,pady=2)
                self.map_content[i][j].set('.')
        self.move_operate_bar = tk.Frame(self.page)
        self.move_operate_bar.grid(row=1,column=0,padx=5,pady=5)
        move_button_text = ['left', 'right', 'up', 'down']
        move_direction = ((0,-1),(0,1),(-1,0),(1,0))
        self.move_button = [tk.Button(self.move_operate_bar, text=move_button_text[i], width=9)
                       for i in range(4)]
        move_button_grid = [(1,0),(1,2),(0,1),(2,1)]
        for i in range(4):
            self.move_button[i].grid(row=move_button_grid[i][0], column=move_button_grid[i][1], padx=5,pady=5)
        self.desc_title = tk.StringVar()
        self.desc_content = tk.StringVar()
        self.map_desc_title = tk.Label(self.map_desc_bar, textvariable=self.desc_title)
        self.map_desc_content = tk.Label(self.map_desc_bar, textvariable=self.desc_content)
        self.map_desc_title.pack(anchor='n')
        self.map_desc_content.pack(anchor='n')
        self.move_bind_command = None
        self.move_cost_check = None
    def move_bind(self, command):
        self.move_bind_command = command
    def move_cost_check_bind(self, command):
        self.move_cost_check = command
    def spawn_map(self):
        global totalsize
        self.map = []
        for i in range(totalsize[1]):
            self.map.append([])
            for j in range(totalsize[0]):
                self.map[i].append(block('field', 'Empty field', 0, dict(), dict()))       
    def repaint_map(self):
        global mapsize
        border_dist_x = (mapsize[0] + 1) // 2 - 1
        border_dist_y = (mapsize[1] + 1) // 2 - 1
        x_left = self.position[0] - border_dist_x
        y_up = self.position[1] - border_dist_y
        matrix = [[' '] * mapsize[1] for u in range(mapsize[0])]
        for y in range(mapsize[1]):
            for x in range(mapsize[0]):
                if not (x+x_left>=0 and x+x_left<totalsize[0]
                    and y+y_up>=0 and y+y_up<totalsize[1]):
                    continue
                visible = self.viewrule(x-(mapsize[0]+1)//2+1, y-(mapsize[1]+1)//2+1)
                if visible:
                    if (x+x_left, y+y_up)==tuple(self.position):
                        matrix[x][y] = SELF_SYMBOL
                    else:
                        matrix[x][y] = type_ascii[self.map[x+x_left][y+y_up].type]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                self.map_content[i][j].set(matrix[i][j])
    def flush_move_button_state(self):
        assert callable(self.move_cost_check)
        playerpos = self.position
        move_direction = ((0,-1),(0,1),(-1,0),(1,0))
        for i in range(4):
            if (not reachable(playerpos[0]+move_direction[i][0],
                              playerpos[1]+move_direction[i][1])) \
            or not self.move_cost_check(self.position, *move_direction[i]):
                self.move_button[i].config(state='disabled')
            else:
                self.move_button[i].config(state='normal')
    def move(self, dx, dy, repaint = True):
        'Move towards a certain direction (x+=dx, y+=dy)'
        if reachable(self.position[0]+dx, self.position[1]+dy):
            self.position[0] += dx
            self.position[1] += dy
            if repaint:
                self.repaint_map()
                self.flush_move_button_state()
            if self.move_bind_command != None:
                try:
                    self.move_bind_command(copy.deepcopy(self.position), dx, dy)
                except:
                    dbg.error(__name__, 'map moving binded command calling error')
                    raise
    def get_ready(self):
        self.spawn_map()
        move_command = (lambda:self.move(0,-1),lambda:self.move(0,1),lambda:self.move(-1,0),lambda:self.move(1,0))
        for i in range(4):
            self.move_button[i].config(command=copy.deepcopy(move_command[i]))
    def get_position(self):
        return tuple(self.position)
