"""The Authentication window for Password Manager"""

import os
from tkinter import (Label, Button, Checkbutton, Entry, Canvas, PhotoImage, Frame, IntVar,
                     N, E, W, NE, NW, LEFT, CENTER, SUNKEN)

from password_manager.data_management.all_data import file_data, data
from password_manager.constants import (SKY_BLUE, FONT_B, FONT_C, FONT_D, FONT_E, LANGUAGES_DIR,
                                        ICONS_DIR)
from password_manager.security.authenticate import is_login_valid
from password_manager.widgets import PWDEntry
from password_manager.ui import start_program
from password_manager.ui.base_ui import Window
from . import field_clear, eye_switch_color
#+ pylint: disable=unused-argument, undefined-variable


class LoginBase(Window):
    """Base class for the login window"""

    def __init__(self):
        super().__init__(root=data.wins['root'])

        self.setup(width=450, height=380)
        self.define_icons()
        self.draw_ui()
        self.password_error = False

    def setup(self, width, height):
        """Create and set up the login window"""
        super().setup(width=width, height=height)
        self.title(file_data.lang['login']['auth_title'])
        data.wins['login'] = self

        # Upon exiting this window terminate the whole application
        self.protocol('WM_DELETE_WINDOW', self.root.quit)
        self.resizable(False, False)

        # Ensure the application will be on focus on startup
        self.grab_set()
        self.grab_release()

        # Make it always on top of other applications. Only valid for login window
        self.attributes('-topmost', True)

    def define_ui(self):
        """Defines the UI widgets for the Authentication window"""
        self._define_canvas()
        self._collect_language_icons()
        self._define_labels()
        self._define_entry_boxes()
        self._define_frames()
        self._define_checkboxes()
        self._define_buttons()
        self._define_language_controls()

    def draw_ui(self):
        """Draws the UI for the Authentication window"""
        self.define_ui()
        self._draw_canvas()
        self._draw_frames()
        self._draw_labels()
        self._draw_entry_boxes()
        self._draw_checkboxes()
        self._draw_buttons()

    def _define_canvas(self):
        """Defines the authentication window's canvas for the logo"""
        self.widgets['auth_canvas'] = Canvas(
            master=self,
            height=200,
            width=200,
            background=data.colors['bgc'],
            highlightthickness=0
        )

    def _collect_language_icons(self):
        """Create an image object for every language in the lang directory"""
        self.widgets['language_flags'] = {}
        for lng in os.scandir(LANGUAGES_DIR):
            if lng.name.endswith('.json'):
                lng_name = ''.join(os.path.splitext(lng.name)[:-1])
                self.widgets['language_flags'][lng_name] = PhotoImage(
                    file=f"{os.path.join(ICONS_DIR, lng_name)}.png")

    def _define_frames(self):
        """Defines the separators between the icons and the entry boxes"""
        self.widgets['sep1'] = Frame(self, bg=data.colors['bgc'], width=2, height=28, bd=0)
        self.widgets['sep2'] = Frame(self, bg=data.colors['bgc'], width=2, height=28, bd=0)

    def _define_labels(self):
        """Defines Labels"""
        common = {'master': self, 'background': data.colors['details2'], 'border': 0}

        self.widgets['auth_text'] = Label(
            self,
            text=file_data.lang['login']['auth_text'],
            background=data.colors['bgc'],
            foreground=data.colors['details1'],
            font=FONT_B
        )
        self.widgets['user_icon_bg'] = Label(
            **common, width=38, height=31, image=self.icons['user_icon'])
        self.widgets['pass_icon_bg'] = Label(
            **common, width=38, height=31, image=self.icons['pass_icon'])

    def _define_entry_boxes(self):
        """Defines Entry boxes"""
        common = {
            'master': self,
            'font': FONT_D,
            'background': data.colors['details2'],
            'border': 0
        }
        self.widgets['log_entry_user'] = Entry(**common, foreground=data.colors['fgc'])
        self.widgets['log_entry_pass'] = PWDEntry(
            **common, foreground=data.colors['bgc'], image=self.icons['no_eye_icon'])

    def _define_buttons(self):
        """Defines Buttons"""
        self.widgets['enter_btn'] = Button(
            self,
            text=file_data.lang['login']['signin'],
            width=15,
            font=FONT_C,
            background=data.colors['bgc'],
            foreground=data.colors['details1'],
            takefocus=0
        )
        self.widgets['create_btn'] = Button(
            self,
            text=file_data.lang['login']['signup'],
            font=FONT_E,
            border=0,
            background=data.colors['bgc'],
            foreground="#61adff",
            highlightcolor=data.colors['bgc'],
            highlightbackground=data.colors['bgc'],
            activebackground=data.colors['bgc'],
            highlightthickness=0,
            relief='sunken',
            activeforeground=data.colors['details2'],
            cursor='hand2',
            takefocus=0
        )

    def _define_checkboxes(self):
        """Defines Checkboxes"""
        self.widgets['keep_lang'] = IntVar(value=1)
        self.widgets['check_keep_lang'] = Checkbutton(
            self,
            text=file_data.lang['keep_language'],
            variable=self.widgets['keep_lang'],
            background=data.colors['bgc'],
            foreground=data.colors['details1'],
            activebackground=data.colors['bgc'],
            activeforeground=data.colors['details1'],
            selectcolor=data.colors['accent'],
            takefocus=0
        )

    def _draw_canvas(self):
        """Draws the login window's canvas and the logo on it"""
        self.widgets['auth_canvas'].create_image(100, 100, image=self.icons['logo2'])
        self.widgets['auth_canvas'].place(relx=0.5, y=0, anchor=N)

    def _draw_frames(self):
        """Draws the separators between the icons and the entry boxes"""
        self.widgets['sep1'].place(x=85, y=245, anchor=E)
        self.widgets['sep2'].place(x=85, y=285, anchor=E)

    def _draw_labels(self):
        """Draws the Labels"""
        self.widgets['auth_text'].place(relx=0.5, y=200, anchor=CENTER)
        self.widgets['user_icon_bg'].place(x=50, y=245, anchor=W)
        self.widgets['pass_icon_bg'].place(x=50, y=285, anchor=W)

    def _draw_entry_boxes(self):
        """Draws the Entry boxes"""
        self.widgets['log_entry_user'].place(x=88, y=245, width=312, anchor=W)
        self.widgets['log_entry_user'].focus()
        self.widgets['log_entry_user'].update()
        width = self.widgets['log_entry_user'].winfo_width()
        height = self.widgets['log_entry_user'].winfo_height()
        self.widgets['log_entry_pass'].place(x=88, y=285, width=width, height=height, anchor=W)
        self.widgets['log_entry_pass'].entry.insert(
            0, file_data.lang['login']['log_entry_pass'])

    def _draw_checkboxes(self):
        """Draws the Checkboxes"""
        self.widgets['check_keep_lang'].place(relx=0.05, y=40, anchor=NW)

    def _draw_buttons(self):
        """Draws the Buttons"""
        self.widgets['enter_btn'].place(relx=0.5, y=340, anchor=CENTER)
        self.widgets['create_btn'].place(relx=0.95, y=10, anchor=NE)

    def _define_language_controls(self):
        """Define and draw all Language controls widgets for the login window"""
        self.widgets['lang_frame'] = Frame(self, background=data.colors['details2'])
        curr_lang = file_data.main_settings['language']
        self.widgets['lang_btn'] = Button(
            self,
            text=curr_lang.capitalize(),
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
            image=self.widgets['language_flags'][curr_lang.lower()],
            compound=LEFT,
            command=lambda: self.widgets['lang_frame'].place(relx=0.05, y=35, anchor=NW)
                            if not self.widgets['lang_frame'].winfo_ismapped()
                            else self.widgets['lang_frame'].place_forget()
        )
        self.widgets['lang_btn'].place(relx=0.05, y=10, anchor=NW)

        # Get the .json files in the lang folder. Assign the corresponding icons to them.
        langs = [os.path.splitext(lng.name)[0].title() for lng in os.scandir(LANGUAGES_DIR)
                                                if lng.name.endswith('.json')]
        self.widgets['lang_opts'] = []

        # Create a new button for every language. Put every new button below the previous one.
        for index, lng in enumerate(langs):
            self.widgets['lng_btn' + str(index)] = Button(
                self.widgets['lang_frame'],
                text=lng,
                font=FONT_E,
                border=0,
                background=data.colors['details2'],
                foreground=data.colors['bgc'],
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
                self.widgets['lng_btn' + str(index)].place(x=0, y=0, anchor=NW)
            else:
                self.widgets['lng_btn' + str(index)].place(x=0, y=pos, anchor=NW)
            self.widgets['lng_btn' + str(index)].update()
            pos=self.widgets[
                'lng_btn' + str(index)].winfo_y() + \
                self.widgets['lng_btn' + str(index)].winfo_height()
            self.widgets['lang_opts'].append(self.widgets['lng_btn' + str(index)])

        # Set the width of the whole dropdown window to be as the widest child button + 2px
        self.widgets['lang_frame'].config(
            width=max(btn.winfo_width() for btn in self.widgets['lang_opts']) + 2,
            height=25 * len(langs)
        )

    def _execute_bindings(self):
        """Sets binding to mouse and keyboard events"""
        log_widgets = self.widgets['log_entry_user'], self.widgets['log_entry_pass'].entry
        self.widgets['create_btn'].bind(
            '<Enter>', lambda event: self.widgets['create_btn'].config(fg=data.colors['details1']))
        self.widgets['create_btn'].bind(
            '<Leave>', lambda event: self.widgets['create_btn'].config(fg=SKY_BLUE))
        self.widgets['log_entry_pass'].entry.bind(
            '<FocusIn>', lambda event: field_clear(event, log_widgets))
        self.widgets['log_entry_pass'].entry.bind(
            '<FocusOut>', lambda event: field_clear(event, log_widgets))
        self.widgets['log_entry_user'].bind(
            '<FocusIn>', lambda event: field_clear(event, log_widgets))
        self.widgets['log_entry_user'].bind(
            '<FocusOut>', lambda event: field_clear(event, log_widgets))
        self.bind(
            '<Button-1>', lambda event: self.focus() if event.widget not in log_widgets else ""
        )

        common_icons = {
            'show': self.icons['eye_icon'],
            'show_hover': self.icons['eye_icon_h'],
            'hide': self.icons['no_eye_icon'],
            'hide_hover': self.icons['no_eye_icon_h']
        }

        self.widgets['log_entry_pass'].btn.bind(
            '<Enter>', lambda event: eye_switch_color(event, common_icons))
        self.widgets['log_entry_pass'].btn.bind(
            '<Leave>', lambda event: eye_switch_color(event, common_icons))
        self.bind(
            '<ButtonRelease-1>', lambda event: self.widgets['lang_frame'].place_forget()
                if event.widget not in self.widgets['lang_opts'] +
                [self.widgets['lang_frame'], self.widgets['lang_btn']] else ""
        )
        self.bind(
            '<Return>',
            lambda event: start_program()
                if is_login_valid(self.widgets['log_entry_user'], self.widgets['log_entry_pass'])
                    else self._run_wrong_password_sequence()
        )

    def _run_wrong_password_sequence(self):
        """Display wrong password error message deleting the wrong password"""
        raise NotImplementedError

    def choose_language(self, lng: str):
        """Update all widgets with the selected language.

        Args:
            lng (str): The language that the user chose
        """
        raise NotImplementedError
