"""Responsibilities related to data management, reading files, etc."""

import os

from datetime import datetime
from shutil import copyfile
from tkinter import Toplevel, messagebox

from password_manager.constants import WORD_FORMAT, DATA, BACKUPS_PATH
from password_manager.data_management.all_data import file_data
from password_manager.ui import start_program

# TODO: Currently unused. Put an option for manual backup data file loading in login window.
def load_backup_data(data_integrity: Toplevel):
    """Replaces the main data file with the latest backup

    Args:
        data_integrity (Toplevel): The custom pop-up message to close
    """
    # Collect all existing backups and copy the newest
    if backups := [dat for dat in os.scandir(BACKUPS_PATH) if dat.name.endswith('.dat')]:
        newest = backups[0]
        for file in backups:
            if file.stat().st_mtime > newest.stat().st_mtime:
                newest = file

        messages = file_data.lang['messages']['replace_backup']
        datetime_ = datetime.fromtimestamp(newest.stat().st_mtime).strftime(WORD_FORMAT)
        msg = f"{messages['text'][0]} {datetime_} {messages['text'][1]}"
        if messagebox.askyesno(title=messages['title'], message=msg, parent=data_integrity):
            copyfile(newest.path, DATA)
            file_data.load_data()
            data_integrity.destroy()
            start_program()
    else:
        msg = file_data.lang['messages']['no_backups']
        messagebox.showerror(title=msg["title"], message=msg["text"], parent=data_integrity)
