"""This module is responsible for the data security"""

from cryptography.fernet import Fernet


def cipher(data: str):
    """Generates a fernet key, encrypts the data with it and
    passes both strings for further encryption

    Args:
        data (dict): The new data that will be encrypted
    """
    # Convert data dict to bytestring data
    b_data = data.encode('utf8')

    # Encrypts the b_data
    fernet = Fernet(data.key)

    return fernet.encrypt(b_data)


def decipher(data: str) -> dict:
    """Decrypts the data file

    Args:
        data (str): A path to the encrypted data file

    Returns:
        dict: A dictionary containing all the data
    """

    # Convert the list versions of the fernet key and the data to strings and then to bytes
    fernet_data = bytes(data, 'utf-8')

    # Decrypts the data and decodes it so it's not in bytes format. Converts the string to a dict.
    fernet = Fernet(data.key)

    return fernet.decrypt(fernet_data).decode('utf-8')
