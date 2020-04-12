import argparse
import collections
import re
import subprocess
from typing import List

import tqdm

WORD_IGNORE_PATTERN = r"[^A-Z]"
MAX_WORD_COUNT_LENGTH = 500_000
PROCESS_CHUNK_SIZE = 50_000


def count_words(args: argparse.Namespace) -> None:
    """Count words in the Stanford Twitter dataset."""
    # Count lines so we can display a nice progress bar
    if not args.quiet:
        print("Analyzing Twitter content (can take a couple minutes)...")
    line_count_output = subprocess.check_output(
        f"wc -l {args.input}", shell=True, encoding="utf-8"
    )
    line_count = int(re.search(r"^\s*(\d+)", line_count_output).groups()[0])

    # Read tweets in from file and process their words
    word_counts = collections.Counter()
    with open(args.input, encoding="utf-8") as f, tqdm.tqdm(
        total=line_count, unit="tweet", unit_scale=True
    ) as progress:
        tweets = []
        for i, tweet in enumerate(f):
            tweets.append(tweet)
            # For efficiency, only periodically turn the tweets into word counts
            if i % PROCESS_CHUNK_SIZE == 0:
                word_counts += _count_words_in_tweets(tweets)
                tweets = []
                # Also trim the least common words, since they're usually
                # gibberish and it's helpful to keep memory pressure down
                word_counts = collections.Counter(
                    dict(word_counts.most_common(MAX_WORD_COUNT_LENGTH))
                )
                progress.update(PROCESS_CHUNK_SIZE)
        word_counts += _count_words_in_tweets(tweets)
        del word_counts[""]

    # Output the word counts to a file
    if not args.quiet:
        print("Writing word counts to disk...")
    _output_word_counts(word_counts, args.output)
    if not args.quiet:
        print(f"Done! See word counts in {args.output}.")


def _count_words_in_tweets(tweets: List[str]) -> collections.Counter:
    """Return a Counter with the word counts from the given list of tweets."""
    return collections.Counter(
        re.sub(WORD_IGNORE_PATTERN, "", word.upper())
        for word in " ".join(tweets).split()
    )


def _output_word_counts(word_counts: collections.Counter, output_file: str) -> None:
    """Output the list of most common words to the output file."""
    with open(output_file, "w") as f:
        for word, count in word_counts.most_common(MAX_WORD_COUNT_LENGTH):
            f.write(f"{word} {count}\n")


if __name__ == "__main__":
    SUBCOMMANDS = {
        "count_words": count_words,
    }
    parser = argparse.ArgumentParser(description="Twitter tools")
    parser.add_argument(
        "subcommand",
        choices=SUBCOMMANDS.keys(),
        help="Which Twitter operation to perform",
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
        default="tweets.txt",
        help="Specifies the tweet dataset to ingest",
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
