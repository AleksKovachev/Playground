"""Contains the FileData class that manages data loading/saving.
Also contains the Data class that holds all the data used throughout the application."""

import json
import os
import sqlite3

from tkinter import messagebox
from dataclasses import dataclass

from password_manager.constants import (
    BLACK, WHITE, MED_GRAY, MED_DARK_GRAY, LIGHT_GRAY, LANGUAGES_DIR, SETTINGS, IMPORTED_PATH,
    BACKUPS_PATH, DATA_PATH, SETTINGS_FILE, DATA, DICTIONARY_PATH
)
from . import get_median_color


class FileData:
    """Manages Files and Directories"""

    def __new__(cls):
        """Singleton"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileData, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.conn = None # The database connection
        self.cursor = None # The cursor to the database
        self.lang = None # The full language file loaded
        self.main_settings = {}
        self.dictionary = {}

        self._manage_paths()
        self.load_language()
        self.load_dictionary()
        self.load_data()

    def load_dictionary(self):
        """Loads a dictionary file to use for password generation"""
        with open(DICTIONARY_PATH, encoding='utf-8') as dictionary:
            self.dictionary = json.load(dictionary)

    def load_data(self):
        """Loads the data from disk into memory"""
        self.create_data_structure()

        self.conn = sqlite3.connect(
            f'file:{os.path.join(os.getcwd(), f"{DATA}?mode=ro")}', uri=True)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def create_data_structure(self):
        """Creates all tables and fields upon database creation if they don't exist"""
        with sqlite3.connect(DATA) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    key TEXT UNIQUE NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    secondary_attempts INTEGER NOT NULL DEFAULT 0,
                    account_status TEXT NOT NULL DEFAULT 'unlocked',
                    unclock_code TEXT NOT NULL DEFAULT ''
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS themes (
                    id INTEGER,
                    bg TEXT NOT NULL DEFAULT '#777777',
                    fg TEXT NOT NULL DEFAULT '#DDDDDD',
                    accent TEXT NOT NULL DEFAULT '#555555',
                    details1 TEXT NOT NULL DEFAULT 'white',
                    details2 TEXT NOT NULL DEFAULT 'black',
                    FOREIGN KEY(id) REFERENCES user_data(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS backup (
                    id INTEGER,
                    period INTEGER NOT NULL DEFAULT 1,
                    date TEXT NOT NULL,
                    FOREIGN KEY(id) REFERENCES user_data(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS defaults (
                    id INTEGER,
                    user TEXT NOT NULL,
                    email TEXT NOT NULL,
                    FOREIGN KEY(id) REFERENCES user_data(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER,
                    language TEXT NOT NULL DEFAULT 'english',
                    autoclose_mins INTEGER NOT NULL,
                    FOREIGN KEY(id) REFERENCES user_data(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER,
                    platform TEXT NOT NULL,
                    user TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    FOREIGN KEY(id) REFERENCES user_data(id)
                )
            """)

    def _manage_paths(self):
        """Creates needed paths and files if they don't already exists"""
        if not os.path.exists(DATA_PATH) or not os.path.exists(BACKUPS_PATH):
            os.makedirs(IMPORTED_PATH)
        elif not os.path.exists(IMPORTED_PATH):
            os.mkdir(IMPORTED_PATH)

        # PM's settings.json
        if not os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, mode='w', encoding='utf-8') as sett:
                json.dump(SETTINGS, sett, indent=4)

        # Create folders for data files and backups if they don't exist
        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)
            if not os.path.exists(BACKUPS_PATH):
                os.mkdir(BACKUPS_PATH)

    def load_language(self, lang: str="", parent=None):
        """Loads the specified language into memory.
            If no file specified - load from the settings.json

        Args:
            lang (str): The desired language.json file from the lang folder.
            parent(Tk): A Tk window to use as a parent for the error messages.
        """
        # We can't use data.wins[parent] since data is being defined below
        if not lang:
            with open(SETTINGS_FILE, encoding='utf-8') as sett:
                self.main_settings = json.load(sett)
            lang = self.main_settings['language']

        path = os.path.join(LANGUAGES_DIR, lang.lower() + ".json")
        try:
            with open(path, encoding='utf-8') as sett:
                self.lang = json.load(sett)
        except FileNotFoundError:
            msg = self.lang['messages']['file_not_found']
            messagebox.showerror(title=msg['title'], message=msg['text'], parent=parent)
        except json.JSONDecodeError:
            msg = self.lang['messages']['wrong_json_format']
            messagebox.showerror(title=msg['title'], message=msg['text'], parent=parent)


@dataclass
class Data:
    """Data class that manages data loaded from files"""

    def __new__(cls):
        """Singleton"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Data, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.uid = None
        self.key = None
        self.wins = {
            'login': None,
            'reg': None,
            'root': None,
            'sett': None,
            'theme': None
        }
        self.autofils = {
            'id': None,
            'user': None,
            'default_user': None,
            'default_email': None
        }

        self.colors = {
            'fgc': BLACK,
            'bgc': MED_GRAY,
            'accent': MED_DARK_GRAY,
            'details1': WHITE,
            'details2': LIGHT_GRAY,
        }
        self.colors['shadow'] = get_median_color(self.colors['accent'], self.colors['bgc'])
        self.spinbox_ypos = 0 # Save the current Y position of the Mouse
        self.autoclose = {'timer': None, 'cd_mins': 5, 'timer_st': "00:00"}
        self.autoclose['countdown'] = self.autoclose['cd_mins'] * 60

        # Get the backup period
        self.backup_period = file_data.lang['backup_period']

    def reset_timer(self, event=None): # pylint: disable=unused-argument
        """Resets the timer when user activity is detected"""
        self.autoclose['countdown'] = self.autoclose['cd_mins'] * 60

    def get_db_entry(self, col: str, platform: str):
        """Gets a column from the entries table of the database"""
        result = file_data.cursor.execute(
            f"SELECT {col} FROM entries WHERE id = ? AND platform = ?", (self.uid, platform))
        return result.fetchone()[0]

    def get_db_data(self, table: str, col: str, by_id=True, single=True):
        """Gets a single piece of data from the database based on arguments"""
        if by_id:
            condition = " WHERE id = ?"
            bindings = (self.uid,)
        else:
            condition = ""
            bindings = ()
        result = file_data.cursor.execute(f"SELECT {col} FROM {table}{condition}", bindings)
        if single:
            return result.fetchone()[0]
        return result.fetchall()

    def set_db_data(self, table: str, col: str, new_val):
        """Updates the database based on arguments"""
        with sqlite3.connect(DATA) as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {table} SET {col} = ? WHERE id = ?", (new_val, data.uid))


file_data = FileData()
data = Data()
