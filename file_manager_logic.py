from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import stat
from pathlib import Path
import shutil
from datetime import datetime


class MainLogic:

    def __init__(self):
        #self.current_folder = os.path.expanduser('~')
        #self.current_selection = None
        self.tree_paths = [[None], [None], [None]]
        self.copied_object = None
        self.cut_object = None


    #
    def get_update_tree(self, path, sort_key=1):  # try except  NotADirectoryError: [Errno 20] Not a directory: '/tmp/config-err-L3yImR'

        self.tree_paths[1].clear()  # s.system("open " + shlex.quote(filename))  import subprocess, os, platformif platform.system() == 'Darwin':       # macOS    subprocess.call(('open', filepath))elif platform.system() == 'Windows':    # Windows    os.startfile(filepath)else:                                   # linux variants    subprocess.call(('xdg-open', filepath))
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

    def insert_tree_values(self, tv, path):
        ''' zarejda informaciqta ot logikata w izbranoto TV'''
        try:
            dir_items = self.get_update_tree(path)
        except PermissionError as pe:
            messagebox.showerror('Error', pe.strerror)
        else:
            for entry in tv.get_children():
                tv.delete(entry)
            for index, item in enumerate(dir_items[1]):
                tv.insert('', END, tags='dir', iid=self.tree_paths[1][index][0], text=self.tree_paths[1][index][0],
                          values=tuple(self.tree_paths[1][index][1:]))

            for index, item in enumerate(dir_items[2]):
                tv.insert('', END, tags='file', text=self.tree_paths[2][index][0],
                          values=tuple(self.tree_paths[2][index][1:]))

            tv.focus(tv.get_children()[0])
            tv.selection_set(tv.get_children()[0])




    def rename(self, path, entry_text, destroy_user_window):

        base_path = str(Path(path).parent)
        old_name = str(Path(path).name)
        if old_name != entry_text.get():
            try:
                os.rename(path, '/'.join([base_path, entry_text.get()]))
            except PermissionError as pe:
                messagebox.showerror('Error', pe.strerror)
        destroy_user_window()

    def delete_file_dir(self, selection):
        path = selection()['text']
        if selection()['values'][0] != '/..':
            if messagebox.askyesno('Delete', 'Are you sure you want to delete {}?'.format(Path(selection()['text']).name)):
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                except PermissionError as pe:
                    messagebox.showerror('Error', pe.strerror)

    def copy_file_folder(self, selection):
        path = selection()['text']
        if selection()['values'][0] != '/..':
            self.copied_object = path
            self.cut_object = None
            # tv.item(selection(), tags='copy')
            # print(selection()['tags'])

            ### da se otrazqwa kopiraneto


    def cut_file_folder(self, selection):
        path = selection()['text']
        if selection()['values'][0] != '/..':
            self.copied_object = None
            self.cut_object = path
            # tv.item(selection(), tags='copy')
            # print(selection()['tags'])

            ### da se otrazqwa kopiraneto

    def paste(self, selected, location):
    #
    # def rename_file(self, *args):
    #     lb, new_name, del_edit_spot, refresh_lb, old_name = args
    #     self.get_tree(lb)
    #     self.current_root = self.get_active_lb_root()
    #     os.chdir(self.current_root)
    #     if old_name != new_name:
    #         os.rename(old_name, new_name)
    #     del_edit_spot()
    #     refresh_lb()


    #
    # def search_alg(self, search_dir, name):
    #     results = []
    #     for root, dirs, files in os.walk(search_dir):
    #         for file in files:
    #             if name.lower() in file.lower():
    #                 results.append(root + '/' + str(file))
    #         for dir_ in dirs:
    #             if name.lower() in dir_.lower():
    #                 results.append(root + '/' + str(dir_))
    #     return results


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