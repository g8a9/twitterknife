Twitterknife
============

<!-- [![image](https://img.shields.io/pypi/v/twitterknife.svg)](https://pypi.python.org/pypi/twitterknife)

[![image](https://img.shields.io/travis/g8a9/twitterknife.svg)](https://travis-ci.com/g8a9/twitterknife)

[![Documentation Status](https://readthedocs.org/projects/twitterknife/badge/?version=latest)](https://twitterknife.readthedocs.io/en/latest/?version=latest) -->

Simple helper functions for tweet preprocessing. \
We support processing the tweet jsonl files extracted from client libraries such as [twarc](https://twarc-project.readthedocs.io/en/latest/twarc2_en_us/).

<!-- -   Free software: MIT license -->
<!-- -   Documentation: <https://twitterknife.readthedocs.io>. -->

## Features

We currently support:

- tweet parsing
- cleaning the text (strip accents, user handles and urls normalization, etc.)
- frequent word sets mining (through FPGrowth from [mlxtend](https://github.com/rasbt/mlxtend))
- association rules mininig
- topic detection (through [CTM](https://github.com/MilaNLProc/contextualized-topic-models))

## Basic Preprocessing

```python
import twitterknife.twitterknife as tkf

# 1. parse the raw jsonl file
tweets = tkf.parse_jsonl("tweets.json")

# 2. extract base information from the tweet structure
tweet_info = tkf.get_base_info(tweets)

# 3. remove tweets we don't have data for
tweet_info = [t for t in tweet_info if t["has_data"]]

# 4. clean texts
proc_texts = tkf.clean_texts((t["tweet_text"] for t in tweet_info))
```

### Text Mining

Frequent Word Sets and Association Rules Mining.

```python
with open("stopwords.txt") as fp:
    stopwords = [l.strip() for l in fp.readlines()]

# clean texts first
texts = tkf.clean_texts(raw_texts, strip_user_handles=False, strip_punctuation=True)

# FP Growth Mining
frequent_word_sets = tkf.frequent_word_sets(
    texts,
    stopwords=stopwords,
    fpgrowth_args={"min_support": 0.005, "max_len": 10}
)

# Association Rules Mining
ass_rules = tkf.association_rules_mining(
    frequent_word_sets, metric="confidence", min_threshold=0.4
)
```

### Topic Discovery

```python
kt = tkf.find_topics(texts, n_topics=5, stopwords=stopwords)
```


Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
