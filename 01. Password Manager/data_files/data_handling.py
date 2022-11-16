"""This module is responsible for the data security"""

import json

from os import path, getenv
from cryptography.fernet import Fernet


############################################################################

# IMPORTANT!!!
# The data encryption in this version is reduced to nothing since
# I don't want to share the actual encryption techniques publicly.

############################################################################


DATA_PATH = path.join(getenv('LOCALAPPDATA'), "PM Master")


def cipher(data: dict):
    """Generates a fernet key, encrypts the data with it and passes both strings for further encryption

    Args:
        data (dict): The new data that will be encrypted
    """

    # Generates a key
    fernet_key = Fernet.generate_key()

    with open(path.join(DATA_PATH, "pm.key"), "wb") as key_file:
        key_file.write(fernet_key)

    # Convert data dict to bytestring data
    b_data = json.dumps(data, indent=4).encode('utf8')

    # Encrypts the b_data
    fernet = Fernet(fernet_key)
    encrypted_data = fernet.encrypt(b_data)

    with open("pmd.dat", "wb") as key_file:
        key_file.write(encrypted_data)


def decipher(data: str) -> dict:
    """Decrypts the data file

    Args:
        data (str): A path to the encrypted data file

    Returns:
        dict: A dictionary containing all the data
    """

    # Get the key
    fernet_key = open(path.join(DATA_PATH, "pm.key"), "rb").read()

    # Initiate Fernet
    fernet = Fernet(fernet_key)

    # Get the data file
    fernet_data = open(data, "rb").read()

    # Return the decrypted data
    return json.loads(fernet.decrypt(fernet_data).decode('utf-8'))


if __name__ == "__main__":
    print(decipher('pmd.dat'))
