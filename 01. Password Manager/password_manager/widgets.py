"""Defines custom tkinter widgets used in the application"""
from tkinter import Frame, Entry, Button, SUNKEN, NE

from password_manager.data_management.all_data import data


class PWDEntry(Frame): # pylint: disable=too-many-ancestors
    """A Password Entry box including a button for toggling password visibility"""
    def __init__(self, master=None, image=None, **kwargs):
        width = kwargs.get('width')
        kwargs.pop('width', None)
        super().__init__(master, bd=0, width=width, takefocus=False)
        self.image = image
        self.entry = Entry(self, **kwargs)
        self.btn   = Button(
            self,
            background=data.colors['details2'],
            border=0,
            width=30,
            height=20,
            pady=0,
            relief=SUNKEN,
            highlightbackground=data.colors['details2'],
            highlightcolor=data.colors['details2'],
            highlightthickness=0,
            activebackground=data.colors['details2'],
            image=self.image,
            takefocus=False,
            cursor='hand2'
        )
        self.entry.place(relwidth=1, relheight=1)
        self.btn.place(width=39, relheight=1, anchor=NE)

        # This line is used instead of update() + btn.place in the .place method where it's buggy
        self.entry.bind('<Configure>', lambda event: self.btn.place(x=self.entry.winfo_width()))

    def place(self, **kwargs):
        """Overridden method to align all widgets on place execute"""
        super().place(**kwargs)
        self.entry.place(relwidth=1)

    def config(self, **kwargs):
        """Overridden method to set the sub-Entry Boxes details"""
        self.entry.config(**kwargs)

    def get(self):
        """Overridden method to get the sub-Entry Boxes details"""
        return self.entry.get()

    def delete(self, start, end):
        """Overriden method to delete sub-Entry Boxes content"""
        self.entry.delete(start, end)
