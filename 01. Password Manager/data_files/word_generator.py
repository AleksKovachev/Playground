"""A word generator"""

from random import choice
from string import ascii_letters
from .dry_data import coding_words, RANDOM_WORDS


class WordGenError(Exception):
    """Custom Exception"""
    __module__ = 'builtins'


class GenWord:
    """Returns a randomly generated word or list of words"""

    def __init__(self, wordfile=RANDOM_WORDS["nouns"]):
        self.wordfile = wordfile

        if wordfile != RANDOM_WORDS["nouns"]:
            with open(wordfile, 'r', encoding='utf-8') as words:
                self.wordfile = words.read()

                for char in self.wordfile:
                    if char not in ascii_letters and char != ' ':
                        self.wordfile = self.wordfile.replace(char, ' ')
                self.wordfile = self.wordfile.split()


    def gen_word(self, minlen=1, maxlen=10000, startlet="", endlet="", coded=False):
        """Returns a randomly chosen word from a list

        Args:
            minlen (int, optional): Minimum length of the word. Defaults to 1.
            maxlen (int, optional): Maximum length of the word. Defaults to 10 000.
            startlet (str, optional): The first letter of the generated word. Defaults to "" (Random).
            endlet (str, optional): The last letter of the generated word. Defaults to "" (Random).
            coded (bool, optional): If True, returns a code-styled word (ex. love - L0v3). Defaults to False.

        Raises:
            WordGenError: Error for wrong 'startlet' argument or no worsd corresponding to the given parameters

        Returns:
            str: The generated word.
        """

        # Word length control
        if maxlen <= 0 and minlen <= 0:
            # Allow long sentences as words
            maxlen = 10000
        if minlen <= 0:
            # If no minimum length was given then it's 1
            minlen = 1
        if maxlen < minlen:
            maxlen = minlen + 8

        # Takes care of the "startlet" parameter
        if startlet == "" and endlet == "":
            search_word = [word for word in self.wordfile if minlen <= len(word) <= maxlen]
        elif startlet not in ascii_letters or len(startlet) > 1 or endlet not in ascii_letters or len(endlet) > 1:
            raise WordGenError('"startlet" and "endlet" can only be a single letter each!')
        elif startlet != "" and endlet != "":
            search_word = [word for word in self.wordfile if word.lower().startswith(startlet.lower())
                            and word.lower().endswith(startlet.lower()) and minlen <= len(word) < maxlen]
        elif startlet != "":
            search_word = [word for word in self.wordfile if word.lower().startswith(startlet.lower()) and minlen <= len(word) < maxlen]
        else:
            search_word = [word for word in self.wordfile if word.lower().endswith(startlet.lower()) and minlen <= len(word) < maxlen]

        # Get a random word from the list. Raise error if list is empty.
        if search_word:
            word = choice(search_word)
        else:
            raise WordGenError('There are no words corresponding to the given parameters!')

        # Return the word, coded or not
        if coded:
            return "".join(choice(coding_words[letter]) for letter in word.lower())
        return word


    def gen_wordchain(self, acronym="", numwords=2, delimiter=" ", coded=False):
        """Generate a number of words separated by the delimiter

        Args:
            acronym (str, optional): If given, each generated word will begin with the corresponding letter from the acronym. Defaults to "".
            numwords (int, optional): Number of words to be generated. Defaults to 2.
            delimiter (str, optional): The separator between the generated words. Defaults to " ".
            coded (bool, optional): If True, returns a code-styled word (ex. love - L0v3). Defaults to False.
        """

        if numwords <= 0:
            WordGenError('The number of words to generate should be a positibe number!')

        gened_words = []
        if acronym == "":
            for _ in range(numwords):
                # Try 10 times to find a word that's not already in the list. If not - add the same one again
                for _ in range(10):
                    gen_word = self.gen_word(minlen=3, coded=coded)
                    if gen_word in gened_words:
                        gen_word = self.gen_word(minlen=3, coded=coded)
                        continue
                    break
                gened_words.append(gen_word)

        elif len(acronym) == numwords:
            for letter in acronym:
                for _ in range(10):
                    gen_word = self.gen_word(minlen=3, startlet=letter, coded=coded)
                    if gen_word in gened_words:
                        continue
                    break
                gened_words.append(gen_word)

        else:
            for num in range(numwords):
                # Try 10 times to find a word that's not already in the list. If not - add the same one again
                for _ in range(10):
                    if num < len(acronym):
                        gen_word = self.gen_word(minlen=3, startlet=acronym[num], coded=coded)
                    else:
                        # If the user wants more words than the letters in the acronym - start repeating them in the same order
                        gen_word = self.gen_word(minlen=3, startlet=acronym[num - int(num/len(acronym))*len(acronym)], coded=coded)
                    if gen_word in gened_words:
                        continue
                    break
                gened_words.append(gen_word)

        return delimiter.join(gened_words)


def gen_adj_noun(maxlen=100, minlen=6, startlet_adj="", startlet_noun="", coded=False, delimiter="") -> str:
    """Generates an adjective+noun word combination

    Args:
        minlen (int, optional): Minimum length of the word. Defaults to 6. (Should never be below 6)
        maxlen (int, optional): Maximum length of the word. Defaults to 100 (no cap).
        startlet_adj (str, optional): The first letter of the generated adjective. Defaults to "" (Random).
        startlet_noun (str, optional): The first letter of the generated noun. Defaults to "" (Random).
        coded (bool, optional): If True, returns a code-styled word (ex. love - L0v3). Defaults to False.
        delimiter (str, optional): The separator between the generated words. Defaults to "" (no delimiter).
    """
    # Word length control
    if maxlen <= 0 and minlen <= 0:
        minlen = 6
        maxlen = 100
    minlen = max(minlen, 6)
    if maxlen < minlen:
        maxlen = minlen + 8

    if (startlet_adj not in ascii_letters and startlet_adj != "" or startlet_noun not in ascii_letters
        and startlet_noun != "") or len(startlet_adj) > 1 or len(startlet_noun) > 1:
        print(startlet_adj not in ascii_letters)
        raise WordGenError('"startlet_adj" and "startlet_noun" can only be a single letter each!')

    if startlet_adj == "" and startlet_noun == "":
        gened_words = choice(RANDOM_WORDS["adjectives"]) + delimiter + choice(RANDOM_WORDS["nouns"])

        for i in range(100000):
            if len(gened_words) > maxlen or len(gened_words) < minlen:
                gened_words = choice(RANDOM_WORDS["adjectives"]) + delimiter + choice(RANDOM_WORDS["nouns"])
                if i == 99999:
                    raise WordGenError('The maxlen is set too low! Couldn\'t find a word combo!')
                continue
            break
    else:
        random_words = RANDOM_WORDS.copy()
        if startlet_adj != "":
            random_words["adjectives"] = [adj for adj in random_words["adjectives"] if adj.startswith(startlet_adj)]
        if startlet_noun != "":
            random_words["nouns"] = [adj for adj in random_words["nouns"] if adj.startswith(startlet_noun)]

        gened_words = choice(random_words["adjectives"]) + delimiter + choice(random_words["nouns"])

        for i in range(100000):
            if len(gened_words) > maxlen or len(gened_words) < minlen:
                gened_words = choice(random_words["adjectives"]) + delimiter + choice(random_words["nouns"])
                if i == 99999:
                    raise WordGenError('The maxlen is set too low! Couldn\'t find a word combo!')
                continue
            break

    if coded:
        return "".join(choice(coding_words[letter]) if letter in ascii_letters else letter for letter in gened_words.lower())
    return gened_words




if __name__ == "__main__":
    # test = GenWord(r"J:\Tutorials\Important\Houdini\Intro to Houdini - Part 1 and 2\3. VOP\-VIDEO DESC.txt")
    # test = GenWord()
    # print(test.gen_word(startlet="c"))
    # print(test.gen_wordchain(acronym='grasp', numwords=300))
    print(gen_adj_noun(maxlen=6))
