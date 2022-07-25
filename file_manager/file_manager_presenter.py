#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
import os

import stat
from pathlib import Path
from datetime import datetime


class FileManagerPresenter:

    def __init__(self, view, model):
        self.last_selection_tree_1 = None
        self.last_selection_tree_2 = None
        self.tree_paths = {view.tree_1: None, view.tree_2: None}
        view.root.bind("<Configure>", lambda event: view.move_user_window(event, view.root))

        view.tree_1.bind('<Double-Button-1>', lambda event: self.item_selected_click(event, model, view, view.tree_1))
        view.tree_2.bind('<Double-Button-1>', lambda event: self.item_selected_click(event, model, view, view.tree_2))

        view.tree_1.bind('<Return>', lambda event: self.item_selected_enter(model, view.tree_1))
        view.tree_2.bind('<Return>', lambda event: self.item_selected_enter(model, view.tree_2))

        view.tree_1.bind('<FocusIn>', lambda event: self.toggle_tv(event, view.tree_1, view))
        view.tree_2.bind('<FocusIn>', lambda event: self.toggle_tv(event, view.tree_2, view))

        view.tree_1.bind('<F5>', lambda event: self.toggle_tree_info(event, view.tree_1))
        view.tree_2.bind('<F5>', lambda event: self.toggle_tree_info(event, view.tree_2))

        view.tree_1.bind('<<TreeviewSelect>>', lambda event: self.active_selection(event, view))
        view.tree_2.bind('<<TreeviewSelect>>', lambda event: self.active_selection(event, view))

        ######

        #

    def tv_list(self, view):
        if len(view.tree_1.selection()) > 0:
            self.tv_order = [view.tree_1, view.tree_2]
        elif len(view.tree_2.selection()) > 0:
            self.tv_order = [view.tree_2, view.tree_1]
        return self.tv_order

        #

    def active_selection(self, event, view):
        if len(view.tree_1.selection()) > 0:
            view.active_pos_1.set(view.tree_1.item(view.tree_1.selection())['values'][0])
            return view.tree_1.item(view.tree_1.focus())
        elif len(view.tree_2.selection()) > 0:
            view.active_pos_2.set(view.tree_2.item(view.tree_2.selection())['values'][0])
            return view.tree_2.item(view.tree_2.focus())

        #

    def rename(self, model):
        path = self.active_selection()['text']
        if self.active_selection()['values'][0] != '/..':
            self.create_user_window()
            self.uw_entry.grid(row=1, column=0, columnspan=2, ipady=3, pady=10, padx=20, sticky=NSEW)
            self.uw_label.configure(text='Enter New Name:')
            self.entry_text.set(Path(path).name)
            self.ok_button.configure(command=lambda: model.rename(path, self.entry_text, self.destroy_user_window))
            self.u_window.update()
            self.u_window_position()

    def info(self, model):
        self.create_user_window()
        self.uw_label.configure(text='System Information')
        self.ok_button.configure(command=lambda: self.destroy_user_window)
        self.info_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=20)

        for i, item in enumerate(model.system_information()):
            Label(self.info_frame, text=item[0], anchor=W).grid(row=i, column=0, sticky=EW)
            Label(self.info_frame, text=item[1], anchor=W).grid(row=i, column=1, sticky=EW)

        self.u_window.update()
        self.u_window_position()

        #

    def change_permisions(self, model):
        path = self.active_selection()['text']
        if self.active_selection()['values'][0] != '/..':
            self.create_user_window()
            self.uf_perm.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
            self.uw_label.configure(text=f"chmod: {Path(path).name}")
            model.get_obj_perm(path, self.permissions)
            self.ok_button.configure(
                command=lambda: model.set_obj_perm(path, self.permissions, self.destroy_user_window))
            self.u_window.update()
            self.u_window_position()

    def change_owner_group(self, model):
        path = self.active_selection()['text']
        if self.active_selection()['values'][0] != '/..':
            self.create_user_window()
            self.uf_owner.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
            self.uw_label.configure(text=f"chown: {Path(path).name}")

            self.cb_groups.configure(values=model.get_groups())
            self.groups_var.set(Path(path).group())
            self.cb_users.configure(values=model.get_users())
            self.users_var.set(Path(path).owner())

            self.ok_button.configure(
                command=lambda: model.obj_chown(path, self.users_var, self.groups_var, self.destroy_user_window))
            self.u_window.update()
            self.u_window_position()

    def search(self, model, tv):
        self.create_user_window()
        # self.uf_owner.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
        self.uw_label.configure(text='Search in:')
        self.uw_label.grid(row=0, column=0, )
        self.uw_entry.grid(row=2, column=0, columnspan=2, ipady=3, pady=10, padx=20, sticky=NSEW)
        self.cb_search_dir.grid(column=0, row=1, columnspan=2, pady=(10, 0))
        self.cb_search_dir.configure(values=['current dir', 'home', 'all'])
        self.cb_search_dir_var.set('current dir')
        if self.cb_search_dir_var.get() == 'current dir':
            path = self.active_selection()['text']
        elif self.cb_search_dir_var.get() == 'home':
            path = os.path.expanduser('~')
        else:
            path = '/'
        print(self.tv_list)
        self.ok_button.configure(
            command=lambda: model.search_alg(path, tv, self.entry_text.get(), self.destroy_user_window))
        self.u_window.update()
        self.u_window_position()

        #

    def toggle_tree_info(self, event, tv):
        """Pokazwa i skriwa dopylnitelnite koloni - F5"""
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

        #

    def update_tree_home_path(self, view, tv, path):
        """obnowqwa nadpisa gore w lqwo"""

        if tv == view.tree_1:
            self.tree_paths[view.tree_1] = path
            view.lf_1.configure(text=path)
        else:
            self.tree_paths[view.tree_1] = path
            view.lf_2.configure(text=path)

        #

    def item_selected_click(self, event, model, view, tree_view):
        """Double click / izbor na papka."""
        region = tree_view.identify("region", event.x, event.y)
        if region == 'heading':
            pass
        elif region == 'cell':
            self.item_selected_enter(model, view, tree_view)

        #

    def item_selected_enter(self, model, view, tree_view):
        selected_path = tree_view.item(tree_view.selection())['text']
        model.insert_tree_values(tree_view, selected_path)
        self.update_tree_home_path(view, tree_view, selected_path)

        #

    def toggle_tv(self, event, tv, view):
        """toggle selection between treeviews """
        if tv == view.tree_1:
            self.last_selection_tree_1 = view.tree_1.focus()
            view.tree_1.selection_set(self.last_selection_tree_1)
            view.tree_2.selection_toggle(view.tree_2.selection())
        else:
            self.last_selection_tree_2 = view.tree_2.focus()
            view.tree_2.selection_set(self.last_selection_tree_2)
            view.tree_1.selection_toggle(view.tree_1.selection())
