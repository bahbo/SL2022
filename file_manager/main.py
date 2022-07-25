#!/usr/bin/env python3
from tkinter import *
import os
from file_manager.file_manager_model import FileManagerModel
from file_manager.file_manager_view import FileManagerView
from file_manager.file_manager_presenter import FileManagerPresenter
root = Tk()

brain = FileManagerModel()
gui = FileManagerView(main_window=root)
fm = FileManagerPresenter(gui, brain)

brain.insert_tree_values(gui.tree_2, os.path.expanduser('~'))
brain.insert_tree_values(gui.tree_1, os.path.expanduser('~'))

fm.update_tree_home_path(gui, gui.tree_2, os.path.expanduser('~'))
fm.update_tree_home_path(gui, gui.tree_1, os.path.expanduser('~'))

root.mainloop()
