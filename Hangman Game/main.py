# sourcery skip: remove-unnecessary-else, swap-if-else-branches, switch
import random, string

# HANGMAN - Day 7

stages = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

logo = '''
 _
| |
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |
                   |___/    '''

word_list = ["childhood",
            "nonsense",
            "cell",
            "food",
            "cells",
            "user",
            "reputation",
            "poem",
            "rhabdomancy",
            "quantity",
            "attention",
            "grandmother",
            "relationship",
            "hippology",
            "attitude",
            "management",
            "storage",
            "disease",
            "jackpot",
            "operation",
            "instrument",
            "disk",
            "aboral",
            "emetology",
            "obsession",
            "infra",
            "pressure",
            "contract",
            "pedicular",
            "employee",
            "improvement",
            "republic",
            "industry",
            "wood",
            "client",
            "enthusiasm",
            "world",
            "measurement",
            "independence",
            "physics",
            "bath",
            "definition",
            "requirement",
            "hotel",
            "area",
            "classroom",
            "bathroom",
            "muscology",
            "agency",
            "oven",
            "visibilia",
            "alcohol",
            "agreement",
            "employer",
            "drawing",
            "environment",
            "possibility",
            "people",
            "direction",
            "marriage",
            "ismatic",
            "profession",
            "triage",
            "nation",
            "examination",
            "possession",
            "accident",
            "apple",
            "surgery",
            "mall",
            "orange",
            "white",
            "kurgan",
            "currency",
            "engineering",
            "obligation",
            "historian",
            "professor",
            "city",
            "manufacturer",
            "penalty",
            "chest",
            "departure",
            "engine",
            "worker",
            "feet",
            "mouth",
            "memory",
            "patrimony",
            "king",
            "synecdochial",
            "tension",
            "dealer",
            "resolution",
            "literature",
            "consequence",
            "variation",
            "personality",
            "town",
            "category",
            "procedure",
            "reflection",
            "hat",
            "addition",
            "finding",
            "fortune",
            "promotion",
            "hall",
            "efficiency",
            "feedback",
            "argil",
            "construction",
            "office",
            "breath",
            "location",
            "aepyornis",
            "university",
            "introduction",
            "basket",
            "leader",
            "inflation",
            "way",
            "wealth",
            "president",
            "dog",
            "importance",
            "mound",
            "preparation",
            "xenodocheionology",
            "potato",
            "basis",
            "difficulty",
            "entry",
            "advertising",
            "drama",
            "freedom",
            "housing",
            "interpretation",
            "doromania",
            "activity",
            "block",
            "acapnotic",
            "nanity",
            "topic",
            "tooth",
            "wife",
            "information",
            "lab",
            "equipment",
            "divination",
            "collection",
            "garden",
            "extent",
            "grocery",
            "dinner",
            "explanation",
            "solution",
            "confusion",
            "marketing",
            "product",
            "membership",
            "narcocracy",
            "politics",
            "flight",
            "lady",
            "recognition",
            "bedroom",
            "warning",
            "presence",
            "vomit",
            "tennis",
            "therm",
            "sphinx",
            "art",
            "responsibility",
            "establishment",
            "bird",
            "judgment",
            "recording",
            "vagitus",
            "negotiation",
            "success",
            "member",
            "airport",
            "driver",
            "quality",
            "thalposis",
            "night",
            "writing",
            "population",
            "sensation",
            "pizza",
            "priority",
            "revolution",
            "cynophilist",
            "dark",
            "restaurant",
            "analyst",
            "assumption",
            "conversation",
            "government",
            "uncle",
            "candidate",
            "teacher",
            "nature",
            "guidance",
            "response",
            "ecarlate",
            "artisan",
            "drug",
            "understanding",
            "aspect",
            "poet",
            "reading",
            "girl",
            "hospital",
            "poetry",
            "police",
            "conclusion",
            "cigarette",
            "recipe",
            "pollarchy",
            "setting",
            "communication",
            "week",
            "manager",
            "theorie",
            "charity",
            "photo",
            "arthroscope",
            "amphigory",
            "interaction",
            "vehicle",
            "grille",
            "birthday",
            "sample",
            "maintenance",
            "appearance",
            "organization",
            "sable",
            "visor",
            "development",
            "problem",
            "tale",
            "emotion",
            "stranger",
            "safety",
            "diamond",
            "society",
            "unit",
            "animal",
            "story",
            "quizz",
            "energy",
            "black",
            "event",
            "affair",
            "dad",
            "suggestion",
            "resource",
            "church",
            "garbage",
            "pain",
            "elevator",
            "boyfriend",
            "cookie",
            "height",
            "insurance",
            "intention",
            "fact",
            "device",
            "wedding",
            "math",
            "power",
            "potager",
            "bathyorographical",
            "effort",
            "drawer",
            "inspector",
            "video",
            "passion",
            "actor",
            "condition",
            "mood",
            "clay",
            "language",
            "instance",
            "ratio",
            "leadership",
            "winner",
            "depth",
            "mixture",
            "science",
            "ambition",
            "truth",
            "estate",
            "ad",
            "proposal",
            "advice",
            "mesnalty",
            "month",
            "salt",
            "reception",
            "opportunity",
            "gate",
            "chemistry",
            "celebration",
            "election",
            "internet",
            "tonneau",
            "osmometer",
            "newspaper",
            "vortex",
            "recommendation",
            "ear",
            "perception",
            "courage",
            "moment",
            "strategy",
            "foundation",
            "bars",
            "goal",
            "friendship",
            "situation",
            "relation",
            "person",
            "vestment",
            "writer",
            "chocolate",
            "horse",
            "menu",
            "buffoon",
            "elevation",
            "news",
            "patience",
            "thanks",
            "comparison",
            "vestiarian",
            "tradition",
            "powder",
            "magazine",
            "contribution",
            "fishing",
            "song",
            "ability",
            "cancer",
            "permission",
            "percentage",
            "pollution",
            "hearing",
            "indication",
            "data",
            "baby",
            "version",
            "committee",
            "apartment",
            "preference",
            "comedogenic",
            "context",
            "medicine",
            "parquet",
            "application",
            "director",
            "child",
            "session",
            "meat",
            "catadromous",
            "helmet",
            "moss",
            "policy",
            "association",
            "pie",
            "bookworm",
            "guest",
            "inheritance",
            "region"
            ]

#Randomly choose a word from the word_list and assign it to a variable called chosen_word.
chosen_word = random.choice(word_list)
end_of_game = False
lives = 6
guessed_letters = []
#For each letter in the chosen_word, add a "_" to 'display'.
display = []
hinted = False

for char in chosen_word:
    if char != " ":
        display.append("_")
    else:
        display.append(char)

word_length = display.count('_')

print(logo)
print("Welcome to HANGMAN!\n\nYour random word has been generated! Can you guess it?\n" + "-"*50)
print(f"Your {word_length} letter word is:\n")
print("".join(display) + "\n")

#Testing code
print(f'Pssst, the solution is {chosen_word}.')

while not end_of_game:

    if len(guessed_letters):
        print(f"\nThe letters you already tried are:\n{guessed_letters}")
    else:
        print(stages[lives])

    #Ask the user to guess a letter and assign their answer to a variable called guess. Make guess lowercase.
    while True:
        guess = input("\nGuess a letter: ").upper()

        # Check if character input is in the alphabet and ask for another input if not
        if len(guess) > 1:
            print("You should only try one letter at a time!")
            continue
        elif guess in string.ascii_uppercase and guess != "":
            # Check if chosen letter has already been guessed
            if guess in guessed_letters:
                print(f"You already tried this {guess}! Try a different letter!")
                continue
            else:
                guessed_letters.append(guess)
                break
        else:
            print("Wrong character! Pick a letter in the range A-Z!")
            print(stages[lives])

    # Check if guessed letter is in the word
    if guess not in chosen_word.upper():
        lives -= 1
    print(stages[lives])

    # If the letter at that position matches 'guess' then reveal that letter in the display at that position.
    for position in range(len(chosen_word)):
        if guess == chosen_word[position].upper():
            display[position] = chosen_word[position].upper()

    # Print refreshed 'display'
    print(f"Your {word_length} letter word is:\n")
    print("\n"+ "".join(display))

    if "_" not in display:
        end_of_game = True
        print("\nYou win!")

    if lives == 1 and not hinted:
        hinted = True
        hint = input("Do you want a hint?\nY/N\n")

        if hint.upper() == "Y":
            remaining_chars = set(string.ascii_uppercase).difference(set(guessed_letters).union({l.upper() for l in chosen_word}))
            count = 0
            print(f"You have {int(len(remaining_chars) / 4)} letter/s added to the guessed letters list!")

            for _ in range(int(len(remaining_chars) / 4)):
                while True:
                    if count == int(len(remaining_chars) / 4):
                        break
                    add_letter = random.choice(list(remaining_chars))
                    if add_letter not in chosen_word.upper():
                        guessed_letters.append(add_letter)
                        count += 1
                    else:
                        continue

    if lives == 0:
        end_of_game = True
        print("\nYou lose!")
        print(f"\nYour word was: {chosen_word.upper()}")