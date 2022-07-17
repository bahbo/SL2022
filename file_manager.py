from tkinter import *
from tkinter import ttk
import os, stat
from pathlib import Path
from datetime import datetime


class UI:

    def __init__(self, root, logic):
        self.root = root
        self.root.title('File Manager')

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1, )
        self.root.columnconfigure(1, weight=1, )

        #
        self.tree_frame_1 = ttk.Frame(self.root)
        self.tree_frame_1.grid(row=0, column=0, sticky=NSEW)

        self.tree_frame_2 = ttk.Frame(self.root)
        self.tree_frame_2.grid(row=0, column=1, sticky=NSEW)

        # self.tree_frame_1.rowconfigure(0, weight=1)
        # self.tree_frame_1.columnconfigure(0, weight=1, uniform='1')
        # self.tree_frame_1.columnconfigure(1, weight=1, uniform='1')
        #
        # self.tree_frame_2.rowconfigure(0, weight=1)
        # self.tree_frame_2.columnconfigure(0, weight=1, uniform='1')
        # self.tree_frame_2.columnconfigure(1, weight=1, uniform='1')

        # self.root.columnconfigure(1, weight=1, uniform='LabelFrame')

        #
        self.lf_1 = ttk.LabelFrame(self.tree_frame_1, text='current path')
        self.lf_1.pack(fill='both', side=TOP, expand=True)

        self.lf_2 = ttk.LabelFrame(self.tree_frame_2, text='current path')
        self.lf_2.pack(fill='both', side=TOP, expand=True)

        self.bot_lf_1 = ttk.LabelFrame(self.tree_frame_1, text='GB', labelanchor=SE)
        self.bot_lf_1.pack(fill=X, side=TOP, expand=False)

        self.bot_lf_2 = ttk.LabelFrame(self.tree_frame_2, text='GB', labelanchor=SE)
        self.bot_lf_2.pack(fill=X, side=TOP, expand=False)

        self.active_pos_1 = StringVar()
        self.but = Label(self.bot_lf_1, textvariable=self.active_pos_1 )
        self.but.pack(side=LEFT)

        self.active_pos_2 = StringVar()
        self.but2 = Label(self.bot_lf_2, textvariable=self.active_pos_2)
        self.but2.pack(side=LEFT)

        self.tree_1 = ttk.Treeview(self.lf_1, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show='headings', selectmode='browse')
        self.tree_1.pack(fill='both', side=LEFT, expand=True)
        #self.last_selection_tree_1 = None

        self.tree_2 = ttk.Treeview(self.lf_2, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show='headings', selectmode='browse')
        self.tree_2.pack(fill='both', side=LEFT, expand=True)
        #self.last_selection_tree_2 = None

        self.tree_paths = {self.tree_1: [None, [None], [None]], self.tree_2: [None, [None], [None]]}


        for tree in (self.tree_1, self.tree_2):
            tree["displaycolumns"] = ('#1', '#2', '#3')
            tree.tag_configure('dir', foreground='light gray')
            tree.tag_configure('file', foreground='cyan4')
            tree.heading('#1', text='Name')
            tree.heading('#2', text='Size')
            tree.heading('#3', text='Modify time')

            tree.column('#1')
            tree.column('#2', width=75, stretch=False, anchor=E)
            tree.column('#3', width=120, stretch=False)


#
        ttk.Separator(self.root, orient='horizontal', ).grid(row=3, column=0, sticky="ew")

        self.b_frame = Frame(self.root)
        self.b_frame.grid(row=4, column=0, columnspan=2, sticky=EW)

        bttns = [
            ['F1 Help', None],
            ['F2 Rename', None],
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
            setattr(self, button[0],
                    ttk.Label(self.b_frame, anchor="center").grid(row=0, column=bttns.index(button), sticky=EW))

        for x in range(len(bttns)):
            self.b_frame.grid_slaves(column=x)[0].config(text=bttns[x][0], takefocus=0, underline=1, )
            self.b_frame.columnconfigure(x, weight=1, uniform='label')










        self.tree_1.bind('<Double-Button-1>', lambda event, x=self.tree_1: item_selected(event, x))
        self.tree_2.bind('<Double-Button-1>', lambda event, x=self.tree_2: item_selected(event, x))

        self.tree_1.bind('<Return>', lambda event, x=self.tree_1: item_selected(event, x))
        self.tree_2.bind('<Return>', lambda event, x=self.tree_2: item_selected(event, x))

        self.tree_1.bind('<<TreeviewSelect>>', lambda event, x=self.tree_1: update_active_position(event, x))
        self.tree_2.bind('<<TreeviewSelect>>', lambda event, x=self.tree_2: update_active_position(event, x))

        self.root.bind('<F5>', lambda event: togle_tree_info(event))

#        self.tree_1.bind('<Button-1>', lambda event, x=self.tree_1: update_current_selection(event, x))

#
        def togle_tree_info(event):
            for tv in (self.tree_1, self.tree_2):
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


        def func(tv,path):
            for entry in tv.get_children():
                tv.delete(entry)
            print(logic.get_update_tree(path))
            dir_items = logic.get_update_tree(path)
            for index, item in enumerate(dir_items[1]):
                tv.insert('', END, tags='dir', text=logic.tree_paths[1][index][0],
                          values=tuple(logic.tree_paths[1][index][1:]))

            for index, item in enumerate(dir_items[2]):
                tv.insert('', END, tags='file', text=logic.tree_paths[2][index][0],
                          values=tuple(logic.tree_paths[2][index][1:]))

        #print(logic.get_update_tree(os.path.expanduser('~')))
        #home_path = os.path.expanduser('~')
        func(self.tree_1, os.path.expanduser('~'))
        func(self.tree_2, os.path.expanduser('~'))



        # def get_update_tree(path, tv):
        #     self.tree_paths[tv][1].clear()
        #     self.tree_paths[tv][2].clear()
        #
        #     if path != os.path.abspath(os.sep):
        #         self.tree_paths[tv][1].append((Path(path).parent, '/..', 'UP--DIR'))
        #     for item in os.scandir(path):
        #         info = [
        #             item.path,
        #             item.name,
        #             item.stat().st_size,
        #             datetime.fromtimestamp(item.stat().st_mtime).strftime('%b %d %-H:%M'),
        #             stat.filemode(item.stat().st_mode),
        #             Path(item.path).owner(),
        #             Path(item.path).group()
        #         ]
        #
        #         if item.is_dir():
        #             info[1] = f'/{item.name}'
        #             self.tree_paths[tv][1].append(info)
        #         else:
        #             self.tree_paths[tv][2].append(info)
        #     func(tv)
        #     update_tree_home_path(tv, path)
        #     tv.focus(tv.get_children()[0])



        def update_tree_home_path(tv, path):
            if tv == self.tree_1:
                self.lf_1.configure(text=path)
            else:
                self.lf_2.configure(text=path)


        def update_active_position(event, tv):
            selected = tv.selection()
            print(selected)
            if tv == self.tree_1:
                self.active_pos_1.set(tv.item(selected, 'values')[0])
                #print(self.last_selection_tree_1)
            else:
                self.active_pos_2.set(tv.item(selected, 'values')[0])

        # def proba_1(event):
        #     self.last_selection_tree_1 = self.tree_1.focus()
        #     self.tree_1.selection_set(self.last_selection_tree_1)
        #     self.tree_2.selection_toggle(self.tree_2.selection())
        #
        #
        # def proba_2(event):
        #     self.last_selection_tree_2 = self.tree_2.focus()
        #     self.tree_2.selection_set(self.last_selection_tree_2)
        #     self.tree_1.selection_toggle(self.tree_1.selection())

        # self.tree_1.bind('<FocusIn>', proba_1)
        # self.tree_2.bind('<FocusIn>', proba_2)


        # self.tree_1.focus(self.tree_1.get_children()[0])
        # self.tree_1.focus_set()
        # #self.tree_1.selection_set(self.tree_1.get_children()[0])
        #
        # self.tree_2.focus(self.tree_2.get_children()[0])
        # #self.tree_2.selection_set(self.tree_2.get_children()[0])
        # self.tree_2.selection_toggle(self.tree_2.selection())
        #





#
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

#
        def item_selected(event, tree_view):
            region = tree_view.identify("region", event.x, event.y)
            if region == 'heading':
                pass
            elif region == 'cell':
                print(tree_view.item(tree_view.focus())['text'])
                func(tree_view, tree_view.item(tree_view.focus())['text'] )

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

class MainLogic:

    def __init__(self):
        self.current_folder = os.path.expanduser('~')
        self.current_selection = None
        self.tree_paths = [[None], [None], [None]]

    def get_update_tree(self, path):
        self.tree_paths[1].clear()
        self.tree_paths[2].clear()

        if path != os.path.abspath(os.sep):
            up_dir = (Path(path).parent, '/..', 'UP--DIR')
            self.tree_paths[1].append(up_dir)
        for item in os.scandir(path):
            info = [
                item.path,
                item.name,
                item.stat().st_size,
                datetime.fromtimestamp(item.stat().st_mtime).strftime('%b %d %-H:%M'),
                stat.filemode(item.stat().st_mode),
                Path(item.path).owner(),
                Path(item.path).group()]
            if item.is_dir():
                info[1] = f'/{item.name}'
                self.tree_paths[1].append(info)
            else:
                self.tree_paths[2].append(info)
        return self.tree_paths




root = Tk()

logic1 = MainLogic()
logic1.get_update_tree(logic1.current_folder)



# logic2 = MainLogic()
# logic2.get_update_tree(logic2.current_folder)

gui = UI(root, logic1)


#pm.get_tree(interface.lb_1)
#pm.get_tree(interface.lb_2)


root.mainloop()


