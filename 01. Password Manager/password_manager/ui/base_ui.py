"""Base functionality for a Toplevel window"""

from tkinter import Toplevel, PhotoImage
from os.path import join
from password_manager.data_management.all_data import data
from password_manager.constants import ICONS_DIR


class Window(Toplevel):
    """Base class for every UI Toplevel Window"""

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.icons = {}
        self.widgets = {}

    def setup(self, width, height):
        """Create and set up the window"""
        root_center_x = int((self.root.winfo_x() + self.root.winfo_width() / 2) - (width / 2))
        root_center_y = int((self.root.winfo_y() + self.root.winfo_height() / 2) - (height / 2))
        self.geometry(f'{width}x{height}+{root_center_x}+{root_center_y}')
        self.config(background=data.colors['bgc'])
        self.iconbitmap(join(ICONS_DIR, "icon.ico"))
        self.focus_force()

    def define_icons(self):
        """Defines Icons"""
        self.icons['logo2'] = PhotoImage(master=self, file=join(ICONS_DIR, "logo.png"))
        self.icons['user_icon'] = PhotoImage(master=self, file=join(ICONS_DIR, "user.png"))
        self.icons['pass_icon'] = PhotoImage(master=self, file=join(ICONS_DIR, "password.png"))
        self.icons['email_icon'] = PhotoImage(master=self, file=join(ICONS_DIR, "email.png"))
        self.icons['eye_icon'] = PhotoImage(file=join(ICONS_DIR, "eye.png"))
        self.icons['no_eye_icon'] = PhotoImage(file=join(ICONS_DIR, "no_eye.png"))
        self.icons['eye_icon_h'] = PhotoImage(file=join(ICONS_DIR, "eye_hover.png"))
        self.icons['no_eye_icon_h'] = PhotoImage(file=join(ICONS_DIR, "no_eye_hover.png"))
