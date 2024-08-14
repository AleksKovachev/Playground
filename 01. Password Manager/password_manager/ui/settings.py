"""This module contains the class responsible for the Options menu window UI"""

from tkinter import messagebox, NW, END

from password_manager.ui.access_control import eye_switch_color
from password_manager.data_management.all_data import data, file_data
from password_manager.security.authenticate import check_email, check_username, check_password
from password_manager.security.encryption import hash_password, verify_password, cipher, decipher
from password_manager.ui.visibility_toggle import PwdButton, check_pass_btn
from .settings_base import CustomizationSettingsBase


#+ pylint: disable=unused-argument


class CustomizationSettings(CustomizationSettingsBase):
    """Defines the Customization settings window"""

    def __init__(self, tk_vars, main_window_fields):
        """Creating a Toplevel window for the Customization Settings

        Args:
            tk_vars (dict): Tkinter variables coming from the main window class
            main_window_fields (dict): Tkinter Entry boxes/Comboboxes from the main window class
        """
        super().__init__(tk_vars, main_window_fields)
        # Update defaults upon closing this window
        self.protocol('WM_DELETE_WINDOW', self.refresh_fields)
        self._execute_bindings()
        self._link_buttons()

    def _execute_bindings(self):
        """BINDINGS"""
        exclude = (
            self.widgets['user_entry'],
            self.widgets['old_pwd_entry'].entry,
            self.widgets['new_pwd_entry'].entry,
            self.widgets['rep_pwd_entry'].entry,
            self.widgets['new_user'],
            self.widgets['new_email']
        )
        self.bind('<Button-1>', lambda event: self.focus() if event.widget not in exclude else "")
        self.bind(
            '<Return>',
            lambda event: update_settings(
                self.widgets['user_entry'],
                self.widgets['new_email'].get(),
                self.widgets['new_user'].get(),
                {
                    'curr': self.widgets['old_pwd_entry'].get(),
                    'new': self.widgets['new_pwd_entry'].get(),
                    'repeat': self.widgets['rep_pwd_entry'].get()
                }
            )
        )
        common_icons = {
            'show'      : self.icons['eye_icon'],
            'show_hover': self.icons['eye_icon_h'],
            'hide'      : self.icons['no_eye_icon'],
            'hide_hover': self.icons['no_eye_icon_h']
        }

        self.widgets['old_pwd_entry'].btn.bind(
            "<Enter>", lambda event: eye_switch_color(event, common_icons))
        self.widgets['old_pwd_entry'].btn.bind(
            "<Leave>", lambda event: eye_switch_color(event, common_icons))
        self.widgets['new_pwd_entry'].btn.bind(
            "<Enter>", lambda event: eye_switch_color(event, common_icons))
        self.widgets['new_pwd_entry'].btn.bind(
            "<Leave>", lambda event: eye_switch_color(event, common_icons))
        self.widgets['rep_pwd_entry'].btn.bind(
            "<Enter>", lambda event: eye_switch_color(event, common_icons))
        self.widgets['rep_pwd_entry'].btn.bind(
            "<Leave>", lambda event: eye_switch_color(event, common_icons))
        self.bind("<Configure>", self.calc_widgets)

    def _link_buttons(self):
        """Defines and draws all widgets for the left panel"""

        self.widgets['login_btn'].config(command=lambda:self.update_right_panel('login'))
        self.widgets['default_btn'].config(command=lambda:self.update_right_panel('default'))

        widgets = {
            'old_pwd_entry': self.widgets['old_pwd_entry'],
            'entrance_pass': self.widgets['new_pwd_entry'],
            'repeat_pass': self.widgets['rep_pwd_entry'],
        }
        icons = {key: self.icons[key] for key in ('eye_icon_h', 'no_eye_icon_h')}
        common = (widgets, icons)

        self.widgets['old_pwd_entry'].btn.config(
            command=lambda: check_pass_btn(PwdButton.OLD_PASSWORD, *common))
        self.widgets['new_pwd_entry'].btn.config(
            command=lambda: check_pass_btn(PwdButton.PASSWORD, *common))
        self.widgets['rep_pwd_entry'].btn.config(
            command=lambda: check_pass_btn(PwdButton.REPEAT, *common))

        self.widgets['apply_btn'].config(command=lambda: update_settings(
                self.widgets['user_entry'],
                self.widgets['new_email'].get(),
                self.widgets['new_user'].get(),
                {
                    'curr': self.widgets['old_pwd_entry'].get(),
                    'new': self.widgets['new_pwd_entry'].get(),
                    'repeat': self.widgets['rep_pwd_entry'].get()
                }
            )
        )
        self.widgets['ac_spin'].config(command=self.update_mins)

    def refresh_fields(self):
        """Refreshes the information in the user and email
        entry boxes and quits CustomizationSettings instance"""
        self.main_window_fields['user_entry'].delete(0, END)
        self.main_window_fields['email_combo'].delete(0, END)
        self.main_window_fields['user_entry'].insert(0, data.get_db_data('defaults', 'user'))
        self.main_window_fields['email_combo'].insert(
            0, decipher(data.get_db_data('defaults', 'email')))

        self.destroy()
        data.wins['çust'] = None

    def calc_widgets(self, event):
        """Recalculate widget placement"""
        log_set = {'wid': self.winfo_width(), 'height': self.winfo_height()}
        pwd_label = self.widgets['password_login']
        padx = 5
        btn_pad = self.l_pane['pad']
        x_pos = pwd_label.winfo_x() + pwd_label.winfo_width() + padx
        width_ = log_set['wid'] - self.max_width - self.l_pane['wid'] - padx - 2 * btn_pad
        autoclose_width = width_ + max(
            self.widgets['user_default'].winfo_width(),
            self.widgets['email_default'].winfo_width()
        ) + padx
        usr_default_x = self.widgets['user_default'].winfo_x()

        self.widgets['tab2'].place(width=log_set['wid'] - self.l_pane['wid'])

        self.widgets['user_entry'].place(   x=x_pos, y=10,  width=width_, anchor=NW)
        height = self.widgets['user_entry'].winfo_height()
        self.widgets['old_pwd_entry'].place(x=x_pos, y=70,  width=width_, height=height, anchor=NW)
        self.widgets['new_pwd_entry'].place(x=x_pos, y=100, width=width_, height=height, anchor=NW)
        self.widgets['rep_pwd_entry'].place(x=x_pos, y=130, width=width_, height=height, anchor=NW)

        self.widgets['new_user'].place( x=x_pos, y=10, width=width_, anchor=NW)
        self.widgets['new_email'].place(x=x_pos, y=40, width=width_, anchor=NW)
        self.widgets['autoclose'].place(x=usr_default_x, y=75, width=autoclose_width, anchor=NW)

        self.widgets['tab3'].place(width=log_set['wid'] - self.l_pane['wid'] - self.l_pane['pad'])

        self.widgets['apply_btn'].place(x=log_set['wid'] - btn_pad, y=log_set['height'] - btn_pad)

    def update_right_panel(self, btn: str):
        """Shows the chosen panel in the Custom Settings window

        Args:
            btn (str): An indicator of which Button (tab) was clicked
        """
        text=file_data.lang['customize']['update_right_panel']
        common_settings = {
            'foreground': data.colors['details1'],
            'activebackground': data.colors['bgc'],
            'activeforeground': data.colors['details1']
        }
        if btn == 'login':
            self.widgets['tab3'].place_forget()
            self.widgets['tab2'].place(x=self.l_pane['wid'], relheight=1, relwidth=0.7, anchor=NW)

            self.widgets['login_btn'].config(
                **common_settings, text=text['login']['login_btn'], bg=data.colors['bgc'])
            self.widgets['default_btn'].config(
                **common_settings, text=text['login']['default_btn'], bg=data.colors['shadow'])

        elif btn == 'default':
            self.widgets['tab2'].place_forget()
            self.widgets['tab3'].place(x=self.l_pane['wid'], relheight=1, relwidth=0.7, anchor=NW)

            self.widgets['login_btn'].config(
                **common_settings, text=text['default']['login_btn'], bg=data.colors['shadow'])
            self.widgets['default_btn'].config(
                **common_settings, text=text['default']['default_btn'], bg=data.colors['bgc'])

    def update_mins(self):
        """Updates the python variable with the tkinter variable"""
        data.autoclose['cd_mins'] = self.main_tk_vars['autoclose_mins'].get()
        data.reset_timer()


def update_settings(log_user, email: str, def_user: str, password: dict):
    """Updates the user defined default/login credentials

    Args:
        log_user (widget): Login username entry box
        email (str): Default email
        def_user (str): Default username
        password (dict): Current password, New password and New password repeated
    """
    same_email = email == data.autofils['default_email']
    curr_user = data.autofils['user']
    countdown_mins = data.get_db_data('settings', 'autoclose_mins')

    no_updates = (
        log_user.get() == curr_user and same_email and def_user == data.autofils['default_user']
        and data.autoclose['cd_mins'] == countdown_mins
        and password['new'] == "" and password['repeat'] == ""
    )
    if no_updates: # Sacrificing short-circuit for readability
        msg = file_data.lang['messages']['no_new_data']
        messagebox.showwarning(title=msg['title'], message=msg['text'], parent=data.wins['sett'])
        return

    if not log_user.get():
        msg = file_data.lang['messages']['login_removed']
        messagebox.showwarning(title=msg['title'], message=msg['text'], parent=data.wins['sett'])
        log_user.insert(0, curr_user)
        return

    text = file_data.lang['messages']['apply_changes']
    if not messagebox.askyesno(title=text['title'], message=text['text'], parent=data.wins['sett']):
        return

    # Check email, login username and password
    email_check = check_email(email=email) if email and not same_email else True
    log_user_check = check_username(user=log_user.get())
    pass_check = check_password(password)

    # Delete contents of all password fields
    if not pass_check:
        data.wins['sett'].widgets['old_pwd_entry'].delete(0, END)
        data.wins['sett'].widgets['new_pwd_entry'].delete(0, END)
        data.wins['sett'].widgets['rep_pwd_entry'].delete(0, END)

    # If all are valid - update current data file and save to disk
    if log_user_check and email_check and pass_check:
        data.set_db_data('defaults', 'email', cipher(email))
        data.set_db_data('defaults', 'user', def_user)

        if password['curr'] != '' and not verify_password(password['curr'], pass_check, data.uid):
            data.set_db_data('user_data', 'password', hash_password(pass_check))
        data.set_db_data('user_data', 'username', log_user.get())

        # Update variables
        data.autofils['user'] = log_user.get()
        data.autofils['default_user'] = def_user
        data.autofils['default_email'] = email

        if data.autoclose['cd_mins'] != countdown_mins:
            data.set_db_data('settings', 'autoclose_mins', data.autoclose['cd_mins'])
