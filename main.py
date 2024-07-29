import tkinter as tk
from tkinter import ttk
import mapservice as mps
import itemservice as its
import debugservice as debug

rootwin = tk.Tk()
rootwin.title('Demo Winter')

font_fs = 'fixedsys'
black = 'black'

left_bar = tk.LabelFrame(rootwin,text='Status')
midleft_bar = tk.Frame(rootwin)
midright_bar = ttk.Notebook(rootwin)
right_bar = tk.Frame(rootwin)

left_bar.grid(row=0, column=0, padx=10, pady=10, ipadx=60, ipady=100, sticky='n')
midleft_bar.grid(row=0, column=1, padx=10, pady=10, ipadx=80)
midright_bar.grid(row=0, column=2, padx=10, pady=10, sticky='n', ipadx=20)
right_bar.grid(row=0, column=3, padx=10, pady=10)

map_page = mps.map_display(midleft_bar, 'Map', (10,10), mps.roundview)
map_page.initalize()
map_page.grid(row=0, column=0)

bagpage = tk.Frame()
craftpage = tk.Frame()
blockpage = tk.Frame()
midright_bar.add(bagpage, text='Bag')
midright_bar.add(craftpage, text='Craft')
midright_bar.add(blockpage, text='Location')

player_bag = its.storage(bagpage, 'Backpack')
player_bag.grid(row=0,column=0, padx=10, pady=10)


map_page.repaint_map()




