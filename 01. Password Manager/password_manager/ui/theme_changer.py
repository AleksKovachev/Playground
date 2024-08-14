"""This module contains the class responsible for the changing the themes of the application"""

import sqlite3
from tkinter import Label, Button, E, W, RIDGE
from tkinter.colorchooser import askcolor
from enum import Enum

from password_manager.constants import (
    FONT_A, BLACK, WHITE, LIGHT_GRAY, MED_DARK_GRAY, MED_GRAY, DATA)
from password_manager.data_management.all_data import data, file_data
from password_manager.ui.base_ui import Window


class Element(Enum):
    """Defines the element type for changing colors"""
    BG = 1
    FG = 2
    ACCENT = 3
    DETAILS1 = 4
    DETAILS2 = 5
    RESET = 6


class ThemeChanger(Window):
    """The UI for the ThemeChanger window"""

    def __init__(self):
        super().__init__(root=data.wins['root'])

        self.setup(width=250, height=250)
        self.create_content()

    def setup(self, width, height):
        """Create and set up the ThemeChanger window"""
        super().setup(width=width, height=height)
        self.title(file_data.lang['theme_changer']['title'])

        # Make this window appear at the center of the main window
        self.resizable(False, False)
        self.config(background=data.colors['bgc'], pady=10, padx=10)

        # Make the main window unclickable until this one is closed
        self.grab_set()

        # Make it a tool window (only X button)
        self.attributes('-toolwindow', True)

    def create_content(self):
        """Creates the UI of the ThemeChanger window"""
        text = file_data.lang['theme_changer']
        common = {
            'master'    : self,
            'font'      : FONT_A,
            'background': data.colors['bgc'],
            'foreground': data.colors['details1']
        }
        self.widgets['bg_label']       = Label(text=text['bg_label'], **common)
        self.widgets['fg_label']       = Label(text=text['fg_label'], **common)
        self.widgets['accent_label']   = Label(text=text['accent_label'], **common)
        self.widgets['details1_label'] = Label(text=text['details1_label'], **common)
        self.widgets['details2_label'] = Label(text=text['details2_label'], **common)
        self.widgets['bg_label'].place(      relx=0, rely=0.15, anchor=W)
        self.widgets['fg_label'].place(      relx=0, rely=0.3,  anchor=W)
        self.widgets['accent_label'].place(  relx=0, rely=0.45, anchor=W)
        self.widgets['details1_label'].place(relx=0, rely=0.6,  anchor=W)
        self.widgets['details2_label'].place(relx=0, rely=0.75, anchor=W)

        common = {'master': self, 'width' : 5, 'border': 2, 'cursor': 'hand2', 'relief': RIDGE}

        self.widgets['bg_btn'] = Button(
            background=data.colors['bgc'],
            activebackground=data.colors['bgc'],
            command=lambda: self.process_color(Element.BG),
            **common
        )
        self.widgets['fg_btn'] = Button(
            background=data.colors['fgc'],
            activebackground=data.colors['fgc'],
            command=lambda: self.process_color(Element.FG),
            **common
        )
        self.widgets['accent_btn'] = Button(
            background=data.colors['accent'],
            activebackground=data.colors['accent'],
            command=lambda: self.process_color(Element.ACCENT),
            **common
        )
        self.widgets['details1_btn'] = Button(
            background=data.colors['details1'],
            activebackground=data.colors['details1'],
            command=lambda: self.process_color(Element.DETAILS1),
            **common
        )
        self.widgets['details2_btn'] = Button(
            background=data.colors['details2'],
            activebackground=data.colors['details2'],
            command=lambda: self.process_color(Element.DETAILS2),
            **common
        )
        self.widgets['reset_btn'] = Button(
            self,
            text=file_data.lang['theme_changer']['reset_btn'],
            background=data.colors['bgc'],
            fg=data.colors['details1'],
            command=lambda: self.process_color(Element.RESET)
        )
        self.widgets['bg_btn'].place(      relx=0.9, rely=0.15, anchor=E)
        self.widgets['fg_btn'].place(      relx=0.9, rely=0.3,  anchor=E)
        self.widgets['accent_btn'].place(  relx=0.9, rely=0.45, anchor=E)
        self.widgets['details1_btn'].place(relx=0.9, rely=0.6,  anchor=E)
        self.widgets['details2_btn'].place(relx=0.9, rely=0.75, anchor=E)
        self.widgets['reset_btn'].place(   relx=1,   rely=0.9,  anchor=E)

    def update_theme(self):
        """Updates the theme of the ThemeChanger window"""
        self.config(bg=data.colors['bgc'])
        self.widgets['bg_label'].config(      bg=data.colors['bgc'], fg=data.colors['details1'])
        self.widgets['fg_label'].config(      bg=data.colors['bgc'], fg=data.colors['details1'])
        self.widgets['accent_label'].config(  bg=data.colors['bgc'], fg=data.colors['details1'])
        self.widgets['details1_label'].config(bg=data.colors['bgc'], fg=data.colors['details1'])
        self.widgets['details2_label'].config(bg=data.colors['bgc'], fg=data.colors['details1'])
        self.widgets['reset_btn'].config(     bg=data.colors['bgc'], fg=data.colors['details1'])
        self.widgets['bg_btn'].config(bg=data.colors['bgc'], activebackground=data.colors['bgc'])
        self.widgets['fg_btn'].config(bg=data.colors['fgc'], activebackground=data.colors['fgc'])
        self.widgets['accent_btn'].config(
            bg=data.colors['accent'], activebackground=data.colors['accent'])
        self.widgets['details1_btn'].config(
            bg=data.colors['details1'], activebackground=data.colors['details1'])
        self.widgets['details2_btn'].config(
            bg=data.colors['details2'], activebackground=data.colors['details2'])

    def process_color(self, element: Element):
        """Processes a color to update the theme with it

        Args:
            element (Element): Used to check which button was clicked
        """
        if element != Element.RESET:
            # Get the color chooser window
            element_color = askcolor(title=file_data.lang['theme_changer']['element_color'])

            color_data = {
                Element.BG.name      : data.colors['bgc'],
                Element.FG.name      : data.colors['fgc'],
                Element.ACCENT.name  : data.colors['accent'],
                Element.DETAILS1.name: data.colors['details1'],
                Element.DETAILS2.name: data.colors['details2'],
            }
        else:
            # Default Element.colors.name for when Reset button is clicked
            color_data = {
                Element.BG.name      : MED_GRAY,
                Element.FG.name      : BLACK,
                Element.ACCENT.name  : MED_DARK_GRAY,
                Element.DETAILS1.name: WHITE,
                Element.DETAILS2.name: LIGHT_GRAY,
            }

        if element != Element.RESET:
            # Get the HEX color
            if not element_color[1]:
                return
            color_data[element.name] = element_color[1]

        with sqlite3.connect(DATA) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE themes SET bg = ?, fg = ?, accent = ?, details1 = ?, details2 = ?
                WHERE id = ?""", (*color_data.values(), data.uid))

        # Update the colors of all widgets in the Theme Changer and the Main windows
        data.wins['root'].update_theme()
        self.update_theme()
