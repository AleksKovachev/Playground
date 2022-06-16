# Caesar Cipher - Day 8
import string

alphabet = list(string.ascii_lowercase) * 2

direction = input("Type 'ENCODE' to encrypt or 'DECODE' to decrypt:\n")
text = input("Type your message:\n")
shift = int(input("Type the shift number:\n")) % 26


def caesar(start_text, shift_amount, cipher_direction):
    '''Encodes and Decodes a message by the Caesar Cypher'''
    while True:
        if cipher_direction.lower() == "encode":
            operator = "+"
            break
        elif cipher_direction.lower() == "decode":
            operator = "-"
            break
        else:
            continue

    # Create a string by getting the char and finding its first occurance's position in the alphabet
    # if it's a letter and shifting it by the shift amount
    # Put the same character if it's not a letter
    end_text = "".join(alphabet[eval(str(alphabet.index(char)) + operator + str(shift_amount))] if char.lower() in string.ascii_lowercase else char for char in start_text.lower())
    print(f"The {direction.lower()}d message is: {end_text}")


caesar(start_text = text, shift_amount = shift, cipher_direction = direction)
