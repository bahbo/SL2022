from tkinter import *
from tkinter import ttk
import os
import stat
from pathlib import Path
from datetime import datetime


class UI:

    def __init__(self, root, logic):
        self.root = root
        self.root.title('File Manager')

        self.my_style = ttk.Style()
        # my_style.theme_use('default')
        # print(my_style.theme_names())
        # my_style.configure('.', font=('Monospace', 11), bg='SteelBlue3', forground='blue')
        self.my_style.configure('TLabel',
                                background='cyan4',
                                font=('Monospace', 11))
        self.my_style.configure('TFrame', background='red')

        self.my_style.configure('Treeview.Heading',
                                # relief=FLAT,
                                font=('Monospace', 11),
                                background='#00458b',
                                foreground='yellow')
        self.my_style.map('Treeview.Heading',
                          foreground=[('pressed', 'yellow'), ('active', 'yellow')],
                          background=[('pressed', '#00458b'), ('active', '#00458b')])

        self.my_style.configure('Treeview',
                                fieldbackground='#00458b',
                                borderwidth=0,
                                background='#00458b',
                                font=('Monospace', 11))

        self.my_style.map('Treeview',
                          background=[('selected', 'cyan4')],
                          foreground=[('selected', 'black')])

        # my_style.map('TButton', background=[('pressed', 'cyan4'), ('active', 'cyan4')])
        self.my_style.configure('TSeparator', background='red')

        self.my_style.configure('TLabelframe.Label',
                                foreground='black',
                                background='green',
                                font=('Monospace', 11))

        self.my_style.configure('TLabelframe', background='#00458b')  # borderwith=5,

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.tree_frame_1 = ttk.Frame(self.root, )  # padding=5
        self.tree_frame_1.grid(row=0, column=0, sticky=NSEW)

        self.tree_frame_2 = ttk.Frame(self.root)
        self.tree_frame_2.grid(row=0, column=1, sticky=NSEW)

        self.lf_1 = ttk.LabelFrame(self.tree_frame_1, text='current path')
        self.lf_1.pack(fill='both', side=TOP, expand=True, )

        self.lf_2 = ttk.LabelFrame(self.tree_frame_2, text='current path')
        self.lf_2.pack(fill='both', side=TOP, expand=True)

        self.bot_lf_1 = ttk.LabelFrame(self.tree_frame_1, text='GB', labelanchor=SE)
        self.bot_lf_1.pack(fill=X, side=TOP, expand=False)

        self.bot_lf_2 = ttk.LabelFrame(self.tree_frame_2, text='GB', labelanchor=SE)
        self.bot_lf_2.pack(fill=X, side=TOP, expand=False)

        self.active_pos_1 = StringVar()
        self.but = Label(self.bot_lf_1, textvariable=self.active_pos_1)
        self.but.pack(side=LEFT)

        self.active_pos_2 = StringVar()
        self.but2 = Label(self.bot_lf_2, textvariable=self.active_pos_2)
        self.but2.pack(side=LEFT)

        self.tree_1 = ttk.Treeview(self.lf_1, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show='headings',
                                   selectmode='browse')
        self.tree_1.pack(fill='both', side=LEFT, expand=True)
        self.last_selection_tree_1 = None
        self.tree_1.focus_set()

        self.tree_2 = ttk.Treeview(self.lf_2, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show='headings',
                                   selectmode='browse')
        self.tree_2.pack(fill='both', side=LEFT, expand=True)
        self.last_selection_tree_2 = None

        self.tree_paths = {self.tree_1: [None, [None], [None]], self.tree_2: [None, [None], [None]]}

        #
        for tree in (self.tree_1, self.tree_2):
            tree["displaycolumns"] = ('#1', '#2', '#3')
            tree.tag_configure('dir', foreground='light gray')
            tree.tag_configure('file', foreground='cyan4')
            tree.heading('#1', text='Name')
            tree.heading('#2', text='Size')
            tree.heading('#3', text='Modify time')

            tree.column('#1', minwidth=250, width=250)
            tree.column('#2', width=75, stretch=False, anchor=E)
            tree.column('#3', width=120, stretch=False)

        #
        ttk.Separator(self.root, orient='horizontal', ).grid(row=3, column=0, sticky="ew")

        self.b_frame = Frame(self.root)
        self.b_frame.grid(row=4, column=0, columnspan=2, sticky=EW)

        bttns = [
            ['F1 Help', None],
            ['F2 Rename', lambda:self.create_user_frame()],
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
                    ttk.Button(self.b_frame, command=button[1]).grid(row=0, column=bttns.index(button), sticky=EW))

        for x in range(len(bttns)):
            self.b_frame.grid_slaves(column=x)[0].config(text=bttns[x][0], takefocus=0, underline=1, )
            self.b_frame.columnconfigure(x, weight=1, uniform='label')




        self.tree_1.bind('<Double-Button-1>', lambda event: self.item_selected_click(event, logic, self.tree_1))
        self.tree_2.bind('<Double-Button-1>', lambda event: self.item_selected_click(event, logic, self.tree_2))

        self.tree_1.bind('<Return>', lambda event: self.item_selected_enter(event, logic, self.tree_1))
        self.tree_2.bind('<Return>', lambda event: self.item_selected_enter(event, logic, self.tree_2))

        self.tree_1.bind('<FocusIn>', lambda event: self.update_active_position(event, self.tree_1))
        self.tree_2.bind('<FocusIn>', lambda event: self.update_active_position(event, self.tree_2))

        self.tree_1.bind('<F5>', lambda event: self.toggle_tree_info(event, self.tree_1))
        self.tree_2.bind('<F5>', lambda event: self.toggle_tree_info(event, self.tree_2))

        # self.tree_1.bind('<Button-1>', lambda event, x=self.tree_1: update_current_selection(event, x))

        # self.tree_1.bind('<FocusIn>', lambda event: self.proba_1)
        # self.tree_2.bind('<FocusIn>', lambda event: self.proba_2)

    ######

    #
    def toggle_tree_info(self, event, tv):
        '''Pokazwa i skriwa dopylnitelnite koloni '''
        #for tv in (self.tree_1, self.tree_2):
        if tv["displaycolumns"] == ('#1', '#2', '#3'):
            tv["displaycolumns"] = ('#1', '#2', '#3', '#4', '#5', '#6')
            tv.heading('#4', text='Permissions')
            tv.heading('#5', text='Owner')
            tv.heading('#6', text='Group')

            tv.column('#1', minwidth=250, width=250)
            tv.column('#2', width=75, stretch=False, anchor=E)
            tv.column('#3', width=120, stretch=False)
            tv.column('#4', width=120, stretch=False)
            tv.column('#5', width=60, stretch=False, anchor=CENTER)
            tv.column('#6', width=60, stretch=False, anchor=CENTER)
            tv.event_generate("<<ThemeChanged>>")
        else:

            tv["displaycolumns"] = ('#1', '#2', '#3')
            tv.column('#1', minwidth=250, width=250)
            tv.column('#2', width=75, stretch=False, anchor=E)
            tv.column('#3', width=120, stretch=False)
            tv.event_generate("<<ThemeChanged>>")

    #   def

    def update_tree_home_path(self, tv, path):
        '''obnowqwa nadpisa gore w lqwo'''
        if tv == self.tree_1:
            self.lf_1.configure(text=path)
        else:
            self.lf_2.configure(text=path)

    #
    def insert_tree_values(self, logic, tv, path):
        ''' zarejda informaciqta ot logikata w izbranoto TV'''
        for entry in tv.get_children():
            tv.delete(entry)

        dir_items = logic.get_update_tree(path)
        for index, item in enumerate(dir_items[1]):
            tv.insert('', END, tags='dir', text=logic.tree_paths[1][index][0],
                      values=tuple(logic.tree_paths[1][index][1:]))

        for index, item in enumerate(dir_items[2]):
            tv.insert('', END, tags='file', text=logic.tree_paths[2][index][0],
                      values=tuple(logic.tree_paths[2][index][1:]))
        self.update_tree_home_path(tv, path)
        tv.focus(tv.get_children()[0])
        tv.selection_set(tv.get_children()[0])

    def update_active_position(self, event, tv):
        '''obnowqwa reda za izbrana pappka '''
        if tv == self.tree_1:
            self.last_selection_tree_1 = self.tree_1.focus()
            self.tree_1.selection_set(self.last_selection_tree_1)
            self.tree_2.selection_toggle(self.tree_2.selection())
            self.active_pos_1.set(tv.item(self.last_selection_tree_1)['values'][0])

        else:
            self.last_selection_tree_2 = self.tree_2.focus()
            self.tree_2.selection_set(self.last_selection_tree_2)
            self.tree_1.selection_toggle(self.tree_1.selection())
            self.active_pos_2.set(tv.item(self.last_selection_tree_2)['values'][0])


    def item_selected_click(self, event, logic, tree_view):
        '''Double click / izbor na papka.'''
        region = tree_view.identify("region", event.x, event.y)
        if region == 'heading':
            pass
        elif region == 'cell':
            # tree_view.selection_set(tree_view.focus())
            selected_path = tree_view.item(tree_view.selection())['text']
            self.insert_tree_values(logic, tree_view, selected_path)

    def item_selected_enter(self, event, logic, tree_view):
        # tree_view.selection_set(tree_view.focus())
        selected_path = tree_view.item(tree_view.selection())['text']
        self.insert_tree_values(logic, tree_view, selected_path)
    #
    #
    def create_user_frame(self):
        print('hi')
        user_frame = Toplevel(root)
        user_frame.transient(master=root)
        user_frame.overrideredirect(True)
        # x = self.root.winfo_x()
        # y = self.root.winfo_y()
        # w = user_frame.winfo_width()
        # h = user_frame.winfo_height()
        # user_frame.geometry("%dx%d+%d+%d" % (w, h, x, y))


        search_entry = ttk.Entry(user_frame).pack()



class MainLogic:

    def __init__(self):
        self.current_folder = os.path.expanduser('~')
        self.current_selection = None
        self.tree_paths = [[None], [None], [None]]

    #
    def get_update_tree(self, path,
                        sort_key=1):  # try except  NotADirectoryError: [Errno 20] Not a directory: '/tmp/config-err-L3yImR'

        self.tree_paths[
            1].clear()  # s.system("open " + shlex.quote(filename))  import subprocess, os, platformif platform.system() == 'Darwin':       # macOS    subprocess.call(('open', filepath))elif platform.system() == 'Windows':    # Windows    os.startfile(filepath)else:                                   # linux variants    subprocess.call(('xdg-open', filepath))
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

        self.tree_paths[1].sort(key=lambda x: x[sort_key])
        self.tree_paths[2].sort(key=lambda x: x[sort_key])
        return self.tree_paths

    #
    def search_alg(self, search_dir, name):
        results = []
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if name.lower() in file.lower():
                    results.append(root + '/' + str(file))
            for dir_ in dirs:
                if name.lower() in dir_.lower():
                    results.append(root + '/' + str(dir_))
        return results


#
# def treeview_sort_column(self, tv, col, reverse):
#     lst = [(tv.set(k, col), k) for k in tv.get_children('')]
#     print(lst)
#     lst.sort(reverse=reverse)
#
#     #
#     # rearrange items in sorted positions
#     for index, (val, k) in enumerate(lst):
#         tv.move(k, '', index)

# # reverse sort next time
# tv.heading(col, text=col, command=lambda _col=col: \
#     treeview_sort_column(tv, _col, not reverse))

#
# columns = ('#1', '#2', '#3')

# for col in columns:
#     self.tree_1.heading(col, text=col, command=lambda _col=col: \
#         treeview_sort_column(tree, _col, False))


#
root = Tk()

logic1 = MainLogic()
logic1.get_update_tree(logic1.current_folder)

gui = UI(root, logic1)

gui.insert_tree_values(logic1, gui.tree_2, os.path.expanduser('~'))
gui.insert_tree_values(logic1, gui.tree_1, os.path.expanduser('~'))

root.mainloop()
