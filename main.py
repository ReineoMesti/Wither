import tkinter as tk
from tkinter import ttk
import lib.map as mps
import lib.item as its
import lib.debug as debug
import lib.fileio as fio
import lib.player as plr

rootwin = tk.Tk()
rootwin.title('Demo Winter')

font_fs = 'fixedsys'
black = 'black'

left_bar = tk.Frame(rootwin)
midleft_bar = tk.Frame(rootwin)
midright_bar = ttk.Notebook(rootwin)
right_bar = tk.Frame(rootwin)

left_bar.pack(side=tk.LEFT, fill = tk.BOTH, padx=5, pady=8)
midleft_bar.pack(side=tk.LEFT, fill = tk.BOTH, padx=5, pady=8)
midright_bar.pack(side=tk.LEFT, fill = tk.BOTH, padx=5, pady=8)
right_bar.pack(side=tk.LEFT, fill = tk.BOTH, padx=5, pady=8)

status_bar = plr.status_page(left_bar, 'Status', 500, 100, 100, 100, [5,5])
status_bar.core.move_cost_query_command = mps.movecost
status_bar.pack(padx=8, pady=8)

map_page = mps.map_page(midleft_bar, 'Map', status_bar.core.pos, mps.roundview)
map_page.move_bind(status_bar.move_consume)
map_page.move_cost_check_bind(status_bar.move_consumability_check)
map_page.get_ready()
map_page.pack(padx=8)

midright_bar_bag_page = tk.Frame()
midright_bar_craft_page = tk.Frame()
midright_bar_block_page = tk.Frame()
midright_bar.add(midright_bar_bag_page, text='Bag')
midright_bar.add(midright_bar_craft_page, text='Craft')
midright_bar.add(midright_bar_block_page, text='Location')

player_bag = its.bag_page_readonly(midright_bar_bag_page, 'backpack', 20)
player_bag.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

handcraft_bar = its.craft_page(midright_bar_craft_page, 'craft', player_bag.bag)
handcraft_bar.grid(row=0, column=0, padx=10, pady=10)

def midright_change_response(*arg):
    global midright_bar, player_bag
    title = midright_bar.tab(midright_bar.select())['text']
    if title == 'Bag':
        player_bag.relist_contents()
midright_bar.bind('<<NotebookTabChanged>>', midright_change_response)

handcraft_bar.load(fio.get_formula('crf.json'))

map_page.repaint_map()

#rootwin.mainloop()

