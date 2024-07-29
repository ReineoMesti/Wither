import tkinter as tk
class storage:
    def __init__(self, master, title):
        self.page = tk.LabelFrame(master, text=title)
        self.storage_counter = dict()
        self.storage_strvar = dict()
        self.labels = dict()
        self.labels_row = dict()
        self.add('Nothing', 0)
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
    def grid(self, row, column, padx=0, pady=0):
        self.page.grid(row=row, column=column, padx=padx, pady=pady)
class craftpage:
    def __init__(self, master, text):
        self.page = tk.LabelFrame(master, text=text)
        self.leftlist = tk.Listbox(self.page, width=20)
        self.leftlist.grid(row=0, column=0, padx=5, pady=5)
        self.rightbar = tk.Frame(self.page)
        self.rightbar.grid(row=0, column=1, padx=5, pady=5)
        self.display = tk.Label(self.rightbar, width=10, bg='white')
        self.display.grid(row=0, column=0, padx=5)
        self.operators = tk.Frame(self.rightbar)
        self.operators.grid(row=1, column=0, pady=5)
        self.do_one = tk.Button(self.operators, text='Craft One')
        self.formula = dict()
    def grid(self, row, column, padx=0, pady=0):
        self.page.grid(row=row, column=column, padx=padx, pady=pady)
