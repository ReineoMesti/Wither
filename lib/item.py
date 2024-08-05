# Module `item` for Withered 0.1 alpha
import tkinter as tk
from tkinter import ttk
import copy
to_import = {"display":"disp", "expandrandom":"exrand", "debug":"dbg"}
for module, newname in to_import.items():
    try:
        exec('import '+module+' as '+newname)
    except ModuleNotFoundError:
        exec('import lib.'+module+' as '+newname)

# NOTE THAT THERE MIGHT BE SOME PROBLEMS WITH  
#   THE USE OF COPY (DEEP OR SHALLOW)
#

class bag_page_readonly(disp.display_page):
    def __init__(self, master, text):
        disp.display_page.__init__(self, master, text)
        self.storage_counter = dict()
        self.storage_strvar = dict()
        self.labels = dict()
        self.labels_row = dict()
        self.add('Nothing', 0)
    def count_item(self, itemname):
        if itemname in self.storage_counter.keys():
            return self.storage_counter[itemname]
        else:
            return 0
    def add(self,itemname, count):
        if 'Nothing' in self.storage_counter:
            self.drop('Nothing', 0, True)
        if itemname in self.storage_counter.keys():
            self.storage_counter[itemname] += count
            self.storage_strvar[itemname].set(str(self.storage_counter[itemname]))
        else:
            self.storage_counter[itemname] = count
            self.storage_strvar[itemname] = tk.StringVar()
            if self.storage_counter[itemname]!=0:
                self.storage_strvar[itemname].set(str(self.storage_counter[itemname]))
            self.labels[itemname] = dict()
            self.labels[itemname]['name'] = tk.Label(self.page, text=itemname)
            self.labels[itemname]['count'] = tk.Label(self.page, textvariable=self.storage_strvar[itemname])
            rownum = len(self.labels)
            self.labels[itemname]['name'].grid(row=rownum,column=0,ipadx=20,ipady=5,sticky='w')
            self.labels[itemname]['count'].grid(row=rownum,column=1,ipadx=20,ipady=5,sticky='e')
            self.labels_row[itemname] = rownum
    def drop(self, itemname, count, serious=False):
        if itemname not in self.storage_counter.keys():
            return False
        else:
            cnt = self.storage_counter[itemname]
            if cnt > count:
                self.storage_counter[itemname] -= count
                self.storage_strvar[itemname].set(str(cnt-count))
                return True
            elif cnt < count:
                return False
            else:
                del self.storage_counter[itemname]
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
                    return True
                self.labels[placekey]['name'].grid(row=rownum, column=0,ipadx=20,ipady=5,sticky='w')
                self.labels[placekey]['count'].grid(row=rownum, column=1,ipadx=20,ipady=5,sticky='e')
                return True
    def relist_contents(self):
        'Flush the display immediately'
        tempt = self.storage_counter
        self.storage_counter = dict()
        self.storage_strvar = dict()
        self.labels = dict()
        self.labels_row = dict()
        for key in tempt.keys():
            self.add(key, tempt[key])
        self.storage_counter = tempt
        del tempt
    def load_bag(self, source):
        self.storage_counter = copy.deepcopy(source)
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
class transferring_window:
    'A toplevel window for item transferring'
    # THIS CLASS IS TESTED FOR NOW AND SEEMED TO BE OF NO
    #   PROBLEM WITH ITS FUNCTION EXPECTED.
    def __init__(self, master, title, leftname, rightname, leftsource, rightsource):
        self.window = tk.Toplevel(master)
        self.window.title(title)
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
    def __init__(self, master, text, source):
        disp.display_page.__init__(self, master, text)
        self.leftlist = tk.Listbox(self.page, width=20,height=26)
        self.leftlist.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.rightbar = tk.Frame(self.page)
        self.rightbar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.display = tk.Label(self.rightbar, height=25, bg='white')
        self.display.pack(fill=tk.X, padx=5, expand=True)
        self.operators = tk.Frame(self.rightbar)
        self.operators.pack(fill=tk.X, pady=5)
        self.do_one = tk.Button(self.operators, text='craft one')
        self.do_one.grid(row=0, column=0, padx=5)
        self.numchoice = tk.Spinbox(self.operators, from_=2, to=100)
        self.numchoice.grid(row=0, column=1, padx=5)
        self.do_several = tk.Button(self.operators, text='craft given')
        self.do_several.grid(row=0, column=2, padx=5)
        self.formulas = dict()
        self.leftlist.bind('<<ListboxSelect>>', self.display_cursel)
        if source!=None:
            self.source = copy.copy(source)
        else:
            self.source = None
        # Source must be a bag, since players are only allowed to craft with staff from their bag.
    def bind_source(self, source):
        self.source = source
    def load_formula(self, formulas):
        'Add new formula to craft page.'
        self.formulas.update(formulas)
        self.leftlist.delete(0, 'end')
        for name in self.formulas.keys():
            self.leftlist.insert('end', name+'\t'+str(self.formulas[name]['out']))
    def display_cursel(self, arg=None):
        cursel_index = self.leftlist.curselection()
        try:
            cursel = self.leftlist.get(cursel_index)
            assert cursel!=None
        except:
            return
        current_formula = self.formulas[cursel]['in']
        dbs.log('item.py', str(current_formula)+'\t selected')
        if self.craftable(current_formula, 1):
            self.do_one['state'] = 'normal'
        else:
            self.do_several['state'] = 'disabled'
            self.do_one['state'] = 'disabled'
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
    def craft_current(self, destination, count=1):
        'Craft according to formula currently selected, make `count` items'
        cursel_index = self.leftlist.curselection()
        if len(cursel_index)==0:
            self.do_one['state'] = 'disabled'
            return False
        current_formula = self.leftlist.get(cursel_index[0])
        ings = self.formulas[current_formula]['in']
        if not self.craftable(ings, count):
            return False
        for key in ings.keys():
            self.source.drop(key, ings[key] * count)
        self.source.add(current_formula, self.formulas[current_formula]['out'])
        return True
    
            
