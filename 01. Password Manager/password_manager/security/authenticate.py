"""Additional functions for Password Manager"""
import re
import string
from tkinter import messagebox

from password_manager.constants import RED, VALID_CHARS, EMAIL_PATTERN
from password_manager.security.encryption import verify_password
from password_manager.data_management.all_data import data, file_data

#+ pylint: disable=unused-argument, anomalous-backslash-in-string


def is_login_valid(username, password, event=None):
    """Checks credentials against the database.

    Args:
        username (widget): The widgets that holds the user name
        password (widget): The widgets that holds the password
    """
    if (username.get() == "Username" and username.cget("fg") == data.colors['bgc']
        or password.get() == "Password" and password.entry.cget('fg') == data.colors['bgc']):
        msg = file_data.lang['messages']['empty_creds']
        messagebox.showerror(
            title=msg['title'],
            message=msg['text'],
            parent=data.wins['login']
        )
        data.wins['login'].password_error = False
        return False

    # Loop through the users and check for corresponding credentials
    file_data.cursor.execute("SELECT id FROM user_data WHERE username = ?", (username.get(),))
    user_id = file_data.cursor.fetchone()
    if user_id is None:
        msg = file_data.lang['messages']['wrong_user']
        messagebox.showerror(
            title=msg['title'],
            message=f"{msg['text'][0]} {username.get()} {msg['text'][1]}",
            parent=data.wins['login']
        )
        data.wins['login'].password_error = False
        return False

    query = file_data.cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_id[0],))
    u_data = dict(query.fetchone())

    if (verify_password(password.get(), u_data['password'], user_id)
        and password.entry.cget('fg') == data.colors['fgc']):
        # Save the username
        data.autofils['user'] = u_data['username']
        data.uid = user_id[0]
        data.key = data.get_db_data('user_data', 'key')
        return True

    data.wins['login'].password_error = True
    return False


def check_email(event=None, email: str=None, widget=None) -> bool | None:
    """Checks if email is valid

    Args:
        event (event): If this is tkinter event type - then it serves as dynamic email check.
                            If str - Checks after confirm
        email (str): The email to check
        widget (Tk widget): A Tk widget supporting bg color (Entry/Label). Defaults to None

    Returns:
        bool | None: bool for static check, else None
    """
    acc_pattern = re.search(EMAIL_PATTERN, email, re.ASCII)
    parent = data.wins['reg'] or data.wins['sett']

    # Check if first or last charactes is a special one
    if len(email) > 1 and (email[0] in string.punctuation or email[-1] in string.punctuation):
        if event:
            widget['fg'] = RED
        else:
            msg = file_data.lang['messages']['special_first_char']
            messagebox.showerror(title=msg['title'], message=msg['text'], parent=parent)
            return False
    # Check if entered email corresponds to the pattern
    elif not acc_pattern:
        if event:
            widget['fg'] = RED
        else:
            msg = file_data.lang['messages']['invalid_email']
            messagebox.showerror(title=msg['title'], message=msg['text'], parent=parent)
            return False
    elif event:
        widget['fg'] = data.colors['fgc']
    return True


def check_username(event=None, user: str=None, widget=None) -> bool | None:
    """Checks if username is valid

    Args:
        event (event): If this is tkinter event type - then it serves as dynamic username check.
                            If str - Checks after confirm
        user (str): The username to check
        widget (Tk widget): A Tk widget supporting bg color (Entry/Label). Defaults to None

    Returns:
        bool | None: bool for static check, else None
    """
    has_correct_length = _check_name_length(event, user, widget)
    if not has_correct_length:
        return has_correct_length

    only_valid_chars = _check_invalid_chars(event, user, widget)
    if not only_valid_chars:
        return only_valid_chars

    duplicate_name = _check_name_exists(event, user, widget)
    if not duplicate_name:
        return duplicate_name

    return True


def _check_name_length(event=None, user: str=None, widget=None):
    """Checks if the length of the name is correct"""
    if 2 < len(user) < 21:
        if event:
            widget['fg'] = data.colors['fgc']
        return True
    if event:
        widget['fg'] = RED
        return None

    msg = file_data.lang['messages']['invalid_size']
    parent = data.wins['reg'] or data.wins['sett']
    messagebox.showerror(title=msg['title'], message=msg['text'], parent=parent)
    return False


def _check_invalid_chars(event=None, user: str=None, widget=None):
    """Check if name contains invalid characters"""
    for char in user:
        if char in VALID_CHARS:
            if event:
                widget['fg'] = data.colors['fgc']
        elif event:
            widget['fg'] = RED
            return None
        else:
            msg = file_data.lang['messages']['invalid_chars']
            parent = data.wins['reg'] or data.wins['sett']
            messagebox.showerror(
                title=msg['title'], message=f"{msg['text']}, {string.punctuation}", parent=parent)
            return False
    return True


def _check_name_exists(event=None, user: str=None, widget=None):
    """Check if username already exists in the database"""
    all_names = data.get_db_data(table="user_data", col="username", by_id=False, single=False)
    for log in all_names:
        if user == log[0] and log[0] != data.autofils['user']:
            if event:
                widget['fg'] = RED
                return None
            msg = file_data.lang['messages']['duplicate_user']
            parent = data.wins['reg'] or data.wins['sett']
            messagebox.showerror(
                msg['title'], f"{msg['text'][0]} {user} {msg['text'][1]}", parent=parent)
            return False
        if event:
            widget['fg'] = data.colors['fgc']
    return True


def check_password(pwd: dict):
    """Checks password validity

    Args:
        pwd (dict): Current password, New password and New password repeated

    Returns:
        bool | str: False if there's an error. Otherwise - the actual password
    """
    # Checks if Old Password field is empty and New password fields are not
    if pwd['curr'] == "" and (pwd['new'] != "" or pwd['repeat'] != ""):
        msg = file_data.lang['messages']['empty_password']
        messagebox.showerror(title=msg['title'], message=msg['text'], parent=data.wins['sett'])
        return False

    # Checks if the old password is correct
    hashed_pass = data.get_db_data("user_data", "password")
    if not any((pwd['curr'] == "", verify_password(pwd['curr'], hashed_pass, data.uid))):
        msg = file_data.lang['messages']['wrong_old_pass']
        messagebox.showerror(title=msg['title'], message=msg['text'], parent=data.wins['sett'])
        return False

    # Checks if the new password and the repeat password are the same
    if pwd['new'] != pwd['repeat']:
        msg = file_data.lang['messages']['pass_no_match']
        messagebox.showerror(title=msg['title'], message=msg['text'], parent=data.wins['sett'])
        return False

    if not _check_new_password(pwd['new']):
        return False

    curr_pass = data.get_db_data(table="user_data", col="password")
    return curr_pass if pwd['repeat'] == "" else pwd['repeat']


def _check_new_password(password: str) -> bool:
    """Checks the New Password's validity

    Args:
        password (str): New password
    """
    # Checks if the new password is longer than 20 characters
    if len(password) > 20:
        msg = file_data.lang['messages']['long_pass']
        messagebox.showerror(title=msg['title'], message=msg['text'], parent=data.wins['sett'])
        return False

    # Checks if the new password is shorter than 4 characters
    if password != "" and len(password) < 4:
        msg = file_data.lang['messages']['short_pass']
        messagebox.showerror(title=msg['title'], message=msg['text'], parent=data.wins['sett'])
        return False

    # Checks for invalid characters
    for char in password:
        if char not in VALID_CHARS:
            msg = file_data.lang['messages']['invalid_chars_pass']
            messagebox.showerror(title=msg['title'], message=msg['text'], parent=data.wins['sett'])
            return False
    return True
