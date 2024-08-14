"""The Authentication window for Password Manager"""

from tkinter import messagebox, END

from password_manager.security.authenticate import is_login_valid
from password_manager.data_management import refresh_startup_language
from password_manager.data_management.all_data import data, file_data
from password_manager.ui.visibility_toggle import show_pass
from password_manager.ui import start_program
from .login_base import LoginBase
from .signup import SignUp

#+ pylint: disable=unused-argument, undefined-variable

# Notes:
# self.attributes('-topmost', True) - Makes the window "Always on top".
    # Also - root.wm_attributes("-topmost", True)
#?  -alpha double - controls opacity (from 0.0 to 1.0).
    #? Changing between 1 and other value may cause the window to flash
#   -fullscreen boolean - ontrols whether the window fills the whole screen, including taskbar
#*  -disabled boolean - makes it impossible to interact with the window and redraws the focus
#   -toolwindow boolean - makes a window with a single close-button (which is smaller than usual)
#= SOME OF THE ABOVE ONLY WORK WITH root.overrideredirect(True)


class Login(LoginBase):
    """Login window"""

    def __init__(self):
        super().__init__()
        self._execute_bindings()
        self._link_buttons()

    def _link_buttons(self):
        """Links the Button widgets to the function they should execute"""
        self.widgets['enter_btn'].config(
            command=lambda: start_program()
                if is_login_valid(self.widgets['log_entry_user'], self.widgets['log_entry_pass'])
                    else self._run_wrong_password_sequence()
        )
        self.widgets['create_btn'].config(command=SignUp)
        self.widgets['log_entry_pass'].btn.config(command=lambda: show_pass(
            self.widgets['log_entry_pass'],
            self.icons['eye_icon_h'],
            self.icons['no_eye_icon_h']
        ))

    def choose_language(self, lng: str):
        """Update all widgets with the selected language.

        Args:
            lng (str): The language that the user chose
        """
        self.widgets['lang_btn'].config(text=lng, image=self.widgets['language_flags'][lng.lower()])
        self.widgets['lang_frame'].place_forget()

        file_data.load_language(lng, self)

        if self.widgets['check_keep_lang']:
            refresh_startup_language(lng.lower())
        else:
            refresh_startup_language("english")
        file_data.main_settings['language'] = lng

        self.title(file_data.lang['login']['auth_title'])
        self.widgets['auth_text'].config(text=file_data.lang['login']['auth_text'])
        self.widgets['enter_btn'].config(text=file_data.lang['login']['signin'])
        self.widgets['create_btn'].config(text=file_data.lang['login']['signup'])
        self.widgets['check_keep_lang'].config(text=file_data.lang['keep_language'])
        if self.widgets['log_entry_user'].cget("fg") == data.colors['bgc']:
            self.widgets['log_entry_user'].delete(0, END)
            self.widgets['log_entry_user'].insert(0, file_data.lang['field_clear']['user'])
        if self.widgets['log_entry_pass'].entry.cget("fg") == data.colors['bgc']:
            self.widgets['log_entry_pass'].entry.delete(0, END)
            self.widgets['log_entry_pass'].entry.insert(
                0, file_data.lang['field_clear']['password'])

    def _run_wrong_password_sequence(self):
        """Display wrong password error message deleting the wrong password"""
        if self.password_error:
            messagebox.showerror(
                title=file_data.lang['messages']['wrong_pass']['title'],
                message=file_data.lang['messages']['wrong_pass']['text'],
                parent=self
            )
        # Delete the wrong password and put the cursor in the password entry box
        self.widgets['log_entry_pass'].entry.delete(0, END)
        self.widgets['log_entry_pass'].entry.config(fg=data.colors['fgc'])
        self.widgets['log_entry_pass'].entry.focus()

        # The below is a bug fix. Without it the password's "show" option resets
        if self.widgets['log_entry_pass'].btn['image'] in (
            str(self.icons['no_eye_icon_h']), str(self.icons['no_eye_icon'])):
            self.widgets['log_entry_pass'].entry["show"] = "✲"
        else:
            self.widgets['log_entry_pass'].entry["show"] = ""
