import argparse
from gutenberg.acquire import get_metadata_cache


def prime_cache():
    """
    Primes the Project Gutenberg cache so future queries are fast.

    Note that this can take ~18 hours on a standard laptop.
    """
    print('Populating Gutenberg cache. This may take a few hours...')
    cache = get_metadata_cache()
    cache.populate()


if __name__ == "__main__":
    SUBCOMMANDS = {
        'prime_cache': prime_cache,
    }
    parser = argparse.ArgumentParser(description='Project Gutenberg tools')
    parser.add_argument('subcommand', choices=SUBCOMMANDS.keys())
    args = parser.parse_args()

    command = SUBCOMMANDS[args.subcommand]
    command()
