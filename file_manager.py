from tkinter import *
from tkinter import ttk
import os, stat
from pathlib import Path
from datetime import datetime


class GUI:

    def __init__(self):
        print('hi')
        print('test new banch')
        self.root = Tk()
        self.root.title('File Manager')
        self.root.configure()

        self.self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1, uniform='LabelFrame')
        self.root.columnconfigure(1, weight=1, uniform='LabelFrame')

        #
        self.fr_label_1 = ttk.Frame(self.root)
        self.fr_label_1.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        #
        self.lf_1 = ttk.LabelFrame(self.fr_label_1, text='current path')
        self.lf_1.pack(fill='both', side=LEFT, expand=True)
        self.lf_2 = ttk.LabelFrame(self.fr_label_1, text='current path')
        self.lf_2.pack(fill='both', side=LEFT, expand=True)

        #

        self.tree_1 = ttk.Treeview(self.lf_1, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show='headings', selectmode='browse')
        self.tree_1.bind('<Double-Button-1>', lambda event, x=self.tree_1: item_selected(event, x))
        self.tree_1.bind('<F5>', lambda event, x=self.tree_1: tree_info(event, x))
        self.tree_1.bind('<Return>', lambda event, x=self.tree_1: item_selected(event, x))
        self.tree_1.pack(fill='both', side=LEFT, expand=True)
        #self.last_selected_tree_1 = None
        self.tree_1["displaycolumns"] = ('#1', '#2', '#3')

        self.tree_2 = ttk.Treeview(self.lf_2, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show='headings', selectmode='browse')
        self.tree_2.bind('<Double-Button-1>', lambda event, x=self.tree_2: item_selected(event, x))
        self.tree_2.bind('<F5>', lambda event, x=self.tree_2: tree_info(event, x))
        self.tree_2.bind('<Return>', lambda event, x=self.tree_2: item_selected(event, x))
        self.tree_2.pack(fill='both', side=LEFT, expand=True)
        #self.last_selected_tree_2 = None
        self.tree_2["displaycolumns"] = ('#1', '#2', '#3')

        self.tree_paths = {self.tree_1: [None, [None], [None]], self.tree_2: [None, [None], [None]]}


        for tree in (self.tree_1, self.tree_2):
            tree.tag_configure('dir', foreground='light gray')
            tree.tag_configure('file', foreground='cyan4')
            tree.heading('#1', text='Name')
            tree.heading('#2', text='Size')
            tree.heading('#3', text='Modify time')

            tree.column('#1', width=300, stretch=False)
            tree.column('#2', width=75, stretch=False, anchor=E)
            tree.column('#3', width=120, stretch=False)


        def proba_1(event):
            self.last_selected_tree_1 = self.tree_1.focus()
            self.tree_1.selection_set(self.last_selected_tree_1)
            self.tree_2.selection_toggle(self.tree_2.selection())

        def proba_2(event):
            self.last_selected_tree_2 = self.tree_2.focus()
            self.tree_2.selection_set(self.last_selected_tree_2)
            self.tree_1.selection_toggle(self.tree_1.selection())

        self.tree_1.bind('<FocusIn>', proba_1)
        self.tree_2.bind('<FocusIn>', proba_2)


        self.sep = ttk.Separator(self.root,orient='horizontal',).grid(row=3, column=0, sticky="ew")

        self.b_frame = Frame(self.root)
        self.b_frame.grid(row=4, column=0, columnspan=2, sticky=EW)

        bttns = [
            ['F1 Help', None],
            ['F2 Rename', lambda: actve_tv],
            ['F3 Cut', None],
            ['F4 Copy', None],
            ['F5 Paste', None],
            ['F6 MkDir', None],
            ['F7 DelDir', None],
            ['F8 MkFile', None],
            ['F9 DelFile', None],
            ['F10 Quit', None]
        ]

        for button in bttns:
            setattr(self, button[0], ttk.Label(self.b_frame, anchor="center").grid(row=0, column=bttns.index(button), sticky=EW))

        for x in range(len(bttns)):
            self.b_frame.grid_slaves(column=x)[0].config(text=bttns[x][0], takefocus=0, underline=1, )
            self.b_frame.columnconfigure(x, weight=1, uniform='label')

        #
        def actve_tv():
            print(self.root.focus_get().item(tree.focus())['values'][0])
#
#
        def tree_info(event, tv):
            if tv["displaycolumns"] == ('#1', '#2', '#3'):
                tv["displaycolumns"] = ('#1', '#2', '#3', '#4', '#5', '#6')
                tv.heading('#4', text='Permissions')
                tv.heading('#5', text='Owner')
                tv.heading('#6', text='Group')

                # tv.column('#1', width=300, stretch=False)
                # tv.column('#2', width=75, stretch=False, anchor=E)
                # tv.column('#3', width=120, stretch=False)
                tv.column('#4', width=120, stretch=False)
                tv.column('#5', width=60, stretch=False, anchor=CENTER)
                tv.column('#6', width=60, stretch=False, anchor=CENTER)
            else:
                tv["displaycolumns"] = ('#1', '#2', '#3')
                # tv.column('#1', width=300, stretch=False)
                # tv.column('#2', width=75, stretch=False, anchor=E)
                # tv.column('#3', width=120, stretch=False)

        #print(os.path.expanduser('~'))
        home_path=os.path.expanduser('~')



        def func(tv):
            for entry in tv.get_children():
                tv.delete(entry)
            if self.tree_paths[tv][0] != os.path.abspath(os.sep):
                tv.insert('', END, tags='dir', text=self.tree_paths[tv][0], values=('/..', 'UP--DIR', datetime.fromtimestamp(self.tree_paths[tv][0].stat().st_mtime).strftime('%b %d %-H:%M'), stat.filemode(os.stat(self.tree_paths[tv][0]).st_mode), 'root','root'))
            for item in self.tree_paths[tv][1]:
                tv.insert('', END, tags='dir', text=item.path, values=(f'/{item.name}', item.stat().st_size, datetime.fromtimestamp(item.stat().st_mtime).strftime('%b %d %-H:%M'), stat.filemode(item.stat().st_mode), Path(item.path).owner(), Path(item.path).group()))
                tv.tag_configure('dir', foreground='light gray')
            for item in self.tree_paths[tv][2]:
                tv.insert('', END, tags='file', text=item.path, values=(item.name, item.stat().st_size, datetime.fromtimestamp(item.stat().st_mtime).strftime('%b %d %-H:%M'), stat.filemode(item.stat().st_mode), Path(item.path).owner(), Path(item.path).group()))
                tv.tag_configure('file', foreground='cyan4')


        def get_update_tree(path, tv):
            #self.tree_paths[tv][0] = os.path.abspath(os.sep)
            self.tree_paths[tv][1].clear()
            self.tree_paths[tv][2].clear()
            #print(os.path.abspath(os.sep))
            # if path != '/':
            #     print(Path(path).parent)
            print(self.tree_paths[tv][0],os.path.abspath(os.sep) )
            #if Path(path).parent != os.path.abspath(os.sep):
            self.tree_paths[tv][0] = Path(path).parent #, tags='file',

            for item in os.scandir(path):
                if item.is_dir():
                    self.tree_paths[tv][1].append(item)
                    # tv.insert('', END, text=item.path, tags='file',
                    #           values=(f'/{item.name}', item.stat().st_size, datetime.fromtimestamp(item.stat().st_mtime).strftime('%b %d %-H:%M'), stat.filemode(item.stat().st_mode), Path(item.path).owner(), Path(item.path).group()))
                else:
                    self.tree_paths[tv][2].append(item)
                    # tv.insert('', END, text=item.path, tags='dir',
                    #           values=(item.name, item.stat().st_size, datetime.fromtimestamp(item.stat().st_mtime).strftime('%b %d %-H:%M'), stat.filemode(item.stat().st_mode), Path(item.path).owner(), Path(item.path).group()))
            func(tv)

        get_update_tree(home_path, self.tree_1)
        get_update_tree(home_path, self.tree_2)


        def search_alg(search_dir, name):
            results = []
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if name.lower() in file.lower():
                        results.append(root + '/' + str(file))
                for dir in dirs:
                    if name.lower() in dir.lower():
                        results.append(root + '/' + str(dir))
            return results


        def item_selected(event, tree_view):
            region = tree_view.identify("region", event.x, event.y)
            if region == 'heading':
                pass
            elif region == 'cell':
                #print(tree_view.item(tree_view.focus())['text'])
                get_update_tree(tree_view.item(tree_view.focus())['text'],tree_view)

        # def treeview_sort_column(tv, col, reverse):
        #     l = [(tv.set(k, col), k) for k in tv.get_children('')]
        #     print(l)
        #     l.sort(reverse=reverse)
        #
        #
        #     # rearrange items in sorted positions
        #     for index, (val, k) in enumerate(l):
        #         tv.move(k, '', index)
        #
        #     # reverse sort next time
        #     tv.heading(col, text=col, command=lambda _col=col: \
        #         treeview_sort_column(tv, _col, not reverse))
        #
        #
        # columns = ('#1', '#2', '#3')
        #
        #
        # for col in columns:
        #     self.tree_1.heading(col, text=col, command=lambda _col=col: \
        #         treeview_sort_column(tree, _col, False))













        my_style = ttk.Style()
        #my_style.theme_use('default')
        #print(my_style.theme_names())
        # my_style.configure('.', font=('Monospace', 11), bg='SteelBlue3', forground='blue')
        my_style.configure('TLabel',
                           background='cyan4',
                           font=('Monospace', 11))

        my_style.configure('Treeview.Heading',
                           # relief=FLAT,
                           font=('Monospace', 11),
                           background='#00458b',
                           foreground='yellow')
        my_style.map('Treeview.Heading',
                     foreground=[('pressed', 'yellow'), ('active', 'yellow')],
                     background=[('pressed', '#00458b'), ('active', '#00458b')])

        my_style.configure('Treeview',
                           fieldbackground='#00458b',
                           borderwidth=0,
                           background='#00458b',
                           font=('Monospace', 11))

        my_style.map('Treeview',
                     background=[('selected', 'cyan4')],
                     foreground=[('selected', 'black')])

        # my_style.map('TButton', background=[('pressed', 'cyan4'), ('active', 'cyan4')])
        my_style.configure('TSeparator', background='red')

        my_style.configure('TLabelframe.Label',
                           foreground='black',
                           background='green',
                           font=('Monospace', 11))

        my_style.configure('TLabelframe',  background='#00458b')  # borderwith=5,




        self.root.mainloop()
interface = GUI()

