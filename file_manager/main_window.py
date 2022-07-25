#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
# import os
# from file_manager_logic import MainLogic
# import stat
# from pathlib import Path
# from datetime import datetime


class MainWindow:
    def __init__(self, main_window):
        self.root = main_window
        self.root.title('File Manager')

        self.my_style = ttk.Style()
        # my_style.theme_use('default')
        # print(my_style.theme_names())
        # my_style.configure('.', font=('Monospace', 11), bg='SteelBlue3', forground='blue')
        self.my_style.configure('TLabel',
                                background='cyan4',
                                font=('Monospace', 11))
        # self.my_style.configure('TFrame', background='red')

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

        self.my_style.map('TButton', relief=FLAT,
                          background=[('pressed', 'cyan4'), ('active', 'cyan4'), ('!active', 'cyan4')])
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

        self.tree_1.focus_set()

        self.tree_2 = ttk.Treeview(self.lf_2, columns=('#1', '#2', '#3', '#4', '#5', '#6'), show='headings',
                                   selectmode='browse')
        self.tree_2.pack(fill='both', side=LEFT, expand=True)

        #
        for tree in (self.tree_1, self.tree_2):
            tree["displaycolumns"] = ('#1', '#2', '#3')
            tree.tag_configure('dir', foreground='light gray')
            tree.tag_configure('file', foreground='cyan4')
            tree.tag_configure('copy', foreground='yellow')
            tree.tag_configure('cut', foreground='cyan4')

            tree.heading('#1', text='Name',)
            tree.heading('#2', text='Size')
            tree.heading('#3', text='Modify time')

            tree.column('#1', minwidth=250, width=250)
            tree.column('#2', width=75, stretch=False, anchor=E)
            tree.column('#3', width=120, stretch=False)

        #
        # ttk.Separator(self.root, orient='horizontal', ).grid(row=3, column=0, sticky="ew")

        self.b_frame = Frame(self.root)
        self.b_frame.grid(row=4, column=0, columnspan=2, sticky=EW)

        self.f1 = ttk.Button(self.b_frame, text='F1 Info', takefocus=0, underline=1)
        self.f1.grid(row=0, column=0, sticky=EW)

        self.f2 =  ttk.Button(self.b_frame, text='F2 Rename', takefocus=0, underline=1)
        self.f2.grid(row=0, column=1, sticky=EW)

        self.f3 =  ttk.Button(self.b_frame, text='F3 Cut', takefocus=0, underline=1)
        self.f3.grid(row=0, column=2, sticky=EW)

        self.f4 =  ttk.Button(self.b_frame, text='F4 Copy', takefocus=0, underline=1)
        self.f4.grid(row=0, column=3, sticky=EW)

        self.f5 =  ttk.Button(self.b_frame, text='F5 Paste', takefocus=0, underline=1)
        self.f5.grid(row=0, column=4, sticky=EW)

        self.f6 =  ttk.Button(self.b_frame, text='F6 Chmod', takefocus=0, underline=1)
        self.f6.grid(row=0, column=5, sticky=EW)

        self.f7 =  ttk.Button(self.b_frame, text='F7 Chown', takefocus=0, underline=1)
        self.f7.grid(row=0, column=6, sticky=EW)

        self.f8 =  ttk.Button(self.b_frame, text='F8 Search', takefocus=0, underline=1)
        self.f8.grid(row=0, column=7, sticky=EW)

        self.f9 =  ttk.Button(self.b_frame, text='F9 Delete', takefocus=0, underline=1)
        self.f9.grid(row=0, column=8, sticky=EW)

        self.f10 =  ttk.Button(self.b_frame, text='F10 Quite', takefocus=0, underline=1)
        self.f10.grid(row=0, column=9, sticky=EW)




        for x in range(9):
            self.b_frame.columnconfigure(x, weight=1, uniform='label')
