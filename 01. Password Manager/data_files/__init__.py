from math import floor
from tkinter import Toplevel
from .ui import ui
from . import updates as ups
from .authenticate import Authenticate

def countdown():
    "Countdown for automatic logout"
    if ups.data.cd_mins == 0:
        # Set the time for the label in the status bar
        ui.cd_var.set(ups.data.auth['check_login']['autoclose_deactivated'])
        # Rerun this function every 1 second
        ups.data.timer = ui.root.after(1000, countdown)
    else:
        # Get the remaining mninutes and seconds
        count_min = floor(ups.data.countdown / 60)
        count_sec = ups.data.countdown % 60

        # Format the seconds with '0' infront of single digits
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        # Write the time to a variable
        ups.data.timer_st = f"{count_min}:{count_sec}"
        # Set the time for the label in the status bar
        ui.cd_var.set(f"{ups.data.auth['check_login']['autoclose']} {ups.data.timer_st}")

        # Subtract 1 second of the remaining time
        ups.data.countdown -= 1
        # Rerun this function every 1 second
        ups.data.timer = ui.root.after(1000, countdown)
        # If timer reaches 0 - stop the timer and logout the user
        if ups.data.countdown <= 0:
            ui.root.after_cancel(ups.data.timer)
            logout()


def logout():
    """Logout of the main application and bring up the Authentication window"""
    ui.root.after_cancel(ups.data.timer)
    ups.data.countdown = ups.data.cd_mins * 60
    # Check the auto-backup options and save a data backup if needed
    ups.auto_backup(ui.root, False)
    # Destroy all TopLevel windows and hide the main application window
    for widget in ui.root.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()
    ui.root.withdraw()
    # Build a new Authentication window
    Authenticate(ui.root)
