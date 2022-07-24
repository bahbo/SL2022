#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
import os
from file_manager_logic import MainLogic
from ui.main_window import MainWindow
from ui.user_window import UserWindow

import stat
from pathlib import Path
from datetime import datetime


root = Tk()

logic1 = MainLogic()

gui = MainWindow(root, logic1)

logic1.insert_tree_values(gui.tree_2, os.path.expanduser('~'))
logic1.insert_tree_values(gui.tree_1, os.path.expanduser('~'))
gui.update_tree_home_path(gui.tree_2, os.path.expanduser('~'))
gui.update_tree_home_path(gui.tree_1, os.path.expanduser('~'))

root.mainloop()
