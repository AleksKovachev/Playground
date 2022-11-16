"""Additional functions for Password Manager"""

#+ pylint: disable=unused-argument

import json
from os.path import exists, dirname, join
from os import getenv, mkdir, makedirs, scandir, remove
from shutil import copyfile
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import Tk, Toplevel, Button, Label, Frame, messagebox
from string import ascii_letters, punctuation, digits
from importlib import import_module
from datetime import datetime
from re import search
from .dry_data import settings as ddsettings
from .data_handling import cipher, decipher


FONT_A = ("CorsicaMX-Regular", 18, "normal")
FONT_B = ("CorsicaMX-Book", 14, "normal")
FONT_C = ("CorsicaMX-Book", 12, "normal")
FONT_F = ("CorsicaMX-Book", 10, "normal")
VALID_CHARS = ascii_letters + punctuation + digits


def get_median_color(color1: str, color2: str):
    """Calculates the average between two colors

    Args:
        color1 (str): HEX color
        color2 (str): HEX color

    Returns:
        str: A hexadecimal representation on a color. ex. "#23C4AC"
    """

    red1, green1, blue1 = [int(color1[p:p+2], 16) for p in range(1, 6, 2)]  # Here, 6 is len(color)
    red2, green2, blue2 = [int(color2[p:p+2], 16) for p in range(1, 6, 2)]
    return f'#{(red1 + red2) // 2:02x}{(green1 + green2) // 2:02x}{(blue1 + blue2) // 2:02x}'


class Data:
    """Data class to store data from files and shared variables"""

    def __init__(self):
        # Define the path for the data files and backups. Create paths and files if they don't exist already
        self.data_path = join(getenv('LOCALAPPDATA'), "PM Master")
        self.backups_path = join(self.data_path, "backups")

        if not exists(self.data_path) or not exists(self.backups_path):
            makedirs(join(self.backups_path, 'Imported'))
        elif not exists(join(self.backups_path, 'Imported')):
            mkdir(join(self.backups_path, 'Imported'))

        # Language-related variables
        if not exists(join(self.data_path, 'settings.json')):
            with open(join(self.data_path, 'settings.json'), mode='w', encoding='utf-8') as sett:
                json.dump(ddsettings, sett, indent=4)
        with open(join(self.data_path, 'settings.json'), encoding='utf-8') as sett:
            self.main_settings = json.load(sett)
        self.lang = import_module(f"data_files.lang.{self.main_settings['language']}")

        self.update_lang_shortcuts()

        # Get the cuurren username, password and default username and email
        self.user = None
        self.default_user = None
        self.default_email = None
        self.login_pass = None

        # Define the color variables
        self.details1 = "#FFFFFF"
        self.fgc = "#000000"
        self.bgc = "#777777"
        self.accent = "#555555"
        self.details2 = "#DDDDDD"

        # Get the backup period
        self.backup_period = self.upd['backup_period']
        # Calculate shadow color
        self.shadow = get_median_color(self.accent, self.bgc)
        # Save the current Y position of the Mouse
        self.spinbox_ypos = 0

        # Get the main data file and save it to a dictionary variable. If none found - create a new empty dictionary
        self.jdata = {}
        self.load_data()
        # Create folders for data files and backups if they don't exist
        if not exists(self.data_path):
            mkdir(self.data_path)
            if not exists(self.backups_path):
                mkdir(self.backups_path)

        # Autoclose controls
        self.timer = None
        self.cd_mins = 5
        self.countdown = self.cd_mins * 60
        self.timer_st = "00:00"


    def load_data(self):
        """Loads and decrypts the data from disk into memory"""
        self.jdata = decipher('pmd.dat') if exists('pmd.dat') else {}


    def update_lang_shortcuts(self):
        """Updates the variables used for translations"""
        self.auth = self.lang.authenticate['authenticate']
        self.integrity = self.lang.authenticate['authenticate']['manage_data_integrity']
        self.upd = self.lang.update
        self.pmui = self.lang.ui["PMUI"]
        self.theme_ch = self.lang.ui["theme_changer_ui"]
        self.cust = self.lang.ui["cust_settings"]


    def save_data(self, save_data: dict=None):
        """Saves the save_data to disk using encryption. If None - saves the default user data.

        Args:
            data (dict, optional): The data to be encrypted and saved to disk. Defaults to None.
        """
        # Write exit code 1 in case of forced quit during encryption and saving file
        refresh_exit_code(1)

        cipher(save_data or self.jdata)
        # Write exit code 0 after data has been successfully saved to disk
        refresh_exit_code(0)


    def reload(self):
        """Reloads the data file in memory"""
        self.jdata = decipher('pmd.dat')


    def load_language(self, lng:str):
        """Loads the specified language into memory.

        Args:
            lng (str): The desired language corresponding to a language.py file in the lang folder.
        """
        self.lang = import_module(f'data_files.lang.{lng.lower()}')


    def reset_timer(self, event):
        """Resets the timer when user activity is detected"""
        self.countdown = self.cd_mins * 60


data = Data()


def update_list(lst: list, sample: str):
    """Orders a given list by relevancy and alphabetical order

    Args:
        lst (list): the list to be ordered
        sample (str): results starting with this string will be shown first

    Returns:
        list: the ordered version of the input list
    """

    lst.sort()
    temp_lst_first = []
    temp_lst_rest = []
    for item in lst:
        if item.lower().startswith(sample.lower()):
            temp_lst_first.append(item)
        else:
            temp_lst_rest.append(item)
    lst = temp_lst_first + temp_lst_rest

    return lst


def open_file_msg():
    """Display an import file dialog and return chosen filepath"""
    return askopenfilename(
        initialdir=dirname(__file__), title=data.upd['import_data']['askopenfile_title'], filetypes=(("PM Data", "*.dat*"),))


def import_data(root: Tk):
    """Import data from a given data file

    Args:
        root (Tk() window): A Tk() window for the custom messagebox to be a Toplevel of
    """
    # Display an import file dialog and save the chosen filepath to a variable
    import_path = open_file_msg()
    if import_path != "":
        # Create a Custom messagebox window
        data_message = Toplevel(root)
        dm_width = 500
        dm_height = 225
        root_xcenter = root.winfo_x() + root.winfo_width() / 2
        root_ycenter = root.winfo_y() + root.winfo_height() / 2
        data_message.geometry(f"{dm_width}x{dm_height}+{int(root_xcenter - dm_width / 2)}+{int(root_ycenter - dm_height / 2)}")
        data_message.resizable(False, False)
        data_message.config(bg=data.bgc, pady=10, padx=10)
        # Make the main window unclickable until this one is closed
        data_message.grab_set()
        # Make it a tool window (only X button)
        data_message.attributes('-toolwindow', True)
        data_message.focus()

        message = Label(data_message, text=data.upd['import_data']['message'], font=FONT_A, bg=data.bgc, fg=data.details1)
        message.place(relx=0.5, rely=0.2, anchor='center')

        question = Label(data_message, text=data.upd['import_data']['question'], font=FONT_A, bg=data.bgc, fg=data.details1)
        question.place(relx=0.5, rely=0.35, anchor='center')

        new_data_btn = Button(data_message, text=data.upd['import_data']['new_data_btn'], font=FONT_B, bg=data.bgc, fg=data.details1,
                            command=lambda: (new_data_func(import_path), data_message.destroy()))
        new_data_btn.place(relx=0.2, rely=0.8, anchor='center')

        merge_data_btn = Button(data_message, text=data.upd['import_data']['merge_data_btn'], font=FONT_B, bg=data.bgc, fg=data.details1,
                                command=lambda: (merge_data_func(data_message, import_path), data_message.destroy()))
        merge_data_btn.place(relx=0.5, rely=0.8, anchor='center')

        old_data_btn = Button(data_message, text=data.upd['import_data']['old_data_btn'], font=FONT_B, bg=data.bgc, fg=data.details1,
                                command=data_message.destroy)
        old_data_btn.place(relx=0.8, rely=0.8, anchor='center')


def new_data_func(imported_file: str, close: Toplevel = None):
    """Replaces current data file with the new one

    Args:
        imported_file (str): A path to the file used for replacement
        close (Toplevel, optional): A window to close. Defaults to None.
    """
    if not imported_file:
        return None
    # Create an "Imported" folder in the data files if it doesn't already exist
    if not exists(join(data.backups_path, "Imported")):
        mkdir(join(data.backups_path, "Imported"))
    time_now = datetime.now().strftime('%b %d, %Y - %H.%M.%S')
    # Make a backup of the current data file appending current datetime to its name
    copy_backup(time_now, join(data.backups_path, "Imported"), join(data.backups_path, "Imported", f"pmd - {time_now}.dat"), 10)

    # Copy to application main directory
    copyfile(imported_file, "pmd.dat")
    data.load_data()

    # Close this window if it exists
    if close:
        # Set the exit code to 0 (No problems)
        refresh_exit_code(0)
        close.destroy()
        return True
    return None


def merge_data_func(tl_root: Toplevel, imported_file: str):
    """Merges the current data file with the new one and saves it

    Args:
        tl_root (Toplevel): A Toplevel() window used to center the dominant messagebox
        imported_file (str): A path to the file used for merging
    """
    # Create an "Imported" folder in the data files if it doesn't already exist
    if not exists(join(data.backups_path, "Imported")):
        mkdir(join(data.backups_path, "Imported"))
    time_now = datetime.now().strftime('%b %d, %Y - %H.%M.%S')
    # Make a backup of the current data file appending current datetime to its name
    copy_backup(time_now, join(data.backups_path, "Imported"), join(data.backups_path, "Imported", f"pmd - {time_now}.dat"), 10)

    # Read both the new and the current data files
    imported = decipher(imported_file)
    existing = decipher('pmd.dat')

    # Update existing files based on user preference and save to disk.
    dominant = merge_dominant(tl_root)
    if dominant[0] == 'imported':
        existing.update(imported)
        data.save_data(existing)
    elif dominant[0] == 'current':
        imported.update(existing)
        data.save_data(imported)
    data.reload()


def merge_dominant(tl_root: Toplevel):
    """Custom Messagebox window

    Args:
        tl_root (Toplevel): A Toplevel() window used to center the messagebox
    """
    dom = Toplevel()
    dom.iconbitmap(r'icons\icon.ico')
    dom.title('Dominant Data File')
    dom_width = 350
    dom_height = 150
    root_xcenter = tl_root.winfo_x() + tl_root.winfo_width() / 2
    root_ycenter = tl_root.winfo_y() + tl_root.winfo_height() / 2
    dom.geometry(f"{dom_width}x{dom_height}+{int(root_xcenter - dom_width / 2)}+{int(root_ycenter - dom_height / 2)}")
    dom.resizable(False, False)
    dom.config(bg='white')
    # Make the main window unclickable until this one is closed
    dom.grab_set()
    dom.focus()
    response = ['current', 'imported']

    msg = Label(dom, text=data.upd['merge_dominant']['msg'], wraplength=300, bg='white')
    frame = Frame(dom, height=50, width=dom_width, bg='#F0F0F0')
    old_btn = Button(frame, text=data.upd['merge_dominant']['old_btn'], relief='groove', bg="#E1E1E1",
                    command=lambda: (response.pop(1), dom.destroy()))
    new_btn = Button(frame, text=data.upd['merge_dominant']['new_btn'], relief='groove', bg="#E1E1E1",
                    command=lambda: (response.pop(0), dom.destroy()))
    frame.place(relx=0.5, rely=1, anchor='s')
    msg.place(relx=0.5, rely=0.3, anchor='center')
    old_btn.place(relx=0.3, rely=0.75, anchor='sw')
    new_btn.place(relx=0.7, rely=0.75, anchor='se')

    dom.wait_window()
    return response


def export_data():
    """Export data to specified location"""
    export_path = askdirectory(initialdir=dirname(__file__), title=data.upd['export_data_title'])
    if export_path != "":
        time_now = datetime.now().strftime("%b %d, %Y - %H.%M.%S")
        copyfile("pmd.dat", join(export_path, f"pmd - {time_now}.dat"))


def auto_backup(root: Tk, destroy: bool):
    """Save a backup version of the current data. Add current date to its name

    Args:
        root (tkinter root object): root object to destroy for the "on close" option
        dest (bool): True if application should be destroyed, else False
    """
    # Get the backup period user setting
    period = data.jdata[data.user]['pm_settings']['backup']['period']
    time_now = datetime.now()
    time_now_s = time_now.strftime('%b %d, %Y - %H.%M.%S')
    file_date = datetime.strptime(data.jdata[data.user]['pm_settings']['backup']['date'], '%b %d, %Y - %H.%M.%S')

    # If period == "No backup" nothing happens
    if period == 1 and file_date.date() < time_now.date(): # Daily
        copy_backup(time_now_s, data.backups_path, join(data.backups_path, f"pmd - {time_now_s}.dat"), 3)
    elif period == 2 and (time_now - file_date).days > 6: # Weekly
        copy_backup(time_now_s, data.backups_path, join(data.backups_path, f"pmd - {time_now_s}.dat"), 3)
    elif period == 3 and abs((file_date.year - time_now.year) * 12 + (file_date.month - time_now.month)) > 0: # Monthly
        copy_backup(time_now_s, data.backups_path, join(data.backups_path, f"pmd - {time_now_s}.dat"), 3)
    elif period == 4: # On close
        copy_backup(time_now_s, data.backups_path, join(data.backups_path, f"pmd - {time_now_s}.dat"), 3)
    # If there are no files in the backup folder - create one
    elif not any(scandir(data.backups_path)):
        copy_backup(time_now_s, data.backups_path, join(data.backups_path, f"pmd - {time_now_s}.dat"), 3)

    if destroy:
        root.destroy()


def refresh_exit_code(exit_code):
    """Refreshes exit_code parameter in settings file upon data encoding

    Args:
        exit_code (int): Exit code 0 = No problems, exit code 1 = program closed unexpectedly
    """
    with open(join(data.data_path, 'settings.json'), 'r+', encoding='utf-8') as jdat:
        read = json.load(jdat)
        read['exit_code'] = exit_code
        jdat.seek(0)
        json.dump(read, jdat, indent=4)


def copy_backup(time_now_s: str, check_dir: str, copy_dir: str, bac_num: int):
    """Checks the backup folder and copies the backup file

    Args:
        time_now_s (str): Formated datetime
        check_dir (str): The directory to check the contents of
        copy_dir (str): Where to copy the backup file
        bac_num (int): The number of backup files to keep before starting to replace the olderst
    """
    # Get a list of all backup files
    bac_files = [item for item in scandir(check_dir) if item.name.startswith("pmd")]
    # Check if the number of bac_files is greater than allowed
    if len(bac_files) >= bac_num:
        bac_files = check_num_files(bac_num, bac_files)
        # If backups >= max allowed - delete oldest one/-s
        for file in bac_files:
            remove(file.path)

    # Save current datetime as last backup in the user data file and copy it file to the backups folder
    data.jdata[data.user]['pm_settings']['backup']['date'] = time_now_s
    data.save_data()
    copyfile("pmd.dat", copy_dir)


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
    # It's written in a way so that if more files get copied manually - they will be deleted and only the N (reps) latest will remain
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
    if messagebox.askyesno(title=data.upd['recover_from_backup']['title'], message=data.upd['recover_from_backup']['message']):

        # Check if the backup/Imported folder exists and create one if not
        if not exists(join(data.backups_path, "Imported")):
            mkdir(join(data.backups_path, "Imported"))
        time_now = datetime.now().strftime('%b %d, %Y - %H.%M.%S')

        # Make a backup copy of the current data file and then replace with the new one
        copy_backup(time_now, join(data.backups_path, "Imported"), join(data.backups_path, "Imported", f"pmd - {time_now}.dat"), 10)
        copyfile(file, "pmd.data")
        data.reload()


def cust_settings(log_user: str, email: str, def_user: str, password: tuple):
    """Updates the user defined default/login credentials

    Args:
        log_user (str): Login username
        email (str): Default email
        def_user (str): Default username
        password (tuple): Login password
    """

    if (
        # Display a confirmation dialog if user chosen settings aren't empty or the same as current
        log_user not in ("", data.user)
        or email != data.default_email
        or def_user not in ("", data.default_user)
        or (password[1] != "" and password[2] != "")
        or data.cd_mins != data.jdata[data.user]['pm_settings']['autoclose_mins']
    ) and messagebox.askyesno(title=data.upd['cust_settings']['title'], message=data.upd['cust_settings']['message']):

        # Check email, login username and password
        email_check = check_email('static', email)
        log_user_check = check_username('static', log_user)
        pass_check = check_password(password)

        # If all are valid - update current data file and save to disk
        if log_user_check and email_check and pass_check:
            data.jdata[data.user]['pm_settings']['defaults']['email'] = email
            data.jdata[data.user]['pm_settings']['defaults']['user'] = def_user
            data.jdata[data.user]['login_data']['password'] = pass_check
            data.jdata[log_user] = data.jdata.pop(data.user)

            if data.cd_mins != data.jdata[data.user]['pm_settings']['autoclose_mins']:
                data.jdata[data.user]['pm_settings']['autoclose_mins'] = data.cd_mins

            data.save_data()

            # Update variables
            data.user = log_user
            data.default_user = def_user
            data.default_email = email
            data.user = log_user
            data.login_pass = pass_check
    else:
        messagebox.showwarning(title=data.upd['cust_settings2']['title'], message=data.upd['cust_settings2']['message'])


def check_email(event: str, email: str, widget=None) -> bool | None:    # sourcery skip
    """Checks if email is valid

    Args:
        event (event|str): If this is tkinter event type - then it serves as dynamic email check. If str - Checks after confirm
        email (str): The email to check
        widget (Tk widget): A Tk widget supporting bg color (Entry/Label). Defaults to None

    Returns:
        bool | None: bool for static check, else None
    """
    # Define custom acceptable email pattern
    patt = "^(?P<NAME>(?P<FIRST_CHAR>\w)(\w{1,63})(?P<LAST_CHAR>\w))@(?P<DOMAIN>\w{2,30})\\.(?P<TOPLEVEL>[a-z]{2,5})$"  # pylint: disable=anomalous-backslash-in-string
    acc_pattern = search(patt, email)

    # Check if first or last charactes is a special one
    if len(email) > 1 and (email[0] in punctuation or email[-1] in punctuation):
        if event != 'static':
            widget['fg'] = "red"
        else:
            messagebox.showerror(title=data.upd['check_email1']['title'], message=data.upd['check_email1']['message'])
            return False
    # Check if entered email corresponds to the pattern
    elif not acc_pattern:
        if event != 'static':
            widget['fg'] = "red"
        else:
            messagebox.showerror(title=data.upd['check_email2']['title'], message=data.upd['check_email2']['message'])
            return False
    else:
        if event != 'static':
            widget['fg'] = "black"
    return True


def check_username(event: str, user: str, widget=None) -> bool | None:    # pylint: disable=W0613
    """Checks if username is valid

    Args:
        event (event|str): If this is tkinter event type - then it serves as dynamic username check. If str - Checks after confirm
        user (str): The username to check
        widget (Tk widget): A Tk widget supporting bg color (Entry/Label). Defaults to None

    Returns:
        bool | None: bool for static check, else None
    """
    # Check name length
    if 2 < len(user) < 21:
        if event != 'static':
            widget['fg'] = "black"
    elif event != 'static':
        widget['fg'] = "red"
        return None
    else:
        messagebox.showerror(title=data.upd['check_username1']['title'], message=data.upd['check_username1']['message'])
        return False

    # Check if name contains invalid characters
    for char in user:
        if char in VALID_CHARS:
            if event != 'static':
                widget['fg'] = "black"
        elif event != 'static':
            widget['fg'] = "red"
            return None
        else:
            messagebox.showerror(title=data.upd['check_username2']['title'], message=f"{data.upd['check_username2']['message']}, {punctuation}")
            return False

    # Check if username already exists in the data file
    for log in data.jdata:
        if user == log and log != data.user:
            if event != 'static':
                widget['fg'] = "red"
                return None
            else:
                messagebox.showerror(title=data.upd['check_username3']['title'],
                                    message=f"{data.upd['check_username3']['message'][0]} {user} {data.upd['check_username3']['message'][1]}")
                return False
        elif event != 'static':
            widget['fg'] = "black"
    return True


def check_password(pwd: tuple):
    """Checks if password is valid

    Args:
        pwd (tuple): pwd[0] = Old Password, pwd[1] = New Password, pwd[2] = Repeat Password

    Returns:
        bool | str: False if there's an error. Otherwise - the actual password
    """
    # Checks if the new password is different from the current one
    if pwd[0] not in ("", data.jdata[data.user]['login_data']['password']):
        messagebox.showerror(title=data.upd['check_password1']['title'], message=data.upd['check_password1']['message'])
        return False

    # Checks if the new password and the repeat password are the same
    if pwd[1] != pwd[2]:
        messagebox.showerror(title=data.upd['check_password2']['title'], message=data.upd['check_password2']['message'])
        return False

    # Checks if new password is longer than 20 characters
    if len(pwd[2]) > 20:
        messagebox.showerror(title=data.upd['check_password3']['title'], message=data.upd['check_password3']['message'])
        return False

    # Checks if new password is shorter than 4 characters
    if pwd[2] != "" and len(pwd[2]) < 4:
        messagebox.showerror(title=data.upd['check_password4']['title'], message=data.upd['check_password4']['message'])
        return False

    # Checks for invalid characters
    for char in pwd[2]:
        if char not in VALID_CHARS:
            messagebox.showerror(title=data.upd['check_password5']['title'], message=data.upd['check_password5']['message'])
            return False

    return data.jdata[data.user]['login_data']['password'] if pwd[2] == "" else pwd[2]
