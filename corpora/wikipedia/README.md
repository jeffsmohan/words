Wikipedia Corpus
================

Tools for extracting the entire English-language wikipedia text corpus and sorting by frequency.

Word Counts File
----------------

The `wordcounts.txt` file in this directory lists all words in the Wikipedia corpus, along with their count. The format is one word per line, in all caps, followed by a space, then an integer count. An example excerpt:

```
FILMS 405214
FESTIVAL 403587
CENSUS 403419
```

Re-Processing The Corpus
------------------------

In order to reproduce the `wordcounts.txt` file, you can follow the steps here. (Depending on the computing power, this process may need several days to run.)

1. Download the latest Wikipedia database dump (this is a ~16GB file):

   `wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2 -P corpora/wikipedia/data`

2. Extract the text from the articles using [Wikipedia Extractor](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) (generates ~15GB of text files and takes a couple days on my laptop):

   `python corpora/wikipedia/WikiExtractor.py -o corpora/wikipedia/data enwiki-latest-pages-articles.xml.bz2`

   This will write many files named `corpora/wikipedia/data/??/wiki_??`.

3. Count the word frequencies from the extracted text using the `wordcount.py` tool:

   `python wordcount.py -i corpora/wikipedia/data -o corpora/wikipedia/data/wordcounts.txt`
