import argparse
import collections
import gzip
import re
import os
import tqdm
from typing import List


WORD_IGNORE_PATTERN = r'[^A-Z]'


def count_words(args: argparse.Namespace) -> None:
    """Counts words in the Stanford Twitter dataset."""
    if not args.quiet:
        print('Processsing Twitter content...')

    # Read tweets in from files
    input_files = _get_input_files(args.input)
    word_counts = collections.Counter()
    for input_file in input_files:
        word_counts += _get_file_word_counts(input_file)

    # Output the word counts to a file
    if not args.quiet:
        print('Writing word counts to disk...')
    _output_word_counts(word_counts, args.output)
    if not args.quiet:
        print(f'Done! See word counts in {args.output}.')


def _get_input_files(input_directory: str) -> List[str]:
    """Walks the filesystem to return *.txt.gz files."""
    input_files = []
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.txt.gz'):
                input_files.append(os.path.join(root, file))
    return input_files


def _get_file_word_counts(input_file: str) -> collections.Counter:
    """Loads the file, extracts the tweet text, and returns the word count."""
    word_counts = collections.Counter()
    with gzip.open(input_file) as f:
        for line in f.readlines():
            # The twitter dataset format includes a "W[tab]" to indicate the start
            # of a tweet's text
            if line.startswith('W'):
                word_counts += collections.Counter(
                    re.sub(WORD_IGNORE_PATTERN, '', word.upper())
                    for word in line[2:].split()
                )
    return word_counts


def _output_word_counts(word_counts: collections.Counter, output_file: str) -> None:
    """Outputs the list of most common words to the output file."""
    with open(output_file, 'w') as f:
        for word, count in word_counts.most_common():
            f.write(f'{word} {count}\n')


if __name__ == "__main__":
    SUBCOMMANDS = {
        'count_words': count_words,
    }
    parser = argparse.ArgumentParser(description='Twitter tools')
    parser.add_argument('subcommand', choices=SUBCOMMANDS.keys(), help='Which Twitter operation to perform')
    parser.add_argument('-q', '--quiet', action='store_true', help='Disables progress indicators on stdout')
    parser.add_argument('-i', '--input', default='data', help='Specifies the top-level directory of the input dataset')
    parser.add_argument('-o', '--output', default='wordcounts.txt', help='Specifies the location to output the results')
    args = parser.parse_args()

    # Call the correct subcommand
    command = SUBCOMMANDS[args.subcommand]
    command(args)
