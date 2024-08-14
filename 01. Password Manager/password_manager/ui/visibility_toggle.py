"""Contains functionality for toggling password visibility."""
from enum import Enum
from tkinter import PhotoImage

from ..data_management.all_data import data


class PwdButton(Enum):
    """Defines the two types of password eye buttons"""
    OLD_PASSWORD = 0
    PASSWORD = 1
    REPEAT = 2


def check_pass_btn(btn: PwdButton, widgets: dict, icons: dict):
    """Hides/Shows the password in the Password or the Repeat Password Entry box
    based on which Eye Button (icon) was clicked.

    Args:
        btn (PwdButton): Determines which method should be executed
    """
    if btn == PwdButton.PASSWORD:
        show_pass(
            widgets['entrance_pass'],
            icons['eye_icon_h'],
            icons['no_eye_icon_h']
        )
    elif btn == PwdButton.REPEAT:
        show_pass(
            widgets['repeat_pass'],
            icons['eye_icon_h'],
            icons['no_eye_icon_h']
        )
    elif btn == PwdButton.OLD_PASSWORD:
        show_pass(
            widgets['old_pwd_entry'],
            icons['eye_icon_h'],
            icons['no_eye_icon_h']
        )


def show_pass(pass_field, eye_hover: PhotoImage, no_eye_hover: PhotoImage):
    """Hides/Shows the password in the entry box

    Args:
        pass_field (PWDEntry): Changes its character visuals. Contains Entry box and Button.
            Also used to check if the button below should have any effect.
        eye_hover (tkinter PhotoImage object): An icon
        no_eye_hover (tkinter PhotoImage object): An icon
    """
    if pass_field.entry.cget("fg") != data.colors['bgc']:
        if pass_field.btn['image'] == str(no_eye_hover):
            pass_field.btn['image'] = eye_hover
        elif pass_field.btn['image'] == str(eye_hover):
            pass_field.btn['image'] = no_eye_hover
        pass_field.entry["show"] = "✲" if pass_field.entry["show"] == "" else ""
