Twitter Corpus
==============

Twitter is a great resource for modern, "in-the-language" words. Unfortunately, Twitter makes it unnecessarily difficult to acquire datasets of tweets. They have very strict rate-limiting for use of their APIs, and they seem to proactively get tweet datasets removed from the internet. There are a number of ways to work around this, so this just represents one that worked for me.

There's a [Stanford dataset](https://snap.stanford.edu/data/twitter7.html) of 467 million tweets collected in the latter half of 2009. It appears to have been removed at Twitter's request, but the files seem to still be available.

Word Counts File
----------------

The `wordcounts.txt` file in this directory lists all words in the Twitter corpus, along with their count. The format is one word per line, in all caps, followed by a space, then an integer count. An example excerpt:

```
FILMS 405214
FESTIVAL 403587
CENSUS 403419
```

Downloaad And Re-Process Tweets
-------------------------------

In order to reproduce the `wordcounts.txt` file, you can follow the steps here. (Depending on the computing power, this process may need several days to run.)

1. Download the 6 raw tweet data files (~10GB gzipped).

   ```
   wget http://snap.stanford.edu/data/bigdata/twitter7/tweets2009-06.txt.gz -P corpora/twitter/data
   wget http://snap.stanford.edu/data/bigdata/twitter7/tweets2009-07.txt.gz -P corpora/twitter/data
   wget http://snap.stanford.edu/data/bigdata/twitter7/tweets2009-08.txt.gz -P corpora/twitter/data
   wget http://snap.stanford.edu/data/bigdata/twitter7/tweets2009-09.txt.gz -P corpora/twitter/data
   wget http://snap.stanford.edu/data/bigdata/twitter7/tweets2009-10.txt.gz -P corpora/twitter/data
   wget http://snap.stanford.edu/data/bigdata/twitter7/tweets2009-11.txt.gz -P corpora/twitter/data
   wget http://snap.stanford.edu/data/bigdata/twitter7/tweets2009-12.txt.gz -P corpora/twitter/data
   ```

2. Activate our Python virtualenv.

   `./env/bin/activate` (or `. env/bin/activate.fish` for fish shell)

3. Install our Python requirements.

   `pip install -r requirements.txt`

4. Count the word frequencies from the extracted text using the `twitter_tools.py` tool:

   `python twitter_tools.py -i corpora/twitter/data -o corpora/twitter/wordcounts.txt`
