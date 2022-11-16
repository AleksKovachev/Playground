"""The Authentication window for Password Manager"""

from tkinter import Tk, Toplevel, Label, Button, Entry, Canvas, PhotoImage, messagebox, Frame, END
from string import ascii_letters, punctuation, digits
from datetime import datetime
from os import scandir
from os.path import dirname, join, splitext
from importlib import import_module
from shutil import copyfile
import json
import data_files
from . import updates as ups
from .ui import ui, update_backup_period


# Notes:
# self.auth.attributes('-topmost', True) - Makes the window "Always on top". Also - root.wm_attributes("-topmost", True)
#?  -alpha double - controls opacity (from 0.0 to 1.0). changing between 1 and other value may cause the window to flash
#   -fullscreen boolean - ontrols whether the window fills the whole screen, including taskbar
#*  -disabled boolean - makes it impossible to interact with the window and redraws the focus
#   -toolwindow boolean - makes a window with a single close-button (which is smaller than usual)
#= SOME OF THE ABOVE ONLY WORK WITH root.overrideredirect(True)


BLACK = 'black'
RED = 'red'
MED_GRAY = '#777777'
LIGHT_GRAY = '#DDDDDD'
WHITE = 'white'
FONT_B = ('CorsicaMX-Book', 14, 'normal')
FONT_C = ('CorsicaMX-Book', 12, 'normal')
FONT_D = ('CorsicaMX-Regular', 17, 'normal')
FONT_E = ('CorsicaMX-Normal', 12, 'normal')
FONT_G = ('CorsicaMX-Book', 11, 'normal')
FONT_H = ('CorsicaMX-Regular', 14, 'normal')
VALID_CHARS = ascii_letters + punctuation + digits


class Authenticate:
    """Authenticates the user upon entry"""

    def __init__(self, root):
        # Create the main login window with the following parameters
        self.window = root
        self.auth = Toplevel(root)
        self.auth.title(ups.data.auth['auth_title'])
        auth_width = 450
        auth_height = 380
        root_xcenter = root.winfo_x() + root.winfo_width() / 2
        self.auth.geometry(f'{auth_width}x{auth_height}+{int(root_xcenter - auth_width / 2)}+{root.winfo_y()}')
        # Upon exiting this window terminate the whole application
        self.auth.protocol('WM_DELETE_WINDOW', self.window.quit)
        self.auth.resizable(False, False)
        self.auth.config(bg=MED_GRAY)
        self.auth.iconbitmap(r'data_files\icons\icon.ico')
        self.auth.grab_set()
        # Make it always on top of other applications. Only valid for login window
        self.auth.attributes('-topmost', True)
        self.auth.focus_force()

        # Define the following icons
        self.logo2 = PhotoImage(master=self.auth, file=r'data_files\icons\logo.png')
        self.user_icon = PhotoImage(master=self.auth, file=r'data_files\icons\user.png')
        self.pass_icon = PhotoImage(master=self.auth, file=r'data_files\icons\password.png')
        self.eye_icon = PhotoImage(file=r'data_files\icons\eye.png')
        self.no_eye_icon = PhotoImage(file=r'data_files\icons\no_eye.png')
        self.eye_icon_h = PhotoImage(file=r'data_files\icons\eye_hover.png')
        self.no_eye_icon_h = PhotoImage(file=r'data_files\icons\no_eye_hover.png')

        # Create an image object for every language in the lang folder
        self.flags = {}
        for lng in scandir(r'data_files\lang'):
            if lng.name.endswith('.py'):
                self.flags[''.join(splitext(lng.name)[:-1])] = PhotoImage(file=f"data_files\\icons\\{''.join(splitext(lng.name)[:-1])}.png")

        # Create a Canvas and put a image on it
        auth_canvas = Canvas(master=self.auth, height=200, width=200, bg=MED_GRAY, highlightthickness=0)
        auth_canvas.create_image(100, 100, image=self.logo2)
        auth_canvas.place(relx=0.5, y=0, anchor='n')

        # Build the rest of the UI
        self.login_ui()

        # BINDINGS
        self.create_btn.bind('<Enter>', lambda event: self.create_btn.config(fg="white"))
        self.create_btn.bind('<Leave>', lambda event: self.create_btn.config(fg="#61adff"))
        self.log_entry_pass.bind('<FocusIn>', lambda event: field_clear(event, self.log_entry_user, self.log_entry_pass))
        self.log_entry_pass.bind('<FocusOut>', lambda event: field_clear(event, self.log_entry_user, self.log_entry_pass))
        self.log_entry_user.bind('<FocusIn>', lambda event: field_clear(event, self.log_entry_user, self.log_entry_pass))
        self.log_entry_user.bind('<FocusOut>', lambda event: field_clear(event, self.log_entry_user, self.log_entry_pass))
        self.auth.bind('<Button-1>', lambda event: self.auth.focus() if event.widget not in (self.log_entry_user, self.log_entry_pass) else "")
        self.eye_btn.bind('<Enter>', lambda event: eye_switch_color(
            event, self.eye_btn, (self.eye_icon, self.eye_icon_h, self.no_eye_icon, self.no_eye_icon_h)))
        self.eye_btn.bind('<Leave>', lambda event: eye_switch_color(
            event, self.eye_btn, (self.eye_icon, self.eye_icon_h, self.no_eye_icon, self.no_eye_icon_h)))
        self.auth.bind('<ButtonRelease-1>',
            lambda event: self.lang_frame.place_forget() if event.widget not in self.lang_btns + [self.lang_frame, self.lang_btn] else "")


    def login_ui(self):
        """Creates the UI for logging in"""
        self.auth_text = Label(self.auth, text=ups.data.auth['auth_text'], bg=MED_GRAY, fg=WHITE, font=FONT_B)
        self.auth_text.place(relx=0.5, y=200, anchor='center')
        self.auth.bind('<Return>', self.check_login)

        user_icon_bg = Label(self.auth, bg=LIGHT_GRAY, width=38, height=31, bd=0, image=self.user_icon)
        user_icon_bg.place(x=50, y=245, anchor='w')

        pass_icon_bg = Label(self.auth, bg=LIGHT_GRAY, width=38, height=31, bd=0, image=self.pass_icon)
        pass_icon_bg.place(x=50, y=285, anchor='w')

        user_end_bg = Label(self.auth, text=' ', font=FONT_D, bg=LIGHT_GRAY, width=3, bd=0)
        user_end_bg.place(x=400, y=245, anchor='e')

        pass_end_bg = Label(self.auth, text=' ', font=FONT_D, bg=LIGHT_GRAY, width=3, bd=0)
        pass_end_bg.place(x=400, y=285, anchor='e')

        sep1 = Frame(self.auth, bg=MED_GRAY, width=2, height=28, bd=0)
        sep1.place(x=85, y=245, anchor='e')

        sep2 = Frame(self.auth, bg=MED_GRAY, width=2, height=28, bd=0)
        sep2.place(x=85, y=285, anchor='e')

        self.enter_btn = Button(
            self.auth, text=ups.data.auth['signin'], width=15, font=FONT_C, command=self.check_login, bg=MED_GRAY, fg=WHITE, takefocus=0)
        self.enter_btn.place(relx=0.5, y=340, anchor='center')

        self.create_btn = Button(
            self.auth, text=ups.data.auth['signup'], font=FONT_E, bd=0, command=lambda: SignUp(self.auth), bg=MED_GRAY, fg="#61adff",
            highlightcolor=MED_GRAY, highlightbackground=MED_GRAY, activebackground=MED_GRAY, highlightthickness=0,
            relief='sunken', activeforeground=LIGHT_GRAY, cursor='hand2', takefocus=0)
        self.create_btn.place(relx=0.95, y=10, anchor='ne')

        self.log_entry_user = Entry(self.auth, font=FONT_D, bg=LIGHT_GRAY, fg=BLACK, bd=0, width=21)
        self.log_entry_user.place(anchor='e', x=363, y=245)
        self.log_entry_user.focus()

        self.log_entry_pass = Entry(self.auth, font=FONT_D, bg=LIGHT_GRAY, fg=MED_GRAY, bd=0, width=21)
        self.log_entry_pass.place(anchor='e', x=363, y=285)
        self.log_entry_pass.insert(0, ups.data.auth['log_entry_pass'])

        self.eye_btn = Button(self.auth, border=0, bg=LIGHT_GRAY, fg=LIGHT_GRAY, pady=0, width=30, height=20,
            image=self.no_eye_icon, highlightcolor=LIGHT_GRAY, highlightbackground=LIGHT_GRAY, takefocus=0,
            activebackground=LIGHT_GRAY, highlightthickness=0, relief='sunken', cursor='hand2', command=lambda:show_pass(
                self.log_entry_pass, self.eye_btn, self.eye_icon_h, self.no_eye_icon_h))
        self.eye_btn.place(anchor='e', x=396, y=285)

        # Language controls
        self.lang_frame = Frame(self.auth, bg=LIGHT_GRAY)
        curr_lang = ups.data.main_settings['language']
        self.lang_btn = Button(self.auth, text=curr_lang.capitalize(), font=FONT_E, bd=0, bg=MED_GRAY,
            fg=WHITE, takefocus=0, cursor='hand2', activebackground=MED_GRAY, highlightthickness=0, relief='sunken',
            activeforeground=LIGHT_GRAY, image=self.flags[curr_lang.lower()], compound='left', command=lambda: self.lang_frame.place(
                anchor='nw', relx=0.05, y=35) if self.lang_frame.winfo_ismapped() == 0 else self.lang_frame.place_forget())
        self.lang_btn.place(anchor='nw', relx=0.05, y=10)
        self.lang_btn.update()

        # Get the .py files in the lang folder. Assign the corresponding icons to them.
        langs = [splitext(lng.name)[0].title() for lng in scandir(join(dirname(__file__), 'lang')) if lng.name.endswith('.py')]
        self.lang_btns = []

        # Create a new button for every language. Put every new button below the previous one.
        for index, lng in enumerate(langs):
            btn = Button(self.lang_frame, text=lng, font=FONT_E, bd=0, bg=LIGHT_GRAY, fg=MED_GRAY, takefocus=0, cursor='hand2',
            activebackground=LIGHT_GRAY, highlightthickness=0, relief='sunken', activeforeground=WHITE, image=self.flags[lng.lower()],
            compound='left', command=lambda lng=lng: self.choose_language(lng))
            if index == 0:
                btn.place(anchor='nw', x=0, y=0)
            else:
                btn.place(anchor='nw', x=0, y=pos)
            btn.update()
            pos=btn.winfo_y() + btn.winfo_height()
            self.lang_btns.append(btn)

        # Set the width of the whole dropdown window to be as the widest child button + 2px
        self.lang_frame.config(width=max(btn.winfo_width() for btn in self.lang_btns)+2, height=25*len(langs))


    def choose_language(self, lng: str):
        """Update all widgets with the selected language.

        Args:
            lng (str): The language that the user chose
        """
        self.lang_btn.config(text=lng, image=self.flags[lng.lower()])
        self.lang_frame.place_forget()

        ups.data.load_language(lng)

        with open(join(ups.data.data_path, 'settings.json'), 'r+', encoding='utf-8') as lng_data:
            settings = json.load(lng_data)
            settings['language'] = lng.lower()
            lng_data.seek(0)
            lng_data.truncate()
            json.dump(settings, lng_data, indent=4, ensure_ascii=False)

        ups.data.update_lang_shortcuts()
        self.auth.title(ups.data.auth['auth_title'])
        self.auth_text.config(text=ups.data.auth['auth_text'])
        self.enter_btn.config(text=ups.data.auth['signin'])
        self.create_btn.config(text=ups.data.auth['signup'])
        self.log_entry_user.delete(0, END)
        self.log_entry_user.insert(0, ups.data.lang.authenticate['field_clear']['user'])
        self.log_entry_pass.delete(0, END)
        self.log_entry_pass.insert(0, ups.data.lang.authenticate['field_clear']['password'])


    def check_login(self, *args):    # pylint: disable=W0613
        """Checks credentials and starts the main program. Refreshes the ui based on user preferences.

        Args:
            *args (event): Used by tkinter binding. This method is used by a tkinter button as well
            as tkinter binding which is why "*args" is used instead of "event"
        """

        # Loop through the users and check for corresponding credentials
        for key in ups.data.jdata:
            if key == self.log_entry_user.get():
                if self.log_entry_pass.get() == ups.data.jdata.get(self.log_entry_user.get())['login_data']['password']:
                    self.auth.attributes('-topmost', False)
                    # Save the username
                    ups.data.user = key
                    if data_integrity_check() == 1:
                        manage_data_integrity(self.window, self.auth)
                    else:
                        self.start_program(self.window, self.auth)
                else:
                    # Hide the authentication window to focus on the error then show it back
                    self.auth.withdraw()
                    messagebox.showerror(
                        title=ups.data.auth['check_login']['showerror1']['title'], message=ups.data.auth['check_login']['showerror1']['message'])
                    self.auth.deiconify()
                    # Delete the wrong password and put the cursor in the password entry box
                    self.log_entry_pass.delete(0, END)
                    self.log_entry_pass.focus()
                return
        messagebox.showerror(title=ups.data.auth['check_login']['showerror2']['title'],
                            message=f"{ups.data.auth['check_login']['showerror2']['message'][0]} " \
                                f"{self.log_entry_user.get()} {ups.data.auth['check_login']['showerror2']['message'][1]}")
        return

    @staticmethod
    def start_program(root: Tk, auth: Toplevel):
        """Remove the authentication window and start the program

        Args:
            root (Tk): The main window
            auth (Toplevel): The authentication window
        """
        # Update the theme with the user chosen preferences
        ui.update_theme(ups.data.user)
        # Update the UI with the chosen language
        ups.data.lang = import_module(f"data_files.lang.{ups.data.jdata[ups.data.user]['pm_settings']['language']}")
        ups.data.update_lang_shortcuts()
        lng = ups.data.jdata[ups.data.user]['pm_settings']['language']
        ui.lang_btn.config(text=lng.capitalize(), image=ui.flags[lng.lower()])
        ui.update_language()
        # Check the user defined backup period and update UI with checkmark
        update_backup_period(ups.data.jdata[ups.data.user]['pm_settings']['backup']['period'], ups.data.user)
        ui.radio_var.set(ups.data.jdata[ups.data.user]['pm_settings']['backup']['period'])
        # Save the user preferences for default username and email
        ups.data.default_user = ups.data.jdata[ups.data.user]['pm_settings']['defaults']['user']
        ups.data.default_email = ups.data.jdata[ups.data.user]['pm_settings']['defaults']['email']
        # Write the default username and email to the UI entry boxes
        ui.emails.set(ups.data.default_email)
        ui.user_entry.delete(0, END)
        ui.user_entry.insert(0, ups.data.default_user)
        # Update the Status bar
        msg = ups.data.auth['check_login']['status_entries_num']
        ui.status_entries_num.set(f"{msg[0]} {ups.data.user}! {msg[1]} {len(ups.data.jdata[ups.data.user]['entries'])} " \
            f"{msg[2]} {ups.data.jdata[ups.data.user]['pm_settings']['backup']['date']}")
        ui.cd_var.set(f"{ups.data.auth['check_login']['autoclose']} {ups.data.timer_st}")
        # Run the auto-close countdown with the user-prefered setting
        ups.data.cd_mins = ups.data.jdata[ups.data.user]['pm_settings']['autoclose_mins']
        ups.data.countdown = ups.data.cd_mins * 60
        ui.autoclose_mins.set(ups.data.cd_mins)
        data_files.countdown()
        # Reveal the main program window and destroy the authentication window
        root.deiconify()
        auth.destroy()


def data_integrity_check():
    """Checks PM's exit_code"""
    with open(join(ups.data.data_path, 'settings.json'), 'r', encoding='utf-8') as jdat:
        read = json.load(jdat)
    return read['exit_code']


def load_backup_data(data_integrity: Toplevel, root: Tk, auth: Toplevel):
    """Replaces the main data file with the lates backup

    Args:
        data_integrity (Toplevel): The pop-up message to close
        root (Tk): The main window needed for starting the program
        auth (Toplevel): The authentication needed to be destroyed to start the program
    """
    # Collect all existing backups and copy the newest
    if backups := [dat for dat in scandir(ups.data.backups_path) if dat.name.endswith('.dat')]:
        newest = backups[0]
        for file in backups:
            if file.stat().st_mtime > newest.stat().st_mtime:
                newest = file
        mbox = ups.data.auth['load_backup_data']
        if messagebox.askyesno(title=ups.data.auth['load_backup_data']['title'],
            message=mbox['message'][0] + datetime.fromtimestamp(newest.stat().st_mtime).strftime('%b %d, %Y - %H.%M.%S') + mbox['message'][1]):
            copyfile(newest.path, 'pmd.dat')
            ups.data.load_data()
            data_integrity.destroy()
            start_program(root, auth)
    else:
        messagebox.showerror(title=ups.data.auth['load_backup_data2']["title"], message=ups.data.auth['load_backup_data2']["message"])


def manage_data_integrity(root: Tk, auth: Toplevel):
    """Displays a pop-up message if exit_code was 1. Gives options for data management

    Args:
        root (Tk): The main root window to use for centering this pop-up window
    """
    # Create a Custom messagebox window
    data_integrity = Toplevel(root)
    data_integrity.title(ups.data.pmui['main_title'])
    di_width = 600
    di_height = 300
    root_xcenter = root.winfo_x() + root.winfo_width() / 2
    root_ycenter = root.winfo_y() + root.winfo_height() / 2
    data_integrity.geometry(f"{di_width}x{di_height}+{int(root_xcenter - di_width / 2)}+{int(root_ycenter - di_height / 2)}")
    data_integrity.protocol('WM_DELETE_WINDOW', lambda: (start_program(root, auth), data_integrity.destroy()))
    data_integrity.resizable(False, False)
    data_integrity.attributes('-topmost', True)
    data_integrity.attributes('-topmost', False)
    data_integrity.config(bg=ups.data.bgc, pady=10, padx=10)
    # Make the main window unclickable until this one is closed
    data_integrity.grab_set()
    # Make it a tool window (only X button)
    data_integrity.attributes('-toolwindow', True)
    data_integrity.focus()

    message = Label(data_integrity, text=ups.data.integrity['message'], font=FONT_H, bg=ups.data.bgc, fg=ups.data.details1,
                    justify='left', wraplength=450)
    message.place(relx=0.05, rely=0.1, anchor='nw')

    explain = Label(data_integrity, text=ups.data.integrity['explain'], font=FONT_G, bg=ups.data.bgc, fg=ups.data.details1,
                    justify='left', wraplength=300)
    explain.place(relx=0.05, rely=0.4, anchor='nw')

    choose_data_btn = Button(data_integrity, text=ups.data.integrity['choose_data_btn'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1,
                            command=lambda: start_program(root, auth) if ups.new_data_func(ups.open_file_msg(), data_integrity) else "")
    choose_data_btn.place(relx=0.98, rely=0.55, anchor='ne')

    use_last_data_btn = Button(data_integrity, text=ups.data.integrity['use_last_data_btn'], font=FONT_C, bg=ups.data.bgc,
                            fg=ups.data.details1, command=lambda: load_backup_data(data_integrity, root, auth))
    use_last_data_btn.place(relx=0.98, rely=0.7, anchor='ne')

    continue_btn = Button(data_integrity, text=ups.data.integrity['continue_btn'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1,
                        command=lambda: (start_program(root, auth), data_integrity.destroy()))
    continue_btn.place(relx=0.98, rely=0.85, anchor='ne')


def check_pwd(event: str, password: str) -> bool | None:
    """Checks if password is valid

    Args:
        event (event|str): If this is tkinter event type - then it serves as dynamic username check. If str - Checks after confirm
        password (str): The password to be checked
        repeat (str): The password from the "repeat password" entry field for comparison with password

    Returns:
        bool: False if there's an error. Otherwise - True.
    """
    if len(password) > 20:
        if event != "static":
            event.widget['fg'] = "red"
            return None
        messagebox.showerror(title=ups.data.auth['check_pwd']['showerror1']['title'], message=ups.data.auth['check_pwd']['showerror1']['message'])
        return False
    if event != 'static':
        event.widget['fg'] = "black"

    if len(password) < 4 or password == "Password":
        if event != "static":
            event.widget['fg'] = "red"
            return None
        messagebox.showerror(title=ups.data.auth['check_pwd']['showerror2']['title'], message=ups.data.auth['check_pwd']['showerror2']['message'])
        return False
    if event != 'static':
        event.widget['fg'] = "black"

    for char in password:
        if char not in VALID_CHARS:
            if event != "static":
                event.widget['fg'] = "red"
                return None
            messagebox.showerror(title=ups.data.auth['check_pwd']['showerror3']['title'],
                                message=ups.data.auth['check_pwd']['showerror3']['message'])
            return False
        if event != 'static':
            event.widget['fg'] = "black"
    return True


def check_pwd_rep(event: str, password: str, repeat: str) -> bool | None:
    """Checks if password is valid

    Args:
        event (event|str): If this is tkinter event type - then it serves as dynamic username check. If str - Checks after confirm
        password (str): The password to be checked
        repeat (str): The password from the "repeat password" entry field for comparison with password

    Returns:
        bool: False if there's an error. Otherwise - True.
    """
    if password != repeat:
        if event != "static":
            event.widget['fg'] = "red"
            return None
        messagebox.showerror(title=ups.data.lang.authenticate['check_pwd_rep']['title'],
                            message=ups.data.lang.authenticate['check_pwd_rep']['message'])
        return False
    if event != "static":
        event.widget['fg'] = "black"
        return None
    return None


class SignUp:
    """Responsible for the Sign-up operations"""

    def __init__(self, root: Tk):
        # Get the login window as a main one and hide it.
        self.root = root
        self.root.withdraw()
        # Create the signup window with the following parameters
        self.reg = Toplevel(root)
        self.reg.title(ups.data.lang.authenticate['signup']['title'])
        su_width = 450
        su_height = 490
        root_xcenter = root.winfo_x() + root.winfo_width() / 2
        self.reg.geometry(f'{su_width}x{su_height}+{int(root_xcenter - su_width / 2)}+{root.winfo_y()}')
        # Upon clicking X close the signup window and show the main signin one
        self.reg.protocol('WM_DELETE_WINDOW', lambda: (self.reg.destroy(), self.root.deiconify()))
        self.reg.resizable(False, False)
        self.reg.config(bg=MED_GRAY)
        self.reg.iconbitmap(r'data_files\icons\icon.ico')
        self.reg.grab_set()
        # Make the signup window always on top
        self.reg.attributes('-topmost', True)
        self.reg.focus_force()

        # Define the following icons
        self.logo2 = PhotoImage(master=self.reg, file=r'data_files\icons\logo.png')
        self.user_icon = PhotoImage(master=self.reg, file=r'data_files\icons\user.png')
        self.pass_icon = PhotoImage(master=self.reg, file=r'data_files\icons\password.png')
        self.email_icon = PhotoImage(master=self.reg, file=r'data_files\icons\email.png')
        self.eye_icon = PhotoImage(file=r'data_files\icons\eye.png')
        self.no_eye_icon = PhotoImage(file=r'data_files\icons\no_eye.png')
        self.eye_icon_h = PhotoImage(file=r'data_files\icons\eye_hover.png')
        self.no_eye_icon_h = PhotoImage(file=r'data_files\icons\no_eye_hover.png')

        # Create a Canvas and put a image on it
        reg_canvas = Canvas(master=self.reg, height=200, width=200, bg=MED_GRAY, highlightthickness=0)
        reg_canvas.create_image(100, 100, image=self.logo2)
        reg_canvas.pack(side='top')

        # Build the rest of the UI
        self.new_account_ui()

        # BINDINGS
        self.entrance_user.bind('<KeyRelease>', lambda event: ups.check_username(event, self.entrance_user.get(), self.entrance_user))
        self.entrance_email.bind('<KeyRelease>', lambda event: ups.check_email(event, self.entrance_email.get(), self.entrance_email))
        self.entrance_pass.bind('<KeyRelease>', lambda event: check_pwd(event, self.entrance_pass.get()))
        self.repeat_pass.bind('<KeyRelease>', lambda event: check_pwd_rep(event, self.entrance_pass.get(), self.repeat_pass.get()))

        self.entrance_pass.bind('<FocusIn>', lambda event: field_clear(
            event, self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass))
        self.entrance_pass.bind('<FocusOut>', lambda event: field_clear(
            event, self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass))
        self.repeat_pass.bind('<FocusIn>', lambda event: field_clear(
            event, self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass))
        self.repeat_pass.bind('<FocusOut>', lambda event: field_clear(
            event, self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass))
        self.entrance_user.bind('<FocusIn>', lambda event: field_clear(
            event, self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass))
        self.entrance_user.bind('<FocusOut>', lambda event: field_clear(
            event, self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass))
        self.entrance_email.bind('<FocusIn>', lambda event: field_clear(
            event, self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass))
        self.entrance_email.bind('<FocusOut>', lambda event: field_clear(
            event, self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass))
        self.reg.bind('<Button-1>', lambda event: self.reg.focus() if event.widget not in (
            self.entrance_user, self.entrance_pass, self.entrance_email, self.repeat_pass) else "")
        self.eye_btn_pass.bind("<Enter>", lambda event: eye_switch_color(
            event, event.widget, (self.eye_icon, self.eye_icon_h, self.no_eye_icon, self.no_eye_icon_h)))
        self.eye_btn_pass.bind("<Leave>", lambda event: eye_switch_color(
            event, event.widget, (self.eye_icon, self.eye_icon_h, self.no_eye_icon, self.no_eye_icon_h)))
        self.eye_btn_rep.bind("<Enter>", lambda event: eye_switch_color(
            event, event.widget, (self.eye_icon, self.eye_icon_h, self.no_eye_icon, self.no_eye_icon_h)))
        self.eye_btn_rep.bind("<Leave>", lambda event: eye_switch_color(
            event, event.widget, (self.eye_icon, self.eye_icon_h, self.no_eye_icon, self.no_eye_icon_h)))
        self.reg.bind('<Return>', self.save_login)


    def check_pass_btn(self, btn: str):
        """Hides/Shows the password in the Password or the Repeat Password Entry box
        based on which Eye Button (icon) was clicked.

        Args:
            btn (str): Can only be "Pass" or "Rep". Defines which method should be executed
        """
        if btn == "Pass":
            show_pass(self.entrance_pass, self.eye_btn_pass, self.eye_icon_h, self.no_eye_icon_h)
        elif btn == "Rep":
            show_pass(self.repeat_pass, self.eye_btn_rep, self.eye_icon_h, self.no_eye_icon_h)


    def new_account_ui(self):
        """Creates the UI for creating a new account"""
        # Shortcut for the text in the chosen language
        nau = ups.data.lang.authenticate['signup']['new_account_ui']

        # Labels
        reg_text = Label(self.reg, text=nau['reg_text'], bg=MED_GRAY, fg=WHITE, font=FONT_B)
        reg_text.place(relx=0.5, y=210, anchor='center')

        user_icon_bg = Label(self.reg, bg=LIGHT_GRAY, width=38, height=29, bd=0, text='  ', compound='left',
                            image=self.user_icon)
        user_icon_bg.place(x=50, y=265, anchor='w')

        self.email_icon_bg = Label(self.reg, bg=LIGHT_GRAY, width=38, height=29, bd=0, text='  ', compound='left',
                            image=self.email_icon)
        self.email_icon_bg.place(x=50, y=310, anchor='w')

        pass_icon_bg = Label(self.reg, bg=LIGHT_GRAY, width=38, height=29, bd=0, text='  ', compound='left',
                            image=self.pass_icon)
        pass_icon_bg.place(x=50, y=355, anchor='w')

        repeat_icon_bg = Label(self.reg, bg=LIGHT_GRAY, width=38, height=29, bd=0, text='  ', compound='left',
                            image=self.pass_icon)
        repeat_icon_bg.place(x=50, y=400, anchor='w')

        pass_eye_bg = Label(self.reg, text=' ', bg=LIGHT_GRAY, fg=WHITE, font=FONT_D, bd=0, width=3)
        pass_eye_bg.place(x=400, y=355, anchor='e')

        repeat_eye_bg = Label(self.reg, text=' ', bg=LIGHT_GRAY, fg=WHITE, font=FONT_D, bd=0, width=3)
        repeat_eye_bg.place(x=400, y=400, anchor='e')

        # Entry boxes
        self.entrance_user = Entry(self.reg, font=FONT_D, fg=MED_GRAY, bg=LIGHT_GRAY, width=24, bd=0)
        self.entrance_user.place(anchor='e', x=400, y=265)
        self.entrance_user.focus()

        self.entrance_email = Entry(self.reg, font=FONT_D, fg=MED_GRAY, bg=LIGHT_GRAY, width=24, bd=0)
        self.entrance_email.place(anchor='e', x=400, y=310)
        self.entrance_email.insert(0, nau['entrance_email'])

        self.entrance_pass = Entry(self.reg, font=FONT_D, fg=MED_GRAY, bg=LIGHT_GRAY, width=21, bd=0)
        self.entrance_pass.place(anchor='e', x=361, y=355)
        self.entrance_pass.insert(0, nau['entrance_pass'])

        self.repeat_pass = Entry(self.reg, font=FONT_D, fg=MED_GRAY, bg=LIGHT_GRAY, width=21, bd=0)
        self.repeat_pass.place(anchor='e', x=361, y=400)
        self.repeat_pass.insert(0, nau['repeat_pass'])

        # Buttons
        e_btn = Button(self.reg, text=nau['e_btn'], width=15, font=FONT_C, command=self.save_login, bg=MED_GRAY, fg=WHITE, takefocus=0)
        e_btn.place(relx=0.5, y=450, anchor='center')

        self.eye_btn_pass = Button(self.reg, border=0, bg=LIGHT_GRAY, fg=LIGHT_GRAY, pady=0, width=30, height=20,
            highlightcolor=LIGHT_GRAY, image=self.no_eye_icon, highlightbackground=LIGHT_GRAY, highlightthickness=0,
            activebackground=LIGHT_GRAY, relief='sunken', cursor='hand2', command=lambda:self.check_pass_btn('Pass'), takefocus=0)
        self.eye_btn_pass.place(anchor='e', x=396, y=355)

        self.eye_btn_rep = Button(self.reg, border=0, bg=LIGHT_GRAY, fg=LIGHT_GRAY, pady=0, width=30, height=20,
            highlightcolor=LIGHT_GRAY, image=self.no_eye_icon, highlightbackground=LIGHT_GRAY, highlightthickness=0,
            activebackground=LIGHT_GRAY, relief='sunken', cursor='hand2', command=lambda:self.check_pass_btn('Rep'), takefocus=0)
        self.eye_btn_rep.place(anchor='e', x=396, y=400)

        # Separators for the icons in the entry boxes
        sep1 = Frame(self.reg, bg=MED_GRAY, width=2, height=28, bd=0)
        sep1.place(x=83, y=265, anchor='e')

        sep2 = Frame(self.reg, bg=MED_GRAY, width=2, height=28, bd=0)
        sep2.place(x=83, y=310, anchor='e')

        sep3 = Frame(self.reg, bg=MED_GRAY, width=2, height=28, bd=0)
        sep3.place(x=83, y=355, anchor='e')

        sep4 = Frame(self.reg, bg=MED_GRAY, width=2, height=28, bd=0)
        sep4.place(x=83, y=400, anchor='e')


    def save_login(self, *args):  # pylint: disable=W0613
        """Saves the new user with their credentials

        Args:
            *args (event): Used by tkinter binding. This method is used by a tkinter button as well
            as tkinter binding which is why "*args" is used instead of "event"
        """
        # Check if all fields are filled
        if any((self.entrance_user.get() == "",
                self.entrance_email.get() == "",
                self.entrance_pass.get() == "",
                self.repeat_pass.get() == "")):
            messagebox.showwarning(title=ups.data.lang.authenticate['signup']['save_login']['title'],
                                    message=ups.data.lang.authenticate['signup']['save_login']['message'])
            return

        # Check if all fields are valid
        if (ups.check_username('static', self.entrance_user.get()) is False or
                ups.check_email('static', self.entrance_email.get()) is False or
                check_pwd('static', self.entrance_pass.get()) is False or
                check_pwd_rep('static', self.entrance_pass.get(), self.repeat_pass.get()) is False):
            return

        # Define the startup data for the new account
        log_data = {
            self.entrance_user.get(): {
                'login_data': {
                    'email': self.entrance_email.get(),
                    'password': self.entrance_pass.get(),
                    'attempts': 0,
                    'secondary_attempts': 0,
                    'date_time': 0,
                    'account_status': 'unlocked',
                    'unlock_code': ''
                },
                'pm_settings': {
                    'theme': {
                        'DETAILS1': 'white',
                        'ACCENT': '#555555',
                        'BG': '#777777',
                        'FG': 'black',
                        'DETAILS2': '#DDDDDD',
                    },
                    'backup': {
                        'period': 1,
                        'date': datetime.now().strftime('%b %d, %Y - %H.%M.%S')
                    },
                    'defaults': {
                        'user': self.entrance_user.get(),
                        'email': self.entrance_email.get()
                    },
                    'language': 'english',
                    'autoclose_mins': 5
                },
                'entries': {}
            }}

        # Update the currently opened data file
        ups.data.jdata.update(log_data)

        # Write the new data to disk
        ups.data.save_data()

        # Show the main application window and destroy the signup one
        self.root.deiconify()
        self.reg.destroy()


# Common functions
def field_clear(event, user: Entry, password: Entry, email: Entry = None, repeat_password: Entry = None):
    """Manages the entry boxex default text

    Args:
        event (event): Used to check which widget is using the funciton
        user (tkinter entry box object): Username Entry Box
        password (tkinter entry box object): Password Entry Box
        email (tkinter entry box object, optional): Email Entry Box. Defaults to None.
        repeat_password (tkinter entry box object, optional): Repeat Password Entry Box. Defaults to None.
    """
    if event.widget == password:
        field = password
        fill = ups.data.lang.authenticate['field_clear']['password']
        is_password = 1
    elif event.widget == user:
        field = user
        fill = ups.data.lang.authenticate['field_clear']['user']
        is_password = False
    elif event.widget == email:
        field = email
        fill = ups.data.lang.authenticate['field_clear']['email']
        is_password = False
    elif event.widget == repeat_password:
        field = repeat_password
        fill = ups.data.lang.authenticate['field_clear']['repeat_password']
        is_password = 2

    if event.type == '9':  # Focus In
        if field.get() == fill:
            field.delete(0, END)
            field['fg'] = BLACK
            if is_password == 1:
                password['show'] = "✲"
            elif is_password == 2:
                repeat_password['show'] = "✲"

    elif event.type == '10':  # Focus Out
        if field.get() == "":
            field.insert(0, fill)
            field['fg'] = MED_GRAY
            if is_password == 1:
                password['show'] = ""
            elif is_password == 2:
                repeat_password['show'] = ""


def eye_switch_color(event, button: Button, icons: tuple):
    """Defines color switching for the eye icon

    Args:
        event (event): Used to check if the Cursor has Entered or Left the Button
        button (tkinter button object): The button that changes its icon. Also used for the event above.
        icons (tuple): A tuple containing 4 icons in the form of tkinter PhotoImage
    """
    if event.type == '7':  # Mouse enter
        if button['image'] == str(icons[2]):
            button['image'] = icons[3]
        elif button['image'] == str(icons[0]):
            button['image'] = icons[1]
    elif event.type == '8':  # Mouse leave
        if button['image'] == str(icons[1]):
            button['image'] = icons[0]
        elif button['image'] == str(icons[3]):
            button['image'] = icons[2]


def show_pass(password: Entry, eye_button: Button, eye_hover: PhotoImage, no_eye_hover: PhotoImage):
    """Hides/Shows the password in the entry box

    Args:
        password (tkinter entry box object): Changes its character visuals.
            Also used to check if the button below should have any effect.
        eye_button (tkinter button object): The button which changes its image
        eye_hover (tkinter PhotoImage object): An icon
        no_eye_hover (tkinter PhotoImage object): An icon
    """
    if password.get() not in (ups.data.lang.authenticate['field_clear']['password'], ups.data.lang.authenticate['field_clear']['repeat_password']):
        if eye_button['image'] == str(no_eye_hover):
            eye_button['image'] = eye_hover
        elif eye_button['image'] == str(eye_hover):
            eye_button['image'] = no_eye_hover
        password["show"] = "✲" if password["show"] == "" else ""
