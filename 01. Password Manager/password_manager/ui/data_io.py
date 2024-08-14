"""Contains functionality for importing data file"""

import os
import shutil
import sqlite3
from enum import Enum
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import Toplevel, Frame, Button, Label, messagebox, CENTER, S, SW, SE, GROOVE
from datetime import datetime

from password_manager.data_management.all_data import data, file_data
from password_manager.constants import (FONT_A, FONT_B, IMPORTED_PATH, WORD_FORMAT, NUM_BACKUPS,
                                        DATA, CONCRETE, WHITE, MILK_WHITE, ICONS_DIR)


class MergeChoice(Enum):
    """Options for user choice to merging data files"""
    CURRENT = 0
    IMPORTED = 1


def import_data():
    """Import data from a given data file"""
    # Display an import file dialog and save the chosen filepath to a variable
    import_path = askopenfilename(
        initialdir=os.path.join(*os.path.dirname(__file__).split(os.sep)[:-2]),
        title=file_data.lang['import_data']['askopenfile_title'],
        filetypes=(("PM Data File", "*.dat*"),)
    )
    if not import_path:
        return

    # Create a Custom messagebox window
    data_message = Toplevel(data.wins['root'])
    dm_width = 500
    dm_height = 225
    root_xcenter = data.wins['root'].winfo_x() + data.wins['root'].winfo_width() / 2
    root_ycenter = data.wins['root'].winfo_y() + data.wins['root'].winfo_height() / 2
    data_message.geometry(
        f"{dm_width}x{dm_height}+" \
        f"{int(root_xcenter - dm_width / 2)}+{int(root_ycenter - dm_height / 2)}"
    )
    data_message.resizable(False, False)
    data_message.config(background=data.colors['bgc'], pady=10, padx=10)
    # Make the main window unclickable until this one is closed
    data_message.grab_set()
    # Make it a tool window (only X button)
    data_message.attributes('-toolwindow', True)
    data_message.focus()

    text = file_data.lang['import_data']
    message = Label(
        data_message,
        text=text['message'],
        font=FONT_A,
        background=data.colors['bgc'],
        foreground=data.colors['details1']
    )
    message.place(relx=0.5, rely=0.2, anchor=CENTER)

    question = Label(
        data_message,
        text=text['question'],
        font=FONT_A,
        background=data.colors['bgc'],
        foreground=data.colors['details1']
    )
    question.place(relx=0.5, rely=0.35, anchor=CENTER)

    new_data_btn = Button(
        data_message,
        text=text['new_data_btn'],
        font=FONT_B,
        background=data.colors['bgc'],
        foreground=data.colors['details1'],
        command=lambda: (new_data_func(import_path), data_message.destroy())
    )
    new_data_btn.place(relx=0.2, rely=0.8, anchor=CENTER)

    merge_data_btn = Button(
        data_message,
        text=text['merge_data_btn'],
        font=FONT_B,
        background=data.colors['bgc'],
        foreground=data.colors['details1'],
        command=lambda: (merge_data_func(data_message, import_path), data_message.destroy())
    )
    merge_data_btn.place(relx=0.5, rely=0.8, anchor=CENTER)

    old_data_btn = Button(
        data_message,
        text=text['old_data_btn'],
        font=FONT_B,
        background=data.colors['bgc'],
        foreground=data.colors['details1'],
        command=data_message.destroy
    )
    old_data_btn.place(relx=0.8, rely=0.8, anchor=CENTER)


def export_data():
    """Export data to specified location"""
    export_path = askdirectory(
        initialdir=os.path.dirname(__file__), title=file_data.lang['export_data_title'])
    if export_path:
        time_now = datetime.now().strftime(WORD_FORMAT)
        shutil.copyfile(DATA, os.path.join(export_path, f"pmd - {time_now}.dat"))


#! Unfinished!!! Don't use the "Merge data"option!
def new_data_func(imported_file_path: str):
    """Replaces current data file with the new one

    Args:
        imported_file (str): A path to the file used for replacement
    """
    # Create an "Imported" folder in the data files if it doesn't already exist
    if not os.path.exists(IMPORTED_PATH):
        os.mkdir(IMPORTED_PATH)
    time_now = datetime.now().strftime(WORD_FORMAT)
    # Make a backup of the current data file appending current datetime to its name
    copy_backup(
        time_now_s=time_now,
        check_dir=IMPORTED_PATH,
        copy_dir=os.path.join(IMPORTED_PATH, f"pmd - {time_now}.dat"),
        bac_num=10
    )

    # Copy to application main directory
    imported_file = sqlite3.connect(imported_file_path)
    imp_cur = imported_file.cursor()
    query = "SELECT name, sql FROM sqlite_master WHERE type='table';"
    imp_schema = imp_cur.execute(query).fetchall()
    data_schema = file_data.cursor.execute(query).fetchall()

    sure = True
    same_structure = True
    if imp_schema != data_schema:
        msg = file_data.lang['messages']['different_db_structure']
        messagebox.showinfo(title=msg['title'], message=msg['text'], parent=data.wins['root'])
        same_structure = False

    if not sure:
        return

    if same_structure:
        copy_database_entries_same_signature(imp_cur, data_schema, update=True)
        return

    with sqlite3.connect(DATA) as conn:
        cur = conn.cursor()

        # Connect to the imported database and get a list of all of its tables
        cur.execute(f"ATTACH DATABASE '{imported_file_path}' AS imp")
        cur.execute("SELECT name FROM imp.sqlite_master WHERE type='table'")
        imp_tables = cur.fetchall()

        for table in imp_tables:
            table = table[0]
            cur.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cur.fetchone()[0] == 1:
                # The table exists in local database, check for new columns and insert data
                cur.execute(f"PRAGMA table_info({table})")
                local_columns = [column[1] for column in cur.fetchall()]

                cur.execute(f"PRAGMA imp.table_info({table})")
                imp_columns = [column[1] for column in cur.fetchall()]

                # Get the columns that are in the imported database but not in the local one
                new_columns = set(imp_columns) - set(local_columns)

                for column in new_columns:
                    # Get the column details from the imported database
                    cur.execute(f"PRAGMA imp.table_info({table})")
                    column_info = [info for info in cur.fetchall() if info[1] == column][0]

                    # TODO: Change the code below to create a new table and copy contents + create
                    #= the new column. This way the new column can be copied WITH UNIQUE if needed.
                    # Add the new column to the table in the local database
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN {column_info[1]} {column_info[2]}")

                # Insert the data from the imported into the local database
                cur.execute(f"INSERT INTO {table} SELECT * FROM imp.{table}")
            else:
                # The table doesn't exist in the local database, create it and insert data
                cur.execute(f"CREATE TABLE {table} AS SELECT * FROM imp.{table}")


def merge_data_func(tl_root: Toplevel, imported_file: str):
    """Merges the current data file with the new one and saves it

    Args:
        tl_root (Toplevel): A Toplevel() window used to center the dominant messagebox
        imported_file (str): A path to the file used for merging
    """
    # Create an "Imported" folder in the data files if it doesn't already exist
    if not os.path.exists(IMPORTED_PATH):
        os.mkdir(IMPORTED_PATH)
    time_now = datetime.now().strftime(WORD_FORMAT)
    # Make a backup of the current data file appending current datetime to its name
    copy_backup(
        time_now_s=time_now,
        check_dir=IMPORTED_PATH,
        copy_dir=os.path.join(IMPORTED_PATH, f"pmd - {time_now}.dat"),
        bac_num=10
    )

    # Read both the new and the current data files
    imported = {} # decipher(imported_file)
    existing = {} # decipher(DATA)

    # Update existing files based on user preference and save to disk.
    dominant = merge_dominant(tl_root)
    if dominant[0] == MergeChoice.IMPORTED:
        existing |= imported
    elif dominant[0] == MergeChoice.CURRENT:
        imported |= existing


def copy_backup(time_now_s: str, check_dir: str, copy_dir: str, bac_num: int = NUM_BACKUPS):
    """Checks the backup folder and copies the backup file

    Args:
        time_now_s (str): Formatted datetime
        check_dir (str): The directory to check the contents of
        copy_dir (str): Where to copy the backup file
        bac_num (int): The number of backup files to keep before starting to replace the olderst
    """
    # Get a list of all backup files
    bac_files = [item for item in os.scandir(check_dir) if item.name.startswith("pmd")]
    # Check if the number of bac_files is greater than allowed
    if len(bac_files) >= bac_num:
        bac_files = check_num_files(bac_num, bac_files)
        # If backups >= max allowed - delete oldest one/-s
        for file in bac_files:
            os.remove(file.path)

    # Save current datetime as last backup in the user data file and copy file to the backups folder
    data.set_db_data('backup', 'date', time_now_s)
    shutil.copyfile(DATA, copy_dir)


def merge_dominant(tl_root: Toplevel):
    """Custom Messagebox window

    Args:
        tl_root (Toplevel): A Toplevel() window used to center the messagebox
    """
    dom = Toplevel()
    dom.iconbitmap(os.path.join(ICONS_DIR, "icon.ico"))
    dom.title('Dominant Data File')
    dom_width = 350
    dom_height = 150
    root_xcenter = tl_root.winfo_x() + tl_root.winfo_width() / 2
    root_ycenter = tl_root.winfo_y() + tl_root.winfo_height() / 2
    dom.geometry(
        f"{dom_width}x{dom_height}+" \
        f"{int(root_xcenter - dom_width / 2)}+{int(root_ycenter - dom_height / 2)}"
    )
    dom.resizable(False, False)
    dom.config(background=WHITE)
    # Make the main window unclickable until this one is closed
    dom.grab_set()
    dom.focus()
    response = [MergeChoice.CURRENT, MergeChoice.IMPORTED]
    text = file_data.lang['merge_dominant']

    message = Label(dom, text=text['msg'], wraplength=300, background=WHITE)
    frame = Frame(dom, height=50, width=dom_width, background=MILK_WHITE)
    old_btn = Button(
        frame,
        text=text['old_btn'],
        relief=GROOVE,
        background=CONCRETE,
        command=lambda: (response.pop(1), dom.destroy())
    )
    new_btn = Button(
        frame,
        text=text['new_btn'],
        relief=GROOVE,
        background=CONCRETE,
        command=lambda: (response.pop(0), dom.destroy())
    )
    frame.place(  relx=0.5, rely=1,    anchor=S)
    message.place(relx=0.5, rely=0.3,  anchor=CENTER)
    old_btn.place(relx=0.3, rely=0.75, anchor=SW)
    new_btn.place(relx=0.7, rely=0.75, anchor=SE)

    dom.wait_window()
    return response


def check_num_files(reps: int, bac_files: list):
    """Checks how many files are in the folder and deletes the oldest ones if above the given number

    Args:
        reps (int): How many times to repeat the process. Corresponds to allowed number of files.
        bac_files (list): A list of all backup files in the given folder

    Returns:
        list: A list containing all files that will be deleted
    """

    # Check which files are the N (reps) newest using date modified and remove them from bac_files
    # In the end usualy only 1 file is left (the oldest) and it gets deleted
    # It's written in a way so that if more files get copied manually - they will be deleted
        # and only the N (reps) latest will remain
    while reps > 1:
        newest = bac_files[0]
        for file in bac_files:
            if file.stat().st_mtime > newest.stat().st_mtime:
                newest = file
        bac_files.remove(newest)
        reps -= 1

    return bac_files


def recover_from_backup(file: object):
    """Replaces the current data file with the selected one

    Args:
        file (file object): A nt.DirEntry file object from os.scandir
    """
    # Display a confirmation dialog
    msg = file_data.lang['messages']['recover_from_backup']
    if messagebox.askyesno(title=msg['title'], message=msg['text'], parent=data.wins['root']):

        # Check if the backup/Imported folder exists and create one if not
        if not os.path.exists(IMPORTED_PATH):
            os.mkdir(IMPORTED_PATH)
        time_now = datetime.now().strftime(WORD_FORMAT)

        # Make a backup copy of the current data file and then replace with the new one
        copy_backup(
            time_now_s=time_now,
            check_dir=IMPORTED_PATH,
            copy_dir=os.path.join(IMPORTED_PATH, f"pmd - {time_now}.dat"),
            bac_num=10
        )
        shutil.copyfile(file, DATA)


def copy_database_entries_same_signature(imp_cur, data_schema, update: bool):
    """Copies all database entries from one database to another.
    The two databases need to have the same structure!

    Args:
        imp_cur (sqlite3.cursor): The cursor of the imported file
        data_schema (tuple): The signature of the local database
        update (bool): Should existing values be updated or skipped
    """
    with sqlite3.connect(DATA) as conn:
        cur = conn.cursor()
        tables = [table[0] for table in data_schema.fetchall()]

        for table in tables:
            # Select all records related to the specific id from the source database
            imp_cur.execute(f'SELECT * FROM {table} WHERE id = ?', (data.uid,))

            # Fetch all the records
            records = imp_cur.fetchall()

            # Get the number of columns in the table
            num_columns = len(imp_cur.description)

            # Create a parameterized query string
            action = "REPLACE" if update else "IGNORE"
            query = f'INSERT OR {action} INTO {table} VALUES ({", ".join(["?"] * num_columns)})'

            # Insert each record into the destination database
            for record in records:
                cur.execute(query, record)
