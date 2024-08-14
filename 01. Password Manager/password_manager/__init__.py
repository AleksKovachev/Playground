"""Defines some functions that are used across the application"""

import os
import math
from tkinter import Toplevel
from datetime import datetime

from .data_management.all_data import data, file_data
from .ui.data_io import copy_backup
from .constants import BACKUPS_PATH, WORD_FORMAT
from .ui.access_control.login import Login


def countdown():
    "Countdown for automatic logout"
    if data.autoclose['cd_mins'] == 0:
        # Set the time for the label in the status bar
        data.wins['root'].tk_vars['countdown_var'].set(
            file_data.lang['status_bar']['autoclose_deactivated'])
        # Rerun this function every 1 second
        data.autoclose['timer'] = data.wins['root'].after(1000, countdown)
    else:
        # Get the remaining mninutes and seconds
        count_min = math.floor(data.autoclose['countdown'] / 60)
        count_sec = data.autoclose['countdown'] % 60

        # Format the seconds with '0' infront of single digits
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        # Write the time to a variable
        data.autoclose['timer_st'] = f"{count_min}:{count_sec}"
        # Set the time for the label in the status bar
        data.wins['root'].tk_vars['countdown_var'].set(
            f"{file_data.lang['status_bar']['autoclose']} {data.autoclose['timer_st']}")

        # Subtract 1 second of the remaining time
        data.autoclose['countdown'] -= 1
        # Rerun this function every 1 second
        data.autoclose['timer'] = data.wins['root'].after(1000, countdown)
        # If timer reaches 0 - stop the timer and logout the user
        if data.autoclose['countdown'] <= 0:
            data.wins['root'].after_cancel(data.autoclose['timer'])
            logout()


def logout():
    """Logout of the main application and bring up the Authentication window"""
    data.wins['root'].after_cancel(data.autoclose['timer'])
    data.autoclose['countdown'] = data.autoclose['cd_mins'] * 60
    # Check the auto-backup options and save a data backup if needed
    auto_backup(destroy=False)
    # Destroy all TopLevel windows and hide the main application window
    for widget in data.wins['root'].winfo_children():
        if isinstance(widget, Toplevel) and not isinstance(widget, Login):
            widget.destroy()
    data.wins['sett'] = None
    data.wins['theme'] = None
    data.wins['root'].withdraw()
    # Build a new Authentication window
    data.wins['login'].deiconify()
    data.wins['login'].widgets['log_entry_user'].focus()


def auto_backup(destroy: bool):
    """Save a backup version of the current data. Add current date to its name

    Args:
        destroy (bool): True if application should be destroyed, else False
    """
    # Get the backup period user setting
    _, period, date = file_data.cursor.execute(
        "SELECT * FROM backup WHERE id = ?", (data.uid,)).fetchall()[0]
    time_now = datetime.now()
    time_now_s = time_now.strftime(WORD_FORMAT)
    file_date = datetime.strptime(date, WORD_FORMAT)

    # If period == "No backup" nothing happens
    backup_period = {
        'daily': period == 1 and file_date.date() < time_now.date(),
        'weekly': period == 2 and (time_now - file_date).days > 6,
        'monthly': period == 3 and abs(
            (file_date.year - time_now.year) * 12 + (file_date.month - time_now.month)) > 0,
        'on_close': period == 4,
        'no_existing_backups': not any(os.scandir(BACKUPS_PATH))
    }

    if any(backup_period.values()):
        copy_backup(time_now_s, BACKUPS_PATH, os.path.join(BACKUPS_PATH, f"pmd - {time_now_s}.dat"))

    if destroy:
        data.wins['root'].destroy()
