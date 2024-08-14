"""Defines the class responsible for the Sign Up window"""

import sqlite3
from tkinter import messagebox
from datetime import datetime

from password_manager.constants import RED, VALID_CHARS, WORD_FORMAT, DEFAULT_AUTOCLOSE_MINS, DATA
from password_manager.data_management.all_data import file_data, data
from password_manager.ui.visibility_toggle import PwdButton, check_pass_btn
from password_manager.security.authenticate import check_username, check_email
from password_manager.security.encryption import  hash_password, generate_key, cipher
from .signup_base import SignUpBase
from . import field_clear, eye_switch_color

#+ pylint: disable=unused-argument


class SignUp(SignUpBase):
    """Responsible for the Sign-up operations"""

    def __init__(self):
        super().__init__()
        self._link_buttons()
        self._execute_bindings()

    def _link_buttons(self):
        """Links Button widgets to the function they should execute"""
        self.widgets['e_btn'].config(command=self.save_login)
        widgets = {
            'pass': self.widgets['pass'],
            're_pass': self.widgets['re_pass'],
        }
        icons = {
            'eye_icon_h': self.icons['eye_icon_h'],
            'no_eye_icon_h': self.icons['no_eye_icon_h']
        }

        self.widgets['pass'].btn.config(
            command=lambda: check_pass_btn(PwdButton.PASSWORD, widgets, icons))
        self.widgets['re_pass'].btn.config(
            command=lambda: check_pass_btn(PwdButton.REPEAT, widgets, icons))

    def _execute_bindings(self):
        """Sets binding to mouse and keyboard events"""
        self.bind('<Unmap>', lambda event: self.root.iconify())
        self.widgets['entrance_user'].bind(
            '<KeyRelease>',
            lambda event: check_username(
                event, self.widgets['entrance_user'].get(), self.widgets['entrance_user']))
        self.widgets['entrance_email'].bind(
            '<KeyRelease>',
            lambda event: check_email(
                event, self.widgets['entrance_email'].get(), self.widgets['entrance_email']))
        self.widgets['pass'].entry.bind(
            '<KeyRelease>',
            lambda event: check_pwd(event, self.widgets['pass'].get()))
        self.widgets['re_pass'].entry.bind(
            '<KeyRelease>',
            lambda event: check_pwd_rep(
                event, self.widgets['pass'].get(), self.widgets['re_pass'].get()))

        common = (
            self.widgets['entrance_user'],
            self.widgets['pass'].entry,
            self.widgets['entrance_email'],
            self.widgets['re_pass'].entry
        )

        self.widgets['pass'].entry.bind('<FocusIn>', lambda event: field_clear(event, common))
        self.widgets['pass'].entry.bind('<FocusOut>', lambda event: field_clear(event, common))
        self.widgets['re_pass'].entry.bind('<FocusIn>', lambda event: field_clear(event, common))
        self.widgets['re_pass'].entry.bind('<FocusOut>', lambda event: field_clear(event, common))
        self.widgets['entrance_user'].bind('<FocusIn>', lambda event: field_clear(event, common))
        self.widgets['entrance_user'].bind('<FocusOut>', lambda event: field_clear(event, common))
        self.widgets['entrance_email'].bind('<FocusIn>', lambda event: field_clear(event, common))
        self.widgets['entrance_email'].bind('<FocusOut>', lambda event: field_clear(event, common))
        self.bind('<Button-1>', lambda event: self.focus() if event.widget not in common else "")

        common_icons = {
            'show'      : self.icons['eye_icon'],
            'show_hover': self.icons['eye_icon_h'],
            'hide'      : self.icons['no_eye_icon'],
            'hide_hover': self.icons['no_eye_icon_h']
        }
        self.widgets['pass'].btn.bind(
            "<Enter>", lambda event: eye_switch_color(event, common_icons))
        self.widgets['pass'].btn.bind(
            "<Leave>", lambda event: eye_switch_color(event, common_icons))
        self.widgets['re_pass'].btn.bind(
            "<Enter>", lambda event: eye_switch_color(event, common_icons))
        self.widgets['re_pass'].btn.bind(
            "<Leave>", lambda event: eye_switch_color(event, common_icons))
        self.bind('<Return>', self.save_login)

    def save_login(self, event=None):
        """Saves the new user with their credentials

        Args:
            event (event): Used if function is called by tkinter binding ('Enter' key).
        """
        # Check if all fields are filled
        data_ = {
            'username': self.widgets['entrance_user'].get(),
            'email': self.widgets['entrance_email'].get(),
            'pwd': self.widgets['pass'].get(),
            'pwd_rep': self.widgets['re_pass'].get()
        }

        if any((data_['username'] in ("", "Username"),
                data_['email'] in ("", "E-mail"),
                data_['pwd'] in ("", "Password"),
                data_['pwd_rep'] in ("", "Repeat Password"))):
            msg = file_data.lang['messages']['fill_fields']
            messagebox.showwarning(title=msg['title'], message=msg['text'], parent=self)
            return

        # Check if all fields are valid with short-circuit
        if (not check_username(user=data_['username'])
            or not check_email(email=data_['email'])
            or not check_pwd(password=data_['pwd'])
            or not check_pwd_rep(password=data_['pwd'], repeat=data_['pwd_rep'])):
            return

        password = hash_password(data_['pwd'])
        with sqlite3.connect(DATA) as conn:
            cursor = conn.cursor()
            key = generate_key()
            cursor.execute(
                "INSERT INTO user_data (username, email, password, key) VALUES (?, ?, ?, ?)",
                (data_['username'], cipher(data_['email'], key), cipher(password, key), key)
            )
            # Get the id of the user that was just inserted
            user_id = cursor.lastrowid

            cursor.execute("INSERT INTO themes (id) VALUES (?)", (user_id,))
            cursor.execute("INSERT INTO backup (id, date) VALUES (?, ?)",
                            (user_id, datetime.now().strftime(WORD_FORMAT)))
            cursor.execute("INSERT INTO defaults (id, user, email) VALUES (?, ?, ?)",
                            (user_id, data_['username'], cipher(data_['email'], key)))
            cursor.execute("INSERT INTO settings (id, autoclose_mins) VALUES (?, ?)",
                            (user_id, DEFAULT_AUTOCLOSE_MINS))

        # Update the currently database connection
        file_data.conn.commit()

        # Show the main application window and destroy the signup one
        self.root.deiconify()
        self.root.widgets['log_entry_user'].focus()
        data.wins['root'].widgets['website_entry'].focus()
        self.destroy()
        data.wins['reg'] = None
        self.root.wm_attributes('-disabled', False)


def check_pwd(event=None, password: str=None) -> bool | None:
    """Checks if password is valid

    Args:
        event (event): Used if this function was called by tkinter event. Serves for dynamic checks.
        password (str): The password to be checked

    Returns:
        bool: False if there's an error. Otherwise - True.
    """
    if password is None:
        raise ValueError("Password argument is required!")

    if len(password) > 20:
        return _check_pwd_len_20(event)
    if event is not None:
        event.widget['fg'] = data.colors['fgc']

    if len(password) < 4 or password == "Password":
        if event is not None:
            event.widget['fg'] = RED
            return None
        msg = file_data.lang['messages']['short_pass']
        messagebox.showerror(title=msg['title'], message=msg['text'], parent=data.wins['reg'])
        return False
    if event is not None:
        event.widget['fg'] = data.colors['fgc']

    for char in password:
        if char not in VALID_CHARS:
            if event is not None:
                event.widget['fg'] = RED
                return None
            msg = file_data.lang['messages']['invalid_chars']
            messagebox.showerror(title=msg['title'], message=msg['text'], parent=data.wins['reg'])
            return False
        if event is not None:
            event.widget['fg'] = data.colors['fgc']
    return True


def _check_pwd_len_20(event):
    """If called by event, makes its widget's font red. Otherwise shows error message"""
    if event is not None:
        event.widget['fg'] = RED
        return None
    messagebox.showerror(
        title=file_data.lang['messages']['long_pass']['title'],
        message=file_data.lang['messages']['long_pass']['text'],
        parent=data.wins['reg']
    )
    return False


def check_pwd_rep(event=None, password: str=None, repeat: str=None) -> bool | None:
    """Checks if password is valid

    Args:
        event (event): Used by tkinter bindings if function is called by a keypress
        password (str): The password to be checked
        repeat (str): Password from the "repeat password" entry field for comparison with password

    Returns:
        bool: False if there's an error. Otherwise - True.
    """
    if password is None or repeat is None:
        raise ValueError("Password and Repeat password arguments are required!")

    if password != repeat:
        if event is not None:
            event.widget['fg'] = RED
            return None
        messagebox.showerror(
            title=file_data.lang['messages']['check_pwd_rep']['title'],
            message=file_data.lang['messages']['check_pwd_rep']['text'],
            parent=data.wins['reg']
        )
        return False
    if event is not None:
        event.widget['fg'] = data.colors['fgc']
        return None
    return True
