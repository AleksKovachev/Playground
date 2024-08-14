"""This module contains the class responsible for the main window UI"""

import random
import sqlite3
import string
from tkinter import END, LEFT, E, W, NW, NE, SE, DISABLED
from tkinter.messagebox import askyesno, showwarning
from enum import Enum

from password_manager import logout
from password_manager.data_management import get_median_color
from password_manager.data_management.all_data import data, file_data
from password_manager.constants import (MOTION, SCROLL_DELTA, WHITE, BLACK, LIGHT_THEME, DARK_THEME,
                                        NUM_BACKUPS, DELIMITERS, DATA, Overwrite)
from password_manager.ui.main_window_base import PasswordManagerBase
from password_manager.ui.data_io import import_data, export_data
from password_manager.word_generator import gen_adj_noun
from password_manager.security import gen_pass
from password_manager.security.encryption import cipher, decipher
from .theme_changer import ThemeChanger
from . import search_creds

#+ pylint: disable=unused-argument


class Theme(Enum):
    """Defines the default theme types"""
    LIGHT = 1
    DARK = 2


class PasswordManagerUI(PasswordManagerBase):
    """The main UI class for Password Manager"""

    def __init__(self):
        super().__init__()
        self._link_widgets()

    def _link_widgets(self):
        """Links widgets to the function they should execute"""
        self.widgets['gen_btn'].config(command=self.gen_pass)
        self.widgets['add_btn'].config(command=self.save_data)
        self.widgets['clear_btn'].config(command=self.clear_all)
        self.widgets['password_entry'].btn.config(command=self.show_pass)
        self.widgets['search_btn'].config(command=search_creds)
        self._build_menu()

    def _build_menu(self):
        """Builds the main menu bar functionality"""
        self.widgets['color_menu'].add_command(
            label=file_data.lang['light_theme'],
            command=lambda: self.theme_preset(Theme.LIGHT, data.autofils['user']),
            image=self.icons['light_icon'],
            compound=LEFT
        )
        self.widgets['color_menu'].add_command(
            label=file_data.lang['dark_theme'],
            command=lambda: self.theme_preset(Theme.DARK, data.autofils['user']),
            image=self.icons['dark_icon'],
            compound=LEFT
        )
        self.widgets['color_menu'].add_separator()
        self.widgets['color_menu'].add_command(
            label=file_data.lang['custom_theme'],
            command=ThemeChanger,
            image=self.icons['prefs_icon'],
            compound='left'
        )
        self.widgets['file_menu'].add_command(
            label=file_data.lang['button1'],
            command=lambda: search_creds(browse=True),
            image=self.icons['browse_icon'],
            compound='left'
        )
        self.widgets['file_menu'].add_separator()
        self.widgets['file_menu'].add_command(
            label=file_data.lang['button2'],
            command=import_data,
            image=self.icons['import_icon'],
            compound='left'
        )
        self.widgets['file_menu'].add_command(
            label=file_data.lang['button3'],
            command=export_data,
            image=self.icons['export_icon'],
            compound='left'
        )
        self.widgets['file_menu'].add_cascade(
            label=file_data.lang['button4'],
            menu=self.widgets['backups_menu'],
            image=self.icons['backup_icon'],
            compound='left'
        )
        self.widgets['file_menu'].add_separator()
        self.widgets['file_menu'].add_command(
            label=file_data.lang['button5'],
            command=logout,
            image=self.icons['logout_icon'],
            compound='left'
        )
        self.widgets['file_menu'].add_separator()
        self.widgets['file_menu'].add_command(
            label=file_data.lang['button6'],
            command=self.destroy,
            image=self.icons['exit_icon'],
            compound='left'
        )

    def choose_language(self, lng: str):
        """Update all widgets with the selected language.

        Args:
            lng (str): The language that the user chose
        """
        self.widgets['lang_btn'].config(text=lng, image=self.widgets['language_flags'][lng.lower()])
        data.set_db_data('settings', 'language', lng.lower())

        self.widgets['lang_frame'].place_forget()

        file_data.load_language(lng, parent=data.wins['root'])
        autoclose_text = file_data.lang['status_bar']['autoclose']
        self.tk_vars['countdown_var'].set(f"{autoclose_text} {data.autoclose['timer_st']}")
        self.update_language()

    def calc_widgets(self, event):
        """Recalculate widget placement and size.
        All "MAGIC" numbers below are either positions or paddings"""
        app_width = self.winfo_width()
        posx = 165
        row1_y = 255
        pad = {'entry': 230, 'btn': 6}

        self._update_language_menu(app_width)
        self._update_entry_boxes(app_width, posx, row1_y, pad)

        # Options frame
        if self.widgets['options_frame'].winfo_ismapped():
            self.widgets['options_frame'].place(
                x=posx, y=420, anchor=W, width=app_width - pad['entry'])

        self._update_buttons(app_width, posx, row1_y, pad['btn'])

        if self.widgets['autocomplete_box'].winfo_ismapped():
            web_entry_width = self.widgets['website_entry'].winfo_width()
            self.widgets['autocomplete_box'].place(x=posx, y=270, anchor=NW, width=web_entry_width)

        self._update_status_bar()

    def _update_language_menu(self, app_width):
        """Updates the Language menu size and position"""
        right_padding = 63
        self.widgets['lang_btn'].place(x=app_width - right_padding)
        if self.widgets['lang_frame'].winfo_ismapped():
            btn_posx = self.widgets['lang_btn'].winfo_x()
            btn_height = self.widgets['lang_btn'].winfo_width()
            self.widgets['lang_frame'].place(x=btn_posx + btn_height, anchor=NE)

    def _update_entry_boxes(self, app_width, posx, row1_y, pad):
        """Updates the Entry boxes size and position"""
        entry_max = app_width - pad['entry']
        opt_btn_wid = self.widgets['opt_btn'].winfo_width() + pad['btn']
        self.widgets['website_entry'].place(x=posx, y=row1_y, width=entry_max - 120)
        self.widgets['user_entry'].place(x=posx, y=row1_y + 40, width=entry_max)
        self.widgets['email_combo'].place(x=posx, y=row1_y + 80, width=entry_max)
        self.widgets['password_entry'].place(x=posx, y=row1_y + 120, width=entry_max - opt_btn_wid)

    def _update_buttons(self, app_width, posx, row1_y, btn_pad):
        """Updates the Buttons size and position"""
        srch_btn_posx = posx + self.widgets['website_entry'].winfo_width() + btn_pad

        self.widgets['search_btn'].place(x=srch_btn_posx, y=row1_y, height=34)
        self.widgets['opt_btn'].place(y=row1_y + 120, height=32)
        if self.widgets['gen_btn'].winfo_ismapped():
            self.widgets['gen_btn'].place(x=app_width - 70, anchor=E)
        self.widgets['add_btn'].place(x=posx, width=app_width - 335)
        self.widgets['clear_btn'].place(x=app_width - 63)

    def _update_status_bar(self):
        """Updates the Status bar elements size and position"""
        status_bar_width = self.widgets['status_bar'].winfo_width()
        if self.state() == 'zoomed':
            self.widgets['sizegrip'].place_forget()
            self.widgets['countdown_label'].place(x=status_bar_width)
        else:
            self.widgets['sizegrip'].place(relx=1, rely=1, anchor=SE)
            self.widgets['countdown_label'].place(x=status_bar_width - 15)

    def spinbox_controls(self, event):
        """Defines the Spinbox behaviour on Mouse scrolling and Mouse Click & Drag"""
        current_value = self._get_current_spinbox_value(event)
        self._define_spinbox_scroll_behavior(event, current_value)

        # If method was triggered with a Mouse Button click and Mouse Motion was detected
        if event.type == MOTION:
            self._define_spinbox_mouse_movement_behavior(event, current_value)

    def _get_current_spinbox_value(self, event):
        """Get the current value of the spinbox"""
        if event.widget == self.widgets['char_spinbox']:
            return self.tk_vars['pass_length'].get()
        return self.tk_vars['autoclose_mins'].get()

    def _define_spinbox_scroll_behavior(self, event, current_value):
        """Define +/- 1 to spinbox current value upon scroll Up/Down"""
        if (event.delta == SCROLL_DELTA
            and current_value < int(event.widget.cget('to'))
                and event.widget['state'] != 'disabled'):
            if event.widget == self.widgets['char_spinbox']:
                self.tk_vars['pass_length'].set(current_value + 1)
            else:
                self.update_autoclose(current_value, 1)

        elif (event.delta == -SCROLL_DELTA
                and current_value > int(event.widget.cget('from'))
                and event.widget['state'] != 'disabled'):
            if event.widget == self.widgets['char_spinbox']:
                self.tk_vars['pass_length'].set(current_value - 1)
            else:
                self.update_autoclose(current_value, -1)

    def _define_spinbox_mouse_movement_behavior(self, event, current_value):
        """Define +/- 1 to spinbox current value for every n pixels mouse move Up/Down on screen"""
        # We get -event.y because the value is inverted
        move_pixels = 25
        traveled_25pix_up = -event.y > data.spinbox_ypos + move_pixels
        traveled_25pix_down = -event.y < data.spinbox_ypos - move_pixels
        not_reached_max = current_value < int(event.widget.cget('to'))
        not_reached_min = current_value > int(event.widget.cget('from'))
        not_disabled = event.widget['state'] != DISABLED
        if traveled_25pix_up and not_reached_max and not_disabled:
            if event.widget == self.widgets['char_spinbox']:
                self.tk_vars['pass_length'].set(current_value + 1)
            else:
                self.update_autoclose(current_value, 1)
            data.spinbox_ypos = -event.y
        elif traveled_25pix_down and not_reached_min and not_disabled:
            if event.widget == self.widgets['char_spinbox']:
                self.tk_vars['pass_length'].set(current_value - 1)
            else:
                self.update_autoclose(current_value, -1)
            data.spinbox_ypos = -event.y

    def update_autoclose(self, curr_value, value):
        """Updates the autoclose minutes and the countdown timer

        Args:
            curr_value (int): The current value of the parameter
            value (int): How much to add to the timer (negative numbers subtract from it).
        """
        self.tk_vars['autoclose_mins'].set(curr_value + value)
        data.autoclose['cd_mins'] = curr_value + value
        data.autoclose['countdown'] = data.autoclose['cd_mins'] * 60

    def update_theme(self):
        """Updates the color for widgets to the current theme's color settings"""
        sett = data.get_db_data('themes', '*', single=False)[0]
        categories = ('bg', 'fg', 'accent', 'details1', 'details2')
        theme = dict(zip(categories, sett[1:]))

        data.colors['details1'] = theme['details1']
        data.colors['fgc'] = theme['fg']
        data.colors['bgc'] = theme['bg']
        data.colors['accent'] = theme['accent']
        data.colors['details2'] = theme['details2']
        data.colors['shadow'] = get_median_color(data.colors['accent'], data.colors['bgc'])

        self._update_menubar()
        self._update_canvas_frames_colors()
        self._update_label_colors()
        self._update_entry_box_colors()
        self._update_combobox_sizegrip_colors()
        self._update_spinbox_colors()
        self._update_button_colors()
        self._update_radio_button_colors()
        self._update_check_button_colors()
        self._update_listbox_colors()

    def _update_menubar(self):
        """Update the colors of the main menu widgets"""
        self.widgets['file_menu'].config(activebackground=data.colors['bgc'])
        self.widgets['edit_menu'].config(activebackground=data.colors['bgc'])
        self.widgets['settings_menu'].config(activebackground=data.colors['bgc'])
        self.widgets['lang_menu'].config(activebackground=data.colors['bgc'])

        self.widgets['backups_menu'].config(activebackground=data.colors['bgc'])
        self.widgets['prefs_menu'].config(activebackground=data.colors['bgc'])
        self.widgets['backup_menu'].config(activebackground=data.colors['bgc'])
        self.widgets['color_menu'].config(activebackground=data.colors['bgc'])
        self.widgets['r_click_popup'].config(activebackground=data.colors['bgc'])

    def _update_canvas_frames_colors(self):
        """Update the colors of the main Window, Canvas and the Frame widgets"""
        self.config(background=data.colors['bgc'])
        self.widgets['canvas'].config(background=data.colors['bgc'])
        self.widgets['options_frame'].config(background=data.colors['accent'])
        self.widgets['status_bar'].config(background=data.colors['accent'])
        self.widgets['lang_frame'].config(background=data.colors['accent'])

    def _update_label_colors(self):
        """Update the colors of the Label widgets"""
        self.widgets['website_label'].config(
            fg=data.colors['details1'], bg=data.colors['bgc'])
        self.widgets['user_label'].config(
            fg=data.colors['details1'], bg=data.colors['bgc'])
        self.widgets['email_label'].config(
            fg=data.colors['details1'], bg=data.colors['bgc'])
        self.widgets['password_label'].config(
            fg=data.colors['details1'], bg=data.colors['bgc'])
        self.widgets['password_length'].config(
            fg=data.colors['details1'], bg=data.colors['accent'])
        self.widgets['status_entries'].config(
            fg=data.colors['details1'], bg=data.colors['accent'])
        self.widgets['countdown_label'].config(
            fg=data.colors['details1'], bg=data.colors['accent'])

    def _update_entry_box_colors(self):
        """Update the colors of the Entry box widgets"""
        options = {
            'background': data.colors['details2'],
            'foreground': data.colors['fgc'],
            'selectbackground': data.colors['bgc']
        }
        self.widgets['website_entry'].config(**options)
        self.widgets['user_entry'].config(**options)
        self.widgets['password_entry'].config(**options)

    def _update_combobox_sizegrip_colors(self):
        """Update the colors of the Combobox and Sizegripwidgets"""
        self.ttk_styles['combostyle'].configure(
            'TCombobox',
            selectbackground=data.colors['bgc'],
            fieldbackground=data.colors['details2'],
            background=data.colors['bgc'],
            foreground=data.colors['fgc'],
            arrowcolor=data.colors['details1'],
            arrowsize=15,
            postoffset=(0, 0, 0, 0)
        )
        self.ttk_styles['combostyle'].map(
            'TCombobox',
            background=[
                ('active', data.colors['accent']),
                ('pressed', data.colors['details2']),
                # ('!disabled', data.colors['accent'])
            ],
            fieldbackground=[('!disabled', data.colors['details2'])]
        )
        self.ttk_styles['combostyle'].configure('TSizegrip', background=data.colors['accent'])
        self.option_add('*TCombobox*Listbox.background', data.colors['bgc'])
        self.option_add('*TCombobox*Listbox.foreground', data.colors['fgc'])
        self.option_add('*TCombobox*Listbox.selectBackground', data.colors['accent'])
        self.option_add('*TCombobox*Listbox.selectForeground', data.colors['details1'])
        self.tk.eval(f'[ttk::combobox::PopdownWindow {self.widgets["email_combo"]}]' \
                          f'.f.l configure -background {data.colors["bgc"]}')
        self.tk.eval(f'[ttk::combobox::PopdownWindow {self.widgets["email_combo"]}]' \
                          f'.f.l configure -selectbackground {data.colors["accent"]}')
        self.tk.eval(f'[ttk::combobox::PopdownWindow {self.widgets["email_combo"]}]' \
                          f'.f.l configure -selectforeground {data.colors["details1"]}')
        self.tk.eval(f'[ttk::combobox::PopdownWindow {self.widgets["email_combo"]}]' \
                          f'.f.l configure -foreground {data.colors["fgc"]}')

    def _update_spinbox_colors(self):
        """Update the colors of the Spinbox widgets"""
        self.widgets['char_spinbox'].config(
            foreground=data.colors['details1'],
            background=data.colors['bgc'],
            buttonbackground=data.colors['bgc'],
            selectbackground=data.colors['accent'],
            disabledbackground=get_median_color(data.colors['accent'], WHITE),
            readonlybackground=data.colors['bgc'],
            disabledforeground=get_median_color(data.colors['accent'], BLACK)
        )

    def _update_button_colors(self):
        """Update the colors of the Button widgets"""
        common = {
            'foreground': data.colors['details1'],
            'background': data.colors['bgc'],
            'activebackground': data.colors['details2']
        }
        self.widgets['gen_btn'].config(**common)
        self.widgets['search_btn'].config(**common)
        self.widgets['add_btn'].config(**common)
        self.widgets['clear_btn'].config(**common)

        if self.widgets['gen_btn'].winfo_ismapped():
            self.widgets['opt_btn'].config(
                foreground=data.colors['accent'],
                background=data.colors['details2'],
                activebackground=data.colors['details2'],
                command=self.manage_options_menu
            )
        else:
            self.widgets['opt_btn'].config(**common, command=self.manage_options_menu)
        self.widgets['password_entry'].btn.config(
            background=data.colors['details2'],
            highlightbackground=data.colors['details2'],
            highlightcolor=data.colors['details2'],
            activebackground=data.colors['details2']
        )
        self.widgets['lang_btn'].config(
            background=data.colors['bgc'],
            foreground=data.colors['details1'],
            activebackground=data.colors['bgc'],
            activeforeground=data.colors['details2']
        )
        for btn in self.widgets['lang_opts']:
            btn.config(
                background=data.colors['accent'],
                foreground=data.colors['details1'],
                activebackground=data.colors['details2'],
                activeforeground=data.colors['details1']
            )

    def _update_radio_button_colors(self):
        """Update the colors of the Radio button widgets"""
        common = {
            'background': data.colors['bgc'],
            'activebackground': data.colors['details2'],
            'selectcolor': data.colors['details2']
        }
        for ind, btn in enumerate((self.widgets['radio1'],
                                   self.widgets['radio2'],
                                   self.widgets['radio3'],
                                   self.widgets['radio4'])):
            if self.tk_vars['radio_val'].get() == str(ind + 1):
                btn.config(foreground=data.colors['fgc'], **common)
            else:
                btn.config(foreground=data.colors['details1'], **common)

    def _update_check_button_colors(self):
        """Update the colors of the Checkbox button widgets"""
        self.widgets['fixed_length'].config(
            background=data.colors['accent'],
            foreground=data.colors['fgc'],
            selectcolor=data.colors['details2'],
            activebackground=data.colors['accent'],
            activeforeground=data.colors['fgc']
        )

    def _update_listbox_colors(self):
        """Update the colors of the Listbox widgets"""
        self.widgets['autocomplete_box'].config(
            foreground=data.colors['details1'],
            background=data.colors['bgc'],
            selectbackground=data.colors['accent']
        )

    def theme_preset(self, mode: Theme, user: str):
        """Switches the app theme

        Args:
            mode (Theme): Defines the theme color mode
            user (str): The user who's theme will be changed
        """
        if mode == Theme.LIGHT:
            color_data = LIGHT_THEME
        elif mode == Theme.DARK:
            color_data = DARK_THEME

        with sqlite3.connect(DATA) as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE themes SET bg = ?, fg = ?, accent = ?, details1 = ?,
                details2 = ? WHERE id = ?""", (*color_data, data.uid))

        self.update_theme()

    def upd_radio(self):
        """Updates the colors of the radio buttons when one is clicked.
        Also updates spinboxes character limits and defaults"""
        common = {
            'background': data.colors['bgc'],
            'activebackground': data.colors['details2'],
            'selectcolor': data.colors['details2']
        }
        for ind, btn in enumerate((self.widgets['radio1'],
                                   self.widgets['radio2'],
                                   self.widgets['radio3'],
                                   self.widgets['radio4'])):
            if self.tk_vars['radio_val'].get() == str(ind + 1):
                btn.config(foreground=data.colors['fgc'], **common)
            else:
                btn.config(foreground=data.colors['details1'], **common)

        match self.tk_vars['radio_val'].get():
            case "1":
                self.widgets['char_spinbox'].config(from_=6)
                self.widgets['char_spinbox'].config(to=20)
                self.tk_vars['pass_length'].set(8)
            case "3":
                self.widgets['char_spinbox'].config(from_=8)
                self.widgets['char_spinbox'].config(to=30)
                self.tk_vars['pass_length'].set(15)
            case _:
                self.widgets['char_spinbox'].config(from_=12)
                self.widgets['char_spinbox'].config(to=35)
                self.tk_vars['pass_length'].set(15)

    def update_language(self, initial=False):
        """Updates all widgets that have text to reload it with the newly chosen language
        
        Args:
            initial (bool): If this is the first time this function executes since application start
        """
        self._update_menu_edit_lang()
        text = {
            'menu': file_data.lang['main_menu'],
            'labels': file_data.lang['main_labels'],
            'buttons': file_data.lang['main_buttons'],
            'radios': file_data.lang['main_radiobuttons']
        }

        # Update entries in File->Recover from backup
        for i in range(NUM_BACKUPS):
            backup = ' '.join(self.widgets['backups_menu'].entrycget(i, 'label').split()[1:])
            self.widgets['backups_menu'].entryconfig(
                i, label=f"{text['menu']['backup_label_date']}: {backup}")

        self.widgets['menubar'].entryconfig(1, label=text['menu']['file'])
        self.widgets['menubar'].entryconfig(2, label=text['menu']['edit'])
        self.widgets['menubar'].entryconfig(3, label=text['menu']['settings'])
        self.widgets['settings_menu'].entryconfig(0, label=text['menu']['themes'])
        self.widgets['settings_menu'].entryconfig(1, label=text['menu']['backup_period'])
        self.widgets['settings_menu'].entryconfig(2, label=text['menu']['settings_menu'])
        self.widgets['website_label'].config(text=text['labels']['website'])
        self.widgets['user_label'].config(text=text['labels']['user'])
        self.widgets['email_label'].config(text=text['labels']['email'])
        self.widgets['password_label'].config(text=text['labels']['password'])
        self.widgets['password_length'].config(text=text['labels']['password_length'])

        msg = file_data.lang['status_bar']['entries_num']
        entries_num = len(data.get_db_data('entries', 'platform', single=False))
        last_backup = data.get_db_data('backup', 'date')
        self.tk_vars['status_entries_num'].set(
            f"{msg[0]} {data.autofils['user']}! {msg[1]} {entries_num} {msg[2]} {last_backup}")

        self.widgets['search_btn'].config(text=text['buttons']['search'])
        self.widgets['opt_btn'].config(text=text['buttons']['options'])
        self.widgets['gen_btn'].config(text=text['buttons']['generate'])
        self.widgets['add_btn'].config(text=text['buttons']['add'])
        self.widgets['clear_btn'].config(text=text['buttons']['clear'])
        self.widgets['radio1'].configure(text=text['radios']['radio1'])
        self.widgets['radio2'].configure(text=text['radios']['radio2'])
        self.widgets['radio3'].configure(text=text['radios']['radio3'])
        self.widgets['radio4'].configure(text=text['radios']['radio4'])
        self.widgets['color_menu'].entryconfig(0, label=file_data.lang['light_theme'])
        self.widgets['color_menu'].entryconfig(1, label=file_data.lang['dark_theme'])
        self.widgets['color_menu'].entryconfig(3, label=file_data.lang['custom_theme'])
        self.widgets['backup_menu'].entryconfig(0, label=file_data.lang['backup_period'][0])
        self.widgets['backup_menu'].entryconfig(1, label=file_data.lang['backup_period'][1])
        self.widgets['backup_menu'].entryconfig(2, label=file_data.lang['backup_period'][2])
        self.widgets['backup_menu'].entryconfig(3, label=file_data.lang['backup_period'][3])
        self.widgets['backup_menu'].entryconfig(4, label=file_data.lang['backup_period'][4])

        self.widgets['file_menu'].entryconfig(0, label=file_data.lang['button1'])
        self.widgets['file_menu'].entryconfig(2, label=file_data.lang['button2'])
        self.widgets['file_menu'].entryconfig(3, label=file_data.lang['button3'])
        self.widgets['file_menu'].entryconfig(4, label=file_data.lang['button4'])
        self.widgets['file_menu'].entryconfig(6, label=file_data.lang['button5'])
        self.widgets['file_menu'].entryconfig(8, label=file_data.lang['button6'])

        if not initial and self.widgets['options_frame'].winfo_ismapped():
            self.manage_options_menu(update=True)

    def _update_menu_edit_lang(self):
        self.title(file_data.lang['main_title'])
        self.widgets['r_click_popup'].entryconfig(0, label=file_data.lang['main_menu']['copy'])
        self.widgets['r_click_popup'].entryconfig(1, label=file_data.lang['main_menu']['paste'])
        self.widgets['r_click_popup'].entryconfig(2, label=file_data.lang['main_menu']['cut'])
        self.widgets['edit_menu'].entryconfig(0, label=file_data.lang['main_menu']['copy'])
        self.widgets['edit_menu'].entryconfig(1, label=file_data.lang['main_menu']['paste'])
        self.widgets['edit_menu'].entryconfig(2, label=file_data.lang['main_menu']['cut'])

    def manage_options_menu(self, update=False):
        """Expands/Contracts the Options menu

        Args:
            update (bool, optional): Is the method is updating the opened menu? Defaults to False.
        """
        if self.widgets['options_frame'].winfo_ismapped() and not update:
            if int(self.geometry().split('x')[1].split('+')[0]) == 560:
                self.geometry(f'{self.geometry()[:3]}x510')
            self.widgets['opt_btn']['bg'] = data.colors['bgc']
            self.widgets['opt_btn']['fg'] = data.colors['details1']
            self.widgets['opt_btn']['bd'] = 1
            self.widgets['password_length'].place_forget()
            self.widgets['gen_btn'].place_forget()
            self.widgets['char_spinbox'].place_forget()
            self.widgets['radio1'].place_forget()
            self.widgets['radio2'].place_forget()
            self.widgets['radio3'].place_forget()
            self.widgets['radio4'].place_forget()
            self.widgets['options_frame'].place_forget()
            self.widgets['fixed_length'].place_forget()
            self.widgets['add_btn'].place(x=165, y=415, anchor=W, width=455)
            self.widgets['clear_btn'].place(x=727, y=415, anchor=E)

        else:
            if int(self.geometry().split('x')[1].split('+')[0]) < 600:
                self.geometry(f'{self.geometry()[:3]}x560')
            self.widgets['opt_btn']['bg'] = data.colors['details2']
            self.widgets['opt_btn']['fg'] = data.colors['accent']
            self.widgets['opt_btn']['bd'] = 0
            self.widgets['gen_btn'].place(x=720, y=420, anchor=E)
            self.widgets['radio1'].place(x=170, y=420, anchor=W)
            rad1_x = 170 + self.widgets['radio1'].winfo_reqwidth()
            self.widgets['radio2'].place(x=rad1_x, y=420, anchor=W)
            rad2_x = rad1_x + self.widgets['radio2'].winfo_reqwidth()
            self.widgets['radio3'].place(x=rad2_x, y=420, anchor=W)
            rad3_x = rad2_x + self.widgets['radio3'].winfo_reqwidth()
            self.widgets['radio4'].place(x=rad3_x, y=420, anchor=W)
            rad4_x = rad3_x + self.widgets['radio4'].winfo_reqwidth()
            self.widgets['fixed_length'].place(x=rad4_x + 8, y=420, anchor=W)
            fl_x = rad4_x + self.widgets['fixed_length'].winfo_reqwidth()
            self.widgets['password_length'].place(x=fl_x + 7, y=420, anchor=W)
            pl_x = fl_x + self.widgets['password_length'].winfo_reqwidth()
            self.widgets['char_spinbox'].place(x=pl_x + 7, y=420, anchor=W)
            self.widgets['options_frame'].place(
                x=165, y=420, anchor=W, width=self.winfo_width() - 230)
            self.widgets['add_btn'].place(x=165, y=467, anchor=W, width=455)
            self.widgets['clear_btn'].place(x=727, y=467, anchor=E)

    def gen_pass(self):
        """Generates a password based on the selected type"""
        # Chose a random delimiters
        delimiter = random.choice(DELIMITERS)

        # Define the total number of characters for the password
        if self.widgets['check_fixed'].get() == 1:
            total_chars = self.tk_vars['pass_length'].get()
        else:
            total_chars = random.randint(12, 35)

        # Check the prefered password type
        match self.tk_vars['radio_val'].get():
            # If "secure" is selected
            case "1":
                # Redefine the character range if Secure option was
                # chosen without specifying password length
                if self.widgets['check_fixed'].get() == 0:
                    total_chars = random.randint(6, 20)
                password = gen_pass(total_chars)
            # If "easy" is selected
            case "2":
                # Generate the phrase +/- a few characters
                password = gen_adj_noun(
                    minlen=total_chars - 7, maxlen=total_chars - 5, delimiter=delimiter)
                # Add random characters at the end for security until total_chars count is reached
                add_pass = [
                    random.choice((random.choice(string.ascii_letters),
                            random.choice(string.digits),
                            random.choice(string.punctuation))) for _ in range(total_chars - len(password) - 1)]
                random.shuffle(add_pass)
                # The final password is the generated phrase with random
                # delimiter + the same delimiter + shuffled random characters
                password += delimiter + ''.join(add_pass)
            # If combo is selected
            case "3":
                # Generate a "coded" version of a phrase. No additional characters in this mode.
                password = gen_adj_noun(
                    minlen=total_chars, maxlen=total_chars, coded=True, delimiter=delimiter)
            # If secure combo is selected
            case "4":
                # Generate a "coded" version of a phrase
                password = gen_adj_noun(
                    minlen=total_chars - 7, maxlen=total_chars - 5, coded=True, delimiter=delimiter)
                # Add random characters at the end for security until total_chars count is reached
                add_pass = [
                    random.choice((random.choice(string.ascii_letters),
                            random.choice(string.digits),
                            random.choice(string.punctuation))) for _ in range(total_chars - len(password))]
                random.shuffle(add_pass)
                # The final password is the generated phrase with random
                # delimiter + shuffled random characters
                password += ''.join(add_pass)

        # Auto-insert it into the password Entry box and copy to clipboard
        self.widgets['password_entry'].entry.delete(0, END)
        self.widgets['password_entry'].entry.insert(0, password)
        self.widgets['password_entry'].entry.clipboard_clear()
        self.widgets['password_entry'].entry.clipboard_append(password)

    def save_data(self, event=None):  # pylint: disable=unused-argument
        """Saves the data from the entry fields

        Args:
            *args (event): Used by tkinter binding. This method is used by a tkinter button as well
            as tkinter binding which is why "*args" is used instead of "event"
        """
        # Save the credentils to a dictionary
        data_ = {
            'user': self.widgets['user_entry'].get(),
            'email': self.widgets['email_combo'].get(),
            'pass': self.widgets['password_entry'].get(),
            'platform': self.widgets['website_entry'].get()
        }

        # Show error if any of the fields is empty
        if not all(data_.values()):
            msg = file_data.lang['messages']['fill_fields']
            showwarning(title=msg['title'], message=msg['text'], parent=data.wins['root'])
            return

        # Ask to overwrite data if platform with this name already exists
        msg = file_data.lang['messages']['overwrite']
        overwrite = Overwrite.NO_NEED

        for key in data.get_db_data('entries', 'platform', single=False):
            if key[0].lower() == data_['platform'].lower():
                overwrite_ = askyesno(msg['title'],
                    f"{msg['text'][0]} {data_['platform']}.\n{msg['text'][1]}",
                    parent=data.wins['root'])
                overwrite = Overwrite.YES if overwrite_ else Overwrite.NO

        # Display the credentials and a confirmation dialog
        msg = file_data.lang['messages']['creds_correct']
        if overwrite != Overwrite.NO and askyesno(title=data_['platform'],
            message=f"{msg[0]} {data_['email']}\n{msg[1]} "\
                f"{data_['user']}\n{msg[2]} {data_['pass']}\n\n{msg[3]}",
                parent=data.wins['root']):
            # Clear all fields, update the opened data and save the creds to disk.
            self.clear_all()
            email = cipher(data_['email'])
            pwd = cipher(data_['pass'])
            with sqlite3.connect(DATA) as conn:
                cursor = conn.cursor()
                if overwrite == Overwrite.YES:
                    query = """UPDATE entries SET user = ?, email = ?, password = ?
                        WHERE platform = ? AND id = ?"""
                elif overwrite == Overwrite.NO_NEED:
                    query = """INSERT INTO entries (user, email, password, platform, id) VALUES
                        (?, ?, ?, ?, ?)"""
                cursor.execute(query, (data_['user'], email, pwd, data_['platform'], data.uid))

    def clear_all(self):
        """Clears all entered creds and populates the default username and email"""
        self.widgets['website_entry'].delete(0, END)
        self.widgets['user_entry'].delete(0, END)
        self.widgets['user_entry'].insert(0, data.get_db_data('defaults', 'user'))
        self.widgets['password_entry'].entry.delete(0, END)
        self.widgets['email_combo'].delete(0, END)
        self.tk_vars['emails_var'].set(decipher(data.get_db_data('defaults', 'email')))
        self.widgets['website_entry'].focus()

    def show_pass(self):
        """Hides/Shows the password in the entry box"""
        # Switch icons
        if self.widgets['password_entry'].btn['image'] == str(self.icons['no_eye_icon_h']):
            self.widgets['password_entry'].btn['image'] = self.icons['eye_icon_h']
        elif self.widgets['password_entry'].btn['image'] == str(self.icons['eye_icon_h']):
            self.widgets['password_entry'].btn['image'] = self.icons['no_eye_icon_h']

        self.widgets['password_entry'].entry['show'] = \
            '✲' if self.widgets['password_entry'].entry['show'] == "" else ""
