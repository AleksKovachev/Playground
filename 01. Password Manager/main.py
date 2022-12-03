"""A Simple Password Generator App"""

from tkinter import Toplevel, Label, Listbox, Scrollbar, Y, LEFT, RIGHT, END, BOTH
from tkinter.messagebox import askyesno, showinfo, showerror, showwarning
from string import ascii_letters, punctuation, digits
from random import randint, choice, shuffle
from math import floor
from data_files import logout
import data_files.updates as ups
from data_files.authenticate import Authenticate
from data_files.word_generator import gen_adj_noun
from data_files.ui import ui, ThemeChanger, update_backup_period


############################################################################################

# TODO Add 3-5 attempts for password login. Then store the next possible time a new attempt can be made.
#      When X number of wrong attempts were made - LOCK the user altogether and send an email with instructions
#      and UNLOCK code which will also reset the password. Instruct the user to change it INSTANTLY!
# TODO Add option for forgotten password
# TODO Minimize button of Sign-up window and Account list (Browse) window not working
# TODO Split data inito multiple files for every user.
# TODO Store accounts backup on a server

############################################################################################


Authenticate(ui.root)


# ---------------------------- CONSTANTS --------------------------------------------- #


FONT_A: tuple = ("CorsicaMX-Regular", 18, "normal")
FONT_B: tuple = ("CorsicaMX-Book", 14, "normal")
FONT_C: tuple = ("CorsicaMX-Book", 12, "normal")
FONT_F: tuple = ("CorsicaMX-Book", 10, "normal")


# ---------------------------- SEARCH ------------------------------------------- #


def check_data(data: dict) -> list | None:
    """Checks the data for existing platforms

    Args:
        data (dict): The date to be checked for similar results to what the user is searching for

    Returns:
        list | None: List of all matching results. None if exact match (not case-sensitive).
    """
    # Get the message parts in the chosen language
    cdat: str = ups.data.lang.main['check_data']

    # Define a list of keys that are similar to the one in search
    similar_keys = []
    for key, value in data.items():
        # Display the credentials if the key in search matches any keys in the data exactly (not case sensitive)
        if ui.website_entry.get().lower() == key.lower():
            showinfo(title=f"{cdat['title']} {key}", message=f"{cdat['message'][0]} {data[key]['user']}\n{cdat['message'][1]} " \
                            f"{data[key]['email']}\n{cdat['message'][2]} {data[key]['password']}")
            ui.password_entry.clipboard_clear()
            ui.password_entry.clipboard_append(value['password'])
            auto_fill(key, data[key]['user'], data[key]['email'], data[key]['password'])
            return None

        # Collect all keys that contain the search in themselves and return them
        if ui.website_entry.get().lower() in key.lower():
            similar_keys.append(key)

    return similar_keys


def search_creds(*args):
    """Searches the credentials for the specified website

    Args:
        *args (event): Used by tkinter binding. This function is used as standalone a as well
        as with tkinter binding which is why "*args" is used instead of "event"
    """
    # Get the message parts in the chosen language
    scred: str = ups.data.lang.main['search_creds']
    # Get the user search
    web: str = ui.website_entry.get()

    # Display an error if a search was initiated but the field is empty
    if (len(args) != 1 or args[0] != "Browse") and not web:
        showerror(title=scred['showerror']['title'], message=scred['showerror']['message'])
        return

    data: dict = ups.data.jdata[ups.data.user]['entries'].copy()

    # If the Browse button was clicked display all platforms
    if len(args) == 1 and args[0] == "Browse":
        win2(data, None)
        return

    # Collect all keys similar to the one in search
    similar_keys: list | None = check_data(data)

    if similar_keys is None:
        return

    # Display the credentials if only one similar key was found
    if len(similar_keys) == 1:
        showinfo(title=f"{scred['showinfo']['title']} {similar_keys[0]}", message=f"{scred['showinfo']['message'][0]} " \
            f"{data[similar_keys[0]]['user']}\n{scred['showinfo']['message'][1]} {data[similar_keys[0]]['email']}\n" \
                    f"{scred['showinfo']['message'][2]} {data[similar_keys[0]]['password']}")
        key: str = similar_keys[0]
        auto_fill(key, data[key]['user'], data[key]['email'], data[key]['password'])
    # Display a window with all similar keys if multiple were found
    elif len(similar_keys) > 1:
        approved_accounts: dict = {acc:creds for acc, creds in data.items() if acc in similar_keys}
        win2(approved_accounts, web, 200)
    # Display a dialog to browse the data if no similar keys were found
    elif askyesno(title=scred['askyesno']['title'], message=scred['askyesno']['message']):
        win2(data, None)


# ---------------------------- Auto Fill ---------------------------------------- #


def auto_fill(website: str, user: str, email: str, password: str):
    """Automatically fills the entry boxes with the found creds

    Args:
        website (str): The website to autofill
        user (str): The user to autofill
        email (str): The email to autofill
        password (str): The password to autofill
    """
    ui.website_entry.delete(0, END)
    ui.user_entry.delete(0, END)
    ui.password_entry.delete(0, END)
    ui.email_combo.delete(0, END)
    ui.website_entry.insert(0, website)
    ui.user_entry.insert(0, user)
    ui.password_entry.insert(0, password)
    ui.email_combo.insert(0, email)


# ---------------------------- Second Window ----------------------------------- #


def win2(data: dict, entry: str, custom_height: int = 450):
    """Opens a new window with a list of all available accounts

    Args:
        data (dict): A dictionary wth the data to process
        entry (str): Checking what's written in the website entry box
        custom_height (int, optional): Setting the window's height. Defaults to 450.
    """

    def copycontents(event):  # pylint: disable=unused-argument
        """Gets current selection from listbox"""
        # Hide this window
        results.withdraw()
        # Delete what the user has entered and fill the name that the user clicked
        ui.website_entry.delete(0, END)
        ui.website_entry.insert(0, listbox.get(listbox.curselection()))
        # Initiate Search Creds to display the credentials and autofill the fields
        search_creds()
        results.destroy()

    # Create a new window with the following parameters and make the main window unclickable.
    results = Toplevel(ui.root)
    results.title(ups.data.lang.main['win2']['title'])
    win2_width = 300
    root_xcenter = ui.root.winfo_x() + ui.root.winfo_width() / 2
    root_ycenter = ui.root.winfo_y() + ui.root.winfo_height() / 2
    results.geometry(f'{win2_width}x{custom_height}+{int(root_xcenter - win2_width / 2)}+{int(root_ycenter - custom_height / 2)}')
    results.resizable(False, True)
    results.minsize(0, 200)
    results.config(padx=50, pady=20, bg=ups.data.bgc)
    results.iconbitmap(r'data_files\icons\icon.ico')
    results.grab_set()

    # Label
    choose_acc = Label(results, text=ups.data.lang.main['win2']['choose_acc'], font=FONT_B, fg=ups.data.details1, bg=ups.data.bgc)
    choose_acc.pack()

    # Scrollbar
    scrollbar = Scrollbar(results)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Listbox
    listbox = Listbox(results, font=FONT_B, fg=ups.data.details1, bg=ups.data.bgc, width=30,
                        highlightthickness=0, yscrollcommand=scrollbar.set)

    # Get a list of all accounts. Order it by displaying accounts that start with the search
    # first and then alphabetically order the accounts that contain the search elsewhere.
    accounts = list(data)
    if entry is not None:
        accounts = ups.update_list(accounts, entry)

    # Populate the window with the results.
    for account in accounts:
        listbox.insert(accounts.index(account), account)
    listbox.bind("<<ListboxSelect>>", copycontents)
    listbox.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=listbox.yview)


# ---------------------------- SAVE PASSWORD --------------------------------#


def save_data(*args):  # pylint: disable=unused-argument
    """Saves the data from the entry fields

    Args:
        *args (event): Used by tkinter binding. This method is used by a tkinter button as well
        as tkinter binding which is why "*args" is used instead of "event"
    """
    # Get the message parts in the chosen language
    sdat = ups.data.lang.main['save_data']
    # Save the credentils to a dictionary
    data = {ui.website_entry.get(): {"user": ui.user_entry.get(), "email": ui.email_combo.get(), "password": ui.password_entry.get()}}

    # Show error if any of the fields is empty
    if any((ui.website_entry.get() == "", ui.email_combo.get() == "", ui.user_entry.get() == "", ui.password_entry.get() == "")):
        showwarning(title=sdat['showwarning']['title'], message=sdat['showwarning']['message'])
        return

    # Ask to overwrite data if platform with this name already exists
    overwrite = next((askyesno(title=sdat['askyesno1']['title'],
        message=f"{sdat['askyesno1']['message'][0]} {ui.website_entry.get()}.\n{sdat['askyesno1']['message'][1]}")
            for key in ups.data.jdata[ups.data.user]["entries"] if key.lower() == ui.website_entry.get().lower()), True)

    # Display the credentials and a confirmation dialog
    if overwrite and askyesno(title=ui.website_entry.get(), message=f"{sdat['askyesno2'][0]} {ui.email_combo.get()}\n{sdat['askyesno2'][1]} " \
        f"{ui.user_entry.get()}\n{sdat['askyesno2'][2]} {ui.password_entry.get()}\n\n{sdat['askyesno2'][3]}"):

        # Clear all fields, update the opened data and save the creds to disk.
        clear_all()
        ups.data.jdata[ups.data.user]['entries'].update(data)
        ups.data.save_data()


# ---------------------------- AUTO COMPLETE ------------------------------------ #


def autocomplete(event):
    """Autocomplete Function for the Search"""
    # Get the user search
    web = ui.website_entry.get()
    # Check if something's written, check uf Up or Down keys were clicked, check if mouse button was clicked
    if web != "" and (event.keysym not in ("Up", "Down") or event.type == 4):
        # Get data and order by relevancy
        data = [key for key in ups.data.jdata[ups.data.user]['entries'] if web.lower() in key.lower()]
        data = ups.update_list(data, web)

        # Show autocomplete box if 5 or less results were found
        if 0 < len(data) <= 5:
            # If There's only one result and it matches the search exactly - hide the autocomplete box
            if web.lower() == data[0].lower() and len(data) < 2:
                ui.autocomplete_box.place_forget()
                return
            # Get the width for the autocomplete box from the search bar and the height - from the number of entries
            ui.autocomplete_box.place(x=165, y=270, anchor='nw', width=ui.website_entry.winfo_width())
            ui.autocomplete_box['height'] = len(data)
            update_autocomplete(data, event)
        # Hide autocomplete box if results are more than 5 or none
        elif not data or len(data) > 5:
            ui.autocomplete_box.place_forget()
    # Never show autocomplete box if nothing's in the search bar
    elif web == "":
        ui.autocomplete_box.place_forget()


def update_autocomplete(data: list, event):
    """Update the list for the autocomplete

    Args:
        data (list): A list with all relevant results
    """
    # Delete everything in the autocomplete box
    ui.autocomplete_box.delete(0, END)
    for entry in data:
        # Populate the autocomplete box
        ui.autocomplete_box.insert(END, entry)
    # Have the first value selected so that the Up and Down keys can work
    if event.keysym not in ("Up", "Down"):
        ui.autocomplete_box.selection_set(first=0, last=None)


def mouseclick_check(event):
    """Check if mouse clicked in the website entry box"""
    # Reset the autoclose timer. The dummy arg is because this func is bound so it takes 'event' as arg
    ups.data.reset_timer('dummy')
    # Hide the autocomplete box if mouse click outside of the website entry box
    if event.widget != ui.website_entry:
        ui.autocomplete_box.place_forget()
    # Remove the writing cursor if mouse click outside of any entry or combo box
    if event.widget not in (ui.website_entry, ui.user_entry, ui.password_entry, ui.email_combo):
        ui.root.focus()


def autocomplete_func(event):  # pylint: disable=unused-argument
    """Upon selecting an item, send it to the search function"""
    # Hide the autocomplete box
    ui.autocomplete_box.place_forget()
    # Get the selection
    selection = ui.autocomplete_box.get(ui.autocomplete_box.curselection())
    # Clear the autocomplete box data and the text in the website entry box
    ui.autocomplete_box.delete(0, END)
    ui.website_entry.delete(0, END)
    # Put the selected item in the website entry box
    ui.website_entry.insert(0, selection)
    # Search and display the credentials
    search_creds()
    ui.root.focus()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    """Generates a password considering the ui.val value for the type"""
    # Define allowed delimiters and chose a random one
    delimits = ("-", "_", "*", "^", "&", "@", "#", ".", "/", "+", "=", ";", ":", "|", "$")
    delimiter = choice(delimits)

    # Define the total number of characters for the password
    if ui.check_fixed.get() == 1:
        total_chars = ui.pass_length.get()
    else:
        total_chars = randint(12, 35)

    # Check the prefered password type
    match ui.val.get():
        # If "secure" is selected
        case "1":
            # Redifine the character range if Secure option was chosen without specifying password length
            if ui.check_fixed.get() == 0:
                total_chars = randint(6, 20)
            password = rand_pass(total_chars)
        # If "easy" is selected
        case "2":
            # Generate the phrase +/- a few characters
            password = gen_adj_noun(maxlen=total_chars - 5, minlen=total_chars - 7, delimiter=delimiter)
            # Add random characters at the end for security until total_chars count is reached
            add_pass = [choice((choice(ascii_letters), choice(digits), choice(punctuation))) for _ in range(total_chars - len(password) - 1)]
            shuffle(add_pass)
            # The final password is the generated phrase with random delimiter + the same delimiter + shuffled random characters
            password += delimiter + ''.join(add_pass)
        # If combo is selected
        case "3":
            # Generate a "coded" version of a phrase. No additional characters in this mode.
            password = gen_adj_noun(maxlen=total_chars - 5, minlen=total_chars - 7, delimiter=delimiter, coded=True)
        # If secure combo is selected
        case "4":
            # Generate a "coded" version of a phrase
            password = gen_adj_noun(maxlen=total_chars - 5, minlen=total_chars - 7, delimiter=delimiter, coded=True)
            # Add random characters at the end for security until total_chars count is reached
            add_pass = [choice((choice(ascii_letters), choice(digits), choice(punctuation))) for _ in range(total_chars - len(password))]
            shuffle(add_pass)
            # The final password is the generated phrase with random delimiter + shuffled random characters
            password += ''.join(add_pass)

    # Auto-insert it into the password Entry box and copy to clipboard
    ui.password_entry.delete(0, END)
    ui.password_entry.insert(0, password)
    ui.password_entry.clipboard_clear()
    ui.password_entry.clipboard_append(password)


def rand_pass(total_chars):
    """Generates a random-character password"""
    # Choose between 2 and half of the total characters to be random digits
    pass_nums = [choice(digits) for _ in range(randint(2, floor(total_chars/2)))]
    # Choose between 2 and 40% of total chars to be random acceptable punctuation characters
    pass_chars = [choice(punctuation) for _ in range(randint(2, floor(0.4 * total_chars)))]
    # Get the number of already generated characters and generate the rest of the total as random letters
    pass_letters = [choice(ascii_letters) for _ in range(total_chars-len(pass_nums + pass_chars))]

    # Combine the lists in a single one, shuffle it and return it as a string.
    password_list = pass_letters + pass_nums + pass_chars
    shuffle(password_list)
    return "".join(password_list)


# ---------------------------- SHOW PASSWORD ------------------------------------ #


def show_pass():
    """Hides/Shows the password in the entry box"""
    # Switch icons
    if ui.eye_btn['image'] == str(ui.no_eye_icon_h):
        ui.eye_btn['image'] = ui.eye_icon_h
    elif ui.eye_btn['image'] == str(ui.eye_icon_h):
        ui.eye_btn['image'] = ui.no_eye_icon_h

    ui.password_entry['show'] = '✲' if ui.password_entry['show'] == "" else ""


# ---------------------------- Clear All ---------------------------------------- #


def clear_all():
    """Clears all entered creds and populates the default username and email"""
    ui.website_entry.delete(0, END)
    ui.user_entry.delete(0, END)
    ui.user_entry.insert(0, ups.data.jdata[ups.data.user]['pm_settings']['defaults']['user'])
    ui.password_entry.delete(0, END)
    ui.email_combo.delete(0, END)
    ui.emails.set(ups.data.jdata[ups.data.user]['pm_settings']['defaults']['email'])
    ui.website_entry.focus()


# ---------------------------- UPDATES ------------------------------------------ #


def update_emails():
    """Updates the email list for the combobox geting all existing emails in the current account"""
    ui.email_combo['values'] = tuple(
        {ups.data.jdata[ups.data.user]['entries'][i]['email'] for i in ups.data.jdata[ups.data.user]['entries']})


def check_autocomplete_state(event):
    """Determines which function <Return> should execute"""
    # If the autocomplete box is visible - execute its selection. Else - execute the search button.
    if ui.autocomplete_box.winfo_ismapped():
        autocomplete_func(event)
    else:
        search_creds(event)


def on_entry_up_down(event):
    """Defines the Autocomplete box arrow key response"""
    # Only work if the autocomplete box is visible
    if ui.autocomplete_box.winfo_ismapped():
        # Get the current selection
        selection = ui.autocomplete_box.curselection()[0]

        # Check if Up/Down keys were pressed or mouse scroll up/down was used.
        if event.keysym == 'Up' or event.delta == 120:
            selection += -1

        if event.keysym == 'Down' or event.delta == -120:
            selection += 1

        # Change the selection based on the input
        if 0 <= selection < ui.autocomplete_box.size():
            ui.autocomplete_box.selection_clear(0, END)
            ui.autocomplete_box.select_set(selection)


def complete_website(event):  # pylint: disable=unused-argument
    """Autocomplete the row"""
    # Only execute if the autocomplete box is visible and the search isn't exactly the same as the first (most relevant) autocomplete suggestion
    if ui.autocomplete_box.winfo_ismapped() and ui.website_entry.get() != ui.autocomplete_box.get(ui.autocomplete_box.curselection()[0]):
        # Get the selected entry from the autocomplete box and replace the search
        selection = ui.autocomplete_box.get(ui.autocomplete_box.curselection()[0])
        ui.website_entry.delete(0, END)
        ui.website_entry.insert(0, selection)
        return 'break'  # Return 'break' to eliminate the built-in Tab function to switch fields


def eye_switch_color(event):
    """Defines color switching for the eye icon on mouseover"""
    if event.type == '7':  # Enter
        if ui.eye_btn['image'] == str(ui.no_eye_icon):
            ui.eye_btn['image'] = ui.no_eye_icon_h
        elif ui.eye_btn['image'] == str(ui.eye_icon):
            ui.eye_btn['image'] = ui.eye_icon_h
    elif event.type == '8':  # Leave
        if ui.eye_btn['image'] == str(ui.eye_icon_h):
            ui.eye_btn['image'] = ui.eye_icon
        elif ui.eye_btn['image'] == str(ui.no_eye_icon_h):
            ui.eye_btn['image'] = ui.no_eye_icon


def expand_options():
    """Expands/Contracts the Options menu"""
    if ui.frame.winfo_ismapped():
        if int(ui.root.geometry().split('x')[1].split('+')[0]) == 560:
            ui.root.geometry(f'{ui.root.geometry()[:3]}x510')
        ui.opt_btn['bg'] = ups.data.bgc
        ui.opt_btn['fg'] = ups.data.details1
        ui.opt_btn['bd'] = 1
        ui.password_length.place_forget()
        ui.gen_btn.place_forget()
        ui.char_spinbox.place_forget()
        ui.radio1.place_forget()
        ui.radio2.place_forget()
        ui.radio3.place_forget()
        ui.radio4.place_forget()
        ui.frame.place_forget()
        ui.fixed_length.place_forget()
        ui.add_btn.place(x=165, y=415, anchor='w', width=455)
        ui.clear_btn.place(x=727, y=415, anchor='e')

    else:
        if int(ui.root.geometry().split('x')[1].split('+')[0]) < 600:
            ui.root.geometry(f'{ui.root.geometry()[:3]}x560')
        ui.opt_btn['bg'] = ups.data.details2
        ui.opt_btn['fg'] = ups.data.accent
        ui.opt_btn['bd'] = 0
        ui.gen_btn.place(x=720, y=420, anchor='e')
        ui.radio1.place(x=170, y=420, anchor='w')
        ui.radio1.update()
        rad1_x = 170 + ui.radio1.winfo_width()
        ui.radio2.place(x=rad1_x, y=420, anchor='w')
        ui.radio2.update()
        rad2_x = rad1_x + ui.radio2.winfo_width()
        ui.radio3.place(x=rad2_x, y=420, anchor='w')
        ui.radio3.update()
        rad3_x = rad2_x + ui.radio3.winfo_width()
        ui.radio4.place(x=rad3_x, y=420, anchor='w')
        ui.radio4.update()
        rad4_x = rad3_x + ui.radio4.winfo_width()
        ui.fixed_length.place(x=rad4_x + 8, y=420, anchor='w')
        ui.fixed_length.update()
        fl_x = rad4_x + ui.fixed_length.winfo_width()
        ui.password_length.place(x=fl_x + 7, y=420, anchor='w')
        ui.password_length.update()
        pl_x = fl_x + ui.password_length.winfo_width()
        ui.char_spinbox.place(x=pl_x + 7, y=420, anchor='w')
        ui.frame.place(x=165, y=420, anchor='w', width=ui.root.winfo_width() - 230)
        ui.add_btn.place(x=165, y=467, anchor='w', width=455)
        ui.clear_btn.place(x=727, y=467, anchor='e')


def save_mose_position(event):
    """Saves the current mouse position"""
    ups.data.spinbox_ypos = -event.y


# ---------------------------- UI SETUP ------------------------------- #


# Give a function to some menu items.
ui.color_menu.add_command(label=ups.data.lang.main['light_theme'],
        command=lambda: ui.theme_preset('light', ups.data.user), image=ui.light_icon, compound='left')
ui.color_menu.add_command(label=ups.data.lang.main['dark_theme'],
        command=lambda: ui.theme_preset('dark', ups.data.user), image=ui.dark_icon, compound='left')
ui.color_menu.add_separator()
ui.color_menu.add_command(label=ups.data.lang.main['custom_theme'],
        command=lambda: ThemeChanger(), image=ui.prefs_icon, compound='left')  # pylint: disable=unnecessary-lambda

# Populate the backup period menu
for index, bac_option in ups.data.backup_period.items():
    ui.backup_menu.add_radiobutton(label=bac_option, value=index, variable=ui.radio_var,
                                command=lambda index=index: update_backup_period(index, ups.data.user))

# Define an update function for the email combobox
ui.email_combo.configure(textvariable=ui.emails, postcommand=update_emails)
ui.email_combo.place(x=165, y=335, anchor='w', width=ui.root.winfo_width() - 230)


# Buttons
ui.file_menu.add_command(label=ups.data.lang.main['button1'], command=lambda: search_creds("Browse"),
                        image=ui.browse_icon, compound='left')
ui.file_menu.add_separator()
ui.file_menu.add_command(label=ups.data.lang.main['button2'], command=lambda: ups.import_data(ui.root),
                        image=ui.import_icon, compound='left')
ui.file_menu.add_command(label=ups.data.lang.main['button3'], command=ups.export_data,
                        image=ui.export_icon, compound='left')
ui.file_menu.add_cascade(label=ups.data.lang.main['button4'], menu=ui.backups_menu, image=ui.backup_icon, compound='left')
ui.file_menu.add_separator()
ui.file_menu.add_command(label=ups.data.lang.main['button5'], command=logout,
                        image=ui.logout_icon, compound='left')
ui.file_menu.add_separator()
ui.file_menu.add_command(label=ups.data.lang.main['button6'], command=ui.root.destroy,
                        image=ui.exit_icon, compound='left')
ui.search_btn.config(command=search_creds)
ui.opt_btn.config(command=expand_options)
ui.gen_btn.config(command=gen_pass)
ui.add_btn.config(command=save_data)
ui.clear_btn.config(command=clear_all)
ui.eye_btn.config(command=show_pass)


# ---------------------------------- BINDINGS -------------------------------------- #


ui.root.bind("<Configure>", ui.calc_width)
ui.root.bind('<Button-1>', mouseclick_check)
ui.root.bind("<MouseWheel>", on_entry_up_down)
ui.root.bind_class('Entry', '<Button-3>', lambda event: ui.r_click_popup.post(event.x_root, event.y_root))
ui.root.bind_class('TCombobox', '<Button-3>', lambda event: ui.r_click_popup.post(event.x_root, event.y_root))
ui.root.bind_all('<Motion>', ups.data.reset_timer)
ui.root.bind_all('<Any-ButtonPress>', ups.data.reset_timer)
ui.root.bind_all('<Any-KeyPress>', ups.data.reset_timer)
ui.file_menu.bind('<Motion>', ups.data.reset_timer)
ui.file_menu.bind('<Any-ButtonPress>', ups.data.reset_timer)
ui.file_menu.bind('<Any-KeyPress>', ups.data.reset_timer)
ui.root.bind_class('Spinbox', "<MouseWheel>", ui.spinbox_controls)
#* The add='+' arg adds this binding to the original, already existing binding for the arrowhead buttons
ui.root.bind_class('Spinbox', "<B1-Motion>", ui.spinbox_controls, add='+')
ui.root.bind_class('Spinbox', "<Button-1>", save_mose_position, '+')
ui.autocomplete_box.bind("<<ListboxSelect>>", autocomplete_func)
ui.website_entry.bind('<KeyRelease>', autocomplete)
ui.website_entry.bind('<Button-1>', autocomplete)
ui.website_entry.bind('<Return>', check_autocomplete_state)
ui.website_entry.bind("<Down>", on_entry_up_down)
ui.website_entry.bind("<Up>", on_entry_up_down)
ui.website_entry.bind("<Tab>", complete_website)
ui.password_entry.bind('<Return>', save_data)
ui.eye_btn.bind("<Enter>", eye_switch_color)
ui.eye_btn.bind("<Leave>", eye_switch_color)


if __name__ == "__main__":
    ui.root.mainloop()
