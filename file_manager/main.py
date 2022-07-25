#!/usr/bin/env python3
from tkinter import *
import os
from file_manager.file_manager_model import FileManagerModel
from file_manager.file_manager_view import FileManagerView
from file_manager.file_manager_presenter import FileManagerPresenter


root = Tk()
gui = FileManagerView(root)

brain = FileManagerModel()

fm = FileManagerPresenter(gui, brain)

brain.insert_tree_values(gui.tree_2, os.path.expanduser('~'))
brain.insert_tree_values(gui.tree_1, os.path.expanduser('~'))

fm.update_tree_home_path(gui, gui.tree_2, os.path.expanduser('~'))
fm.update_tree_home_path(gui, gui.tree_1, os.path.expanduser('~'))

# for attribute, value in gui.__dict__.items():
#     print(attribute, '=', value)
root.mainloop()
