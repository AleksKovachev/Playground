"""Contains shared security functionality"""

import math
from random import randint, choice, shuffle
from string import ascii_letters, punctuation, digits

def gen_pass(total_chars):
    """Generates a random-character password

    Args:
        total_chars (int): How many characters to generate

    Returns:
        str: The final randomly generated password
    """
    # Choose between 2 and half of the total characters to be random digits
    pass_nums = [choice(digits) for _ in range(randint(2, math.floor(total_chars / 2)))]
    # Choose between 2 and 40% of total chars to be random acceptable punctuation characters
    pass_chars = [choice(punctuation) for _ in range(randint(2, math.floor(0.4 * total_chars)))]
    # Get the number of already generated chars and generate the rest of the total as random letters
    pass_letters = [choice(ascii_letters) for _ in range(total_chars - len(pass_nums + pass_chars))]

    # Combine the lists in a single one, shuffle it and return it as a string.
    password_list = pass_letters + pass_nums + pass_chars
    shuffle(password_list)
    return "".join(password_list)
