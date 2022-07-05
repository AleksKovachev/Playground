"The english language for Password Manager"

authenticate = {
    "authenticate": {
        "auth_title": "Authentication",
        "auth_text": "Enter your credentials to continue:",
        "signin": "Sign-in",
        "signup": "Sign-up",
        "log_entry_pass": "Password",
        "check_login": {
            "status_entries_num": ("Hello", "You currently have", "accounts! | Your last backup is from:"),
            "autoclose": "Autoclose in:",
            "autoclose_deactivated": "Autoclose DEACTIVATED",
            "showerror1": {
                "title": "Wrong Password",
                "message": "You've entered a wrong password! Please try again!"
            },
            "showerror2": {
                "title": "No sutch user",
                "message": ("The username", "was not found!")
            }
        },
        "load_backup_data": {
            "title": "Replace?",
            "message": ("The latest backup if from: ", "!\nDo you wat to replace all data with this backup?")
        },
        "load_backup_data2": {
            "title": "No backups!",
            "message": "No backup files were found!"
        },
        "manage_data_integrity":{
            "message": "Last time Password manager didn't close properly! What do you want to do?",
            "explain": "Press Continue to try to run Password Manager with the same data file as before (Recommanded)\nPress Use last backup to use the latest backup file you have on your system\nPress Open data file to select a data file from you drive",
            "continue_btn": "Continue",
            "use_last_data_btn": "Use the last backup",
            "choose_data_btn": "Open a data file"
        },
        "check_pwd": {
            "showerror1": {
                "title": "Wrong Password",
                "message": "The password is too long!"
            },
            "showerror2": {
                "title": "Wrong Password",
                "message": "The password is too short!"
            },
            "showerror3": {
                "title": "Wrong Password",
                "message": "The password contains invalid characters!"
            },
        }
    },
    "check_pwd_rep": {
        "title": "Mismatch",
        "message": "The password doesn't match!"
    },
    "signup": {
        "title": "Registration",
        "new_account_ui": {
            "reg_text": "Please fill out all the fields:",
            "e_btn": "Create",
            "entrance_email": "E-mail",
            "entrance_pass": "Password",
            "repeat_pass": "Repeat Password"
        },
        "save_login": {
            "title": "Ooops",
            "message": "You must fill all fields!"
        }
    },
    "field_clear": {
        "password": "Password",
        "user": "Username",
        "email": "E-mail",
        "repeat_password": "Repeat Password"
    }
}

ui = {
    "PMUI": {
        "main_title": "Password Manager",
        "menu": {
            "copy": "Copy",
            "paste": "Paste",
            "cut": "Cut",
            "backup_label_date": "Date",
            "menubar_file": "File",
            "menubar_edit": "Edit",
            "menubar_settings": "Settings",
            "menubar_themes": "Themes & Colors",
            "menubar_backup_period": "Backup period",
            "menubar_settings_menu": "Settings..."
        },
        "labels": {
            "website_label": "Website:",
            "user_label": "Username:",
            "email_label": "Email:",
            "password_label": "Password:",
            "password_length": "Length:",
            "status_entries": "Hello!"
        },
        "buttons": {
            "search_btn": "Search",
            "options_btn": "Options",
            "generate_btn": "Generate",
            "add_btn": "Add",
            "clear_btn": "Clear All"
        },
        "radiobuttons": {
            "radio1": "Secure",
            "radio2": "Easy",
            "radio3": "Combo",
            "radio4": "Secure Combo"
        }
    },
    "theme_changer_ui": {
        "title": "Customize Theme",
        "bg_label": "Background:",
        "fg_label": "Foreground:",
        "accent_label": "Accents:",
        "details1_label": "Details 1:",
        "details2_label": "Details 2:",
        "reset_btn": "Reset",
        "element_color": "Choose a color"
    },
    "cust_settings": {
        "left_panel": {
            "login_btn": "Login Settings⏵",
            "default_btn": "Default Settings"
        },
        "right_panel_login": {
            "user": "Username:",
            "password": "Password ---▼",
            "old_pwd": "Old:",
            "new_pwd": "New:",
            "rep_pwd": "Repeat:"
        },
        "right_panel_default": {
            "user": "Username:",
            "email": "E-mail:",
            "autoclose": "Autoclose",
            "mins": "Minutes",
            "tip": "(0 means no Autoclose)"
        },
        "apply_btn": "Apply",
        "update_cust_settings": {
            "if_login": {
                "login_btn": "Login Settings⏵",
                "default_btn": "Default Settings"
            },
            "elif_default": {
                "login_btn": "Login Settings",
                "default_btn": "Default Settings⏵"
            }
        }
    }
}

update = {
    "import_data": {
        "askopenfile_title": "Select a File",
        "message": "You already have a data file!",
        "question": "What do you want to do?",
        "new_data_btn": "Use new data",
        "merge_data_btn": "Merge data",
        "old_data_btn": "Use old data",
    },
    "merge_dominant": {
        "msg": "In case of data conflict do you want to keep the current information or the one from the imported file?",
        "old_btn": "Current",
        "new_btn": "Imported"
    },
    "export_data_title": "Choose a Folder",
    "recover_from_backup": {
        "title": "WARNING!",
        "message": "Are you sure you want to recover this file?\nThis will delete all of the current data you have!"
    },
    "backup_period": {
        0: "No backups",
        1: "Daily",
        2: "Weekly",
        3: "Monthly",
        4: "On close"
    },
    "cust_settings": {
        "title": "WARNING!",
        "message": "Are you sure you want to apply changes?"
    },
    "cust_settings2": {
        "title": "No New Data",
        "message": "There's nothing new to apply or you have wrong information in the fields!"
    },
    "check_email1": {
        "title": "Invalid e-mail",
        "message": "The e-mail can't begin or end with a special character!"
    },
    "check_email2": {
        "title": "Invalid e-mail",
        "message": "The e-mail you entered is not valid!"
    },
    "check_username1": {
        "title": "Incorrect username",
        "message": "The username should be between 3 and 20 characters!"
    },
    "check_username2": {
        "title": "Incorrect username",
        "message": "The username should only contain characters in the range:\na-z, A-Z, 0-9"
    },
    "check_username3": {
        "title": "Duplicate username",
        "message": ("Username", "is already taken!")
    },
    "check_password1" : {
        "title": "ERROR!",
        "message": "The old password is incorrect!"
    },
    "check_password2" : {
        "title": "ERROR!",
        "message": "The new password doesn't match!"
    },
    "check_password3" : {
        "title": "Wrong password",
        "message": "The password is too long!"
    },
    "check_password4" : {
        "title": "Wrong password",
        "message": "The password is too short!"
    },
    "check_password5" : {
        "title": "Wrong password",
        "message": "The password contains invalid characters!"
    }
}

main = {
    "check_data": {
        "title": "Credentials for",
        "message": ("User:", "E-mail:", "Password:")
    },
    "search_creds": {
        "showerror": {
            "title": "No website",
            "message": "You have to Enter a website or platform!"
        },
        "showinfo": {
            "title": "Credentials for",
            "message": ("User:", "E-mail:", "Password:")
        },
        "askyesno": {
            "title": "Missing credentials",
            "message": "Couldn't find the credentials you're looking for.\nDo you want to open a list of all accounts?"
        }
    },
    "win2": {
        "title": "Account List:",
        "choose_acc": "Choose a website:"
    },
    "save_data": {
        "showwarning": {
            "title": "Ooops",
            "message": "You must fill all fields!"
        },
        "askyesno1": {
            "title": "Overwrite?",
            "message": ("You already have credentials for", "Do you want to overwrite them?")
        },
        "askyesno2": ("These are the entered details:\n\nEmail:", "User:", "Password:", "Are these correct?")
    },
    "light_theme": "Light",
    "dark_theme": "Dark",
    "custom_theme": "Custom...",
    "button1": "Browse Data...",
    "button2": "Import Data",
    "button3": "Export Data",
    "button4": "Recover from backup",
    "button5": "Logout",
    "button6": "Exit"
}
