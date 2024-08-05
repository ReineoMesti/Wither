import tkinter as tk
from tkinter import ttk
import lib.map as mps
import lib.item as its
import lib.debug as debug

rootwin = tk.Tk()
rootwin.title('Demo Winter')

font_fs = 'fixedsys'
black = 'black'

left_bar = tk.LabelFrame(rootwin,text='Status')
midleft_bar = tk.Frame(rootwin)
midright_bar = ttk.Notebook(rootwin)
right_bar = tk.Frame(rootwin)

left_bar.pack(side=tk.LEFT, fill = tk.BOTH, padx=5, pady=8)
midleft_bar.pack(side=tk.LEFT, fill = tk.BOTH, padx=5, pady=8)
midright_bar.pack(side=tk.LEFT, fill = tk.BOTH, padx=5, pady=8)
right_bar.pack(side=tk.LEFT, fill = tk.BOTH, padx=5, pady=8)

map_page = mps.map_page(midleft_bar, 'Map', (10,10), mps.roundview)
map_page.get_ready()
map_page.pack(padx=8)

midright_bar_bag_page = tk.Frame()
midright_bar_craft_page = tk.Frame()
midright_bar_block_page = tk.Frame()
midright_bar.add(midright_bar_bag_page, text='Bag')
midright_bar.add(midright_bar_craft_page, text='Craft')
midright_bar.add(midright_bar_block_page, text='Location')

player_bag = its.bag_page_readonly(midright_bar_bag_page, 'backpack')
player_bag.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

handcraft_bar = its.craft_page(midright_bar_craft_page, 'craft')
handcraft_bar.grid(row=0, column=0, padx=10, pady=10)

map_page.repaint_map()
