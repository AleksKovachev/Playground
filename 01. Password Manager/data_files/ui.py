"""The main UI module for Password Manager"""

from tkinter import (Tk, Toplevel, Canvas, Frame, Menu, Label, Button, Radiobutton, Checkbutton, Entry, Spinbox, Listbox,
                    LabelFrame, PhotoImage, IntVar, StringVar, SINGLE)
from tkinter.colorchooser import askcolor
from tkinter.ttk import Combobox, Style, Sizegrip
from datetime import datetime
from os import scandir, getenv
from os.path import dirname, join, splitext, exists
from . import updates as ups


# ---------------------------- CONSTANTS --------------------------------------------- #


FONT_A = ("CorsicaMX-Regular", 18, "normal")
FONT_B = ("CorsicaMX-Book", 14, "normal")
FONT_C = ("CorsicaMX-Book", 12, "normal")
FONT_E = ('CorsicaMX-Normal', 12, 'normal')
FONT_F = ("CorsicaMX-Book", 10, "normal")


class PMUI:
    """The main UI class for Password Manager"""

    def __init__(self):
        # Create the main window with the following parameters
        self.root = Tk()
        self.root.withdraw()
        self.root.title(ups.data.pmui['main_title'])
        app_width = 790
        app_height = 510
        scr_wdt = self.root.winfo_screenwidth()
        scr_hgt = self.root.winfo_screenheight()
        self.root.geometry(f'{app_width}x{app_height}+{int(scr_wdt / 2 - app_width / 2)}+{int(scr_hgt / 2 - app_height)}')
        # Upon exit check the backup period and create a data backup if needed
        self.root.protocol('WM_DELETE_WINDOW', lambda: ups.auto_backup(self.root, True))
        self.root.minsize(app_width, app_height)
        self.root.config(bg=ups.data.bgc)
        self.root.iconbitmap(r'data_files\icons\icon.ico')
        # Define a variable for the radio buttons in the Options menu. Also for the autoclose minutes
        # Defined here because in main.py this executes too early and gives error
        self.autoclose_mins = IntVar(value=ups.data.cd_mins)
        self.radio_var = IntVar()

        # BINDINGS
        self.root.bind('<ButtonRelease-1>', lambda event: self.lang_frame.place_forget()
                        if event.widget not in self.lang_btns + [self.lang_frame, self.lang_btn] else "")

        self.draw_ui()

    def draw_ui(self):
        """Draws the UI for the Main window"""
        # Canvas
        self.canvas = Canvas(bg=ups.data.bgc, height=200, width=200, highlightthickness=0)
        self.logo = PhotoImage(master=self.root, file=r'data_files\icons\logo.png')
        self.canvas.create_image(100, 100, image=self.logo)
        self.canvas.place(relx=0.5, y=25, anchor='n')

        # Define the following icons
        self.eye_icon = PhotoImage(file=r'data_files\icons\eye.png')
        self.no_eye_icon = PhotoImage(file=r'data_files\icons\no_eye.png')
        self.eye_icon_h = PhotoImage(file=r'data_files\icons\eye_hover.png')
        self.no_eye_icon_h = PhotoImage(file=r'data_files\icons\no_eye_hover.png')
        self.browse_icon = PhotoImage(file=r'data_files\icons\browse.png')
        self.import_icon = PhotoImage(file=r'data_files\icons\import.png')
        self.export_icon = PhotoImage(file=r'data_files\icons\export.png')
        self.backup_icon = PhotoImage(file=r'data_files\icons\backup.png')
        self.logout_icon = PhotoImage(file=r'data_files\icons\logout.png')
        self.exit_icon = PhotoImage(file=r'data_files\icons\exit.png')
        self.copy_icon = PhotoImage(file=r'data_files\icons\copy.png')
        self.paste_icon = PhotoImage(file=r'data_files\icons\paste.png')
        self.cut_icon = PhotoImage(file=r'data_files\icons\cut.png')
        self.themes_icon = PhotoImage(file=r'data_files\icons\themes.png')
        self.light_icon = PhotoImage(file=r'data_files\icons\light.png')
        self.prefs_icon = PhotoImage(file=r'data_files\icons\prefs.png')
        self.dark_icon = PhotoImage(file=r'data_files\icons\dark.png')
        self.backup_period_icon = PhotoImage(file=r'data_files\icons\backup_period.png')
        self.settings_icon = PhotoImage(file=r'data_files\icons\settings.png')

        # Create an image object for every language in the lang folder
        self.flags = {}
        for lng in scandir(r'data_files\lang'):
            if lng.name.endswith('.py'):
                self.flags[''.join(splitext(lng.name)[:-1])] = PhotoImage(file=f"data_files\\icons\\{''.join(splitext(lng.name)[:-1])}.png")

        # Main Menu Bar
        self.menubar = Menu()
        self.root.config(menu=self.menubar)

        self.file_menu = Menu(self.menubar, tearoff=False, font=FONT_F, activebackground='#999999')
        self.edit_menu = Menu(self.menubar, tearoff=False, font=FONT_F, activebackground='#999999')
        self.settings_menu = Menu(self.menubar, tearoff=False, font=FONT_F, activebackground='#999999')
        self.lang_menu = Menu(self.menubar, tearoff=False, font=FONT_F, activebackground='#999999')

        self.backups_menu = Menu(self.file_menu, tearoff=False, font=FONT_F, activebackground='#999999')
        prefs_menu = Menu(self.settings_menu, tearoff=False, font=FONT_F, activebackground='#999999')
        self.backup_menu = Menu(self.settings_menu, tearoff=False, font=FONT_F, activebackground='#999999')
        self.color_menu = Menu(prefs_menu, tearoff=False, font=FONT_F, activebackground='#999999')
        self.r_click_popup = Menu(self.root, tearoff=False, font=FONT_F, activebackground='#999999')

        # Define the Copy, Paste and Cut commands for the Edit menu as well as for the right click menu
        self.r_click_popup.add_command(label=ups.data.pmui['menu']['copy'],
                command=lambda: self.root.focus_get().event_generate(('<<Copy>>')), image=self.copy_icon, compound='left')
        self.r_click_popup.add_command(label=ups.data.pmui['menu']['paste'],
                command=lambda: self.root.focus_get().event_generate(('<<Paste>>')), image=self.paste_icon, compound='left')
        self.r_click_popup.add_command(label=ups.data.pmui['menu']['cut'],
                command=lambda: self.root.focus_get().event_generate(('<<Cut>>')), image=self.cut_icon, compound='left')
        self.edit_menu.add_command(label=ups.data.pmui['menu']['copy'],
                command=lambda: self.root.focus_get().event_generate(('<<Copy>>')), image=self.copy_icon, compound='left')
        self.edit_menu.add_command(label=ups.data.pmui['menu']['paste'],
                command=lambda: self.root.focus_get().event_generate(('<<Paste>>')), image=self.paste_icon, compound='left')
        self.edit_menu.add_command(label=ups.data.pmui['menu']['cut'],
                command=lambda: self.root.focus_get().event_generate(('<<Cut>>')), image=self.cut_icon, compound='left')

        # Populate the recover from backups menu
        if exists(join(getenv('LOCALAPPDATA'), 'PM Master', 'backups')):
            for item in scandir(ups.data.backups_path):
                if item.name.startswith("pmd"):
                    label = datetime.strptime(item.name[6:-5], "%b %d, %Y - %H.%M.%S").strftime(
                                                                f"{ups.data.pmui['menu']['backup_label_date']}: %d/%m/%y - %H:%M:%S")
                    self.backups_menu.add_command(label=label, command=lambda item=item: ups.recover_from_backup(item))

        self.menubar.add_cascade(label=ups.data.pmui['menu']['menubar_file'], menu=self.file_menu)
        self.menubar.add_cascade(label=ups.data.pmui['menu']['menubar_edit'], menu=self.edit_menu)
        self.menubar.add_cascade(label=ups.data.pmui['menu']['menubar_settings'], menu=self.settings_menu)
        self.settings_menu.add_cascade(label=ups.data.pmui['menu']['menubar_themes'], menu=self.color_menu,
                                    image=self.themes_icon, compound='left')
        self.settings_menu.add_cascade(label=ups.data.pmui['menu']['menubar_backup_period'], menu=self.backup_menu,
                                    image=self.backup_period_icon, compound='left')
        self.settings_menu.add_command(label=ups.data.pmui['menu']['menubar_settings_menu'],
                                    command=lambda: CustSettings(self.root), image=self.settings_icon, compound='left')

        # Frames
        self.status_bar = Frame(bg=ups.data.accent, bd=1, height=22, relief='flat', )
        self.status_bar.place(relx=0, rely=1, relwidth=1, anchor='sw')

        self.frame = Frame(bg=ups.data.accent, width=565, height=45)

        # Labels
        self.website_label = Label(text=ups.data.pmui['labels']['website_label'], font=FONT_B, fg=ups.data.details1, bg=ups.data.bgc)
        self.website_label.place(x=160, y=255, anchor='e')

        self.user_label = Label(text=ups.data.pmui['labels']['user_label'], font=FONT_B, fg=ups.data.details1, bg=ups.data.bgc)
        self.user_label.place(x=160, y=295, anchor='e')

        self.email_label = Label(text=ups.data.pmui['labels']['email_label'], font=FONT_B, fg=ups.data.details1, bg=ups.data.bgc)
        self.email_label.place(x=160, y=335, anchor='e')

        self.password_label = Label(text=ups.data.pmui['labels']['password_label'], font=FONT_B, fg=ups.data.details1, bg=ups.data.bgc)
        self.password_label.place(x=160, y=375, anchor='e')

        self.password_eye_bg = Label(text="", font=('CorsicaMX-Regular', 16, 'normal'), fg=ups.data.details1, bg=ups.data.details2, width=3)
        self.password_eye_bg.place(x=642, y=375, anchor='e')

        self.password_length = Label(text=ups.data.pmui['labels']['password_length'], font=FONT_B, fg=ups.data.details1, bg=ups.data.accent)

        self.status_entries_num = StringVar()
        self.status_entries = Label(text=ups.data.pmui['labels']['status_entries'], font=FONT_F, fg=ups.data.details1,
                                    bg=ups.data.accent, textvariable=self.status_entries_num)
        self.status_entries.place(x=10, rely=1, anchor='sw')

        self.cd_var = StringVar()
        self.countdown_label = Label(text=ups.data.timer_st, font=FONT_F, fg=ups.data.details1, bg=ups.data.accent,
                                    textvariable=self.cd_var)
        self.status_bar.update()
        self.countdown_label.place(x=self.status_bar.winfo_width() - 20, rely=1, anchor='se')

        # Entriy boxes
        self.website_entry = Entry(width=29, bg=ups.data.details2, fg=ups.data.fgc, border=0, font=FONT_A,
                                selectbackground=ups.data.bgc)
        self.website_entry.place(x=165, y=255, anchor='w', width=self.root.winfo_width() - 380)
        self.website_entry.focus()

        self.user_entry = Entry(width=40, bg=ups.data.details2, fg=ups.data.fgc, border=0, font=FONT_A,
                                selectbackground=ups.data.bgc)
        self.user_entry.place(x=165, y=295, anchor='w', width=self.root.winfo_width() - 230)

        self.password_entry = Entry(
            font=FONT_A, bg=ups.data.details2, fg=ups.data.fgc, bd=0, width=31, selectbackground=ups.data.bgc, show="✲")
        self.password_entry.place(x=165, y=375, anchor='w', width=self.root.winfo_width() - 355)

        # Combobox Style
        self.combostyle = Style()
        self.combostyle.theme_create('combostyle', parent='alt',
                                settings = {'TCombobox': {
                                    'configure': {
                                        'selectbackground': ups.data.bgc,
                                        'fieldbackground': ups.data.details2,
                                        'background': ups.data.bgc,
                                        'arrowcolor': ups.data.details1,
                                        'arrowsize': 15,
                                        'postoffset': 4,
                                    },
                                'map': {
                                    'background':
                                        [('active', ups.data.accent),
                                        ('pressed', ups.data.details2)],
                                }
                                },
                                    'TSizegrip': {
                                        'configure': {
                                        'background': ups.data.accent
                                        }
                                    }
                                }
                                )

        # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
        self.combostyle.theme_use('combostyle')

        self.root.option_add('*TCombobox*Listbox.font', FONT_A)
        self.root.option_add('*TCombobox*Listbox.background', ups.data.bgc)
        self.root.option_add('*TCombobox*Listbox.foreground', ups.data.fgc)
        self.root.option_add('*TCombobox*Listbox.selectBackground', ups.data.accent)
        self.root.option_add('*TCombobox*Listbox.selectForeground', ups.data.details1)
        self.root.option_add('*TCombobox*Listbox.highlightThickness', 0)
        self.root.option_add('*TCombobox*Listbox.borderWidth', 0)

        # Spinbox
        self.pass_length = IntVar(value=8)
        self.char_spinbox = Spinbox(from_=6, to=20, font=FONT_C, fg=ups.data.details1, bg=ups.data.bgc, bd=1, width=2,
            buttonbackground=ups.data.bgc, state='disabled', selectbackground=ups.data.accent,
            readonlybackground=ups.data.bgc, textvariable=self.pass_length, takefocus=False, cursor='sb_v_double_arrow')

        # Buttons
        self.search_btn = Button(
            text=ups.data.pmui['buttons']['search_btn'], font=FONT_C, fg=ups.data.details1, bg=ups.data.bgc, width=15, takefocus=False)
        self.opt_btn = Button(
            text=ups.data.pmui['buttons']['options_btn'], font=FONT_C, fg=ups.data.details1, bg=ups.data.bgc, bd=1, width=8, pady=0, takefocus=False)
        self.gen_btn = Button(
            text=ups.data.pmui['buttons']['generate_btn'], font=FONT_C, fg=ups.data.details1, bg=ups.data.bgc, bd=1, pady=0, takefocus=False)
        self.add_btn = Button(text=ups.data.pmui['buttons']['add_btn'], font=FONT_C, fg=ups.data.details1, bg=ups.data.bgc, width=48, takefocus=False)
        self.clear_btn = Button(
            text=ups.data.pmui['buttons']['clear_btn'], font=FONT_C, fg=ups.data.details1, bg=ups.data.bgc, width=10, takefocus=False)
        self.eye_btn = Button(bg=ups.data.details2, bd=0, width=30, height=20, pady=0, relief='sunken',
                            highlightbackground=ups.data.details2, highlightcolor=ups.data.details2, highlightthickness=0,
                            activebackground=ups.data.details2, image=self.no_eye_icon, takefocus=False, cursor='hand2')

        self.search_btn.place(x=727, y=255, anchor='e', height=34)
        self.opt_btn.place(x=727, y=375, height=32, anchor='e')
        self.add_btn.place(x=165, y=415, anchor='w', width=455)
        self.clear_btn.place(x=727, y=415, anchor='e')
        self.eye_btn.place(x=636, y=375, anchor='e')

        # Radiobuttons
        self.val = StringVar(value='1')
        self.radio1 = Radiobutton(text=ups.data.pmui['radiobuttons']['radio1'], font=FONT_C, variable=self.val, value=1, indicator=0, bg=ups.data.bgc,
                                fg=ups.data.fgc, activebackground=ups.data.details2, command=self.upd_radio)
        self.radio2 = Radiobutton(text=ups.data.pmui['radiobuttons']['radio2'], font=FONT_C, variable=self.val, value=2, indicator=0, bg=ups.data.bgc,
                                fg=ups.data.fgc, activebackground=ups.data.details2, command=self.upd_radio)
        self.radio3 = Radiobutton(text=ups.data.pmui['radiobuttons']['radio3'], font=FONT_C, variable=self.val, value=3, indicator=0, bg=ups.data.bgc,
                                fg=ups.data.fgc, activebackground=ups.data.details2, command=self.upd_radio)
        self.radio4 = Radiobutton(text=ups.data.pmui['radiobuttons']['radio4'], font=FONT_C, variable=self.val, value=4, indicator=0, bg=ups.data.bgc,
                                fg=ups.data.fgc, activebackground=ups.data.details2, command=self.upd_radio)

        # Checkbuttons
        self.check_fixed = IntVar(value=0)
        self.fixed_length = Checkbutton(variable=self.check_fixed, bg=ups.data.accent, fg=ups.data.fgc,
            activebackground=ups.data.accent, selectcolor=ups.data.details2,
            command=lambda: self.char_spinbox.config(state='readonly') if self.check_fixed.get() == 1 else self.char_spinbox.config(state='disabled'))

        # Combobox
        self.emails = StringVar()
        self.email_combo = Combobox(self.root, font=FONT_A, width=39)
        self.password_entry.lift()

        # Listbox
        self.autocomplete_box = Listbox(font=FONT_A, fg=ups.data.details1, bg=ups.data.bgc, bd=0, width=29, height=1,
                    selectbackground=ups.data.accent, selectmode=SINGLE, takefocus=0, exportselection=0, cursor='hand2')

        # Sizegrip
        self.sizegrip = Sizegrip()
        self.sizegrip.place(relx=1, rely=1, anchor='se')

        # Language controls
        self.lang_frame = Frame(self.root, bg=ups.data.accent)
        self.lang_btn = Button(self.root, text="English", font=FONT_E, bd=0, bg=ups.data.bgc, fg=ups.data.details1, takefocus=0, cursor='hand2',
            activebackground=ups.data.bgc, highlightthickness=0, relief='sunken', activeforeground=ups.data.details2, image=self.flags['english'],
            compound='left', command=lambda: self.lang_frame.place(anchor='ne', x=self.lang_btn.winfo_x() + self.lang_btn.winfo_width(), y=35
                                        ) if self.lang_frame.winfo_ismapped() == 0 else self.lang_frame.place_forget())
        self.lang_btn.place(anchor='ne', x=727, y=10)
        self.lang_btn.update()

        # Get the .py files in the lang folder. Assign the corresponding icons to them.
        langs = [splitext(lng.name)[0].title() for lng in scandir(join(dirname(__file__), 'lang')) if lng.name.endswith('.py')]
        self.lang_btns = []

        # Create a new button for every language. Put every new button below the previous one.
        for index, lng in enumerate(langs):
            btn = Button(self.lang_frame, text=lng, font=FONT_E, bd=0, bg=ups.data.accent, fg=ups.data.details1, takefocus=0,
            cursor='hand2', activebackground=ups.data.details2, highlightthickness=0, relief='sunken', activeforeground=ups.data.details1,
            image=self.flags[lng.lower()], compound='left', command=lambda lng=lng: self.choose_language(lng))
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
        ups.data.jdata[ups.data.user]['pm_settings']['language'] = lng.lower()
        # Write the new data to disk
        ups.data.save_data()

        self.lang_frame.place_forget()

        ups.data.load_language(lng)
        ups.data.auth = ups.data.lang.authenticate['authenticate']
        ups.data.upd = ups.data.lang.update
        ups.data.pmui = ups.data.lang.ui["PMUI"]
        ups.data.theme_ch = ups.data.lang.ui["theme_changer_ui"]
        ups.data.cust = ups.data.lang.ui["cust_settings"]
        self.cd_var.set(f"{ups.data.auth['check_login']['autoclose']} {ups.data.timer_st}")
        self.update_language()


    def calc_width(self, event):  # pylint: disable=unused-argument
        """Recalculate widget placement and size"""
        self.lang_btn.place(x=self.root.winfo_width() - 63)
        if self.lang_frame.winfo_ismapped():
            self.lang_frame.place(x=self.lang_btn.winfo_x() + self.lang_btn.winfo_width())
        self.search_btn.place(x=self.root.winfo_width() - 63, y=255, anchor='e', height=34)
        self.opt_btn.place(x=self.root.winfo_width() - 63, y=375, height=32, anchor='e')
        self.clear_btn.place(x=self.root.winfo_width() - 63, anchor='e')
        if self.gen_btn.winfo_ismapped():
            self.gen_btn.place(x=self.root.winfo_width() - 70, anchor='e')
        self.website_entry.place(x=165, y=255, anchor='w', width=self.root.winfo_width() - 380)
        self.user_entry.place(x=165, y=295, anchor='w', width=self.root.winfo_width() - 230)
        ui.email_combo.place(x=165, y=335, anchor='w', width=ui.root.winfo_width() - 230)
        self.password_entry.place(x=165, y=375, anchor='w', width=self.root.winfo_width() - 355)
        self.password_eye_bg.place(x=self.root.winfo_width() - 148, y=375, anchor='e')
        self.eye_btn.place(x=self.root.winfo_width() - 154, y=375, anchor='e')
        self.add_btn.place(x=165, anchor='w', width=self.root.winfo_width() - 335)
        if self.frame.winfo_ismapped():
            ui.frame.place(x=165, y=420, anchor='w', width=ui.root.winfo_width() - 230)
        if self.autocomplete_box.winfo_ismapped():
            self.autocomplete_box.place(x=165, y=270, anchor='nw', width=self.website_entry.winfo_width())
        if self.root.state() == 'zoomed':
            self.sizegrip.place_forget()
            self.countdown_label.place(x=self.status_bar.winfo_width())
        else:
            self.sizegrip.place(relx=1, rely=1, anchor='se')
            self.countdown_label.place(x=self.status_bar.winfo_width() - 15)


    def spinbox_controls(self, event):
        """Defines the Spinbox behaviour on Mouse scrolling and Mouse Click & Drag"""
        # Get the current value of the spinbox
        if event.widget == self.char_spinbox:
            current_value = self.pass_length.get()
        else:
            current_value = self.autoclose_mins.get()

        # Define +/- 1 to spinbox current value upon scroll Up/Down
        if event.delta == 120 and current_value < int(event.widget.cget('to')) and event.widget['state'] != 'disabled':
            if event.widget == self.char_spinbox:
                self.pass_length.set(current_value + 1)
            else:
                self.update_autoclose(current_value, 1)

        elif event.delta == -120 and current_value > int(event.widget.cget('from')) and event.widget['state'] != 'disabled':
            if event.widget == self.char_spinbox:
                self.pass_length.set(current_value - 1)
            else:
                self.update_autoclose(current_value, -1)

        # If method was triggered with a Mouse Button click and Mouse Motion was detected
        if int(event.type) == 6:
            # Define +/- 1 to spinbox current value for every 25 pixels mouse moved Up/Down on the screen
            if -event.y > ups.data.spinbox_ypos + 25 and current_value < int(event.widget.cget('to')) and event.widget['state'] != 'disabled':
                if event.widget == self.char_spinbox:
                    self.pass_length.set(current_value + 1)
                else:
                    self.update_autoclose(current_value, 1)
                ups.data.spinbox_ypos = -event.y
            elif -event.y < ups.data.spinbox_ypos - 25 and current_value > int(event.widget.cget('from')) and event.widget['state'] != 'disabled':
                if event.widget == self.char_spinbox:
                    self.pass_length.set(current_value - 1)
                else:
                    self.update_autoclose(current_value, -1)
                ups.data.spinbox_ypos = -event.y


    def update_autoclose(self, curr_value, value):
        """Updates the autoclose minutes and the countdown timer

        Args:
            curr_value (int): The current value of the parameter
            value (int): How much to add to the timer (negative numbers subtract from it).
        """
        self.autoclose_mins.set(curr_value + value)
        ups.data.cd_mins = curr_value + value
        ups.data.countdown = ups.data.cd_mins * 60


    def update_theme(self, user: str):
        """Updates the color for widgets to the current theme's color settings

        Args:
            user (str): The user who's settings are being updated
        """

        sett = ups.data.jdata[user]['pm_settings']['theme']
        ups.data.details1 = sett['DETAILS1']
        ups.data.fgc = sett['FG']
        ups.data.bgc = sett['BG']
        ups.data.accent = sett['ACCENT']
        ups.data.details2 = sett['DETAILS2']
        ups.data.shadow = ups.get_median_color(ups.data.accent, ups.data.bgc)

        # Main widgets
        self.root.config(bg=ups.data.bgc)
        self.canvas.config(bg=ups.data.bgc)
        self.frame.config(bg=ups.data.accent)

        # Frames
        self.status_bar.config(bg=ups.data.accent)
        self.lang_frame.config(bg=ups.data.accent)

        # Labels
        self.website_label.config(fg=ups.data.details1, bg=ups.data.bgc)
        self.user_label.config(fg=ups.data.details1, bg=ups.data.bgc)
        self.email_label.config(fg=ups.data.details1, bg=ups.data.bgc)
        self.password_label.config(fg=ups.data.details1, bg=ups.data.bgc)
        self.password_length.config(fg=ups.data.details1, bg=ups.data.accent)
        self.password_eye_bg.config(fg=ups.data.details1, bg=ups.data.details2)
        self.status_entries.config(fg=ups.data.details1, bg=ups.data.accent)
        self.countdown_label.config(fg=ups.data.details1, bg=ups.data.accent)

        # Entries
        self.website_entry.config(bg=ups.data.details2, fg=ups.data.fgc, selectbackground=ups.data.bgc)
        self.user_entry.config(bg=ups.data.details2, fg=ups.data.fgc, selectbackground=ups.data.bgc)
        self.password_entry.config(bg=ups.data.details2, fg=ups.data.fgc, selectbackground=ups.data.bgc)

        # Combobox
        self.combostyle.configure('TCombobox', selectbackground=ups.data.bgc, fieldbackground=ups.data.details2,
            background=ups.data.bgc, foreground=ups.data.fgc, arrowcolor=ups.data.details1, arrowsize=15, postoffset=4)
        self.combostyle.map('TCombobox', background=[('active', ups.data.accent), ('pressed', ups.data.details2)])
        self.root.option_add('*TCombobox*Listbox.background', ups.data.bgc)
        self.root.option_add('*TCombobox*Listbox.foreground', ups.data.fgc)
        self.root.option_add('*TCombobox*Listbox.selectBackground', ups.data.accent)
        self.root.option_add('*TCombobox*Listbox.selectForeground', ups.data.details1)
        self.root.tk.eval(f'[ttk::combobox::PopdownWindow {self.email_combo}].f.l configure -background {ups.data.bgc}')
        self.root.tk.eval(f'[ttk::combobox::PopdownWindow {self.email_combo}].f.l configure -selectbackground {ups.data.accent}')
        self.root.tk.eval(f'[ttk::combobox::PopdownWindow {self.email_combo}].f.l configure -selectforeground {ups.data.details1}')
        self.root.tk.eval(f'[ttk::combobox::PopdownWindow {self.email_combo}].f.l configure -foreground {ups.data.fgc}')

        # Sizegrip
        self.combostyle.configure('TSizegrip', background=ups.data.accent)

        # Spinbox
        self.char_spinbox.config(fg=ups.data.details1, bg=ups.data.bgc, buttonbackground=ups.data.bgc,
            selectbackground=ups.data.accent, disabledbackground=ups.get_median_color(ups.data.accent, '#FFFFFF'),
            readonlybackground=ups.data.bgc, disabledforeground=ups.get_median_color(ups.data.accent, '#000000'))

        # Buttons
        self.gen_btn.config(fg=ups.data.details1, bg=ups.data.bgc, activebackground=ups.data.details2)
        self.search_btn.config(fg=ups.data.details1, bg=ups.data.bgc, activebackground=ups.data.details2)
        self.add_btn.config(fg=ups.data.details1, bg=ups.data.bgc, activebackground=ups.data.details2)
        self.clear_btn.config(fg=ups.data.details1, bg=ups.data.bgc, activebackground=ups.data.details2)
        if self.gen_btn.winfo_ismapped():
            self.opt_btn.config(fg=ups.data.accent, bg=ups.data.details2, activebackground=ups.data.details2)
        else:
            self.opt_btn.config(fg=ups.data.details1, bg=ups.data.bgc, activebackground=ups.data.details2)
        self.eye_btn.config(bg=ups.data.details2, highlightbackground=ups.data.details2, highlightcolor=ups.data.details2,
                            activebackground=ups.data.details2)
        self.lang_btn.config(bg=ups.data.bgc, fg=ups.data.details1, activebackground=ups.data.bgc, activeforeground=ups.data.details2)
        for btn in self.lang_btns:
            btn.config(bg=ups.data.accent, fg=ups.data.details1, activebackground=ups.data.details2, activeforeground=ups.data.details1)

        # Radiobuttons
        for ind, btn in enumerate((self.radio1, self.radio2, self.radio3, self.radio4)):
            if self.val.get() == str(ind+1):
                btn.config(fg=ups.data.fgc, bg=ups.data.bgc, activebackground=ups.data.details2, selectcolor=ups.data.details2)
            else:
                btn.config(fg=ups.data.details1, bg=ups.data.bgc, activebackground=ups.data.details2, selectcolor=ups.data.details2)

        # Checkbuttons
        self.fixed_length.config(bg=ups.data.accent, fg=ups.data.fgc, selectcolor=ups.data.details2,
                                activebackground=ups.data.accent, activeforeground=ups.data.fgc)

        # Listbox
        self.autocomplete_box.config(fg=ups.data.details1, bg=ups.data.bgc, selectbackground=ups.data.accent)


    def theme_preset(self, mode: str, user: str):
        """Switches the app theme

        Args:
            mode (str): Defines the theme color mode
            user (str): The user who's theme will be changed
        """
        if mode == "light":
            color_data = {
                "theme": {
                    'DETAILS2': "white",
                    'ACCENT': "#888888",
                    'BG': "#AAAAAA",
                    'FG': "black",
                    'DETAILS1': "black",
                }}
        elif mode == "dark":
            color_data = {
                "theme": {
                    'DETAILS2': "#DDDDDD",
                    'ACCENT': "#555555",
                    'BG': "#777777",
                    'FG': "black",
                    'DETAILS1': "white",
                }}

        ups.data.jdata[user]["pm_settings"].update(color_data)
        ups.data.save_data()
        self.update_theme(user)


    def upd_radio(self):
        """Updates the colors of the radio buttons when one is clicked. Also updates spinboxes character limits and defaults"""
        for ind, btn in enumerate((self.radio1, self.radio2, self.radio3, self.radio4)):
            if self.val.get() == str(ind+1):
                btn.config(fg=ups.data.fgc, bg=ups.data.bgc, activebackground=ups.data.details2, selectcolor=ups.data.details2)
            else:
                btn.config(fg=ups.data.details1, bg=ups.data.bgc, activebackground=ups.data.details2, selectcolor=ups.data.details2)

        if self.val.get() == "1":
            self.char_spinbox.config(from_=6)
            self.char_spinbox.config(to=20)
            self.pass_length.set(8)
        else:
            self.char_spinbox.config(from_=12)
            self.char_spinbox.config(to=35)
            self.pass_length.set(30)


    def update_language(self):
        """Updates all widgets that have text to reload it with the newly chosen language"""
        self.root.title(ups.data.pmui['main_title'])
        self.r_click_popup.entryconfig(0, label=ups.data.pmui['menu']['copy'])
        self.r_click_popup.entryconfig(1, label=ups.data.pmui['menu']['paste'])
        self.r_click_popup.entryconfig(2, label=ups.data.pmui['menu']['cut'])
        self.edit_menu.entryconfig(0, label=ups.data.pmui['menu']['copy'])
        self.edit_menu.entryconfig(1, label=ups.data.pmui['menu']['paste'])
        self.edit_menu.entryconfig(2, label=ups.data.pmui['menu']['cut'])

        self.backups_menu.entryconfig(
            0, label=f"{ups.data.pmui['menu']['backup_label_date']}: {' '.join(self.backups_menu.entrycget(0, 'label').split()[1:])}")
        self.backups_menu.entryconfig(
            1, label=f"{ups.data.pmui['menu']['backup_label_date']}: {' '.join(self.backups_menu.entrycget(1, 'label').split()[1:])}")
        self.backups_menu.entryconfig(
            2, label=f"{ups.data.pmui['menu']['backup_label_date']}: {' '.join(self.backups_menu.entrycget(2, 'label').split()[1:])}")

        self.menubar.entryconfig(1, label=ups.data.pmui['menu']['menubar_file'])
        self.menubar.entryconfig(2, label=ups.data.pmui['menu']['menubar_edit'])
        self.menubar.entryconfig(3, label=ups.data.pmui['menu']['menubar_settings'])
        self.settings_menu.entryconfig(0, label=ups.data.pmui['menu']['menubar_themes'])
        self.settings_menu.entryconfig(1, label=ups.data.pmui['menu']['menubar_backup_period'])
        self.settings_menu.entryconfig(2, label=ups.data.pmui['menu']['menubar_settings_menu'])
        self.website_label.config(text=ups.data.pmui['labels']['website_label'])
        self.user_label.config(text=ups.data.pmui['labels']['user_label'])
        self.email_label.config(text=ups.data.pmui['labels']['email_label'])
        self.password_label.config(text=ups.data.pmui['labels']['password_label'])
        self.password_length.config(text=ups.data.pmui['labels']['password_length'])
        msg = ups.data.auth['check_login']['status_entries_num']
        self.status_entries_num.set(f"{msg[0]} {ups.data.user}! {msg[1]} {len(ups.data.jdata[ups.data.user]['entries'])} " \
                        f"{msg[2]} {ups.data.jdata[ups.data.user]['pm_settings']['backup']['date']}")
        self.search_btn.config(text=ups.data.pmui['buttons']['search_btn'])
        self.opt_btn.config(text=ups.data.pmui['buttons']['options_btn'])
        self.gen_btn.config(text=ups.data.pmui['buttons']['generate_btn'])
        self.add_btn.config(text=ups.data.pmui['buttons']['add_btn'])
        self.clear_btn.config(text=ups.data.pmui['buttons']['clear_btn'])
        self.radio1.configure(text=ups.data.pmui['radiobuttons']['radio1'])
        self.radio2.configure(text=ups.data.pmui['radiobuttons']['radio2'])
        self.radio3.configure(text=ups.data.pmui['radiobuttons']['radio3'])
        self.radio4.configure(text=ups.data.pmui['radiobuttons']['radio4'])
        ui.color_menu.entryconfig(0, label=ups.data.lang.main['light_theme'])
        ui.color_menu.entryconfig(1, label=ups.data.lang.main['dark_theme'])
        ui.color_menu.entryconfig(3, label=ups.data.lang.main['custom_theme'])  # pylint: disable=unnecessary-lambda
        ups.data.backup_period = ups.data.upd['backup_period']
        ui.backup_menu.entryconfig(0, label=ups.data.backup_period[0])
        ui.backup_menu.entryconfig(1, label=ups.data.backup_period[1])
        ui.backup_menu.entryconfig(2, label=ups.data.backup_period[2])
        ui.backup_menu.entryconfig(3, label=ups.data.backup_period[3])
        ui.backup_menu.entryconfig(4, label=ups.data.backup_period[4])

        self.file_menu.entryconfig(0, label=ups.data.lang.main['button1'])
        self.file_menu.entryconfig(2, label=ups.data.lang.main['button2'])
        self.file_menu.entryconfig(3, label=ups.data.lang.main['button3'])
        self.file_menu.entryconfig(4, label=ups.data.lang.main['button4'])
        self.file_menu.entryconfig(6, label=ups.data.lang.main['button5'])


class ThemeChanger:
    """The UI for the ThemeChanger window"""

    def __init__(self):
        # Create the Theme Changer window with the following parameters
        self.theme = Toplevel(ui.root)
        self.theme.title(ups.data.theme_ch['title'])
        tc_width = 250
        tc_height = 250
        root_xcenter = ui.root.winfo_x() + ui.root.winfo_width() / 2
        root_ycenter = ui.root.winfo_y() + ui.root.winfo_height() / 2
        # Make this window appear at the center of the main window
        self.theme.geometry(f"{tc_width}x{tc_height}+{int(root_xcenter - tc_width / 2)}+{int(root_ycenter - tc_height / 2)}")
        self.theme.resizable(False, False)
        self.theme.config(bg=ups.data.bgc, pady=10, padx=10)
        # Make the main window unclickable until this one is closed
        self.theme.grab_set()
        # Make it a tool window (only X button)
        self.theme.attributes('-toolwindow', True)
        self.theme.focus()
        self.create_content()


    def create_content(self):
        """Creates the UI of the Theme Changer window"""
        self.bg_label = Label(self.theme, text=ups.data.theme_ch['bg_label'], font=FONT_A, bg=ups.data.bgc, fg=ups.data.details1)
        self.bg_label.place(relx=0, rely=0.15, anchor='w')
        self.fg_label = Label(self.theme, text=ups.data.theme_ch['fg_label'], font=FONT_A, bg=ups.data.bgc, fg=ups.data.details1)
        self.fg_label.place(relx=0, rely=0.3, anchor='w')
        self.accent_label = Label(self.theme, text=ups.data.theme_ch['accent_label'], font=FONT_A, bg=ups.data.bgc, fg=ups.data.details1)
        self.accent_label.place(relx=0, rely=0.45, anchor='w')
        self.details1_label = Label(self.theme, text=ups.data.theme_ch['details1_label'], font=FONT_A, bg=ups.data.bgc, fg=ups.data.details1)
        self.details1_label.place(relx=0, rely=0.6, anchor='w')
        self.details2_label = Label(self.theme, text=ups.data.theme_ch['details2_label'], font=FONT_A, bg=ups.data.bgc, fg=ups.data.details1)
        self.details2_label.place(relx=0, rely=0.75, anchor='w')

        self.bg_btn = Button(self.theme, width=5, bd=2, bg=ups.data.bgc, activebackground=ups.data.bgc,
                            cursor='hand2', relief='ridge', command=lambda: self.process_color('BG'))
        self.bg_btn.place(relx=0.9, rely=0.15, anchor='e')
        self.fg_btn = Button(self.theme, width=5, bd=2, bg=ups.data.fgc, activebackground=ups.data.fgc,
                            cursor='hand2', relief='ridge', command=lambda: self.process_color('FG'))
        self.fg_btn.place(relx=0.9, rely=0.3, anchor='e')
        self.accent_btn = Button(self.theme, width=5, bd=2, bg=ups.data.accent, activebackground=ups.data.accent,
                                cursor='hand2', relief='ridge', command=lambda: self.process_color('ACCENT'))
        self.accent_btn.place(relx=0.9, rely=0.45, anchor='e')
        self.details1_btn = Button(self.theme, width=5, bd=2, bg=ups.data.details1, activebackground=ups.data.details1,
                                    cursor='hand2', relief='ridge', command=lambda: self.process_color('DETAILS1'))
        self.details1_btn.place(relx=0.9, rely=0.6, anchor='e')
        self.details2_btn = Button(self.theme, width=5, bd=2, bg=ups.data.details2, activebackground=ups.data.details2,
                                    cursor='hand2', relief='ridge', command=lambda: self.process_color('DETAILS2'))
        self.details2_btn.place(relx=0.9, rely=0.75, anchor='e')
        self.reset_btn = Button(self.theme, text=ups.data.theme_ch['reset_btn'], bg=ups.data.bgc, fg=ups.data.details1,
                                command=lambda: self.process_color('RESET'))
        self.reset_btn.place(relx=1, rely=0.9, anchor='e')


    def update_theme(self):
        """Updates the theme of the Theme Changer window"""
        self.theme.config(bg=ups.data.bgc)
        self.bg_label.config(bg=ups.data.bgc, fg=ups.data.fgc)
        self.fg_label.config(bg=ups.data.bgc, fg=ups.data.fgc)
        self.accent_label.config(bg=ups.data.bgc, fg=ups.data.fgc)
        self.details1_label.config(bg=ups.data.bgc, fg=ups.data.fgc)
        self.details2_label.config(bg=ups.data.bgc, fg=ups.data.fgc)
        self.bg_btn.config(bg=ups.data.bgc, activebackground=ups.data.bgc)
        self.fg_btn.config(bg=ups.data.fgc, activebackground=ups.data.fgc)
        self.accent_btn.config(bg=ups.data.accent, activebackground=ups.data.accent)
        self.details1_btn.config(bg=ups.data.details1, activebackground=ups.data.details1)
        self.details2_btn.config(bg=ups.data.details2, activebackground=ups.data.details2)
        self.reset_btn.config(bg=ups.data.bgc, fg=ups.data.fgc)


    def process_color(self, element: str):
        """Processes a color to update the theme with it

        Args:
            element (str): Used to check which button was clicked
        """

        if element != "RESET":
            # Get the color chooser window
            element_color = askcolor(title=ups.data.theme_ch['element_color'])

            color_data = {
                'theme': {
                    'DETAILS2': ups.data.details2,
                    'ACCENT': ups.data.accent,
                    'BG': ups.data.bgc,
                    'FG': ups.data.fgc,
                    'DETAILS1': ups.data.details1,
                }}
        else:
            # Default colors for when Reset button is clicked
            color_data = {
                'theme': {
                    'DETAILS2': "#DDDDDD",
                    'ACCENT': "#555555",
                    'BG': "#777777",
                    'FG': "black",
                    'DETAILS1': "white",
                }}

        if element != "RESET":
            # Get the HEX color
            if element_color[1]:
                color_data['theme'][element] = element_color[1]
            else:
                return

        # Update the currently opened data file
        ups.data.jdata[ups.data.user]['pm_settings'].update(color_data)

        # Write new color information to disk
        ups.data.save_data()

        # Update the colors of all widgets in the Theme Changer and the Main windows
        ui.update_theme(ups.data.user)
        self.update_theme()


def update_backup_period(period: str, user: str):
    """Updates the period of data backup

    Args:
        period (str): A period over which the autobackup will execute
        user (str): The user who's settings are being changed
    """
    if ups.data.jdata[user]['pm_settings']['backup']['period'] != period:
        ups.data.jdata[user]['pm_settings']['backup']['period'] = period
        ups.data.save_data()


class CustSettings:
    """Defines the Custom settings window"""

    def __init__(self, root: Tk):
        """Creating a Toplevel window for the Custom Settings

        Args:
            root (Tk): The main Tk window
        """
        # Create the Custom Settings window with the following parameters
        self.log_sett = Toplevel(root)
        cs_width = 550
        cs_height = 225
        root_xcenter = ui.root.winfo_x() + ui.root.winfo_width() / 2
        root_ycenter = ui.root.winfo_y() + ui.root.winfo_height() / 2
        self.log_sett.geometry(f"{cs_width}x{cs_height}+{int(root_xcenter - cs_width / 2)}+{int(root_ycenter - cs_height / 2)}")
        self.log_sett.minsize(cs_width, cs_height)
        self.log_sett.config(bg=ups.data.bgc)
        # Update defaults upon closing this window
        self.log_sett.protocol('WM_DELETE_WINDOW', self.refresh_fields)
        # Make the main window unclickable until this one is closed
        self.log_sett.grab_set()
        # Make it a tool window (only X button)
        self.log_sett.attributes('-toolwindow', True)
        self.log_sett.focus()
        self.draw_ui()

        self.log_sett.bind('<Button-1>', lambda event: self.log_sett.focus() if event.widget not in (
            self.user_entry, self.old_pwd_entry, self.new_pwd_entry, self.rep_pwd_entry, self.new_user, self.new_email) else "")


    def draw_ui(self):
        """Draws the UI for the window"""
        # Left Panel
        tab1 = Frame(self.log_sett, bg=ups.data.accent)
        tab1.place(x=0, y=0, relheight=1, width=175, anchor='nw')

        self.login_btn = Button(tab1, text=ups.data.cust['left_panel']['login_btn'], bd=0, font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1,
            relief='flat', activebackground=ups.data.bgc, activeforeground=ups.data.details1, command=lambda:self.update_cust_settings('login'))
        self.login_btn.place(relx=0, y=0, relwidth=1, anchor='nw')
        self.default_btn = Button(tab1, text=ups.data.cust['left_panel']['default_btn'], bd=0, font=FONT_C, bg=ups.data.shadow, fg=ups.data.details1,
            relief='flat', activebackground=ups.data.bgc, activeforeground=ups.data.details1, command=lambda:self.update_cust_settings('default'))
        self.default_btn.place(relx=0, y=30, relwidth=1, anchor='nw')

        # Right Panel - Login
        self.tab2 = Frame(self.log_sett, bg=ups.data.bgc)
        self.tab2.place(x=175, relheight=1, width=self.log_sett.winfo_width() - 175, anchor='nw')

        user = Label(self.tab2, text=ups.data.cust['right_panel_login']['user'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1)
        password = Label(self.tab2, text=ups.data.cust['right_panel_login']['password'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1)
        old_pwd = Label(self.tab2, text=ups.data.cust['right_panel_login']['old_pwd'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1)
        new_pwd = Label(self.tab2, text=ups.data.cust['right_panel_login']['new_pwd'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1)
        rep_pwd = Label(self.tab2, text=ups.data.cust['right_panel_login']['rep_pwd'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1)

        password.place(x=10, y=40, anchor='nw')
        password.update()

        user.place(x=10 + password.winfo_width(), y=10, anchor='ne')
        old_pwd.place(x=10 + password.winfo_width(), y=70, anchor='ne')
        new_pwd.place(x=10 + password.winfo_width(), y=100, anchor='ne')
        rep_pwd.place(x=10 + password.winfo_width(), y=130, anchor='ne')

        self.log_sett.update()
        self.maxw = max(user.winfo_width(), password.winfo_width(), old_pwd.winfo_width(), new_pwd.winfo_width(), rep_pwd.winfo_width())

        self.user_entry = Entry(self.tab2, width=29, bg=ups.data.details2, fg=ups.data.fgc, border=0, font=FONT_C, selectbackground=ups.data.bgc)
        self.user_entry.place(x=self.log_sett.winfo_width() - 185, y=10, width=self.log_sett.winfo_width() - 200 - self.maxw, anchor='ne')
        self.user_entry.insert(0, f"{ups.data.user}")

        self.old_pwd_entry = Entry(self.tab2, width=29, bg=ups.data.details2, fg=ups.data.fgc, border=0, font=FONT_C, selectbackground=ups.data.bgc)
        self.old_pwd_entry.place(x=100, y=70, width=self.log_sett.winfo_width() - 285, anchor='ne')

        self.new_pwd_entry = Entry(self.tab2, width=29, bg=ups.data.details2, fg=ups.data.fgc, border=0, font=FONT_C, selectbackground=ups.data.bgc)
        self.new_pwd_entry.place(x=100, y=100, width=self.log_sett.winfo_width() - 285, anchor='ne')

        self.rep_pwd_entry = Entry(self.tab2, width=29, bg=ups.data.details2, fg=ups.data.fgc, border=0, font=FONT_C, selectbackground=ups.data.bgc)
        self.rep_pwd_entry.place(x=100, y=130, width=self.log_sett.winfo_width() - 285, anchor='ne')


        # Right Panel - Default
        self.tab3 = Frame(self.log_sett, bg=ups.data.bgc)

        user = Label(self.tab3, text=ups.data.cust['right_panel_default']['user'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1)
        user.place(x=10 + password.winfo_width(), y=10, anchor='ne')

        email = Label(self.tab3, text=ups.data.cust['right_panel_default']['email'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1)
        email.place(x=10 + password.winfo_width(), y=40, anchor='ne')

        self.new_user = Entry(self.tab3, width=29, bg=ups.data.details2, fg=ups.data.fgc, border=0, font=FONT_C, selectbackground=ups.data.bgc)
        self.new_user.place(x=100, y=10, width=self.log_sett.winfo_width() - 285, anchor='ne')
        self.new_user.insert(0, f"{ups.data.default_user}")

        self.new_email = Entry(self.tab3, width=29, bg=ups.data.details2, fg=ups.data.fgc, border=0, font=FONT_C, selectbackground=ups.data.bgc)
        self.new_email.place(x=100, y=40, width=self.log_sett.winfo_width() - 285, anchor='ne')
        self.new_email.insert(0, f"{ups.data.default_email}")

        self.apply_btn = Button(self.log_sett, text=ups.data.cust['apply_btn'], font=FONT_C, bg=ups.data.bgc, fg=ups.data.details1,
                                command=lambda: ups.cust_settings(
                                    self.user_entry.get(), self.new_email.get(), self.new_user.get(), (
                                        self.old_pwd_entry.get(), self.new_pwd_entry.get(), self.rep_pwd_entry.get())))


        # Create a frame within the Default panel to store Autoclose settings.
        self.autoclose = LabelFrame(self.tab3, text=ups.data.cust['right_panel_default']['autoclose'], height=75,
                                bg=ups.data.bgc, fg=ups.data.details1, font=FONT_F)
        user.update()
        self.autoclose.place(x=user.winfo_x(), y=75, width=self.log_sett.winfo_width() - 185 - user.winfo_x(), anchor='nw')
        autoclose_label = Label(self.autoclose, text=ups.data.cust['right_panel_default']['mins'], bg=ups.data.bgc, fg=ups.data.details1, font=FONT_C)
        autoclose_label2 = Label(self.autoclose, text=ups.data.cust['right_panel_default']['tip'], bg=ups.data.bgc, fg=ups.data.details1, font=FONT_C)
        autoclose_label.place(x=5, y=0, anchor='nw')
        autoclose_label2.place(x=5, y=25, anchor='nw')
        self.ac_spin = Spinbox(self.autoclose, from_=0, to=30, font=FONT_C, fg=ups.data.details1, bg=ups.data.bgc, bd=1,
            width=2, buttonbackground=ups.data.bgc, state='readonly', selectbackground=ups.data.accent,
            readonlybackground=ups.data.bgc, textvariable=ui.autoclose_mins, cursor='sb_v_double_arrow', command=update_mins)
        autoclose_label.update()
        self.ac_spin.place(x=autoclose_label.winfo_x() + autoclose_label.winfo_width(), y=0, anchor='nw')

        self.apply_btn.place(x=540, y=215, anchor='se')
        self.log_sett.bind("<Configure>", self.calc_width)


    def refresh_fields(self):
        """Refreshes the information in the user and email entry boxes and quits CustSettings instance"""
        ui.user_entry.delete(0, 'end')
        ui.email_combo.delete(0, 'end')
        ui.user_entry.insert(0, ups.data.jdata[ups.data.user]['pm_settings']['defaults']['user'])
        ui.email_combo.insert(0, ups.data.jdata[ups.data.user]['pm_settings']['defaults']['email'])

        self.log_sett.destroy()


    def calc_width(self, event):  # pylint: disable=unused-argument
        """Recalculate widget placement"""
        self.tab2.place(width=self.log_sett.winfo_width() - 175)
        self.user_entry.place(x=self.log_sett.winfo_width() - 185,  width=self.log_sett.winfo_width() - 200 - self.maxw)
        self.old_pwd_entry.place(x=self.log_sett.winfo_width() - 185,  width=self.log_sett.winfo_width() - 200 - self.maxw)
        self.new_pwd_entry.place(x=self.log_sett.winfo_width() - 185,  width=self.log_sett.winfo_width() - 200 - self.maxw)
        self.rep_pwd_entry.place(x=self.log_sett.winfo_width() - 185,  width=self.log_sett.winfo_width() - 200 - self.maxw)

        self.new_user.place(x=self.log_sett.winfo_width() - 185,  width=self.log_sett.winfo_width() - 200 - self.maxw)
        self.new_email.place(x=self.log_sett.winfo_width() - 185,  width=self.log_sett.winfo_width() - 200 - self.maxw)
        self.autoclose.place(width=self.log_sett.winfo_width() - 185 - self.autoclose.winfo_x())

        self.tab3.place(width=self.log_sett.winfo_width() - 285)

        self.apply_btn.place(x=self.log_sett.winfo_width() - 10, y=self.log_sett.winfo_height() - 10)


    def update_cust_settings(self, btn: str):
        """Shows the chosen panel in the Custom Settings window

        Args:
            btn (str): An indicator of which Button (tab) was clicked
        """
        if btn == 'login':
            self.tab3.place_forget()
            self.tab2.place(x=175, relheight=1, relwidth=0.7, anchor='nw')

            self.login_btn.config(text=ups.data.cust['update_cust_settings']['if_login']['login_btn'], bg=ups.data.bgc, fg=ups.data.details1,
                                    activebackground=ups.data.bgc, activeforeground=ups.data.details1)
            self.default_btn.config(text=ups.data.cust['update_cust_settings']['if_login']['default_btn'], bg=ups.data.shadow, fg=ups.data.details1,
                                    activebackground=ups.data.bgc, activeforeground=ups.data.details1)

        elif btn == 'default':
            self.tab2.place_forget()
            self.tab3.place(x=175, relheight=1, relwidth=0.7, anchor='nw')

            self.login_btn.config(text=ups.data.cust['update_cust_settings']['elif_default']['login_btn'], bg=ups.data.shadow, fg=ups.data.details1,
                                    activebackground=ups.data.bgc, activeforeground=ups.data.details1)
            self.default_btn.config(text=ups.data.cust['update_cust_settings']['elif_default']['default_btn'], bg=ups.data.bgc, fg=ups.data.details1,
                                    activebackground=ups.data.bgc, activeforeground=ups.data.details1)


def update_mins():
    """Updates the python variable with the tkinter variable"""
    ups.data.cd_mins = ui.autoclose_mins.get()


ui = PMUI()
