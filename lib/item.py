# Module `item` for Withered 0.1 alpha
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import copy

to_import = {"display":"disp", "expandrandom":"exrand",
             "debug":"dbg", 'fileio':'fio'}
for module, newname in to_import.items():
    try:
        exec('import '+module+' as '+newname)
    except ModuleNotFoundError:
        exec('import lib.'+module+' as '+newname)

# NOTE THAT THERE MIGHT BE SOME PROBLEMS WITH  
#   THE USE OF COPY (DEEP OR SHALLOW)
#
class bag_core:
    def __init__(self, size, name):
        self.contains = dict()
        self.weight = 0
        self.size = size
        self.name = name
    def add(self, item, count):
        if self.weight == self.size:
            return 0
        elif self.weight + count <= self.size:
            if item in self.contains.keys():
                self.contains[item] += count
            else:
                self.contains[item] = count
            self.weight += count
            return count
        else:
            remain = self.size - self.weight
            if item in self.contains.keys():
                self.contains[item] += remain
            else:
                self.contains[item] = remain
            self.weight = self.size
            return remain
    def drop(self, item, count):
        if item not in self.contains.keys():
            return count
        elif self.contains[item] <= count:
            dropcount = self.contains[item]
            self.weight -= dropcount
            del self.contains[item]
            return count - dropcount
        else:
            self.contains[item] -= count
            self.weight -= count
            return 0
    def count_item(self, item):
        if item not in self.contains.keys():
            return 0
        return self.contains[item]
    def remain(self):
        return self.size - self.weight
class bag_page_readonly(disp.display_page):
    def __init__(self, master, text, size):
        disp.display_page.__init__(self, master, text)
        self.bag = bag_core(size, text)
        self.storage_strvar = dict()
        self.labels = dict()
        self.labels_row = dict()
        self.add('Nothing', 0)
    def count_item(self, itemname):
        return self.bag.count_item(itemname)
    def add(self,itemname, count):
        'Add item to bag, return the number of item NOT added' 
        undone = max(count - self.bag.remain(), 0)
        count -= undone
        if count == 0:
            return undone
        if 'Nothing' in self.bag.contains:
            self.drop('Nothing', 0, True)
        if itemname in self.bag.contains.keys():
            self.bag.add(itemname, count)
            self.storage_strvar[itemname].set(str(self.bag.contains[itemname]))
        else:
            self.bag.add(itemname, count)
            self.storage_strvar[itemname] = tk.StringVar()
            if self.bag.count_item(itemname)!=0:
                # If it's zero we dont display it.
                self.storage_strvar[itemname].set(str(self.bag.contains[itemname]))
            self.labels[itemname] = dict()
            self.labels[itemname]['name'] = tk.Label(self.page, text=itemname)
            self.labels[itemname]['count'] = tk.Label(self.page, textvariable=self.storage_strvar[itemname])
            if len(self.labels_row)>0:
                rownum = max(self.labels_row.values())+1
            else:
                rownum = 0
            self.labels[itemname]['name'].grid(row=rownum,column=0,ipadx=20,ipady=5,sticky='w')
            self.labels[itemname]['count'].grid(row=rownum,column=1,ipadx=20,ipady=5,sticky='e')
            self.labels_row[itemname] = rownum
        return undone
    def drop(self, itemname, count, serious=False):
        'Drop item from bag, return the number of item NOT dropped'
        if self.bag.count_item(itemname)==0:
            return count
        else:
            cnt = self.bag.count_item(itemname)
            if cnt > count:
                self.bag.drop(itemname, count)
                self.storage_strvar[itemname].set(str(cnt-count))
                return 0
            else:
                undone = count - cnt
                count = cnt
                self.bag.drop(itemname, count)
                self.labels[itemname]['name'].destroy()
                del self.labels[itemname]['name']
                self.labels[itemname]['count'].destroy()
                del self.labels[itemname]['count']
                del self.labels[itemname]
                rownum = self.labels_row[itemname]
                del self.labels_row[itemname]
                del self.storage_strvar[itemname]
                placekey = None
                for key in self.labels_row:
                    if placekey == None:
                        placekey = key
                    elif self.labels_row[placekey] < self.labels_row[key]:
                        placekey = key
                if placekey==None:
                    if not serious:
                        self.add('Nothing', 0)
                    return undone
                if self.labels_row[placekey] < rownum:
                    return undone
                self.labels[placekey]['name'].grid(row=rownum, column=0,ipadx=20,ipady=5,sticky='w')
                self.labels[placekey]['count'].grid(row=rownum, column=1,ipadx=20,ipady=5,sticky='e')
                return undone
    def flush(self):
        self.relist_contents()
    def relist_contents(self):
        'Flush the display immediately'
        tempt = self.bag
        self.bag = bag_core(tempt.size, tempt.name)
        self.storage_strvar = dict()
        self.labels = dict()
        self.labels_row = dict()
        for key in tempt.contains.keys():
            self.add(key, tempt.count_item(key))
        self.bag = tempt
        del tempt
    def load_bag(self, source):
        self.bag = source
        self.relist_contents()
class storage_page(disp.display_page):
    # A storage page used in interactive facilities.
    # Exists in a tk.toplevel for item tranferring.
    def __init__(self, master, text, source):
        disp.display_page.__init__(self, master, text)
        self.table = ttk.Treeview(self.page, columns = ('item', 'count'), height=8, show='headings')
        self.table.heading('item', text='Item')
        self.table.heading('count', text='Count')
        self.table.column('item', width=120, anchor=tk.CENTER)
        self.table.column('count', width=120, anchor=tk.CENTER)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.source = source     # MIND THAT self.source is a DICT. NOT BAG.
        self.table_rows = dict()
        self.yscroll = tk.Scrollbar(self.page)
        self.yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.table['yscrollcommand'] = self.yscroll.set
        self.yscroll['command'] = self.table.yview
        self.relist_contents()
    def add(self, itemname, count):
        if itemname in self.source.keys():
            self.source[itemname] += count
            self.table.set(self.table_rows[itemname], column = 'count', value=str(self.source[itemname]))
        else:
            self.source[itemname] = count
            newrow = self.table.insert('', tk.END, values=(itemname, str(count)))
            self.table_rows[itemname] = newrow
    def drop(self, itemname, count):
        if itemname not in self.source.keys():
            dbg.error('item.py', 'empty storage page drop')
            return False
        if self.source[itemname] - count == 0:
            self.table.delete(self.table_rows[itemname])
            del self.table_rows[itemname]
            del self.source[itemname]
        elif self.source[itemname] - count < 0:
            return False
        else:
            self.source[itemname] -= count
            self.table.set(self.table_rows[itemname], column = 'count', value=str(self.source[itemname]))
        return True
    def flush(self):
        self.relist_contents()
    def relist_contents(self):
        stor = self.source
        self.source = dict()
        for key in stor.keys():
            self.add(key, stor[key])
        self.source = stor
        del stor
    def export(self):
        return copy.deepcopy(self.source)
    def drop_selected(self, count):
        cursel = self.table.selection()
        if cursel == None:
            return (False, None)
        try:
            name = self.table.item(cursel)['values'][0]
        except:
            return (False, None)
        return (self.drop(name, count), name)
    def count_selected(self):
        cursel = self.table.selection()
        if cursel == None:
            return None
        try:
            return int(self.table.item(cursel)['values'][1])
        except:
            return None
class transferring_window(disp.child_window):
    'A toplevel window for item transferring'
    # THIS CLASS IS TESTED FOR NOW AND SEEMED TO BE OF NO
    #   PROBLEM WITH ITS FUNCTION EXPECTED.
    def __init__(self, master, title, leftname, rightname, leftsource, rightsource):
        disp.child_window(self, master, title, grab=True)
        self.leftsto = storage_page(self.window, text=leftname, source=leftsource)
        self.rightsto = storage_page(self.window, text=rightname, source=rightsource)
        self.transfer_bar = tk.Frame(self.window)
        self.leftsto.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.transfer_bar.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.rightsto.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.move_to_left = tk.LabelFrame(self.transfer_bar, text='<<<', font='fixedsys')
        self.move_to_left.pack(padx=5, pady=5)
        self.move_to_right = tk.LabelFrame(self.transfer_bar, text='>>>', font='fixedsys')
        self.move_to_right.pack(padx=5, pady=5)
        self.one_to_left = tk.Button(self.move_to_left, text='move one', width=9)
        self.one_to_right = tk.Button(self.move_to_right, text='move one', width=9)
        self.all_to_left = tk.Button(self.move_to_left, text='move all', width=9)
        self.all_to_right = tk.Button(self.move_to_right, text='move all', width=9)
        self.one_to_left.pack(fill=tk.BOTH, padx=5, pady=5)
        self.one_to_right.pack(fill=tk.BOTH, padx=5, pady=5)
        self.all_to_left.pack(fill=tk.BOTH, padx=5, pady=5)
        self.all_to_right.pack(fill=tk.BOTH, padx=5, pady=5)
        self.one_to_left['state'] = 'disabled'
        self.one_to_right['state'] = 'disabled'
        self.all_to_left['state'] = 'disabled'
        self.all_to_right['state'] = 'disabled' # Of course you haven't selected yet.
        # set commands.
        self.one_to_left['command'] = self.transfer_one_to_left
        self.one_to_right['command'] = self.transfer_one_to_right
        self.all_to_left['command'] = self.transfer_all_to_left
        self.all_to_right['command'] = self.transfer_all_to_right
        self.leftsto.table.bind('<<TreeviewSelect>>', self.release_button_to_right)
        self.rightsto.table.bind('<<TreeviewSelect>>', self.release_button_to_left)
        self.window.protocol('WM_DELETE_WINDOW', self.export)
    def release_button_to_left(self, arg=None):
        self.one_to_left['state'] = 'normal'
        self.all_to_left['state'] = 'normal'
        self.one_to_right['state'] = 'disabled'
        self.all_to_right['state'] = 'disabled'
    def release_button_to_right(self, arg=None):
        self.one_to_right['state'] = 'normal'
        self.all_to_right['state'] = 'normal'
        self.one_to_left['state'] = 'disabled'
        self.all_to_left['state'] = 'disabled'
    def transfer_one_to_left(self):
        success, itemname = self.rightsto.drop_selected(1)
        if not success:
            self.one_to_left['state'] = 'disabled'
            self.all_to_left['state'] = 'disabled'
            return
        self.leftsto.add(itemname, 1)
    def transfer_one_to_right(self):
        success, itemname = self.leftsto.drop_selected(1)
        if not success:
            self.one_to_left['state'] = 'disabled'
            self.all_to_left['state'] = 'disabled'
            return
        self.rightsto.add(itemname, 1)
    def transfer_all_to_left(self):
        num = self.rightsto.count_selected()
        success, itemname = self.rightsto.drop_selected(num)
        if not success:
            self.one_to_left['state'] = 'disabled'
            self.all_to_left['state'] = 'disabled'
            return
        self.leftsto.add(itemname, num)
    def transfer_all_to_right(self):
        num = self.rightsto.count_selected()
        success, itemname = self.leftsto.drop_selected(num)
        if not success:
            self.one_to_left['state'] = 'disabled'
            self.all_to_left['state'] = 'disabled'
            return
        self.rightsto.add(itemname, num)
    def export(self):
        return (copy.deepcopy(self.leftsto.source), copy.deepcopy(self.rightsto.source))
class craft_page(disp.display_page):
    # NOT done yet.
    # Craft formula should be like:
    # { "plank": {"in": {"wood":4, "saw":0}, "out:4}, ...}
    def __init__(self, master, text, source):
        disp.display_page.__init__(self, master, text)
        self.leftlist = tk.Listbox(self.page, width=20,height=26)
        self.leftlist.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.rightbar = tk.Frame(self.page)
        self.rightbar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.display_text = tk.StringVar()
        self.display = tk.Label(self.rightbar, height=25,
                                bg='white', textvariable=self.display_text)
        self.display.pack(fill=tk.X, expand=True, padx=5)
        self.operators = tk.Frame(self.rightbar)
        self.operators.pack(fill=tk.X, pady=5)
        self.do_one = tk.Button(self.operators, text='craft one')
        self.do_one.grid(row=0, column=0, padx=5)
<<<<<<< HEAD
        self.numchoice = tk.Spinbox(self.operators, from_=2, to=100)
=======
        self.do_several = tk.Button(self.operators, text='craft given')
        self.do_several.grid(row=0, column=2, padx=5)
        self.num_textvar = tk.StringVar(value='1')
        self.numchoice = tk.Spinbox(self.operators,
                                    from_ = 1, to = 100,
                                    command = self.update_button,
                                    textvariable = self.num_textvar,
                                    validate = tk.ALL,
                                    validatecommand=self.check_spinbox,
                                    invalidcommand=self.reset_spinbox)
>>>>>>> dev
        self.numchoice.grid(row=0, column=1, padx=5)
        self.formulas = dict()
        self.leftlist.bind('<<ListboxSelect>>', self.display_cursel)
        if source!=None:
            self.source = source
        else:
            self.source = None
        # Source must be a bag_core, since players are only allowed to
        # craft with items from their bag.
        self.do_one['command'] = self.responser_do_one
        self.do_several['command'] = self.responser_do_several
    def responser_do_one(self):
        self.craft_current(1)
    def responser_do_several(self):
        number = int(self.numchoice.get())
        result = self.craft_current(number)
        if result == False:
            messagebox.showinfo('craft failed', 'No enough ingredients')
<<<<<<< HEAD
=======
    def update_button(self):
        current_formula = self.get_current_formula()
        if current_formula == None:
            self.do_several.config(state=tk.DISABLED)
            self.do_one.config(state=tk.DISABLED)
            return
        current_formula = current_formula['in']
        if not self.craftable(current_formula, 1):
            self.do_one.config(state=tk.DISABLED)
            self.do_several.config(state=tk.DISABLED)
            return
        self.do_one.config(state=tk.NORMAL)
        try:
            number = int(self.num_textvar.get())
            if self.craftable(current_formula, number):
                self.do_several.config(state=tk.NORMAL)
            else:
                self.do_several.config(state=tk.DISABLED)
        except:
            dbg.error('item.py', 'Craft spinbox invalid value.')
            self.do_several.config(state=tk.DISABLED)
            return
>>>>>>> dev
    def bind_source(self, source):
        self.source = source
    def load(self, formulas, clear=False):
        'Add new formula to craft page.'
        if clear:
            self.formulas = dict()
        self.formulas.update(copy.deepcopy(formulas))
        self.leftlist.delete(0, 'end')
        for name in self.formulas.keys():
            self.leftlist.insert('end', name)
    def display_cursel(self, arg=None):
        'Flush the display of currently selected formula'
        cursel_index = self.leftlist.curselection()
        try:
            assert len(cursel_index)>0
            cursel = self.leftlist.get(cursel_index[0])
            assert cursel!=None
        except:
            return
        current_formula = self.formulas[cursel]['in'] # ingredients req.
        dbg.log('item.py', str(current_formula)+'\t selected')
        if self.craftable(current_formula, 1):
            self.do_one['state'] = 'normal'
        else:
            self.do_several['state'] = 'disabled'
            self.do_one['state'] = 'disabled'
        outtext = ''
        for key in current_formula.keys():
            outtext += key + '\t' + str(current_formula[key]) + '\n'
        self.display_text.set(outtext)
    def craftable(self, required, count):
        if self.source == None:
            dbs.error('item.py', 'Craft with source unbinded')
            return False
        for itemname, icount in required.items():
            if self.source.count_item(itemname) < icount * count:
                return False
            if self.source.count_item(itemname) == 0:
                # This is for tools.
                # Some craft needs tools, which are listed in the
                # formula but as 0, e.g.
                #   plank: wood * 1, saw * 0
                # 0 means not consumed. But it is still required.
                return False
        return True
    def craft_current(self, count=1):
        'Craft according to formula currently selected, make `count` items'
        cursel_index = self.leftlist.curselection()
        if len(cursel_index)==0:
            self.do_one['state'] = 'disabled'
            return False
        current_formula = self.leftlist.get(cursel_index[0]) #product name + option
        ings = self.formulas[current_formula]['in']
        if not self.craftable(ings, count):
            self.do_one['state'] = 'disabled'
            return False
        for key in ings.keys():
            self.source.drop(key, ings[key] * count)
        product = current_formula.split(':')[0]
        # for some formula with same output name, we have
        # "plank:formulaA": ....
        # "plank:formulaB": ....
        self.source.add(product, self.formulas[current_formula]['out'])
        return True
    def flush(self):
        self.leftlist.select_clear(0)
        self.update_button()
        self.display_text.set('')
