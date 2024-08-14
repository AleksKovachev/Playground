"""This module contains the class responsible for the Options menu window UI"""

import os
from tkinter import Frame, Label, Button, Entry, Spinbox, LabelFrame, PhotoImage, NW, NE, SE, FLAT

from password_manager.constants import FONT_C, FONT_F, ICONS_DIR
from password_manager.data_management.all_data import data, file_data
from password_manager.widgets import PWDEntry
from password_manager.ui.base_ui import Window


class CustomizationSettingsBase(Window):
    """Defines the Customization settings window"""

    def __init__(self, tk_vars, main_window_fields):
        """Creating a Toplevel window for the Customization Settings

        Args:
            tk_vars (dict): Tkinter variables coming from the main window class
            main_window_fields (dict): Tkinter Entry boxes/Comboboxes from the main window class
        """
        super().__init__(root=data.wins['root'])

        self.main_tk_vars       = tk_vars
        self.main_window_fields = main_window_fields
        self.max_width          = 0
        self.l_pane             = {'wid': 175, 'pad': 10}

        self.setup(width=550, height=225)
        self.define_icons()
        self.draw_ui()

    def setup(self, width, height):
        """Create and set up the Customizations window"""
        super().setup(width=width, height=height)
        data.wins['sett'] = self
        self.minsize(width, height)

        # Make the main window unclickable until this one is closed
        self.grab_set()

        # Make it a tool window (only X button)
        self.attributes('-toolwindow', True)

    def define_icons(self):
        """Defines Icons"""
        self.icons['eye_icon']      = PhotoImage(file=os.path.join(ICONS_DIR, "eye.png"))
        self.icons['no_eye_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "no_eye.png"))
        self.icons['eye_icon_h']    = PhotoImage(file=os.path.join(ICONS_DIR, "eye_hover.png"))
        self.icons['no_eye_icon_h'] = PhotoImage(file=os.path.join(ICONS_DIR, "no_eye_hover.png"))

    def draw_ui(self):
        """Draws the UI for the Customizations window"""
        self.define_ui()
        self.draw_left_panel()
        self.draw_right_panel_login()
        self.draw_right_panel_default()

    def define_ui(self):
        """Defines the UI widgets for the Customizations window"""
        self.define_left_panel()
        self.define_right_panel_login()
        self.define_right_panel_default()

    def define_left_panel(self):
        """Defines the widgets for the left panel"""
        self.widgets['tab1'] = Frame(self, background=data.colors['accent'])
        common = {
            'master'          : self.widgets['tab1'],
            'relief'          : FLAT,
            'border'          : 0,
            'font'            : FONT_C,
            'foreground'      : data.colors['details1'],
            'activebackground': data.colors['bgc'],
            'activeforeground': data.colors['details1']
        }
        self.widgets['login_btn'] = Button(
            **common,
            text=file_data.lang['customize']['left_panel']['login_btn'],
            background=data.colors['bgc']
        )
        self.widgets['default_btn'] = Button(
            **common,
            text=file_data.lang['customize']['left_panel']['default_btn'],
            background=data.colors['shadow']
        )

    def define_right_panel_login(self):
        """Defines the widgets for the login panel on the right"""
        self.widgets['tab2'] = Frame(self, background=data.colors['bgc'])
        common = {
            'master'    : self.widgets['tab2'],
            'font'      : FONT_C,
            'background': data.colors['bgc'],
            'foreground': data.colors['details1']
        }
        text = file_data.lang['customize']['right_panel_login']
        self.widgets['user_login']     = Label(**common, text=text['user'])
        self.widgets['password_login'] = Label(**common, text=text['password'])
        self.widgets['old_pwd_login']  = Label(**common, text=text['old_pwd'])
        self.widgets['new_pwd_login']  = Label(**common, text=text['new_pwd'])
        self.widgets['rep_pwd_login']  = Label(**common, text=text['rep_pwd'])

        common = {
            'master': self.widgets['tab2'],
            'width': 29,
            'background': data.colors['details2'],
            'foreground': data.colors['fgc'],
            'border': 0,
            'font': FONT_C,
            'selectbackground': data.colors['bgc'],
            'image': self.icons['no_eye_icon'],
            'show': "✲"
        }
        usr_options = {k: v for k, v in common.items() if k not in ('image', 'show')}
        self.widgets['user_entry']    = Entry(**usr_options)
        self.widgets['old_pwd_entry'] = PWDEntry(**common)
        self.widgets['new_pwd_entry'] = PWDEntry(**common)
        self.widgets['rep_pwd_entry'] = PWDEntry(**common)
        self.widgets['user_entry'].insert(0, f"{data.autofils['user']}")

    def define_right_panel_default(self):
        """Defines the widgets for the Defaults panel on the right"""
        self.widgets['tab3'] = Frame(self, background=data.colors['bgc'])
        common = {
            'master': self.widgets['tab3'],
            'font': FONT_C,
            'background': data.colors['bgc'],
            'foreground': data.colors['details1']
        }
        text = file_data.lang['customize']['right_panel_default']
        self.widgets['user_default']  = Label(**common, text=text['user'])
        self.widgets['email_default'] = Label(**common, text=text['email'])

        common = {
            'master': self.widgets['tab3'],
            'width': 29,
            'font': FONT_C,
            'border': 0,
            'background': data.colors['details2'],
            'foreground': data.colors['fgc'],
            'selectbackground': data.colors['bgc']
        }

        self.widgets['new_user']  = Entry(**common)
        self.widgets['new_email'] = Entry(**common)
        self.widgets['new_user'].insert( 0, f"{data.autofils['default_user']}")
        self.widgets['new_email'].insert(0, f"{data.autofils['default_email']}")

        self.widgets['apply_btn'] = Button(
            self,
            text=file_data.lang['customize']['apply_btn'],
            font=FONT_C,
            background=data.colors['bgc'],
            foreground=data.colors['details1']
        )

        self.widgets['autoclose'] = LabelFrame(
            self.widgets['tab3'],
            text=text['autoclose'],
            height=75,
            background=data.colors['bgc'],
            foreground=data.colors['details1'],
            font=FONT_F
        )
        text = file_data.lang['customize']['right_panel_default']
        common = {
            'master': self.widgets['autoclose'],
            'background': data.colors['bgc'],
            'foreground': data.colors['details1'],
            'font': FONT_C
        }
        self.widgets['autoclose_label'] = Label(**common, text=text['mins'])
        self.widgets['autoclose_label2'] = Label(**common, text=text['tip'])
        self.widgets['ac_spin'] = Spinbox(
            self.widgets['autoclose'],
            from_=0,
            to=30,
            font=FONT_C,
            foreground=data.colors['details1'],
            background=data.colors['bgc'],
            border=1,
            width=2,
            buttonbackground=data.colors['bgc'],
            state='readonly',
            selectbackground=data.colors['accent'],
            readonlybackground=data.colors['bgc'],
            textvariable=self.main_tk_vars['autoclose_mins'],
            cursor='sb_v_double_arrow'
        )

    def draw_left_panel(self):
        """Defines and draws all widgets for the left panel"""
        self.widgets['tab1'].place(x=0, y=0, relheight=1, width=self.l_pane['wid'], anchor=NW)

        self.widgets['login_btn'].place(  relx=0, y=0,  relwidth=1, anchor=NW)
        self.widgets['default_btn'].place(relx=0, y=30, relwidth=1, anchor=NW)

    def draw_right_panel_login(self):
        """Defines and draws all widgets for the Login page in the Right Panel"""
        pwd_x_pos = 10

        self.widgets['tab2'].place(x=self.l_pane['wid'], relheight=1, anchor=NW)

        self.widgets['password_login'].place(x=pwd_x_pos, y=40, anchor=NW)

        x_pos = pwd_x_pos + self.widgets['password_login'].winfo_reqwidth()
        self.widgets['user_login'].place(   x=x_pos, y=10,  anchor=NE)
        self.widgets['old_pwd_login'].place(x=x_pos, y=70,  anchor=NE)
        self.widgets['new_pwd_login'].place(x=x_pos, y=100, anchor=NE)
        self.widgets['rep_pwd_login'].place(x=x_pos, y=130, anchor=NE)

        self.max_width = max(
            self.widgets['user_login'].winfo_reqwidth(),
            self.widgets['password_login'].winfo_reqwidth(),
            self.widgets['old_pwd_login'].winfo_reqwidth(),
            self.widgets['new_pwd_login'].winfo_reqwidth(),
            self.widgets['rep_pwd_login'].winfo_reqwidth()
        )

    def draw_right_panel_default(self):
        """Defines and draws all widgets for the Default page in the Right Panel"""
        pwd_login_width = self.widgets['password_login'].winfo_reqwidth()
        self.widgets['user_default'].place(x=10 + pwd_login_width, y=10, anchor=NE)
        self.widgets['email_default'].place(x=10 + pwd_login_width, y=40, anchor=NE)

        self._autoclose_frame()

    def _autoclose_frame(self):
        """Define and draw a frame within the Default panel to store Autoclose settings."""
        self.widgets['autoclose_label'].place(x=5, y=0, anchor=NW)
        self.widgets['autoclose_label2'].place(x=5, y=25, anchor=NW)

        self.widgets['autoclose_label'].update()
        label = self.widgets['autoclose_label']
        self.widgets['ac_spin'].place(x=label.winfo_x() + label.winfo_width(), y=0, anchor=NW)
        self.widgets['apply_btn'].place(anchor=SE)
