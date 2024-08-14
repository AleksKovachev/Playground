"""Defines main window's event bindings and some functions used in the bindings"""
import re
from tkinter import END, INSERT

from password_manager.data_management.all_data import data
from password_manager.data_management import update_list
from . import search_creds


def bind_events():
    """Binds events to functionality"""
    data.wins['root'].bind("<Configure>", data.wins['root'].calc_widgets)
    data.wins['root'].bind('<ButtonRelease-1>', unset_focus)
    data.wins['root'].bind('<Button-1>', mouseclick_check)
    data.wins['root'].bind("<MouseWheel>", on_entry_up_down)
    data.wins['root'].bind_all('<Motion>', data.reset_timer)
    data.wins['root'].bind_all('<Any-ButtonPress>', data.reset_timer)
    data.wins['root'].bind_all('<Any-KeyPress>', data.reset_timer)
    #* The add='+' arg adds this binding to the already existing binding for the arrow buttons
    data.wins['root'].bind_class(
        'Spinbox', "<B1-Motion>", data.wins['root'].spinbox_controls, add='+')
    data.wins['root'].bind_class('Spinbox', "<Button-1>", save_mouse_position, '+')
    data.wins['root'].bind_class('Spinbox', "<MouseWheel>", data.wins['root'].spinbox_controls)
    data.wins['root'].bind_class(
        'Entry',
        '<Button-3>',
        lambda event: data.wins['root'].widgets['r_click_popup'].post(event.x_root, event.y_root)
    )
    data.wins['root'].bind_class(
        'TCombobox',
        '<Button-3>',
        lambda event: data.wins['root'].widgets['r_click_popup'].post(event.x_root, event.y_root)
    )
    data.wins['root'].bind_class('Entry', "<Control-BackSpace>", ctrl_cursor)
    data.wins['root'].bind_class('Entry', "<Control-Delete>", ctrl_cursor)
    data.wins['root'].bind_class('TCombobox', "<Control-BackSpace>", ctrl_cursor)
    data.wins['root'].bind_class('TCombobox', "<Control-Delete>", ctrl_cursor)
    data.wins['root'].widgets['file_menu'].bind('<Motion>', data.reset_timer)
    data.wins['root'].widgets['file_menu'].bind('<Any-ButtonPress>', data.reset_timer)
    data.wins['root'].widgets['file_menu'].bind('<Any-KeyPress>', data.reset_timer)
    data.wins['root'].widgets['website_entry'].bind("<Down>", on_entry_up_down)
    data.wins['root'].widgets['website_entry'].bind("<Up>", on_entry_up_down)
    data.wins['root'].widgets['website_entry'].bind('<Return>', check_autocomplete_state)
    data.wins['root'].widgets['website_entry'].bind('<KeyRelease>', autocomplete)
    data.wins['root'].widgets['website_entry'].bind('<Button-1>', autocomplete)
    data.wins['root'].widgets['website_entry'].bind("<Tab>", complete_website)
    data.wins['root'].widgets['password_entry'].btn.bind("<Enter>", eye_switch_color)
    data.wins['root'].widgets['password_entry'].btn.bind("<Leave>", eye_switch_color)
    data.wins['root'].widgets['password_entry'].entry.bind('<Return>', data.wins['root'].save_data)
    data.wins['root'].widgets['autocomplete_box'].bind("<<ListboxSelect>>", autocomplete_func)
    data.wins['root'].widgets['email_combo'].bind(
            '<<ComboboxSelected>>', lambda event: event.widget.selection_clear())
    data.wins['root'].widgets['search_btn'].bind(
        '<Configure>', lambda event: data.wins['root'].widgets['opt_btn'].place(
            x=(data.wins['root'].widgets['search_btn'].winfo_x()
                + data.wins['root'].widgets['search_btn'].winfo_width())))


def ctrl_cursor(event):
    """Controls the cursor movement in Entry Box widgets when using Ctrl.
    Example: Ctrl + Left Arrow will move left until non-word character.
    Example: Ctrl + BackSpace will delete the last word.
    """
    cursor_pos = event.widget.index(INSERT)
    if event.widget.cget("show"):
        delete_range = (0, cursor_pos) if event.keysym == "BackSpace" else (cursor_pos, END)
        event.widget.delete(*delete_range)
        return
    idx = 0

    content = event.widget.get()
    if event.keysym == "BackSpace":
        if match_char := re.search(r"\W+$", content[:cursor_pos]):
            idx = match_char.start()
        elif match_word := re.search(r"\W\w*$", content[:cursor_pos]):
            idx = match_word.start() + 1

        event.widget.delete(idx, cursor_pos)

    elif event.keysym == "Delete":
        cursor_pos = event.widget.index(INSERT)

        if match_word := re.search(r"^\w+", content[cursor_pos:]):
            idx = len(content) - len(content[cursor_pos:]) + match_word.end()
        elif match_char := re.search(r"^\W+", content[cursor_pos:]):
            idx = len(content) - len(content[cursor_pos:]) + match_char.end()

        event.widget.delete(cursor_pos, idx)


def unset_focus(event):
    """Set focus to the window instead of a widget if mouse clicked outside exclusions"""
    exclusions = [data.wins['root'].widgets['lang_frame'], data.wins['root'].widgets['lang_btn']]
    if event.widget not in data.wins['root'].widgets['lang_opts'] + exclusions:
        data.wins['root'].widgets['lang_frame'].place_forget()


def mouseclick_check(event):
    """Check if mouse clicked in the website entry box"""
    # Reset the autoclose timer.
    data.reset_timer()
    # Hide the autocomplete box if mouse click outside of the website entry box
    if event.widget != data.wins['root'].widgets['website_entry']:
        data.wins['root'].widgets['autocomplete_box'].place_forget()
    # Remove the writing cursor if mouse click outside of any entry or combo box
    if event.widget not in (
        data.wins['root'].widgets['website_entry'],
        data.wins['root'].widgets['user_entry'],
        data.wins['root'].widgets['password_entry'].entry,
        data.wins['root'].widgets['email_combo']):
        data.wins['root'].focus()


def on_entry_up_down(event):
    """Defines the Autocomplete box arrow key response"""
    # Only work if the autocomplete box is visible
    if data.wins['root'].widgets['autocomplete_box'].winfo_ismapped():
        # Get the current selection
        selection = data.wins['root'].widgets['autocomplete_box'].curselection()[0]

        # Check if Up/Down keys were pressed or mouse scroll up/down was used.
        if event.keysym == 'Up' or event.delta == 120:
            selection += -1

        if event.keysym == 'Down' or event.delta == -120:
            selection += 1

        # Change the selection based on the input
        if 0 <= selection < data.wins['root'].widgets['autocomplete_box'].size():
            data.wins['root'].widgets['autocomplete_box'].selection_clear(0, END)
            data.wins['root'].widgets['autocomplete_box'].select_set(selection)


def save_mouse_position(event):
    """Saves the current mouse position"""
    data.spinbox_ypos = -event.y


def autocomplete_func(event=None): # pylint: disable=unused-argument
    """Upon selecting an item, send it to the search function"""
    # Hide the autocomplete box
    data.wins['root'].widgets['autocomplete_box'].place_forget()
    # Get the selection
    selection = data.wins['root'].widgets['autocomplete_box'].get(
        data.wins['root'].widgets['autocomplete_box'].curselection())
    # Clear the autocomplete box data and the text in the website entry box
    data.wins['root'].widgets['autocomplete_box'].delete(0, END)
    data.wins['root'].widgets['website_entry'].delete(0, END)
    # Put the selected item in the website entry box
    data.wins['root'].widgets['website_entry'].insert(0, selection)
    # Search and display the credentials
    search_creds()
    data.wins['root'].focus()


def check_autocomplete_state(event): # pylint: disable=unused-argument
    """Determines which function <Return> should execute"""
    # If the autocomplete box is visible - execute its selection. Else - execute the search button.
    if data.wins['root'].widgets['autocomplete_box'].winfo_ismapped():
        autocomplete_func()
    else:
        search_creds()


def autocomplete(event):
    """Autocomplete Function for the Search"""
    # Get the user search
    web = data.wins['root'].widgets['website_entry'].get()
    # Check if something's written | if Up or Down keys were clicked | if mouse button was clicked
    if web != "" and (event.keysym not in ("Up", "Down") or event.type == 4):
        # Get data and order by relevancy
        platforms = data.get_db_data('entries', 'platform', single=False)
        data_ = [platform[0] for platform in platforms if web.lower() in platform[0].lower()]
        data_ = update_list(data_, web)

        # Only show the 5 most relevant results
        if len(data_) > 5:
            data_ = data_[:5]

        # Hide autocomplete box if results are no results
        if not data_:
            data.wins['root'].widgets['autocomplete_box'].place_forget()
            return

        # If There's only one result and it exactly matches the search hide the autocomplete box
        if web.lower() == data_[0].lower() and len(data_) < 2:
            data.wins['root'].widgets['autocomplete_box'].place_forget()
            return
        # Get the width for the autocomplete box from the search bar
        # Get the height - from the number of entries
        data.wins['root'].widgets['autocomplete_box'].place(
            x=165,
            y=270,
            anchor='nw',
            width=data.wins['root'].widgets['website_entry'].winfo_width()
        )
        data.wins['root'].widgets['autocomplete_box']['height'] = len(data_)
        update_autocomplete(data_, event)
    elif web == "" and data.wins['root'].widgets['autocomplete_box'].winfo_ismapped():
        data.wins['root'].widgets['autocomplete_box'].place_forget()


def complete_website(event):  # pylint: disable=unused-argument
    """Autocomplete the row"""
    # Only execute if the autocomplete box is visible and the search isn't exactly the same as
    # the first (most relevant) autocomplete suggestion
    if (data.wins['root'].widgets['autocomplete_box'].winfo_ismapped()
        and (data.wins['root'].widgets['website_entry'].get()
                != data.wins['root'].widgets['autocomplete_box'].get(
                    data.wins['root'].widgets['autocomplete_box'].curselection()[0]))):
        # Get the selected entry from the autocomplete box and replace the search
        selection = data.wins['root'].widgets['autocomplete_box'].get(
            data.wins['root'].widgets['autocomplete_box'].curselection()[0])
        data.wins['root'].widgets['website_entry'].delete(0, END)
        data.wins['root'].widgets['website_entry'].insert(0, selection)
        return 'break'  # Return 'break' to eliminate the built-in Tab function to switch fields
    return None


def update_autocomplete(data_: list, event):
    """Update the list for the autocomplete

    Args:
        data (list): A list with all relevant results
    """
    # Delete everything in the autocomplete box
    data.wins['root'].widgets['autocomplete_box'].delete(0, END)
    for entry in data_:
        # Populate the autocomplete box
        data.wins['root'].widgets['autocomplete_box'].insert(END, entry)
    # Have the first value selected so that the Up and Down keys can work
    if event.keysym not in ("Up", "Down"):
        data.wins['root'].widgets['autocomplete_box'].selection_set(first=0, last=None)


def eye_switch_color(event):
    """Defines color switching for the eye icon on mouseover"""
    if event.type == '7':  # Enter
        if (data.wins['root'].widgets['password_entry'].btn['image']
                == str(data.wins['root'].icons['no_eye_icon'])):
            data.wins['root'].widgets['password_entry'].btn['image'] = \
                data.wins['root'].icons['no_eye_icon_h']
        elif (data.wins['root'].widgets['password_entry'].btn['image']
                == str(data.wins['root'].icons['eye_icon'])):
            data.wins['root'].widgets['password_entry'].btn['image'] = \
                data.wins['root'].icons['eye_icon_h']
    elif event.type == '8':  # Leave
        if (data.wins['root'].widgets['password_entry'].btn['image']
                == str(data.wins['root'].icons['eye_icon_h'])):
            data.wins['root'].widgets['password_entry'].btn['image'] = \
                data.wins['root'].icons['eye_icon']
        elif (data.wins['root'].widgets['password_entry'].btn['image']
                == str(data.wins['root'].icons['no_eye_icon_h'])):
            data.wins['root'].widgets['password_entry'].btn['image'] = \
                data.wins['root'].icons['no_eye_icon']
