import os
import time

import threading as thread
from tkinter import messagebox as msgbox

start_time = time.time()

def error(source:str, message:str)->None:
    msgbox.showerror("Error from "+source, message)
def log(source:str, message:str)->None:
    msgbox.showinfo("Log message from "+source, message)

class UnimplementError(Exception):
    def __init__(self, *arg, **kw):
        Exception.__init__(self, *arg, **kwa)

