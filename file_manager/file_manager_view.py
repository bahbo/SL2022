from tkinter import *
from tkinter import ttk
from pathlib import Path
from file_manager.main_window import MainWindow


class FileManagerView(MainWindow):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.u_window = None
        self.uw_label = ttk.Label(self.u_window)
        self.entry_text = StringVar()
        vcmd = (main_window.register(self.accepted_characters), '%S')
        self.uw_entry = Entry(self.u_window, width=25, textvariable=self.entry_text, validate='key', vcmd=vcmd)

        # Buttons
        self.ok_button = ttk.Button(self.u_window, text='OK')
        self.cancel_button = ttk.Button(self.u_window, text='Cancel', command=self.destroy_user_window)

        # chmod widgets
        self.uf_perm = ttk.Frame(self.u_window)
        var_irusr = IntVar()
        var_iwusr = IntVar()
        var_ixusr = IntVar()
        var_irgrp = IntVar()
        var_iwgrp = IntVar()
        var_ixgrp = IntVar()
        var_iroth = IntVar()
        var_iwoth = IntVar()
        var_ixoth = IntVar()

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

    def show_user_window(self):
        self.u_window = Toplevel(self.root)
        self.u_window.transient(self.root)
        self.u_window.wm_attributes('-type', 'splash')
        self.u_window.grab_set()

    def add_label(self):
        self.uw_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

    def add_buttons(self):
        self.ok_button.grid(row=2, column=0, pady=(0, 10))
        self.cancel_button.grid(row=2, column=1, pady=(0, 10))

    def info_screen(self, main_window, logic):
        """Show system information."""
        self.show_user_window()
        self.add_label()
        self.uw_label.configure(text='System Information')
        self.ok_button.grid(row=2, column=0, pady=(0, 10))
        self.ok_button.configure(command=lambda: self.destroy_user_window)
        self.info_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=20)

        for i, item in enumerate(logic.system_information()):
            Label(self.info_frame, text=item[0], anchor=W).grid(row=i, column=0, sticky=EW)
            Label(self.info_frame, text=item[1], anchor=W).grid(row=i, column=1, sticky=EW)

        self.cancel_button.grid_forget()
        self.u_window_position(main_window)

    #
    def rename(self):
        """Rename selected object."""
        self.show_user_window()
        self.add_buttons()
        self.uw_label.configure(text='Enter New Name:')
        self.uw_entry.grid(row=1, column=0, columnspan=2, ipady=3, pady=10, padx=20, sticky=NSEW)

        self.u_window_position()

    def chmod_window(self, main_window, selection, logic):
        """Change objects permissions"""
        self.show_user_window(main_window)
        self.add_buttons()
        path = selection()['text']
        if selection()['values'][0] != '/..':
            self.uw_label.configure(text=f"chmod: {Path(path).name}")
            self.uf_perm.grid(row=1, column=0, columnspan=2, pady=10, padx=20)
            logic.get_obj_perm(path, self.permissions)
            self.ok_button.configure(
                command=lambda: logic.set_obj_perm(path, self.permissions, self.destroy_user_window))

            self.u_window_position(main_window)

    #
    def chown_window(self, main_window, selection, logic):
        self.show_user_window(main_window)
        self.add_buttons()
        """Change objects group or/and owner"""
        path = selection()['text']
        if selection()['values'][0] != '/..':
            self.uw_label.configure(text=f"chown: {Path(path).name}")
            self.uf_owner.grid(row=1, column=0, columnspan=2, pady=10, padx=20)

            self.cb_groups.configure(values=logic.get_groups())
            self.groups_var.set(Path(path).group())
            self.cb_users.configure(values=logic.get_users())
            self.users_var.set(Path(path).owner())

            self.ok_button.configure(
                command=lambda: logic.obj_chown(path, self.users_var, self.groups_var, self.destroy_user_window))
            self.u_window.update()
            self.u_window_position(main_window)

    #
    def accepted_characters(self, S):
        if S != '/':
            return True
        return False

    def u_window_position(self):
        """Places user window in the center of main window"""
        self.u_window.update()
        x_r = self.root.winfo_x()
        y_r = self.root.winfo_y()
        w_r = self.root.winfo_width()
        h_r = self.root.winfo_height()

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
