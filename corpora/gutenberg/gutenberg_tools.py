import argparse
import collections
import itertools
import re
import tqdm
from gutenberg.acquire import get_metadata_cache, load_etext
from gutenberg.query import get_etexts
from gutenberg import Error as GutenbergError
from typing import List


# Mirrors: https://www.gutenberg.org/MIRRORS.ALL
MIRRORS = [
    'http://www.mirrorservice.org/sites/ftp.ibiblio.org/pub/docs/books/gutenberg/',
    'http://eremita.di.uminho.pt/gutenberg/',
    'http://mirror.csclub.uwaterloo.ca/gutenberg/',
    'http://www.gutenberg.org/dirs/',
    'http://mirrors.xmission.com/gutenberg/',
    'https://gutenberg.pglaf.org/',
    'http://aleph.gutenberg.org/',
    'http://gutenberg.readingroo.ms/',
]
WORD_IGNORE_PATTERN = r'[^A-Z]'


def prime_query_cache(args: argparse.Namespace) -> None:
    """
    Primes the Project Gutenberg metadata cache so future queries are fast.

    Note that this can take ~18 hours on a standard laptop, and is not required
    if you're only doing a few simple queries.
    """
    if not args.quiet:
        print('Populating Gutenberg cache. This may take a few hours...')
    cache = get_metadata_cache()
    cache.populate()
    if not args.quiet:
        print('Done!')


def prime_text_cache(args: argparse.Namespace) -> None:
    """
    Primes the Project Gutenberg text cache so text retrieval is entirely local.

    This will download all Gutenberg book texts onto your local machine, which
    will take many hours and ~10-20GB.
    """
    if not args.quiet:
        print('Downloading Project Gutenberg book texts...')
    etexts = get_etexts('language', args.language)
    # Cycle through mirrors so as not to overload anyone's servers and get rate-limited
    etexts_with_mirrors = list(zip(etexts, itertools.cycle(MIRRORS)))
    etexts_iter = tqdm.tqdm(etexts_with_mirrors) if not args.quiet else etexts_with_mirrors

    success_count = 0
    total_count = 0
    try:
        for etext, mirror in etexts_iter:
            total_count += 1
            try:
                content = load_etext(etext, mirror=mirror)
                success_count += 1
            except GutenbergError as e:
                if not args.quiet:
                    print(f'Failure (mirror: {mirror}) ', e)
                continue
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Error with mirror: ', mirror, etext)
        raise

    if not args.quiet:
        print(f'{success_count} / {total_count} books downloaded to cache')
        print('Done!')


def count_words(args: argparse.Namespace) -> None:
    """Counts the words in all Gutenberg books for a given language."""
    # Pull the list of book IDs
    if not args.quiet:
        print('Processsing Project Gutenberg books...')
    etexts = get_etexts('language', args.language)
    etexts_iter = tqdm.tqdm(etexts) if not args.quiet else etexts

    # Load each book and count the words
    word_counts = collections.Counter()
    failed_etexts = []
    for etext in etexts_iter:
        try:
            content = load_etext(etext)
        except GutenbergError as e:
            failed_etexts.append(etext)
            print('Failure: ', e)
            continue
        word_counts += _count_words_in_content(content)
    del word_counts['']

    # Output the word counts to a file
    if not args.quiet:
        print(f'Failed to download {len(failed_etexts)} books. (A few of these are normal, as some books have no text.)')
        print(f'--- Failed: {", ".join(str(etext) for etext in failed_etexts)}')
        print('Writing word counts to disk...')
    _output_word_counts(word_counts, args.output)
    if not args.quiet:
        print(f'Done! See word counts in {args.output}.')



def _count_words_in_content(content: str) -> collections.Counter:
    """Returns a Counter with the word counts from the given text."""
    return collections.Counter(
        re.sub(WORD_IGNORE_PATTERN, '', word.upper())
        for word in content.split()
    )


def _output_word_counts(word_counts: collections.Counter, output_file: str) -> None:
    """Outputs the list of most common words to the output file."""
    with open(output_file, 'w') as f:
        for word, count in word_counts.most_common():
            f.write(f'{word} {count}\n')


if __name__ == "__main__":
    SUBCOMMANDS = {
        'prime_query_cache': prime_query_cache,
        'prime_text_cache': prime_text_cache,
        'count_words': count_words,
    }
    parser = argparse.ArgumentParser(description='Project Gutenberg tools')
    parser.add_argument('subcommand', choices=SUBCOMMANDS.keys(), help='Which Gutenberg operation to perform')
    parser.add_argument('-q', '--quiet', action='store_true', help='Disables progress indicators on stdout')
    parser.add_argument('-l', '--language', default='en', help='Specifies the language of books to use')
    parser.add_argument('-o', '--output', default='wordcounts.txt', help='For count_words, specifies the location to output the results')
    args = parser.parse_args()

    # Call the correct subcommand
    command = SUBCOMMANDS[args.subcommand]
    command(args)
