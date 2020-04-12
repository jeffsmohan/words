import argparse
import collections
import os
import re
from typing import List

import tqdm

FILE_IGNORE_PATTERN = r"(</?doc.*?>|-)"
WORD_IGNORE_PATTERN = r"[^A-Z]"


def count_words(args: argparse.Namespace) -> None:
    """Count the words in the Wikipedia corpus."""
    if not args.quiet:
        print("Processing Wikipedia...")

    # Read wikipedia data in from files, track word counts
    input_files = _find_input_files(args.input)
    input_files_iter = tqdm.tqdm(input_files) if not args.quiet else input_files
    word_counts = collections.Counter()
    for input_file in input_files_iter:
        word_counts += _count_words_in_file(input_file)
    del word_counts[""]

    # Output the word counts to a file
    if not args.quiet:
        print("Writing word counts to disk...")
    _output_word_counts(word_counts, args.output)
    if not args.quiet:
        print(f"Done! See word counts in {args.output}.")


def _find_input_files(top: str) -> List[str]:
    """Find all files within subdirectories."""
    input_files = []
    for root, dirs, files in os.walk(top):
        for file in files:
            input_files.append(os.path.join(root, file))
    return input_files


def _count_words_in_file(input_file: str) -> collections.Counter:
    """Return a Counter with the word counts from the given file."""
    with open(input_file) as f:
        contents = f.read()
    cleaned = re.sub(FILE_IGNORE_PATTERN, " ", contents)
    return collections.Counter(
        re.sub(WORD_IGNORE_PATTERN, "", word.upper()) for word in cleaned.split()
    )


def _output_word_counts(word_counts: collections.Counter, output_file: str) -> None:
    """Output the list of most common words to the output file."""
    with open(output_file, "w") as f:
        for word, count in word_counts.most_common():
            f.write(f"{word} {count}\n")


if __name__ == "__main__":
    SUBCOMMANDS = {
        "count_words": count_words,
    }
    parser = argparse.ArgumentParser(description="Wikipedia tools")
    parser.add_argument(
        "subcommand",
        choices=SUBCOMMANDS.keys(),
        help="Which Wikipedia operation to perform",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Disables progress indicators on stdout",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="data",
        help="Specifies the directory to crawl for input Wikipedia corpus data",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="wordcounts.txt",
        help="Specifies the location to output the results",
    )
    args = parser.parse_args()

    # Call the correct subcommand
    command = SUBCOMMANDS[args.subcommand]
    command(args)
