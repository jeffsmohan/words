"""
Tool to read in word lists and write out the intersection.

Useful for reading in a way-too-large-to-be-fun tournament-legal word list and
a list of the top most common English words, in order to make a more everyday
word list.

To start out, I'm using `tournament_dictionary.txt`, which ~280,000 
tournament-legal words, and `wiki-100k.txt`, which is the top ~100,000
English words from wiktionary (including some gibberish). The result is
`dictionary.txt` in this directory, which is ~40,000 reasonably common
English words.
"""

import argparse
import functools
import re
import sys
from typing import List


IGNORE_PATTERNS = [
    r'^#!comment:',
]


def clean_word(word: str) -> str:
    """Ensures words are uppercase and don't contain special characters."""
    return re.sub(r'[^A-Z]', '', word.upper())


def read_word_lists(paths: List[str], ignore_patterns: List[str]) -> List[set]:
    """Reads word lists from disk and returns a list of sets."""
    word_lists = []
    for path in paths:
        word_list = set()
        word_lists.append(word_list)
        with open(path) as f:
            for line in f:
                for pattern in ignore_patterns:
                    if re.search(pattern, line):
                        break
                else:
                    # Line didn't match any ignore patterns, add to word list
                    word_list.add(clean_word(line))
    return word_lists


def intersect_word_lists(word_lists: List[set]) -> set:
    """Builds the intersection of the word lists."""
    return functools.reduce(lambda a, b: a & b, word_lists)


def write_intersection(intersection: set, path: str) -> None:
    """Writes out the final intersected word list."""
    with open(path, 'w') as f:
        f.writelines(word + '\n' for word in sorted(intersection))


if __name__ == '__main__':
    # Pull arguments from the command line
    parser = argparse.ArgumentParser(description='Intersect two datasets of words.')
    parser.add_argument('--input', '-i', action='append', required=True, help='Input text files of words to intersect (provide two or more)')
    parser.add_argument('--output', '-o', default='intersection.txt', help='Output file to write intersected word list to')
    parser.add_argument('--ignore', action='append', default=IGNORE_PATTERNS, help='Regex patterns identifying lines to ignore from the word lists (e.g., `^#!comment:`)')
    args = parser.parse_args()

    # Validate input args
    if len(args.input) < 2:
        print('You must provide at least two inputs to intersect', file=sys.stderr)
        sys.exit(1)

    # Process the input word lists, and write the intersected output
    print('Processing input datasets...')
    word_lists = read_word_lists(args.input, args.ignore)
    intersection = intersect_word_lists(word_lists)
    write_intersection(intersection, args.output)
    print(f'Success! Your intersected word list is at `{args.output}`.')
