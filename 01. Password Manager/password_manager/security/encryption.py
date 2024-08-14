"""This module is responsible for the data security"""
import random
import sqlite3

from cryptography.fernet import Fernet
from argon2 import PasswordHasher, exceptions

from password_manager.constants import DATA
from password_manager.data_management.all_data import data
from . import gen_pass


def hash_password(password: str):
    """Hashes the given password"""
    pass_hash = PasswordHasher()
    return pass_hash.hash(password)


def verify_password(password: str, hashed_pass: str, user_id: int):
    """Unhashes and returns the password"""
    pass_hash = PasswordHasher()
    try:
        pass_hash.verify(hashed_pass, password)
        if rehash := check_and_rehash(hashed_pass, password):
            update_password_hash(rehash, user_id)
        return True
    except (exceptions.VerifyMismatchError, exceptions.InvalidHashError):
        return False


def check_and_rehash(hashed, password):
    """Checks a given hash and rehashes it if needed"""
    pass_hash = PasswordHasher()
    if pass_hash.check_needs_rehash(hashed):
        return pass_hash.hash(password)
    return None


def update_password_hash(rehash, user_id):
    """Updates the password hash in the database"""
    with sqlite3.connect(DATA) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE user_data SET password = ? WHERE id = ?", (rehash, user_id))


def generate_key():
    """Generates a Fernet key. Unique per user."""
    return Fernet.generate_key().decode('utf-8')


def decipher(data_: str):
    """Deciphers the data based on the provided key"""
    fernet = Fernet(data.key.encode('utf-8'))
    return fernet.decrypt(data_.encode('utf-8')).decode('utf-8')


def cipher(data_: str, key: str = None):
    """Generates a fernet key, encrypts the data with it and
    passes both strings for further encryption

    Args:
        data (dict): The new data that will be encrypted
    """
    fernet = Fernet(data.key.encode('utf-8')) if key is None else Fernet(key.encode('utf-8'))
    return fernet.encrypt(data_.encode('utf-8')).decode('utf-8')


def generate_custom_cipher(data_: str):
    """Encrypts the data using a custom cipher

    Args:
        data_ (str): The string to be encrypted
        code (int): A custom code to recognize if it's
                    the key that's being passed or the actual data
    """

    # Get a random(7-15) number of positions in the string and sort them
    samp = random.sample(range(len(data_)), random.randint(7, 15))
    samp.sort()

    # Dictionary with random number of random charactes as
    # value and the position number from samp as key
    modifications = {samp[i]: gen_pass(random.randint(35, 55)) for i in range(len(samp))}

    # Dictionary with every samp position as key and the number of generated characters as value
    actual_custom_key = {key: len(value) for key, value in modifications.items()}

    # Create a list with all original key characters and the
    # randomly generated characters at random positinos from "modifications"
    modified_key = [
        data_[:i] + modifications[i] if i == samp[0] else \
            data_[samp[pos-1]:i] + modifications[i] for pos, i in enumerate(samp)
    ]
    modified_key.append(data_[samp[-1]:])
    mod = ''.join(modified_key)

    final_key = (
        mod[:int(0.15*len(mod))],
        mod[int(0.15*len(mod)):int(0.35*len(mod))],
        mod[int(0.35*len(mod)):int(0.55*len(mod))],
        mod[int(0.55*len(mod)):int(0.85*len(mod))],
        mod[int(0.85*len(mod)):],
        gen_pass(random.randint(70, 150)),
        gen_pass(random.randint(70, 150)),
        gen_pass(random.randint(70, 150))
    )

    # Use Caesar cipher-type of code to cipher the original keys and values
    changed_custom_key = {}
    for key, value in actual_custom_key.items():
        key = key + 4 if key % 2 == 0 else key * 3
        value = value - 6 if value % 2 == 0 else value + 8
        changed_custom_key[key] = value

    # Shuffle the positions of the keys and the values and
    # save them to a list called 'convert_custom_key'
    temp_var1 = []
    temp_var2 = []
    convert_custom_key = []

    for num, (key, value) in enumerate(changed_custom_key.items()):
        if num < 5:
            temp_var1.append(key)
            temp_var2.append(value)
        elif num == 5:
            temp_var2.reverse()
            convert_custom_key = temp_var1 + temp_var2
            convert_custom_key.extend((value, key))
        else:
            convert_custom_key.extend((value, key))

    # Send a string representation of the list for archiving
    var = str(convert_custom_key)[1:-1]


def assemble_pieces(files_data: dict) -> tuple[list, list, str, str]:
    """Assembles all data pieces according to a custom encryption pattern

    Args:
        files_data (dict): A dictionary containing all data as
                            values and the sub-zipfiles names as keys

    Returns:
        tuple[list, list, str, str]: The lists are the custom-coded fernet key and the data while
            the strings are the keys to actually get the real fernet key and the real data.
    """
    # assembled_key = []
    # assembled_data = []

    # files_data, ak_cipher, ad_cipher = get_coded_custom_cipher(files_data)

    # # Go through all data and collect the relevant
    # for key, val in files_data.items():
    #     file_name, extension = key.split('.')
    #     # The first part of the strings
    #     if file_name in take_names(1)[0]:
    #         assembled_key.append(val)
    #     elif file_name in take_names(2)[0]:
    #         assembled_data.append(val)

    #     # The second part of the strings
    #     elif extension in take_names(1)[8]:
    #         assembled_key.append(val)
    #     elif extension in take_names(2)[8]:
    #         assembled_data.append(val)

    #     # The third part of the strings
    #     elif file_name in take_names(1)[1]:
    #         assembled_key.append(val)
    #     elif file_name in take_names(2)[1]:
    #         assembled_data.append(val)

    #     # The fourth part of the strings
    #     elif file_name in take_names(1)[4] and extension in take_names(1)[9]:
    #         assembled_key.append(val)
    #     elif file_name in take_names(2)[4] and extension in take_names(2)[9]:
    #         assembled_data.append(val)

    #     # The fifth part of the strings
    #     elif extension in take_names(1)[7]:
    #         assembled_key.append(val)
    #     elif extension in take_names(2)[7]:
    #         assembled_data.append(val)

    # return assembled_key, assembled_data, ak_cipher, ad_cipher


def rearrange_key(key: str):
    """Rearrange the key strings to get the actual order of the keys

    Args:
        key (str): A string representing a key to decipher a code

    Returns:
        tuple[list, list]: A tuple containing the numbers to create a dictionary
    """
    keys = []
    values = []

    for count, item in enumerate(key):
        if count < 5 or count >= 10 and count != 10 and count % 2 != 0:
            keys.append(int(item))
        elif count < 10 or count != 10:
            values.append(int(item))
        else:
            values.reverse()
            values.append(int(item))

    return keys, values


def get_original_key(ciphered_key: dict):
    """Order the shuffled dictionary to get the original custom key as a dictionary

    Args:
        ciphered_key (dict): The ciphered version of the key

    Returns:
        dict: A decoded version of the same key
    """
    original_key = {}

    for key, value in ciphered_key.items():
        key = key - 4 if key % 2 == 0 else int(key / 3)
        value = value + 6 if value % 2 == 0 else value - 8
        original_key[key] = value

    return original_key


def decode_string(og_key: dict, strand: list):
    """Decode the fernet key/data using the original custom key

    Args:
        og_key (dict): A decoded version of the ciphered key
        strand (list): A list version of the whole key/data where
                        every character is a string in this list

    Returns:
        list: A list cleared of all unnecessary characters
    """
    while og_key:
        remove_min = min(og_key.keys())
        for _ in range(og_key[remove_min]):
            strand.pop(remove_min)
        og_key.pop(remove_min)

    return strand


# def decipher(data: str) -> dict:
#     """Decrypts the data file

#     Args:
#         data (str): A path to the encrypted data file

#     Returns:
#         dict: A dictionary containing all the data
#     """
#     # Get a dictionary with all data
#     files_data = get_files_data(data)
#     # Assemble the data into coded lists and strings
#     assembled_key, assembled_data, ak_cipher, ad_cipher = assemble_pieces(files_data)

#     # Rearrange the key strings to get the actual order of the keys
#     keys, values = rearrange_key(ak_cipher)
#     ak_cipherd = dict(zip(keys, values))
#     keys, values = rearrange_key(ad_cipher)
#     ad_cipherd = dict(zip(keys, values))

#     # Order the shuffled dictionary to get the original custom key as a dictionary
#     original_ak_key = get_original_key(ak_cipherd)
#     original_ad_key = get_original_key(ad_cipherd)

#     # Convert the assembled pieces to a string and then to a list for further processing
#     fernet_ak_key = list("".join(assembled_key))
#     fernet_data = list("".join(assembled_data))

#     # Decode the fernet key using the original custom key
#     fernet_ak_key = decode_string(original_ak_key, fernet_ak_key)
#     fernet_data = decode_string(original_ad_key, fernet_data)

#     # Convert the list versions of the fernet key and the data to strings and then to bytes
#     fernet_ak_key = ''.join(fernet_ak_key) + "="
#     fernet_key = bytes(fernet_ak_key, 'utf-8')
#     fernet_data = ''.join(fernet_data) + "="
#     fernet_data = bytes(fernet_data, 'utf-8')

#     # Decrypts the data and decodes it so it's not in bytes format.
#     # Converts the string to a dictionary.
#     fernet = Fernet(fernet_key)

#     return json.loads(fernet.decrypt(fernet_data).decode('utf-8'))
