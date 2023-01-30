"""Main module."""
import json
import string
import unicodedata

import ftfy
from beartype import beartype
from beartype.typing import Generator, List, Union
from tqdm import tqdm


@beartype
def parse_jsonl(path: str):
    with open(path) as fp:
        tweets = [json.loads(f.strip()) for f in fp.readlines()]
    return tweets


@beartype
def get_base_info(tweets: List[dict], show_progress: bool = True):
    tweet_info = list()

    for t in tqdm(tweets, disable=not show_progress):
        if "data" not in t:
            tweet_id = None
            tweet_text = None
            tweet_proc_text = None
            author_id = None
            created_at = None
            lang = None
            has_data = False
        else:
            tweet_id = t["data"]["id"]
            tweet_text = t["data"]["text"]
            author_id = t["data"]["author_id"]
            created_at = t["data"]["created_at"]
            lang = t["data"]["lang"]
            has_data = True

        tweet_info.append(
            dict(
                tweet_id=tweet_id,
                tweet_text=tweet_text,
                author_id=author_id,
                created_at=created_at,
                lang=lang,
                has_data=has_data,
            )
        )
    return tweet_info


@beartype
def clean_texts(
    texts: Union[List[str], Generator],
    clean_ftfy: bool = True,
    strip_new_lines: bool = True,
    strip_accents: bool = True,
    strip_punctuation: bool = False,
    keep_symbols: List[str] = ["@", "#", "<", ">"],
    strip_user_handles: bool = True,
    user_placeholder: str = "<user>",
    strip_urls: bool = True,
    url_placeholder: str = "<url>",
    show_progress: bool = True,
):
    new_texts = list()
    for text in tqdm(texts, desc="Cleaning:", disable=not show_progress):

        if clean_ftfy:
            text = ftfy.fix_text(text)

        if strip_new_lines:
            text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

        if strip_accents:
            text = "".join(
                (
                    c
                    for c in unicodedata.normalize("NFD", text)
                    if unicodedata.category(c) != "Mn"
                )
            )

        new_text = []
        for t in text.split():
            if strip_user_handles:
                t = user_placeholder if t.startswith("@") and len(t) > 1 else t

            if strip_urls:
                t = url_placeholder if t.startswith("http") else t

            new_text.append(t)

        new_text = " ".join(new_text)

        if strip_punctuation:
            target = list(string.punctuation)
            if keep_symbols:
                for symbol in keep_symbols:
                    target.pop(target.index(symbol))
            target = "".join(target)

            new_text = new_text.translate(str.maketrans("", "", target))

        new_texts.append(new_text)

    return new_texts


@beartype
def retrieve_context(tweet_ids):
    raise NotImplementedError()
