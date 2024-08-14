"""A Simple Password Generator App"""

from password_manager.data_management.all_data import data
from password_manager.ui import event_bindings, update_backup_period
from password_manager.ui.access_control.login import Login
from password_manager.ui.main_window import PasswordManagerUI

############################################################################################

# Protection techniques
#+ https://martinheinz.dev/blog/59
#! Use the information for extra security, hashing and securely keeping the passwords

############################################################################################

# TODO: Add 3-5 attempts for password login. Then store the next possible time a new attempt can be made.
# TODO: Test application extensively when finished integrating the Database and remove old ways
# TODO: Fix the merge accounts function
# TODO: Upgrade security of fernet keys. Don't store them directly.
# TODO: When entered a platform and clicked OKAY, the copied text to clipboard is NOT decrypted


def fill_backups():
    """Populate the backup period menu"""
    for index, bac_option in enumerate(data.backup_period):
        data.wins['root'].widgets['backup_menu'].add_radiobutton(
            label=bac_option,
            value=index,
            variable=data.wins['root'].tk_vars['radio_var'],
            command=lambda index=index: update_backup_period(index))


if __name__ == "__main__":
    data.wins['root'] = PasswordManagerUI()
    Login()
    fill_backups()
    event_bindings.bind_events()
    data.wins['root'].mainloop()
