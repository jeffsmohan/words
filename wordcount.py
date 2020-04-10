"""
Tool to read in wikipedia corpus and output ordered word counts.
"""

import argparse
import collections
import os
import re
import sys
import tqdm
from typing import List


FILE_IGNORE_PATTERN = r'(</?doc.*?>|-)'
WORD_IGNORE_PATTERN = r'[^A-Z]'


def find_input_files(top: str) -> List[str]:
    """Finds all files within subdirectories."""
    input_files = []
    for root, dirs, files in os.walk(top):
        for file in files:
            input_files.append(os.path.join(root, file))
    return input_files

def count_words(input_file: str) -> collections.Counter:
    """Returns a Counter with the word counts from the given file."""
    with open(input_file) as f:
        contents = f.read()
    cleaned = re.sub(FILE_IGNORE_PATTERN, ' ', contents)
    return collections.Counter(
        re.sub(WORD_IGNORE_PATTERN, '', word.upper())
        for word in cleaned.split()
    )


def output_word_counts(word_counts: collections.Counter, output_file: str) -> None:
    """Outputs the list of most common words to the output file."""
    with open(output_file, 'w') as f:
        for word, count in word_counts.most_common():
            f.write(f'{word} {count}\n')


if __name__ == '__main__':
    # Pull arguments from the command line
    parser = argparse.ArgumentParser(description='Build ordered word counts from wikipedia corpus.')
    parser.add_argument('--input', '-i', default='text', help='Directory containing wikipedia files')
    parser.add_argument('--output', '-o', default='wordcounts.txt', help='Output file to write word list to')
    args = parser.parse_args()

    # Process the input word lists, and write the intersected output
    print('Processing wikipedia...')
    input_files = find_input_files(args.input)
    word_counts = collections.Counter()
    for input_file in tqdm.tqdm(input_files):
        word_counts += count_words(input_file)
    del word_counts['']
    print('Writing word counts to disk...')
    output_word_counts(word_counts, args.output)
    print(f'Done! See word counts in {args.output}.')
