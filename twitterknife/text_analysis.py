"""Module with helper function to extract information from text."""

import pandas as pd
from beartype import beartype
from beartype.typing import List, Optional
from contextualized_topic_models.models.kitty_classifier import Kitty
from mlxtend.frequent_patterns import association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder
from nltk.tokenize import TweetTokenizer

FPGROWTH_ARGS = {"min_support": 0.6, "max_len": None}


@beartype
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


@beartype
def association_rules_mining(
    frequent_word_sets: pd.DataFrame,
    metric: Optional[str] = "confidence",
    min_threshold: Optional[float] = 0.7,
):
    return association_rules(
        frequent_word_sets, metric=metric, min_threshold=min_threshold
    )


def find_topics(
    texts: List[str],
    embedding_model: Optional[str] = "paraphrase-multilingual-mpnet-base-v2",
    contextual_size: Optional[int] = 768,
    n_topics: Optional[int] = 5,
    epochs: Optional[int] = 5,
    stopwords: Optional[List[str]] = None,
):
    kt = Kitty()
    kt.train(
        texts,
        topics=n_topics,
        embedding_model=embedding_model,
        contextual_size=contextual_size,
        epochs=epochs,
        stopwords_list=stopwords,
    )

    print(kt.pretty_print_word_classes())
    return kt
