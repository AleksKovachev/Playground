"""This Module contains a class that implements some functionality for the UI"""

import os
from tkinter import (
    Tk, Canvas, Frame, Menu, PhotoImage, Label, Button, Radiobutton, Checkbutton, Entry, Spinbox,
    Listbox, IntVar, StringVar, SINGLE, FLAT, SUNKEN, DISABLED, LEFT, N, E, W, NE, NW, SE, SW
)
from tkinter.ttk import Combobox, Style, Sizegrip
from datetime import datetime

from password_manager.widgets import PWDEntry
from password_manager.data_management.all_data import data, file_data
from password_manager.constants import (FONT_A, FONT_B, FONT_C, FONT_E, FONT_F, ICONS_DIR,
                                        LANGUAGES_DIR, BACKUPS_PATH, WORD_FORMAT, DIGIT_FORMAT)
from password_manager.security.encryption import decipher
from password_manager.ui.settings import CustomizationSettings
from password_manager.ui.data_io import recover_from_backup
from password_manager import auto_backup

#+ pylint: disable=unused-argument


class PasswordManagerBase(Tk):
    """Implements UI functionality"""

    def __init__(self):
        super().__init__()
        self.widgets = {}
        self.tk_vars = {}
        self.ttk_styles = {}
        self.icons = {}
        self.fields_to_refresh = {}

        self._set_up()
        self.define_icons()
        self.draw_ui()

    def _set_up(self):
        """Create and set up the main window"""
        data.wins['root'] = self
        self.withdraw()
        self.title(file_data.lang['main_title'])

        app_width, app_height = 790, 510
        scr_pos_x = int(self.winfo_screenwidth() / 2 - app_width / 2)
        scr_pos_y = int(self.winfo_screenheight() / 2 - app_height)
        self.geometry(f'{app_width}x{app_height}+{scr_pos_x}+{scr_pos_y}')

        # Upon exit check the backup period and create a data backup if needed
        self.protocol('WM_DELETE_WINDOW', lambda: auto_backup(destroy=True))
        self.minsize(app_width, app_height)
        self.config(background=data.colors['bgc'])
        self.iconbitmap(os.path.join(ICONS_DIR, "icon.ico"))

    def define_icons(self):
        """Defines Icons"""
        self.icons['logo']          = PhotoImage(file=os.path.join(ICONS_DIR, "logo.png"))
        self.icons['eye_icon']      = PhotoImage(file=os.path.join(ICONS_DIR, "eye.png"))
        self.icons['no_eye_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "no_eye.png"))
        self.icons['eye_icon_h']    = PhotoImage(file=os.path.join(ICONS_DIR, "eye_hover.png"))
        self.icons['no_eye_icon_h'] = PhotoImage(file=os.path.join(ICONS_DIR, "no_eye_hover.png"))
        self.icons['browse_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "browse.png"))
        self.icons['import_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "import.png"))
        self.icons['export_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "export.png"))
        self.icons['backup_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "backup.png"))
        self.icons['logout_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "logout.png"))
        self.icons['exit_icon']     = PhotoImage(file=os.path.join(ICONS_DIR, "exit.png"))
        self.icons['copy_icon']     = PhotoImage(file=os.path.join(ICONS_DIR, "copy.png"))
        self.icons['paste_icon']    = PhotoImage(file=os.path.join(ICONS_DIR, "paste.png"))
        self.icons['cut_icon']      = PhotoImage(file=os.path.join(ICONS_DIR, "cut.png"))
        self.icons['themes_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "themes.png"))
        self.icons['light_icon']    = PhotoImage(file=os.path.join(ICONS_DIR, "light.png"))
        self.icons['prefs_icon']    = PhotoImage(file=os.path.join(ICONS_DIR, "prefs.png"))
        self.icons['dark_icon']     = PhotoImage(file=os.path.join(ICONS_DIR, "dark.png"))
        self.icons['backup_icon']   = PhotoImage(file=os.path.join(ICONS_DIR, "backup_period.png"))
        self.icons['settings_icon'] = PhotoImage(file=os.path.join(ICONS_DIR, "settings.png"))

    def define_ui(self):
        """Defines the UI widgets for the Main window"""
        self._define_canvas()
        self._collect_language_icons()
        self._define_menu_bar()
        self._define_frames()
        self._define_labels()
        self._define_entry_boxes()
        self._define_spinboxes()
        self._define_buttons()
        self._define_radio_buttons()
        self._define_checkboxes()
        self._define_combobox_style()
        self._define_comboboxes()
        self._define_listboxes()
        self._define_sizegrip()
        self._define_language_controls()

        # Fix the focus order when using Tab key
        self.widgets['password_entry'].lift()
        self.widgets['autocomplete_box'].lift()

    def draw_ui(self):
        """Draws the UI for the Main window"""
        self.define_ui()
        self._draw_canvas()
        self._draw_menu_bar()
        self._define_edit_commands()
        self._populate_backups()
        self._draw_frames()
        self._draw_labels()
        self._draw_entry_boxes()
        self._draw_buttons()
        self._draw_sizegrip()
        self._draw_comboboxes()

    def _define_canvas(self):
        """Defines the main window's canvas for the logo"""
        self.widgets['canvas'] = Canvas(
            background=data.colors['bgc'], height=200, width=200, highlightthickness=0)

    def _collect_language_icons(self):
        """Create an image object for every language in the lang directory"""
        self.widgets['language_flags'] = {}
        for lng in os.scandir(LANGUAGES_DIR):
            if lng.name.endswith('.json'):
                lng_name = ''.join(os.path.splitext(lng.name)[:-1])
                self.widgets['language_flags'][lng_name] = PhotoImage(
                    file=f"{os.path.join(ICONS_DIR, lng_name)}.png")

    def _define_menu_bar(self):
        """Define the Menu Bar and all sub-menus"""
        common = {'tearoff': False, 'font': FONT_F, 'activebackground': data.colors['bgc']}

        self.widgets['menubar'] = Menu()

        self.widgets['file_menu'] = Menu(self.widgets['menubar'], **common)
        self.widgets['edit_menu'] = Menu(self.widgets['menubar'], **common)
        self.widgets['settings_menu'] = Menu(self.widgets['menubar'], **common)
        self.widgets['lang_menu'] = Menu(self.widgets['menubar'], **common)

        self.widgets['backups_menu'] = Menu(self.widgets['file_menu'], **common)
        self.widgets['prefs_menu'] = Menu(self.widgets['settings_menu'], **common)
        self.widgets['backup_menu'] = Menu(self.widgets['settings_menu'], **common)
        self.widgets['color_menu'] = Menu(self.widgets['prefs_menu'], **common)
        self.widgets['r_click_popup'] = Menu(self, **common)

        # Define variable for the radio buttons in the Options menu and for the autoclose minutes
        self.tk_vars['autoclose_mins'] = IntVar(value=data.autoclose['cd_mins'])
        self.tk_vars['radio_var'] = IntVar()

    def _define_frames(self):
        """Defines the frames for the Status Bar and the password Options menu"""
        self.widgets['status_bar'] = Frame(
            bg=data.colors['accent'], bd=1, height=22, relief=FLAT)
        self.widgets['options_frame'] = Frame(bg=data.colors['accent'], width=565, height=45)

    def _define_labels(self):
        """Defines Labels"""
        common = {
            'font': FONT_B,
            'foreground': data.colors['details1'],
            'background': data.colors['bgc']
        }
        self.tk_vars['status_entries_num'] = StringVar()
        self.tk_vars['countdown_var'] = StringVar()

        self.widgets['website_label'] = Label(
            text=file_data.lang['main_labels']['website'], **common)
        self.widgets['user_label'] = Label(
            text=file_data.lang['main_labels']['user'], **common)
        self.widgets['email_label'] = Label(
            text=file_data.lang['main_labels']['email'], **common)
        self.widgets['password_label'] = Label(
            text=file_data.lang['main_labels']['password'], **common)

        self.widgets['password_length'] = Label(
            text=file_data.lang['main_labels']['password_length'],
            font=FONT_B,
            foreground=data.colors['details1'],
            background=data.colors['accent']
        )
        self.widgets['status_entries'] = Label(
            text=file_data.lang['main_labels']['status_entries'],
            font=FONT_F,
            foreground=data.colors['details1'],
            background=data.colors['accent'],
            textvariable=self.tk_vars['status_entries_num']
        )
        self.widgets['countdown_label'] = Label(
            text=data.autoclose['timer_st'],
            font=FONT_F,
            foreground=data.colors['details1'],
            background=data.colors['accent'],
            textvariable=self.tk_vars['countdown_var']
        )

    def _define_entry_boxes(self):
        """Defines Entry boxes"""
        common = {
            'background': data.colors['details2'],
            'foreground': data.colors['fgc'],
            'font': FONT_A,
            'selectbackground': data.colors['bgc'],
            'border': 0
        }

        self.widgets['website_entry'] = Entry(width=29, **common)
        self.widgets['user_entry'] = Entry(width=40, **common)
        self.widgets['password_entry'] = PWDEntry(
            width=31, show="✲", **common, image=self.icons['no_eye_icon'])
        self.fields_to_refresh['user_entry'] = self.widgets['user_entry']

    def _define_spinboxes(self):
        """Defines Spinboxes"""
        self.tk_vars['pass_length'] = IntVar(value=8)
        self.widgets['char_spinbox'] = Spinbox(
            from_=6,
            to=20,
            font=FONT_C,
            foreground=data.colors['details1'],
            background=data.colors['bgc'],
            border=1,
            width=2,
            buttonbackground=data.colors['bgc'],
            state=DISABLED,
            selectbackground=data.colors['accent'],
            readonlybackground=data.colors['bgc'],
            textvariable=self.tk_vars['pass_length'],
            takefocus=False,
            cursor='sb_v_double_arrow'
        )

    def _define_buttons(self):
        """Defines Buttons"""
        options = {
            'font': FONT_C,
            'fg': data.colors['details1'],
            'bg': data.colors['bgc'],
            'takefocus': False
        }
        text = file_data.lang['main_buttons']
        self.widgets['search_btn'] = Button(text=text['search'], width=15, takefocus=False)
        self.widgets['opt_btn'] = Button(text=text['options'], width=8, bd=1, pady=0, **options)
        self.widgets['gen_btn'] = Button(text=text['generate'], bd=1, pady=0, **options)
        self.widgets['add_btn'] = Button(text=text['add'], width=48, **options)
        self.widgets['clear_btn'] = Button(text=text['clear'], width=10, **options)

    def _define_radio_buttons(self):
        """Defines Radio Buttons"""
        self.tk_vars['radio_val'] = StringVar(value='1')
        common = {
            'font': FONT_C,
            'variable': self.tk_vars['radio_val'],
            'indicator': 0,
            'background': data.colors['bgc'],
            'foreground': data.colors['fgc'],
            'activebackground': data.colors['details2'],
            'command': self.upd_radio
        }
        self.widgets['radio1'] = Radiobutton(
            text=file_data.lang['main_radiobuttons']['radio1'], value=1, **common)
        self.widgets['radio2'] = Radiobutton(
            text=file_data.lang['main_radiobuttons']['radio2'], value=2, **common)
        self.widgets['radio3'] = Radiobutton(
            text=file_data.lang['main_radiobuttons']['radio3'], value=3, **common)
        self.widgets['radio4'] = Radiobutton(
            text=file_data.lang['main_radiobuttons']['radio4'], value=4, **common)

    def _define_checkboxes(self):
        """Defines Checkbox Buttons"""
        self.widgets['check_fixed'] = IntVar(value=0)
        self.widgets['fixed_length'] = Checkbutton(
            variable=self.widgets['check_fixed'],
            background=data.colors['accent'],
            foreground=data.colors['fgc'],
            activebackground=data.colors['accent'],
            selectcolor=data.colors['details2'],
            command=self.__define_spinbox_state
        )

    def __define_spinbox_state(self):
        if self.widgets['check_fixed'].get() == 1:
            self.widgets['char_spinbox'].config(state='readonly')
        else:
            self.widgets['char_spinbox'].config(state='disabled')

    def _define_combobox_style(self):
        """Defines a style for Comboboxes and Sizegrips"""
        self.ttk_styles['combostyle'] = Style()
        self.ttk_styles['combostyle'].theme_create(
            'combostyle',
            parent='alt',
            settings={
                'TCombobox': {
                    'configure': {
                        'selectbackground': data.colors['bgc'],
                        'fieldbackground': data.colors['details2'],
                        'background': data.colors['bgc'],
                        'arrowcolor': data.colors['details1'],
                        'arrowsize': 15,
                        'postoffset': (0, 0, 0, 0),
                        'padding': 0
                    },
                    'map': {
                        'background': [
                            ('active',  data.colors['accent']),
                            ('pressed', data.colors['details2']),
                            # ('!disabled', data.colors['accent']) # Arrow Button BG color
                        ],
                        'fieldbackground' : [('!disabled', data.colors['details2'])],
                    #     "foreground": [
                    #         ("focus", "red"), # Text when Combobox is focused
                    #         ("!disabled", "blue") # Text in combobox
                    #     ]
                    }
                },
                'TSizegrip': {
                    'configure': {
                        'background': data.colors['accent']
                    }
                }
            }
        )

        # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        self.ttk_styles['combostyle'].theme_use('combostyle')

        self.option_add('*TCombobox*Listbox.font', FONT_A)
        self.option_add('*TCombobox*Listbox.background', data.colors['bgc'])
        self.option_add('*TCombobox*Listbox.foreground', data.colors['fgc'])
        self.option_add('*TCombobox*Listbox.selectBackground', data.colors['accent'])
        self.option_add('*TCombobox*Listbox.selectForeground', data.colors['details1'])
        self.option_add('*TCombobox*Listbox.highlightThickness', 0)
        self.option_add('*TCombobox*Listbox.borderWidth', 0)

    def _define_comboboxes(self):
        """Defines Comboboxes"""
        self.tk_vars['emails_var'] = StringVar()
        self.widgets['email_combo'] = Combobox(
            self,
            font=FONT_A,
            width=39,
            height=5,
            textvariable=self.tk_vars['emails_var'],
            postcommand=self.update_emails
        )
        self.fields_to_refresh['email_combo'] = self.widgets['email_combo']

    def _define_listboxes(self):
        """Defines Listboxes"""
        self.widgets['autocomplete_box'] = Listbox(
            font=FONT_A,
            foreground=data.colors['details1'],
            background=data.colors['bgc'],
            border=0,
            width=29,
            height=1,
            selectbackground=data.colors['accent'],
            selectmode=SINGLE,
            takefocus=0,
            exportselection=0,
            cursor='hand2'
        )

    def _define_sizegrip(self):
        """Defines Sizegrips"""
        self.widgets['sizegrip'] = Sizegrip()

    def _define_language_controls(self):
        """Define and draw all widgets related to the Language controls for the main window"""
        self.widgets['lang_frame'] = Frame(self, bg=data.colors['accent'])
        self.widgets['lang_btn'] = Button(
            master=self,
            text="English",
            font=FONT_E,
            border=0,
            background=data.colors['bgc'],
            foreground=data.colors['details1'],
            takefocus=0,
            cursor='hand2',
            activebackground=data.colors['bgc'],
            highlightthickness=0,
            relief=SUNKEN,
            activeforeground=data.colors['details2'],
            image=self.widgets['language_flags']['english'],
            compound=LEFT,
            command=self.__toggle_language_buttons
        )
        self.widgets['lang_btn'].place(y=10, anchor=NE)

        # Get the .json files in the lang folder. Assign the corresponding icons to them.
        langs = [os.path.splitext(lng.name)[0].title()
                for lng in os.scandir(LANGUAGES_DIR) if lng.name.endswith('.json')]
        self.widgets['lang_opts'] = []

        # Create a new button for every language. Put every new button below the previous one.
        for index, lng in enumerate(langs):
            btn = Button(
                master=self.widgets['lang_frame'],
                text=lng,
                font=FONT_E,
                border=0,
                background=data.colors['accent'],
                foreground=data.colors['details1'],
                takefocus=0,
                cursor='hand2',
                activebackground=data.colors['details2'],
                highlightthickness=0,
                relief=SUNKEN,
                activeforeground=data.colors['details1'],
                image=self.widgets['language_flags'][lng.lower()],
                compound=LEFT,
                command=lambda lng=lng: self.choose_language(lng)
            )
            if index == 0:
                btn.place(anchor=NW, x=0, y=0)
            else:
                btn.place(anchor=NW, x=0, y=pos)
            btn.update()
            pos = btn.winfo_y() + btn.winfo_height()
            self.widgets['lang_opts'].append(btn)

        # Set the width of the whole dropdown window to be as the widest child button + 2px
        self.widgets['lang_frame'].config(
            width=max(btn.winfo_width() for btn in self.widgets['lang_opts']) + 2,
            height=25 * len(langs)
        )

    def __toggle_language_buttons(self):
        posx = self.widgets['lang_btn'].winfo_x()
        width = self.widgets['lang_btn'].winfo_width()
        if not self.widgets['lang_frame'].winfo_ismapped():
            self.widgets['lang_frame'].place(anchor=NE, x=posx + width, y=35)
        else:
            self.widgets['lang_frame'].place_forget()

    def _draw_canvas(self):
        """Draws the main window's canvas and the logo on it"""
        self.widgets['canvas'].create_image(100, 100, image=self.icons['logo'])
        self.widgets['canvas'].place(relx=0.5, y=25, anchor=N)

    def _draw_menu_bar(self):
        """Draw the Menu Bar with all sub-menus"""
        self.config(menu=self.widgets['menubar'])

        self.widgets['menubar'].add_cascade(
            label=file_data.lang['main_menu']['file'], menu=self.widgets['file_menu'])
        self.widgets['menubar'].add_cascade(
            label=file_data.lang['main_menu']['edit'], menu=self.widgets['edit_menu'])
        self.widgets['menubar'].add_cascade(
            label=file_data.lang['main_menu']['settings'], menu=self.widgets['settings_menu'])
        self.widgets['settings_menu'].add_cascade(
            label=file_data.lang['main_menu']['themes'],
            menu=self.widgets['color_menu'],
            image=self.icons['themes_icon'],
            compound=LEFT
        )
        self.widgets['settings_menu'].add_cascade(
            label=file_data.lang['main_menu']['backup_period'],
            menu=self.widgets['backup_menu'],
            image=self.icons['backup_icon'],
            compound=LEFT
        )
        self.widgets['settings_menu'].add_command(
            label=file_data.lang['main_menu']['settings_menu'],
            command=lambda: CustomizationSettings(self.tk_vars, self.fields_to_refresh),
            image=self.icons['settings_icon'],
            compound=LEFT
        )

    def _define_edit_commands(self):
        """Define the Copy, Paste and Cut commands for the Edit menu and the right click menu"""
        self.widgets['r_click_popup'].add_command(
            label=file_data.lang['main_menu']['copy'],
            command=lambda: self.focus_get().event_generate(('<<Copy>>')),
            image=self.icons['copy_icon'],
            compound=LEFT
        )
        self.widgets['r_click_popup'].add_command(
            label=file_data.lang['main_menu']['paste'],
            command=lambda: self.focus_get().event_generate(('<<Paste>>')),
            image=self.icons['paste_icon'],
            compound=LEFT
        )
        self.widgets['r_click_popup'].add_command(
            label=file_data.lang['main_menu']['cut'],
            command=lambda: self.focus_get().event_generate(('<<Cut>>')),
            image=self.icons['cut_icon'],
            compound=LEFT
        )
        self.widgets['edit_menu'].add_command(
            label=file_data.lang['main_menu']['copy'],
            command=lambda: self.focus_get().event_generate(('<<Copy>>')),
            image=self.icons['copy_icon'],
            compound=LEFT
        )
        self.widgets['edit_menu'].add_command(
            label=file_data.lang['main_menu']['paste'],
            command=lambda: self.focus_get().event_generate(('<<Paste>>')),
            image=self.icons['paste_icon'],
            compound=LEFT
        )
        self.widgets['edit_menu'].add_command(
            label=file_data.lang['main_menu']['cut'],
            command=lambda: self.focus_get().event_generate(('<<Cut>>')),
            image=self.icons['cut_icon'],
            compound=LEFT
        )

    def _populate_backups(self):
        """Populate the "Recover from backup" menu"""
        if os.path.exists(BACKUPS_PATH):
            for backup in os.scandir(BACKUPS_PATH):
                if backup.name.startswith("pmd"):
                    label = datetime.strptime(backup.name[6:-5], WORD_FORMAT).strftime(
                        f"{file_data.lang['main_menu']['backup_label_date']}: {DIGIT_FORMAT}")
                    self.widgets['backups_menu'].add_command(
                        label=label, command=lambda backup=backup: recover_from_backup(backup))

    def _draw_frames(self):
        """Draws the frame for the Status Bar"""
        self.widgets['status_bar'].place(relx=0, rely=1, relwidth=1, anchor=SW)

    def _draw_labels(self):
        """Draws the Labels"""
        status_wid = self.widgets['status_bar'].winfo_width()
        self.widgets['website_label'].place(x=160, y=255, anchor=E)
        self.widgets['user_label'].place(x=160, y=295, anchor=E)
        self.widgets['email_label'].place(x=160, y=335, anchor=E)
        self.widgets['password_label'].place(x=160, y=375, anchor=E)
        self.widgets['status_entries'].place(x=10, rely=1, anchor=SW)
        self.widgets['countdown_label'].place(x=status_wid - 20, rely=1, anchor=SE)

    def _draw_entry_boxes(self):
        """Draws the Entry boxes"""
        self.widgets['website_entry'].place(anchor=W)
        self.widgets['user_entry'].place(anchor=W)
        height = self.widgets['user_entry'].winfo_reqheight()
        self.widgets['password_entry'].place(anchor=W, height=height)

    def _draw_buttons(self):
        """Draws the Buttons"""
        self.widgets['search_btn'].place(anchor=W)
        self.widgets['opt_btn'].place(x=727, height=32, anchor=E)
        self.widgets['add_btn'].place(y=415, anchor=W)
        self.widgets['clear_btn'].place(y=415, anchor=E)

    def _draw_sizegrip(self):
        """Draws the Sizegrip"""
        self.widgets['sizegrip'].place(relx=1, rely=1, anchor=SE)

    def _draw_comboboxes(self):
        """Draws the Combo boxes"""
        self.widgets['email_combo'].place(anchor=W)

    def update_emails(self):
        """Updates the email list for the combobox geting all emails in the current account"""
        acc_emails = {i[0] for i in data.get_db_data('entries', 'email', single=False)}
        account_emails = [decipher(i) for i in acc_emails]
        self.widgets['email_combo']['values'] = account_emails

    def upd_radio(self):
        """Updates the colors of the radio buttons when one is clicked.
        Also updates spinboxes character limits and defaults"""
        raise NotImplementedError

    def choose_language(self, lng: str):
        """Update all widgets with the selected language.

        Args:
            lng (str): The language that the user chose
        """
        raise NotImplementedError
