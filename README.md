Twitterknife
============

<!-- [![image](https://img.shields.io/pypi/v/twitterknife.svg)](https://pypi.python.org/pypi/twitterknife)

[![image](https://img.shields.io/travis/g8a9/twitterknife.svg)](https://travis-ci.com/g8a9/twitterknife)

[![Documentation Status](https://readthedocs.org/projects/twitterknife/badge/?version=latest)](https://twitterknife.readthedocs.io/en/latest/?version=latest) -->

Simple helper functions for tweet preprocessing. \
We support processing the tweet jsonl files extracted from client libraries such as [twarc](https://twarc-project.readthedocs.io/en/latest/twarc2_en_us/).

<!-- -   Free software: MIT license -->
<!-- -   Documentation: <https://twitterknife.readthedocs.io>. -->

## Getting Started


```python
import twitterknife.twitterknife as tkf

tweets = tkf.parse_jsonl("tweets.json")
tweet_info = tkf.get_base_info(tweets)

# remove tweets we don't have data for
tweet_info = [t for t in tweet_info if t["has_data"]]

# clean texts
proc_texts = tkf.clean_texts((t["tweet_text"] for t in tweet_info if t["has_data"]))
```

### Text Mining

Frequent Word Sets Mining

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
```


## Features

We currently support:

- tweet parsing
- cleaning the text (strip accents, substitute user handles and urls with placeholders)
- frequent word sets mining (fp growth)
- association rules mininig


Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
