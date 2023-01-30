"""Module with helper function to extract information from text."""

import pandas as pd
from beartype.typing import List, Optional
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
from nltk.tokenize import TweetTokenizer

FPGROWTH_ARGS = {"min_support": 0.6, "max_len": None}


def frequent_word_sets(
    texts: List[str],
    preserve_case: Optional[bool] = False,
    stopwords: Optional[List[str]] = None,
    fpgrowth_args: Optional[dict] = None,
):
    tknr = TweetTokenizer(preserve_case=preserve_case)

    if stopwords is not None:
        stopwords = set(stopwords)

    bow = list()
    for text in texts:
        if stopwords:
            bow.append(
                [token for token in tknr.tokenize(text) if token not in stopwords]
            )
        else:
            bow.append([token for token in text.split(" ")])

    # get bag of word repr
    te = TransactionEncoder()
    te_ary = te.fit(bow).transform(bow)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    algo_args = fpgrowth_args if fpgrowth_args is not None else FPGROWTH_ARGS
    frequent_items = fpgrowth(df, **algo_args, use_colnames=True)

    return frequent_items
