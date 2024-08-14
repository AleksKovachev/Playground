"""UI functionality that can be used across the application"""

from tkinter import Label, Listbox, Scrollbar, Y, LEFT, RIGHT, END, BOTH
from tkinter.messagebox import askyesno, showinfo, showerror

import password_manager

from password_manager.data_management import update_list
from password_manager.data_management.all_data import data, file_data
from password_manager.constants import FONT_B
from password_manager.security.encryption import decipher
from password_manager.ui.base_ui import Window


class BrowseWindow(Window):
    """Defines a new window with a list of all available accounts

        Args:
            data_ (dict): A dictionary wth the data to process
            entry (str): Checking what's written in the website entry box
            custom_height (int, optional): Setting the window's height. Defaults to 450.
    """

    def __init__(self, data_: dict, entry: str, custom_height: int = 450):
        super().__init__(root=data.wins['root'])
        self.data = data_
        self.entry = entry

        self.setup(300, custom_height)
        self.define_draw_ui()
        self.order_accounts()

    def setup(self, width, height):
        """Create and set up the Browse window"""
        super().setup(width=width, height=height)
        self.title(file_data.lang['win2']['title'])

        self.resizable(False, True)
        self.minsize(0, 200)
        self.config(padx=50, pady=20)

        self.grab_set()

    def define_draw_ui(self):
        """Defines the UI widgets for the Browse window"""
        # Label
        self.widgets['choose_acc'] = Label(
            self,
            text=file_data.lang['win2']['choose_acc'],
            font=FONT_B,
            foreground=data.colors['details1'],
            background=data.colors['bgc']
        )
        self.widgets['choose_acc'].pack()

        # Scrollbar
        self.widgets['scrollbar'] = Scrollbar(self)
        self.widgets['scrollbar'].pack(side=RIGHT, fill=Y)

        # Listbox
        self.widgets['listbox'] = Listbox(
            self,
            font=FONT_B,
            foreground=data.colors['details1'],
            background=data.colors['bgc'],
            width=30,
            highlightthickness=0,
            yscrollcommand=self.widgets['scrollbar'].set
        )

    def order_accounts(self):
        """Order all accounts by displaying those starting with the search first
        and then alphabetically order the accounts that contain the search elsewhere."""
        accounts = list(self.data)
        if self.entry is not None:
            accounts = update_list(accounts, self.entry)
        # Apply alphabetical case-insensitive sort
        accounts.sort(key=str.lower)

        # Populate the window with the results.
        for account in accounts:
            self.widgets['listbox'].insert(accounts.index(account), account)
        self.widgets['listbox'].bind("<<ListboxSelect>>", self.copy_contents)
        self.widgets['listbox'].pack(side=LEFT, fill=BOTH)
        self.widgets['scrollbar'].config(command=self.widgets['listbox'].yview)

    def copy_contents(self, event):  # pylint: disable=unused-argument
        """Gets current selection from listbox"""
        # Hide this window
        self.withdraw()
        # Delete what the user has entered and fill the name that the user clicked

        data.wins['root'].widgets['website_entry'].delete(0, END)
        data.wins['root'].widgets['website_entry'].insert(
            0, self.widgets['listbox'].get(self.widgets['listbox'].curselection()))
        # Initiate Search Creds to display the credentials and autofill the fields
        search_creds()
        self.destroy()


def start_program():
    """Remove the authentication window and start the program"""
    # Update the theme with the user chosen preferences
    data.wins['root'].update_theme()
    # Update the UI with the chosen language
    lng = data.get_db_data('settings', 'language')
    file_data.load_language(lng, parent=data.wins['login'])
    data.wins['root'].widgets['lang_btn'].config(
        text=lng.capitalize(), image=data.wins['root'].widgets['language_flags'][lng.lower()])
    data.wins['root'].update_language(initial=True)
    # Check the user defined backup period and update UI with check mark
    bak_period = data.get_db_data('backup', 'period')
    update_backup_period(bak_period)
    data.wins['root'].tk_vars['radio_var'].set(bak_period)
    # Save the user preferences for default username and email
    data.autofils['default_user'] = data.get_db_data('defaults', 'user')
    data.autofils['default_email'] = decipher(data.get_db_data('defaults', 'email'))
    # Write the default username and email to the UI entry boxes
    data.wins['root'].tk_vars['emails_var'].set(data.autofils['default_email'])
    data.wins['root'].widgets['user_entry'].delete(0, END)
    data.wins['root'].widgets['user_entry'].insert(0, data.autofils['default_user'])
    # Update the Status bar
    msg = file_data.lang['status_bar']['entries_num']
    username = data.autofils['user']
    num_entries = len(data.get_db_data('entries', 'platform', single=False))
    last_backup = data.get_db_data('backup', 'date')
    data.wins['root'].tk_vars['status_entries_num'].set(
        f"{msg[0]} {username}! {msg[1]} {num_entries} {msg[2]} {last_backup}")
    data.wins['root'].tk_vars['countdown_var'].set(
        f"{file_data.lang['status_bar']['autoclose']} {data.autoclose['timer_st']}")
    # Run the auto-close countdown with the user-preferred setting
    data.autoclose['cd_mins'] = data.get_db_data('settings', 'autoclose_mins')
    data.autoclose['countdown'] = data.autoclose['cd_mins'] * 60
    data.wins['root'].tk_vars['autoclose_mins'].set(data.autoclose['cd_mins'])
    password_manager.countdown()
    # Reveal the program's main window and destroy the authentication window
    data.wins['root'].deiconify()
    data.wins['root'].widgets['website_entry'].focus()
    data.wins['root'].update_emails()
    data.wins['login'].attributes('-topmost', False)
    data.wins['login'].withdraw()
    data.wins['login'].widgets['log_entry_user'].delete(0, END)
    data.wins['login'].widgets['log_entry_pass'].delete(0, END)


def update_backup_period(period: str):
    """Updates the period of data backup

    Args:
        period (str): A period over which the autobackup will execute
        user (str): The user who's settings are being changed
    """
    if data.get_db_data('backup', 'period') != period:
        data.set_db_data('backup', 'period', period)


def search_creds(browse=False):
    """Searches the data for the specified website

    Args:
        browse (bool): If this function was executed by the Browse menu button.
    """
    # Get the user search
    web: str = data.wins['root'].widgets['website_entry'].get()

    # Display an error if a search was initiated but the field is empty
    if not browse and not web:
        msg = file_data.lang['messages']['no_website']
        showerror(title=msg['title'], message=msg['text'], parent=data.wins['root'])
        return

    # Create a dictionary out of the data for ease of use
    db_data = data.get_db_data('entries', '*', single=False)
    data_ = {row[1]: {'user': row[2], 'email': row[3], 'password': row[4]} for row in db_data}

    # If the Browse button was clicked display all platforms
    if browse:
        BrowseWindow(data_, None)
        return

    # Collect all keys similar to the one in search
    similar_keys: list | None = check_data(data_)

    if similar_keys is None:
        return

    # Display the credentials if only one similar key was found
    browse_msg = file_data.lang['messages']['browse_acc']
    if len(similar_keys) == 1:
        msg = file_data.lang['messages']['display_creds']
        email = decipher(data.get_db_entry('email', similar_keys[0]))
        pwd = decipher(data.get_db_entry('password', similar_keys[0]))

        showinfo(title=f"{msg['title']} {similar_keys[0]}",
                message=f"{msg['text'][0]} {data_[similar_keys[0]]['user']}\n" \
                        f"{msg['text'][1]} {email}\n{msg['text'][2]} {pwd}",
                parent=data.wins['root']
        )
        key: str = similar_keys[0]
        auto_fill(key, data_[key]['user'], email, pwd)
    # Display a window with all similar keys if multiple were found
    elif len(similar_keys) > 1:
        approved_accounts: dict = {acc:creds for acc, creds in data_.items() if acc in similar_keys}
        BrowseWindow(approved_accounts, web, 200)
    # Display a dialog to browse the data if no similar keys were found
    elif askyesno(title=browse_msg['title'], message=browse_msg['text'], parent=data.wins['root']):
        BrowseWindow(data_, None)


def auto_fill(website: str, user: str, email: str, password: str):
    """Automatically fills the entry boxes with the found creds

    Args:
        website (str): The website to autofill
        user (str): The user to autofill
        email (str): The email to autofill
        password (str): The password to autofill
    """
    data.wins['root'].widgets['website_entry'].delete(0, END)
    data.wins['root'].widgets['user_entry'].delete(0, END)
    data.wins['root'].widgets['password_entry'].entry.delete(0, END)
    data.wins['root'].widgets['email_combo'].delete(0, END)
    data.wins['root'].widgets['website_entry'].insert(0, website)
    data.wins['root'].widgets['user_entry'].insert(0, user)
    data.wins['root'].widgets['password_entry'].entry.insert(0, password)
    data.wins['root'].widgets['email_combo'].insert(0, email)


def check_data(data_: dict) -> list | None:
    """Checks the data for existing platforms

    Args:
        data (dict): The date to be checked for similar results to what the user is searching for

    Returns:
        list | None: List of all matching results. None if exact match (not case-sensitive).
    """
    # Get the message parts in the chosen language
    msg: str = file_data.lang['messages']['display_creds']

    # Define a list of keys that are similar to the one in search
    similar_keys: list = []
    for key, value in data_.items():
        # Display the credentials if the key in search matches
        # any keys in the data exactly (case insensitive)
        if data.wins['root'].widgets['website_entry'].get().lower() == key.lower():
            email = decipher(data_[key]['email'])
            pwd = decipher(data_[key]['password'])
            showinfo(title=f"{msg['title']} {key}",
                    message=f"{msg['text'][0]} {data_[key]['user']}\n{msg['text'][1]} " \
                            f"{email}\n{msg['text'][2]} {pwd}",
                    parent=data.wins['root'])
            data.wins['root'].widgets['password_entry'].clipboard_clear()
            data.wins['root'].widgets['password_entry'].clipboard_append(value['password'])
            auto_fill(key, data_[key]['user'], email, pwd)
            return None

        # Collect all keys that contain the search in themselves and return them
        if data.wins['root'].widgets['website_entry'].get().lower() in key.lower():
            similar_keys.append(key)

    return similar_keys
