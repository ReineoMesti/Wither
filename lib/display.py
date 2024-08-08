import tkinter as tk
from tkinter import ttk

to_import = {"debug":"dbg"}
for module, newname in to_import.items():
    try:
        exec('import '+module+' as '+newname)
    except ModuleNotFoundError:
        exec('import lib.'+module+' as '+newname)

class display_page:
    def __init__(self, master, text):
        self.page = tk.LabelFrame(master, text=text)
    def grid(self, **kw):
        self.page.grid(**kw)
    def pack(self, **kw):
        self.page.pack(**kw)
    def destroy(self):
        self.page.destroy()
    def config(self, **kw):
        self.page.config(**kw)
    def __del__(self):
        self.page.destroy()
class child_window:
    def __init__(self, master, title, grab=False):
        self.window = tk.Toplevel(master)
        self.window.title(title)
        if grab:
            self.window.grab_set()
    def iconify(self):
        self.window.inconify()
    def deiconify(self):
        self.window.deiconify()
    def protocol(self, event, function):
        self.window.protocol(event, function)
