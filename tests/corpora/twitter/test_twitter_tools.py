import argparse
import collections
import os
import unittest
from tempfile import NamedTemporaryFile

from corpora.twitter import twitter_tools

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
INPUT_FIXTURE = os.path.join(DIR_PATH, "fixtures", "input.txt")
OUTPUT_FIXTURE = os.path.join(DIR_PATH, "fixtures", "output.txt")


class TestTwitterTools(unittest.TestCase):
    """Tests for the Twitter corpus tooling."""

    def test_count_words_in_tweets_empty(self):
        """Test counting words in empty list of tweets."""
        tweets = []
        expected = collections.Counter()
        self.assertEqual(twitter_tools._count_words_in_tweets(tweets), expected)

    def test_count_words_in_tweets_basic(self):
        """Test counting words in simple list of tweets."""
        tweets = [
            "test tweet one",
            "test tweet two",
            "test tweet three",
        ]
        expected = collections.Counter(
            {"TEST": 3, "TWEET": 3, "ONE": 1, "TWO": 1, "THREE": 1}
        )
        self.assertEqual(twitter_tools._count_words_in_tweets(tweets), expected)

    def test_count_words_in_tweets_punctuation(self):
        """Test counting words in tweets with weird characters and punctuation."""
        tweets = [
            "That's data. ",  # punctuation is ignored
            "UK weather data 11:00 PM 11.8°C 83 pct",  # strange characters ignored
            "ηταν περιεργα ρρ",  # only handle a-z characters
        ]
        expected = collections.Counter(
            {
                "": 5,  # This is expected; it's more efficient to remove it later on
                "THATS": 1,
                "DATA": 2,
                "UK": 1,
                "WEATHER": 1,
                "PM": 1,
                "C": 1,
                "PCT": 1,
            }
        )
        self.assertEqual(twitter_tools._count_words_in_tweets(tweets), expected)

    def test_count_words_for_basic_input(self):
        """Test that the tool counts the words in a short file."""
        with NamedTemporaryFile(mode="w+t", delete=False) as i, NamedTemporaryFile(
            mode="w+t"
        ) as o:
            # Write some simple "tweets" into the input file
            i.write("tweet foo\n")
            i.write("tweet bar\n")
            i.write("tweet bar\n")
            i.close()
            # Set up the args with our temp input/output files, and call count_words
            args = argparse.Namespace(input=i.name, output=o.name, quiet=True)
            twitter_tools.count_words(args)
            # Check that the counts are correct
            word_counts = o.read()
        self.assertEqual(word_counts, "TWEET 3\nBAR 2\nFOO 1\n")

    def test_count_words_with_realistic_input(self):
        """Test the tool counts the words in a reasonably large, real-looking file."""
        with NamedTemporaryFile(mode="w+t") as o:
            # Set up the args with our temp input/output files, and call count_words
            args = argparse.Namespace(input=INPUT_FIXTURE, output=o.name, quiet=True)
            twitter_tools.count_words(args)
            # Check that the counts are correct
            word_counts = o.read()
        with open(OUTPUT_FIXTURE) as f:
            self.assertEqual(word_counts, f.read())
