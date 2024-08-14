"""Defines the class responsible for the Sign Up window"""

from tkinter import Label, Button, Entry, Canvas, Frame, TOP, E, W, CENTER

from password_manager.constants import FONT_B, FONT_C, FONT_D
from password_manager.data_management.all_data import file_data, data
from password_manager.widgets import PWDEntry
from password_manager.ui.base_ui import Window

#+ pylint: disable=unused-argument


class SignUpBase(Window):
    """Responsible for the Sign-up operations"""

    def __init__(self):
        super().__init__(root=data.wins['login'])

        self.setup(width=450, height=490)
        self.define_icons()
        self.draw_ui()

    def setup(self, width, height):
        """Create and set up the signup window"""
        super().setup(width=width, height=height)
        self.title(file_data.lang['signup']['title'])
        data.wins['reg'] = self

        self.protocol('WM_DELETE_WINDOW', self._destroy_sequence)
        self.resizable(False, False)

        self.root.wm_attributes('-disabled', True)
        # Make the signup window always on top
        self.attributes('-topmost', True)

    def _destroy_sequence(self):
        """Upon clicking X close the signup window and show the main signin one"""
        self.destroy()
        data.wins['reg'] = None
        self.root.deiconify()
        self.root.wm_attributes('-disabled', False)

    def define_ui(self):
        """Defines the UI widgets for the SignUp window"""
        self._define_canvas()
        self._define_labels()
        self._define_entry_boxes()
        self._define_frames()
        self._define_buttons()

    def draw_ui(self):
        """Draws the UI for the SignUp window"""
        self.define_ui()
        self._draw_canvas()
        self._draw_frames()
        self._draw_labels()
        self._draw_entry_boxes()
        self._draw_buttons()

    def _define_canvas(self):
        """Defines the SignUp window's canvas for the logo"""
        self.widgets['reg_canvas'] = Canvas(
            master=self, height=200, width=200, bg=data.colors['bgc'], highlightthickness=0)

    def _define_frames(self):
        """Defines the Separators for the icons in the entry boxes"""
        common = {'master': self, 'bg': data.colors['bgc'], 'bd': 0, 'width': 2, 'height': 28}
        self.widgets['sep1'] = Frame(**common)
        self.widgets['sep2'] = Frame(**common)
        self.widgets['sep3'] = Frame(**common)
        self.widgets['sep4'] = Frame(**common)

    def _define_labels(self):
        """Defines Labels"""
        self.widgets['reg_text'] = Label(
            self,
            text=file_data.lang['signup']['reg_text'],
            background=data.colors['bgc'],
            foreground=data.colors['details1'],
            font=FONT_B
        )

        common = {
            'master': self,
            'background': data.colors['details2'],
            'border': 0,
            'width': 38,
            'height': 29,
            'text': '  ',
            'compound': 'left'
        }

        self.widgets['user_icon_bg']   = Label(**common, image=self.icons['user_icon'])
        self.widgets['email_icon_bg']  = Label(**common, image=self.icons['email_icon'])
        self.widgets['pass_icon_bg']   = Label(**common, image=self.icons['pass_icon'])
        self.widgets['repeat_icon_bg'] = Label(**common, image=self.icons['pass_icon'])

    def _define_entry_boxes(self):
        """Defines Entry boxes"""
        common = {
            'master': self,
            'font': FONT_D,
            'background': data.colors['details2'],
            'foreground': data.colors['bgc'],
            'border': 0,
            'width': 21
        }
        self.widgets['entrance_user'] = Entry(**common)
        self.widgets['entrance_email'] = Entry(**common)
        self.widgets['pass'] = PWDEntry(**common, image=self.icons['no_eye_icon'])
        self.widgets['re_pass'] = PWDEntry(**common, image=self.icons['no_eye_icon'])

    def _define_buttons(self):
        """Defines Buttons"""
        self.widgets['e_btn'] = Button(
            self,
            text=file_data.lang['signup']['e_btn'],
            width=15,
            font=FONT_C,
            background=data.colors['bgc'],
            foreground=data.colors['details1'],
            takefocus=0
        )

    def _draw_canvas(self):
        """Draws the SignUp window's canvas and the logo on it"""
        self.widgets['reg_canvas'].create_image(100, 100, image=self.icons['logo2'])
        self.widgets['reg_canvas'].pack(side=TOP)

    def _draw_frames(self):
        """Draws the frame for the separators in the entry boxes"""
        self.widgets['sep1'].place(x=83, y=265, anchor=E)
        self.widgets['sep2'].place(x=83, y=310, anchor=E)
        self.widgets['sep3'].place(x=83, y=355, anchor=E)
        self.widgets['sep4'].place(x=83, y=400, anchor=E)

    def _draw_labels(self):
        """Draws the Labels"""
        self.widgets['reg_text'].place(relx=0.5, y=210, anchor=CENTER)
        self.widgets['user_icon_bg'].place(x=50, y=265, anchor=W)
        self.widgets['email_icon_bg'].place(x=50, y=310, anchor=W)
        self.widgets['pass_icon_bg'].place(x=50, y=355, anchor=W)
        self.widgets['repeat_icon_bg'].place(x=50, y=400, anchor=W)

    def _draw_entry_boxes(self):
        """Draws the Entry boxes"""
        # Shortcut for the text in the chosen language
        text = file_data.lang['signup']
        self.widgets['user_icon_bg'].update()
        x_pos = self.widgets['user_icon_bg'].winfo_x() + self.widgets['user_icon_bg'].winfo_width()

        self.widgets['entrance_user'].place(x=x_pos, y=265, width=310, anchor=W)
        self.widgets['entrance_user'].focus()
        self.widgets['entrance_email'].place(x=x_pos, y=310, width=310, anchor=W)
        self.widgets['entrance_email'].insert(0, text['entrance_email'])
        height = self.widgets['entrance_email'].winfo_reqheight()
        self.widgets['pass'].place(x=x_pos, y=355, width=310, height=height, anchor=W)
        self.widgets['pass'].entry.insert(0, text['entrance_pass'])
        self.widgets['re_pass'].place(x=x_pos, y=400, width=310, height=height, anchor=W)
        self.widgets['re_pass'].entry.insert(0, text['repeat_pass'])

    def _draw_buttons(self):
        """Draws the Buttons"""
        self.widgets['e_btn'].place(relx=0.5, y=450, anchor=CENTER)
