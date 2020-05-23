"""Tool to clean wordcounts files by removing the count."""

import argparse


def clean_word_counts(args):
    """Remove count from wordcounts file."""
    with open(args.valid_words) as f:
        valid_words = set(word.strip() for word in f)
    with open(args.word_counts) as i, open(args.output, "w") as o:
        o.writelines(
            line.split()[1] + "\n" for line in i if line.split()[0] in valid_words
        )


if __name__ == "__main__":
    # Pull arguments from the command line
    parser = argparse.ArgumentParser(description="Intersect two datasets of words.")
    parser.add_argument(
        "--word-counts", "-w", required=True, help="Input word counts",
    )
    parser.add_argument(
        "--valid-words", "-v", required=True, help="Valid word list",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="intersection.txt",
        help="Output file to write intersected word list to",
    )
    args = parser.parse_args()

    # Process the input word lists, and write the intersected output
    print("Processing input datasets...")
    clean_word_counts(args)
    # word_lists = read_word_lists(args.input, args.ignore)
    # intersection = intersect_word_lists(word_lists)
    # write_intersection(intersection, args.output)
    print(f"Success! Your intersected word list is at `{args.output}`.")
