from tkinter import *
from tkinter import ttk
import os
from file_manager_logic import MainLogic
import stat
from pathlib import Path
from datetime import datetime


class UI:

    def __init__(self, root, logic):
        self.permissions = None
        self.uf_perm = None
        self.entry_text = None
        self.uf_cancel_button = None
        self.uf_ok_button = None
        self.uf_entry = None
        self.uf_label = None
        self.user_window = None
        self.tv_order = [None]
        self.root = root
        self.root.title('File Manager')



        self.my_style = ttk.Style()
        # my_style.theme_use('default')
        # print(my_style.theme_names())
        # my_style.configure('.', font=('Monospace', 11), bg='SteelBlue3', forground='blue')
        self.my_style.configure('TLabel',
                                background='cyan4',
                                font=('Monospace', 11))
        #self.my_style.configure('TFrame', background='red')

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

        self.tree_paths = {self.tree_1: None, self.tree_2: None}

        #
        for tree in (self.tree_1, self.tree_2):
            tree["displaycolumns"] = ('#1', '#2', '#3')
            tree.tag_configure('dir', foreground='light gray')
            tree.tag_configure('file', foreground='cyan4')
            tree.tag_configure('copy', foreground='yellow')
            tree.tag_configure('cut', foreground='cyan4')


            tree.heading('#1', text='Name')
            tree.heading('#2', text='Size')
            tree.heading('#3', text='Modify time')

            tree.column('#1', minwidth=250, width=250)
            tree.column('#2', width=75, stretch=False, anchor=E)
            tree.column('#3', width=120, stretch=False)

        #
        ttk.Separator(self.root, orient='horizontal', ).grid(row=3, column=0, sticky="ew")

        self.user_window = None

        self.b_frame = Frame(self.root)
        self.b_frame.grid(row=4, column=0, columnspan=2, sticky=EW)

        bttns = [
            ['F1 Help', None],
            ['F2 Rename', lambda: self.rename(logic)],
            ['F3 Cut', lambda: logic.cut_file_folder(self.active_selection)],
            ['F4 Copy', lambda: logic.copy_file_folder(self.active_selection)],
            ['F5 Paste', lambda: logic.paste(self.tv_list(), self.tree_paths)],
            ['F6 Chmod', lambda: self.edit_permisions(logic)],
            ['F7 Delete', lambda: logic.delete_file_dir(self.active_selection)],
            ['F8 MkFile', None],
            ['F9 ?!?!?', None],
            ['F10 Quit', None]
        ]

        for button in bttns:
            setattr(self, button[0],
                    ttk.Button(self.b_frame, command=button[1]).grid(row=0, column=bttns.index(button), sticky=EW))

        for x in range(len(bttns)):
            self.b_frame.grid_slaves(column=x)[0].config(text=bttns[x][0], takefocus=0, underline=1, )
            self.b_frame.columnconfigure(x, weight=1, uniform='label')



        self.root.bind("<Configure>", lambda event: self.move_user_frame(event))

        self.tree_1.bind('<Double-Button-1>', lambda event: self.item_selected_click(event, logic, self.tree_1))
        self.tree_2.bind('<Double-Button-1>', lambda event: self.item_selected_click(event, logic, self.tree_2))

        self.tree_1.bind('<Return>', lambda event: self.item_selected_enter(logic, self.tree_1))
        self.tree_2.bind('<Return>', lambda event: self.item_selected_enter(logic, self.tree_2))

        self.tree_1.bind('<FocusIn>', lambda event: self.update_active_position(event, self.tree_1))
        self.tree_2.bind('<FocusIn>', lambda event: self.update_active_position(event, self.tree_2))

        self.tree_1.bind('<F5>', lambda event: self.toggle_tree_info(event, self.tree_1))
        self.tree_2.bind('<F5>', lambda event: self.toggle_tree_info(event, self.tree_2))

        # self.tree_1.bind('<Button-1>', lambda event, x=self.tree_1: update_current_selection(event, x))

        # self.tree_1.bind('<FocusIn>', lambda event: self.proba_1)
        # self.tree_2.bind('<FocusIn>', lambda event: self.proba_2)

    ######

    #
    def tv_list(self):
        if len(self.tree_1.selection()) > 0:
            self.tv_order = [self.tree_1, self.tree_2]
        elif len(self.tree_2.selection()) > 0:
            self.tv_order = [self.tree_1, self.tree_2]
        return self.tv_order



    def active_selection(self):
        if len(self.tree_1.selection()) > 0:
            return self.tree_1.item(self.tree_1.focus())
        elif len(self.tree_2.selection()) > 0:
            return self.tree_2.item(self.tree_2.focus())


    def rename(self, logic):
        path = self.active_selection()['text']
        if self.active_selection()['values'][0] != '/..':
            self.create_user_window()
            self.uf_entry.grid(row=1, column=0, columnspan=2, ipady=3, pady=10, padx=20, sticky=NSEW)
            self.uf_label.configure(text='Enter New Name:')
            self.entry_text.set(Path(path).name)
            self.uf_ok_button.configure(command=lambda: logic.rename(path, self.destroy_user_window))


    def edit_permisions(self, logic):
        path = self.active_selection()['text']
        if self.active_selection()['values'][0] != '/..':
            self.create_user_window()
            self.uf_perm.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
            self.uf_label.configure(text='Chmod')
            self.entry_text.set(Path(path).name)
            logic.get_obj_perm(path, self.permissions)
            self.uf_ok_button.configure(command=lambda: logic.set_obj_perm(path, self.permissions, self.destroy_user_window))



    def toggle_tree_info(self, event, tv):
        '''Pokazwa i skriwa dopylnitelnite koloni '''
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
            self.tree_paths[self.tree_1] = path
            self.lf_1.configure(text=path)
        else:
            self.tree_paths[self.tree_1] = path
            self.lf_2.configure(text=path)



    def item_selected_click(self, event, logic, tree_view):
        '''Double click / izbor na papka.'''
        region = tree_view.identify("region", event.x, event.y)
        if region == 'heading':
            pass
        elif region == 'cell':
            self.item_selected_enter(logic, tree_view)

    #
    def item_selected_enter(self, logic, tree_view):
        selected_path = tree_view.item(tree_view.selection())['text']
        logic.insert_tree_values(tree_view, selected_path)
        self.update_tree_home_path(tree_view, selected_path)
        #print(bool(os.stat(selected_path).st_mode & stat.S_IRGRP))
        # def isgroupreadable(filepath):
        #     st = os.stat(filepath)
        #     return bool(st.st_mode & stat.S_IRGRP)


    #
    def update_active_position(self, event, tv):
        '''obnowqwa reda za izbrana pappka '''
        if tv == self.tree_1:
            self.last_selection_tree_1 = self.tree_1.focus()
            self.tree_1.selection_set(self.last_selection_tree_1)
            self.tree_2.selection_toggle(self.tree_2.selection())
            self.active_pos_1.set(tv.item(self.tree_1.selection())['values'][0])

        else:
            self.last_selection_tree_2 = self.tree_2.focus()
            self.tree_2.selection_set(self.last_selection_tree_2)
            self.tree_1.selection_toggle(self.tree_1.selection())
            self.active_pos_2.set(tv.item(self.tree_2.selection())['values'][0])


    #
    def accepted_characters(self, S):
        if S != '/':
            return True
        return False

    def create_user_window(self):
        '''Creates new Toplavel window, and places it in the center of the mainwindow.
        Creates , buttons, label and entry.'''
        self.user_window = Toplevel(root)
        self.user_window.transient(master=root)
        self.user_window.wm_attributes('-type', 'splash')
        self.user_window.grab_set()
        #


        self.uf_label = ttk.Label(self.user_window)
        self.uf_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))  ##########

        self.entry_text = StringVar()
        vcmd = (root.register(self.accepted_characters), '%S')
        self.uf_entry = Entry(self.user_window, width=25, textvariable=self.entry_text, validate='key', vcmd=vcmd)

        self.uf_ok_button = ttk.Button(self.user_window, text='OK')
        self.uf_ok_button.grid(row=2, column=0, pady=(0, 10))

        self.uf_cancel_button = ttk.Button(self.user_window, text='Cancel', command=self.destroy_user_window)
        self.uf_cancel_button.grid(row=2, column=1, pady=(0, 10))


        var_s_irusr = IntVar()
        var_s_iwusr = IntVar()
        var_s_ixusr = IntVar()
        var_s_irgrp = IntVar()
        var_s_iwgrp = IntVar()
        var_s_ixgrp = IntVar()
        var_s_iroth = IntVar()
        var_s_iwoth = IntVar()
        var_s_ixoth = IntVar()

        self.permissions = {
            'Read by owner': [stat.S_IRUSR, var_s_irusr],
            'Write by owner': [stat.S_IWUSR, var_s_iwusr],
            'Execute by owner': [stat.S_IXUSR, var_s_ixusr],
            'Read by group': [stat.S_IRGRP, var_s_irgrp],
            'Write by group': [stat.S_IWGRP, var_s_iwgrp],
            'Execute by group': [stat.S_IXGRP, var_s_ixgrp],
            'Read by others': [stat.S_IROTH, var_s_iroth],
            'Write by others': [stat.S_IWOTH, var_s_iwoth],
            'Execute by others': [stat.S_IXOTH, var_s_ixoth]
        }

        self.uf_perm = ttk.Frame(self.user_window)
        for index, perm in enumerate(self.permissions):
            Checkbutton(self.uf_perm, text=perm, variable=self.permissions[perm][1]).grid(row=index, column=1, sticky=W)

        self.user_window.update()
        self.user_frame_position()

    def user_frame_position(self):
        '''Moves user window with main window'''
        x_r = self.root.winfo_x()
        y_r = self.root.winfo_y()
        w_r = self.root.winfo_width()
        h_r = self.root.winfo_height()

        w_uf = self.user_window.winfo_width()
        h_uf = self.user_window.winfo_height()
        self.user_window.geometry(f"+{x_r + (w_r - w_uf) // 2}+{y_r + (h_r - h_uf) // 2}")

    def move_user_frame(self, event):
        if self.user_window is not None:
            self.user_frame_position()

    def destroy_user_window(self):
        self.user_window.destroy()
        self.user_window = None





root = Tk()

logic1 = MainLogic()

gui = UI(root, logic1)

logic1.insert_tree_values(gui.tree_2, os.path.expanduser('~'))
logic1.insert_tree_values(gui.tree_1, os.path.expanduser('~'))

root.mainloop()
