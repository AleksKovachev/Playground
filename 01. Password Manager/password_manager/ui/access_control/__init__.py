"""Contains common functionality for the Login and the SignUp operations"""
from enum import Enum
from tkinter import END

from password_manager.data_management.all_data import file_data, data
from password_manager.constants import FOCUS_IN, FOCUS_OUT, MOUSE_ENTER, MOUSE_LEAVE


class PassType(Enum):
    """Defines the password entry box. Password field or Repeat Password field"""
    NORMAL = 0
    REPEAT = 1


def field_clear(event, fields: tuple):
    """Manages the entry boxes default text

    Args:
        event (event): Used to check which widget is using the function
        fields (tuple): Contains the fields to clear. Defaults to None.
    """
    # If fields parameter is changed to dict instead of tuple - this no longer works as expected
    # Tuple map: 0: username field, 1: password field, 2: email field, 3: repeat password field
    if event.widget == fields[1]:
        field = fields[1]
        default = file_data.lang['field_clear']['password']
        is_password = PassType.NORMAL
    elif event.widget == fields[0]:
        field = fields[0]
        default = file_data.lang['field_clear']['user']
        is_password = False
    elif event.widget == fields[2]:
        field = fields[2]
        default = file_data.lang['field_clear']['email']
        is_password = False
    elif event.widget == fields[3]:
        field = fields[3]
        default = file_data.lang['field_clear']['repeat_password']
        is_password = PassType.REPEAT

    if event.type == FOCUS_IN:
        if field.get() == default and field.cget("fg") == data.colors['bgc']:
            field.delete(0, END)
            field.config(fg=data.colors['fgc'])
            if is_password == PassType.NORMAL:
                fields[1].config(show="✲")
            elif is_password == PassType.REPEAT:
                fields[3].config(show="✲")

    elif event.type == FOCUS_OUT:
        if field.get() == "":
            field.insert(0, default)
            field.config(fg=data.colors['bgc'])
            if is_password == PassType.NORMAL:
                fields[1].config(show="")
            elif is_password == PassType.REPEAT:
                fields[3].config(show="")


def eye_switch_color(event, icons: dict):
    """Defines color switching for the eye icon

    Args:
        event (event): Used to check if the Cursor has Entered or Left the Button
        icons (dict): A dictionary containing 4 icons in the form of tkinter PhotoImage
    """
    if event.type == MOUSE_ENTER:
        if event.widget['image'] == str(icons['hide']):
            event.widget['image'] = icons['hide_hover']
        elif event.widget['image'] == str(icons['show']):
            event.widget['image'] = icons['show_hover']
    elif event.type == MOUSE_LEAVE:
        if event.widget['image'] == str(icons['show_hover']):
            event.widget['image'] = icons['show']
        elif event.widget['image'] == str(icons['hide_hover']):
            event.widget['image'] = icons['hide']
