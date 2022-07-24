#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
import os
from file_manager_logic import MainLogic
import stat
from pathlib import Path
from datetime import datetime


class UserWindow:
    def __init__(self, main_window, logic):
        self.u_window = Toplevel(main_window)
        self.u_window.transient(master=main_window)
        self.u_window.wm_attributes('-type', 'splash')
        self.u_window.grab_set()

        # Buttons
        self.ok_button = ttk.Button(self.u_window, text='OK')
        self.ok_button.grid(row=3, column=0, pady=(0, 10))

        self.cancel_button = ttk.Button(self.u_window, text='Cancel', command=self.destroy_user_window)
        self.cancel_button.grid(row=3, column=1, pady=(0, 10))

        # Label
        self.uw_label = ttk.Label(self.u_window)
        self.uw_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        # Entry
        self.entry_text = StringVar()
        vcmd = (main_window.register(self.accepted_characters), '%S')
        self.uw_entry = Entry(self.u_window, width=25, textvariable=self.entry_text, validate='key', vcmd=vcmd)

        # chmod widgets
        self.uf_perm = ttk.Frame(self.u_window)
        var_irusr, var_iwusr, var_ixusr, var_irgrp, var_iwgrp, var_ixgrp, var_iroth, var_iwoth, var_ixoth = IntVar()

        self.permissions = [
            ['Read by owner', var_irusr],
            ['Write by owner', var_iwusr],
            ['Execute by owner', var_ixusr],
            ['Read by group', var_irgrp],
            ['Write by group', var_iwgrp],
            ['Execute by group', var_ixgrp],
            ['Read by others', var_iroth],
            ['Write by others', var_iwoth],
            ['Execute by others', var_ixoth]
        ]
        for index, value in enumerate(self.permissions):
            Checkbutton(self.uf_perm, text=value[0], variable=value[1]).grid(row=index, column=1, sticky=W)

        # chown widgets
        self.uf_owner = ttk.Frame(self.u_window)

        lf_owner = LabelFrame(self.uf_owner, text='User', labelanchor=N)
        lf_owner.grid(column=0, row=0)
        self.users_var = StringVar()
        self.cb_users = ttk.Combobox(lf_owner, textvariable=self.users_var, justify='center', state='readonly')
        self.cb_users.grid(column=0, row=0)

        lf_group = LabelFrame(self.uf_owner, text='Group', labelanchor=N)
        lf_group.grid(column=1, row=0)
        self.groups_var = StringVar()
        self.cb_groups = ttk.Combobox(lf_group, textvariable=self.groups_var, justify='center', state='readonly')
        self.cb_groups.grid(column=1, row=0)

        # search widgets
        self.cb_search_dir_var = StringVar()
        self.cb_search_dir = ttk.Combobox(self.u_window, textvariable=self.cb_search_dir_var, justify='center',
                                          state='readonly')
        # info
        self.info_frame = Frame(self.u_window)

    def info_screen(self, root, logic):
        """Show system information."""
        self.uw_label.configure(text='System Information')
        self.ok_button.configure(command=lambda: self.destroy_user_window)
        self.info_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=20)

        for i, item in enumerate(logic.system_information()):
            Label(self.info_frame, text=item[0], anchor=W).grid(row=i, column=0, sticky=EW)
            Label(self.info_frame, text=item[1], anchor=W).grid(row=i, column=1, sticky=EW)

        self.u_window.update()
        self.u_window_position(root)

    def rename(self, selection, logic):
        """Rename selected object."""
        path = selection()['text']
        if selection()['values'][0] != '/..':
            self.uw_label.configure(text='Enter New Name:')
            self.uw_entry.grid(row=1, column=0, columnspan=2, ipady=3, pady=10, padx=20, sticky=NSEW)
            self.entry_text.set(Path(path).name)
            self.ok_button.configure(command=lambda: logic.rename(path, self.entry_text, self.destroy_user_window))

            self.u_window.update()
            self.u_window_position()

    def chmod_window(self, selection, logic):
        """Change objects permisions"""
        path = selection()['text']
        if selection()['values'][0] != '/..':

            self.uf_perm.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
            self.uw_label.configure(text=f"chmod: {Path(path).name}")
            logic.get_obj_perm(path, self.permissions)
            self.ok_button.configure(
                command=lambda: logic.set_obj_perm(path, self.permissions, self.destroy_user_window))

            self.u_window.update()
            self.u_window_position()







    def chown_window(self):
        pass

    def accepted_characters(self, S):
        if S != '/':
            return True
        return False

    def u_window_position(self, main_window):
        """Places user window in the center of main window"""
        x_r = main_window.winfo_x()
        y_r = main_window.winfo_y()
        w_r = main_window.winfo_width()
        h_r = main_window.winfo_height()

        w_uf = self.u_window.winfo_width()
        h_uf = self.u_window.winfo_height()
        self.u_window.geometry(f"+{x_r + (w_r - w_uf) // 2}+{y_r + (h_r - h_uf) // 2}")

    def move_user_window(self, event):
        """Moves user window with main window"""
        if self.u_window is not None:
            self.u_window_position()

    def destroy_user_window(self):
        self.u_window.destroy()
        self.u_window = None
