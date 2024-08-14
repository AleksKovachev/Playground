"""A word generator"""

import random
import string
from .constants import CODE_CHARS
from .data_management.all_data import file_data


class WordGenError(Exception):
    """Custom Exception"""
    __module__ = 'builtins'


class GenWord:
    """Responsible for random generation of words"""

    def __init__(self, wordfile=file_data.dictionary["nouns"]):

        if wordfile != file_data.dictionary["nouns"]:
            with open(wordfile, 'r', encoding='utf-8') as words:
                wordstring = words.read()

            for char in wordstring:
                if char not in string.ascii_letters and char != ' ':
                    wordstring = wordstring.replace(char, ' ')
            self.dict = wordstring.lower().split()

    @staticmethod
    def gen_adj_noun(minlen=6, maxlen=100, coded=False, delimiter="") -> str:
        """Generates an adjective+noun word combination

        Args:
            minlen (int, optional): Minimum length of the word. Defaults to 6.
            maxlen (int, optional): Maximum length of the word. Defaults to 100 (no cap).
            coded (bool, optional): If True, returns a coded word (love: L0v3). Defaults to False.
            delimiter (str, optional): The separator between the generated words. Defaults to "".
        """
        minlen, maxlen = check_range(minlen, maxlen)

        pass_len = minlen if minlen == maxlen else random.randint(minlen, maxlen)
        pass_len -= 1 if pass_len == maxlen else 0

        longest_adj = 14
        longest_noun = 16
        shortest_word = 3

        if maxlen < shortest_word * 2 + 1:
            raise WordGenError("The maxlen is set too low! Couldn't find a word combo!")
        if minlen > longest_adj + longest_noun + 1:
            raise WordGenError("The minlen is set too high! Couldn't find a word combo!")

        adj_min_len = max(shortest_word, pass_len - longest_noun)
        adj_max_len = min(longest_adj, pass_len - shortest_word)

        adj_len = random.randint(adj_min_len, adj_max_len)
        noun_len = pass_len - adj_len

        adj, noun = "", ""
        while len(adj) != adj_len:
            adj = random.choice(file_data.dictionary['adjectives'])
        while len(noun) != noun_len:
            noun = random.choice(file_data.dictionary['nouns'])

        gened_words = adj + delimiter + noun

        if coded:
            return "".join(random.choice(CODE_CHARS[letter]) if letter in string.ascii_letters
                else letter for letter in gened_words.lower())
        return gened_words

    def gen_word(self, minlen: int = 1, maxlen:int = 10_000, coded: bool = False, exclude=()):
        """Returns a randomly chosen word from a list

        Args:
            minlen (int, optional): Minimum length of the generated word. Defaults to 1.
            maxlen (int, optional): Maximum length of the generated word. Defaults to 10 000.
            coded (bool, optional): If True, returns a coded word (love: L0v3). Defaults to False.
        """
        # Word length control
        maxlen = 10_000 if maxlen <= 0 else maxlen # Allow long sentences as words
        minlen = 1 if minlen <= 0 else minlen

        if maxlen < minlen:
            maxlen = minlen + 8

        # Get a random word from the list. Raise error if list is empty.
        if search_word := [word for word in self.dict if minlen <= len(word) <= maxlen]:
            if search_word := [word for word in search_word if word not in exclude]:
                word = random.choice(search_word)
            else:
                return ""
        else:
            raise WordGenError('There are no words corresponding to the given parameters!')

        # Return the word, coded or not
        if coded:
            return "".join(random.choice(CODE_CHARS[letter]) for letter in word)
        return word


def check_range(minlen, maxlen):
    """Checks if the range is within working values"""
    # Word length control
    if maxlen <= 0 and minlen <= 0:
        minlen, maxlen = 6, 100

    minlen = max(minlen, 6)

    if maxlen < minlen:
        maxlen = minlen + 8

    return (minlen, maxlen)


def gen_adj_noun(minlen=6, maxlen=100, coded=False, delimiter="") -> str:
    """Generates an adjective+noun word combination

    Args:
        minlen (int, optional): Minimum length of the word. Defaults to 6. (Should never be below 6)
        maxlen (int, optional): Maximum length of the word. Defaults to 100 (no cap).
        coded (bool, optional): If True, returns a code-styled word (ex. love - L0v3).
                                    Defaults to False.
        delimiter (str, optional): The separator between the generated words.
                                Defaults to "" (no delimiter).
    """
    minlen, maxlen = check_range(minlen, maxlen)

    pass_len = minlen if minlen == maxlen else random.randint(minlen, maxlen)
    pass_len -= 1 if pass_len == maxlen else 0

    longest_adj = 14
    longest_noun = 16
    shortest_word = 3

    if maxlen < shortest_word * 2 + 1:
        raise WordGenError('The maxlen is set too low! Couldn\'t find a word combo!')
    if minlen > longest_adj + longest_noun + 1:
        raise WordGenError('The minlen is set too high! Couldn\'t find a word combo!')

    adj_min_len = max(shortest_word, pass_len - longest_noun)
    adj_max_len = min(longest_adj, pass_len - shortest_word)

    adj_len = random.randint(adj_min_len, adj_max_len)
    noun_len = pass_len - adj_len

    adj, noun = "", ""
    while len(adj) != adj_len:
        adj = random.choice(file_data.dictionary["adjectives"])
    while len(noun) != noun_len:
        noun = random.choice(file_data.dictionary["nouns"])

    gened_words = adj + delimiter + noun

    if coded:
        return "".join(random.choice(CODE_CHARS[letter]) if letter in string.ascii_letters
            else letter for letter in gened_words.lower())
    return gened_words


if __name__ == "__main__":
    # test = GenWord(
        # r"J:\Tutorials\Important\Houdini\Intro to Houdini - Part 1 and 2\3. VOP\-VIDEO DESC.txt")
    # test = GenWord()
    # print(test.gen_word(startlet="c"))
    # print(test.gen_wordchain(acronym='grasp', numwords=300))
    print(gen_adj_noun(minlen=0, maxlen=6))
