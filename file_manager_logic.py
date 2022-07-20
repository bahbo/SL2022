from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import stat
from pathlib import Path
from datetime import datetime


class MainLogic:

    def __init__(self):
        self.current_folder = os.path.expanduser('~')
        self.current_selection = None
        self.tree_paths = [[None], [None], [None]]

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
            messagebox.showerror("showerror", f'{pe}')
        else:
            for entry in tv.get_children():
                tv.delete(entry)
            for index, item in enumerate(dir_items[1]):
                tv.insert('', END, tags='dir', text=self.tree_paths[1][index][0],
                          values=tuple(self.tree_paths[1][index][1:]))

            for index, item in enumerate(dir_items[2]):
                tv.insert('', END, tags='file', text=self.tree_paths[2][index][0],
                          values=tuple(self.tree_paths[2][index][1:]))

            tv.focus(tv.get_children()[0])
            tv.selection_set(tv.get_children()[0])




    def rename(self, selection, entry_text, uf_label, destroy_user_window):
        #tv_order, uf_label, entry_text, destroy_user_window = args

        if selection['values'][0] != '/..':
            path = selection['text']
            base_path = path.rsplit('/', 1)[0]
            old_name = path.rsplit('/', 1)[1]
            if old_name != entry_text.get():
                try:
                    os.rename(path, '/'.join([base_path, entry_text.get()]))
                except PermissionError as pe:
                    messagebox.showerror("showerror", f'{pe}')
            destroy_user_window()



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