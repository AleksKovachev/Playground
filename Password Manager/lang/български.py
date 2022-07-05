"The bulgarian language for Password Manager"

authenticate = {
    "authenticate": {
        "auth_title": "Оторизация",
        "auth_text": "Въведете данните си, за да продължите:",
        "signin": "Влез",
        "signup": "Регистриране",
        "log_entry_pass": "Парола",
        "check_login": {
            "status_entries_num": ("Здравейте", "Имате", "запазени акаунта! | Последното резервно копие е от:"),
            "autoclose": "Затваряне след:",
            "autoclose_deactivated": "Затваряне ДЕАКТИВИРАНО",
            "showerror1": {
                "title": "Грешна Парола",
                "message": "Въведохте грешна парола! Моля опитайте отново!"
            },
            "showerror2": {
                "title": "Няма такъв потребител",
                "message": ("Потребителското име", "не е намерено!")
            }
        },
        "load_backup_data": {
            "title": "Заместване?",
            "message": ("Последното копие е от: ", "!\nИскате ли да заместите всички данни с това копие?")
        },
        "load_backup_data2": {
            "title": "Няма резервни копия!",
            "message": "Не са намерении резервни копия!"
        },
        "manage_data_integrity":{
            "message": "Последният път Мениджър за Пароли не се затвори правилно! Какво искате да направите?",
            "explain": "Натиснете Продължи за да се опитате да стартирате Мениджър за Пароли със същия файл с данни като преди (Препоръчително)\nНатиснете Използвай резервно копие за да използвате последното запазено резервно копие на системата\nНатиснете Отвори файл с данни за да изберете файл от диска си",
            "continue_btn": "Продължи",
            "use_last_data_btn": "Използвай резервно копие",
            "choose_data_btn": "Отвори файл с данни"
        },
        "check_pwd": {
            "showerror1": {
                "title": "Грешна Парола",
                "message": "Паролате е твърде дълга!"
            },
            "showerror2": {
                "title": "Грешна Парола",
                "message": "Паролата е твърде кратка!"
            },
            "showerror3": {
                "title": "Грешна Парола",
                "message": "Паролата съдържа забранени символи!"
            },
        }
    },
    "check_pwd_rep": {
        "title": "Несъвпадение",
        "message": "Паролите не съвпадат!"
    },
    "signup": {
        "title": "Регистрация",
        "new_account_ui": {
            "reg_text": "Моля попълнете всички полета:",
            "e_btn": "Създай",
            "entrance_email": "Е-поща",
            "entrance_pass": "Парола",
            "repeat_pass": "Повтори паролата"
        },
        "save_login": {
            "title": "Опа",
            "message": "Трябва да попълните всички полета!"
        }
    },
    "field_clear": {
        "password": "Парола",
        "user": "Потребителско име",
        "email": "Е-поща",
        "repeat_password": "Повтори паролата"
    }
}

ui = {
    "PMUI": {
        "main_title": "Мениджър за пароли",
        "menu": {
            "copy": "Копирай",
            "paste": "Постави",
            "cut": "Изрежи",
            "backup_label_date": "Дата",
            "menubar_file": "Файл",
            "menubar_edit": "Редактиране",
            "menubar_settings": "Настройки",
            "menubar_themes": "Теми и Цветове",
            "menubar_backup_period": "Период за резервно копие",
            "menubar_settings_menu": "Настройки..."
        },
        "labels": {
            "website_label": "Уебсайт:",
            "user_label": "Потребител:",
            "email_label": "Поща:",
            "password_label": "Парола:",
            "password_length": "Дължина:",
            "status_entries": "Здравейте!"
        },
        "buttons": {
            "search_btn": "Търсене",
            "options_btn": "Опции",
            "generate_btn": "Генерирай",
            "add_btn": "Добави",
            "clear_btn": "Изчисти"
        },
        "radiobuttons": {
            "radio1": "Сигурно",
            "radio2": "Лесно",
            "radio3": "Комбо",
            "radio4": "Сигурно комбо"
        }
    },
    "theme_changer_ui": {
        "title": "Персонализиране на Тема",
        "bg_label": "Фон:",
        "fg_label": "Основен:",
        "accent_label": "Акценти:",
        "details1_label": "Детайли 1:",
        "details2_label": "Детайли 2:",
        "reset_btn": "Възстанови",
        "element_color": "Избиране на цвят"
    },
    "cust_settings": {
        "left_panel": {
            "login_btn": "Настройки за влизане⏵",
            "default_btn": "Стандартни настройки"
        },
        "right_panel_login": {
            "user": "Потребител:",
            "password": "Парола ---▼",
            "old_pwd": "Стара:",
            "new_pwd": "Нова:",
            "rep_pwd": "Повтори:"
        },
        "right_panel_default": {
            "user": "Потребител:",
            "email": "Е-Поща:",
            "autoclose": "Автоматично затваряне",
            "mins": "Минути",
            "tip": "(0 означава без Автоматично затваряне)"
        },
        "apply_btn": "Приложи",
        "update_cust_settings": {
            "if_login": {
                "login_btn": "Настройки за влизане⏵",
                "default_btn": "Стандартни настройки"
            },
            "elif_default": {
                "login_btn": "Настройки за влизане",
                "default_btn": "Стандартни настройки⏵"
            }
        }
    }
}

update = {
    "import_data": {
        "askopenfile_title": "Избери файл",
        "message": "Вече имате файл с данни!",
        "question": "Кои искате да използвате?",
        "new_data_btn": "Нови",
        "merge_data_btn": "Смеси данните",
        "old_data_btn": "Стари"
    },
    "merge_dominant": {
        "msg": "В случай на конфликт искате да запазите информацията от съществуващия файл или да използвате тази от новия?",
        "old_btn": "Съществуваща",
        "new_btn": "Нова"
    },
    "export_data_title": "Избери папка",
    "recover_from_backup": {
        "title": "ВНИМАНИЕ!",
        "message": "Сигурни ли сте, че искате да възстановите този файл?\nТова ще изтрие цялата информация, която имате в момента!"
    },
        "backup_period": {
        0: "Без резервни копия",
        1: "Дневно",
        2: "Седмично",
        3: "Месечно",
        4: "При затваряне"
    },
    "cust_settings": {
        "title": "ВНИМАНИЕ!",
        "message": "Сигурни ли сте, че искате да приложите промените?"
    },
    "cust_settings2": {
        "title": "Няма Нова Информация",
        "message": "Няма нова информация за прилагане или има грешни данни!!"
    },
    "check_email1": {
        "title": "Грешна поща",
        "message": "Пощата не може да започва или завършва със специален символ!"
    },
    "check_email2": {
        "title": "Грешна поща",
        "message": "Въведената поща е невалидна!"
    },
    "check_username1": {
        "title": "Грешно потребителско име",
        "message": "Потребителското име трябва да е между 3 и 20 знака!"
    },
    "check_username2": {
        "title": "Грешно потребителско име",
        "message": "Потребителското име може да съдържа само следните символи:\na-z, A-Z, 0-9"
    },
    "check_username3": {
        "title": "Заето потребителско име",
        "message": ("Потребителското име", "е заето!")
    },
    "check_password1" : {
        "title": "ГРЕШКА!",
        "message": "Старата парола е грешна!"
    },
    "check_password2" : {
        "title": "ГРЕШКА!",
        "message": "Новата парола не съвпада!"
    },
    "check_password3" : {
        "title": "Грешна парола",
        "message": "Паролата е твърде дълга!"
    },
    "check_password4" : {
        "title": "Грешна парола",
        "message": "Паролата е твърде къса!"
    },
    "check_password5" : {
        "title": "Грешна парола",
        "message": "Паролата съдържа невалидни символи!"
    }
}

main = {
    "check_data": {
        "title": "Данни за",
        "message": ("Потребителско име:", "Е-Поща:", "Парола:")
    },
    "search_creds": {
        "showerror": {
            "title": "Няма уебсайт",
            "message": "Трябва да въведете уебсайт или платформа!"
        },
        "showinfo": {
            "title": "Данни за",
            "message": ("Потребителско име:", "Е-Поща:", "Парола:")
        },
        "askyesno": {
            "title": "Липсващи данни",
            "message": "Данните, които търсите не са намерени.\nИскате ли да отворите списък с всички акаунти?"
        }
    },
    "win2": {
        "title": "Списък с акаунти:",
        "choose_acc": "Изберете уебсайт:"
    },
    "save_data": {
        "showwarning": {
            "title": "Опа",
            "message": "Трябва да попълните всички полета!"
        },
        "askyesno1": {
            "title": "Презаписване?",
            "message": ("Вече имате данни за", "Искате ли да ги заместите?")
        },
        "askyesno2": ("Това са въведените данни:\n\nПоща:", "Потребителско име:", "Парола:", "Правилни ли са?")
    },
    "light_theme": "Светла",
    "dark_theme": "Тъмна",
    "custom_theme": "Персонализирай...",
    "button1": "Разглеждане на данни...",
    "button2": "Вмъкване на данни",
    "button3": "Запазване на данни",
    "button4": "Възстановяване на резервно копие",
    "button5": "Излез от профила",
    "button6": "Изход"
}
