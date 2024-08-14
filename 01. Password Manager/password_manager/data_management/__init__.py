"""Contains common functions for updating data"""

import json

from password_manager.constants import SETTINGS_FILE


def update_list(lst: list, sample: str):
    """Orders a given list by relevancy and alphabetical order

    Args:
        lst (list): the list to be ordered
        sample (str): results starting with this string will be shown first

    Returns:
        list: the ordered version of the input list
    """

    lst.sort()
    temp_lst_first = []
    temp_lst_rest = []
    for item in lst:
        if item.lower().startswith(sample.lower()):
            temp_lst_first.append(item)
        else:
            temp_lst_rest.append(item)
    lst = temp_lst_first + temp_lst_rest

    return lst


def refresh_startup_language(language: str):
    """Refreshes language parameter in settings file

    Args:
        language (str): The Language of the program upon next startup
    """
    with open(SETTINGS_FILE, 'r+', encoding='utf-8') as settings:
        read = json.load(settings)
        read['language'] = language
        settings.seek(0)
        settings.truncate()
        json.dump(read, settings, indent=4, ensure_ascii=False)


def get_median_color(color1: str, color2: str):
    """Calculates the average between two colors

    Args:
        color1 (str): HEX color
        color2 (str): HEX color

    Returns:
        str: A hexadecimal representation on a color. ex. "#c0ffee"
    """
    color1 = color1.strip("#")
    color2 = color2.strip("#")

    red1, green1, blue1 = [int(color1[p:p+2], 16) for p in range(0, 5, 2)]  # Here, 6 is len(color)
    red2, green2, blue2 = [int(color2[p:p+2], 16) for p in (0, 2, 4)]

    return f'#{(red1 + red2) // 2:02x}{(green1 + green2) // 2:02x}{(blue1 + blue2) // 2:02x}'
