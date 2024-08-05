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
        command = 'self.page.grid('
        for key, val in kw.items():
            command += key + '=\'' + str(val) + '\','
        if command[-1] == ',':
            command = command[:-1]
        command += ')'
        exec(command)
    def pack(self, **kw):
        command = 'self.page.pack('
        for key, val in kw.items():
            command += key + '=\'' + str(val) + '\','
        if command[-1] == ',':
            command = command[:-1]
        command += ')'
        exec(command)
    def destroy(self):
        self.page.destroy()
    def config(self, **kw):
        # It's a pity these arguments cannot be passed
        #   directly to self.page.config, at least, well,
        #   I have never heard of skills for that.
        # But if you know how to do, please rewrite this function.
        # Lots of thanks.
        command = 'self.page.config('
        for key, val in kw.items():
            command += key + '=\'' + str(val) + '\','
        if command[-1] == ',':
            command = command[:-1]
        command += ')'
        exec(command)
    def __del__(self):
        self.destroy()

