"""
Helper functions for finding pangrams using words in a set.

For example, given a list of 100 animals, this tool can return sets like
{CHIMPANZEE, GIRAFFE, JACKRABBIT, LYNX, SQUID, WOLVERINE} that contain every
letter of the alphabet.
"""

import collections
import string


ALPHABET = set(string.ascii_uppercase)


def analyze_words(word_set):
    """
    Utility to identify uncommon letters in a word set.

    Returns a list of 2-tuples, each containing the letter of the alphabet and
    how many words in the set have that letter.

    Useful for identifying under-represented letters so you can beef up your
    word set with more helpful words.
    """
    counts = collections.Counter()
    for word in word_set:
        for letter in set(word.upper()):
            counts.update(letter)
    return reversed(counts.most_common())


def find_pangrams(word_set, depth_max=6, current_words=None):
    """
    Finds minimal pangrams out of a set of words.

    Call with any iterable of words, and it returns a list of pangrams,
    if any, sorted by increasing letter count. You can set depth_max to control
    search depth if your word set calls for it.

    Depth-first recursive search with minor optimizations for prioritizing
    branches most likely to be fruitful and pruning branches with no
    possibility of success. Runs in under a second for e.g. a list of ~100
    words.
    """
    # Recursion base case: we found a pangram! No need to recurse and add more words
    if current_words is None:
        current_words = []
    letters = set(letter for word in current_words for letter in word)
    if letters >= ALPHABET:
        return [(len(''.join(current_words)), sorted(current_words))]

    # Recursion base case: we're at maximum search depth
    if depth_max == 0:
        return []

    # Recursion base cases: we've run out of useful wordss
    if len(word_set) == 0:
        return []

    # Optimization: order word_set by usefulness and remove useless words
    word_set = set(word.upper() for word in word_set)
    needed_letters = ALPHABET - letters
    optimized_word_set = sorted(
        (len(set(word) & needed_letters), word)
        for word in word_set
    )

    # Otherwise: add a word to the list and recurse
    solutions = []
    while optimized_word_set:
        value, word = optimized_word_set.pop()
        # Optimization: if value * depth is less than needed letters, branch would be impossible
        if value * depth_max < len(needed_letters):
            continue
        solutions += find_pangrams(
            set(word for value, word in optimized_word_set),
            depth_max=depth_max - 1,
            current_words=current_words + [word],
        )
    return sorted(solutions)


if __name__ == "__main__":
    ANIMALS = [
        'Aardvark',
        'Aardwolf',
        'Addax',
        'Alligator',
        'Armadillo',
        'Badger',
        'Butterfly',
        'Capybara',
        'Caribou',
        'Cheetah',
        'Chicken',
        'Chimpanzee',
        'Chinchilla',
        'Chipmunk',
        'Coyote',
        'Crocodile',
        'Dolphin',
        'Dragonfly',
        'Earthworm',
        'Elephant',
        'Flatworm',
        'Giraffe',
        'Gorilla',
        'Grasshopper',
        'Hamster',
        'Hedgehog',
        'Hippopotamus',
        'Hornet',
        'Horse',
        'Impala',
        'Jackal',
        'Jaguar',
        'Jellyfish',
        'Kinkajou',
        'Koala',
        'Lemming',
        'Lemur',
        'Lizard',
        'Lynx',
        'Manatee',
        'Meerkat',
        'Monkey',
        'Ocelot',
        'Okapi',
        'Penguin',
        'Porcupine',
        'Rattlesnake',
        'Rhinoceros',
        'Seahorse',
        'Skylark',
        'Sloth',
        'Tapir',
        'Tortoise',
        'Turtle',
        'Vulture',
        'Wallaby',
        'Wasp',
        'Weasel',
        'Whale',
        'Wildebeest',
        'Wolverine',
        'Wolf',
        'Wombat',
        'Worm',
        'Zebra',
        'Quail',
        'Quetzal',
        'Quokka',
        'Squirrel',
        'Gazelle',
        'Buzzard',
        'Ox',
        'Ibex',
        'Fox',
        'Squid',
        'Macaque',
        'Oryx',
        'Viper',
        'Vole',
        'Vulture',
        'Muntjac',
        'Bluejay',
        'Jerboa',
        'Jackrabbit',
        'Kipunji',
        'Zebu',
        'Zebrafish',
        'Zorilla',
        'Zokor',
        'Finch',
        'Frog',
        'Fossa',
        'Ferret',
        'Axolotl',
        'Hyrax',
        'Plover',
        'Pangolin',
        'Beaver',
        'Vervet',
        'Serval',
        'Civet',
        'Otter',
        'Tardigrade',
        'Narwhal',
    ]

    for count, solution in find_pangrams(ANIMALS):
        print(f'({count}) {", ".join(solution)}')
