"""Main module."""
import json
import os
from typing import List

import ftfy
from beartype import beartype
from tqdm import tqdm
from twarc.client2 import Twarc2


@beartype
def parse_jsonl(path: str) -> dict:
    with open(path) as fp:
        tweets = [json.loads(f.strip()) for f in fp.readlines()]
    return tweets


@beartype
def clean_text(
    texts: List[str],
    clean_ftfy: bool = True,
    strip_user_handles: bool = True,
    user_placeholder: str = "<user>",
    strip_urls: bool = False,
    url_placeholder: str = "<url>",
    show_progress: bool = True,
):
    new_texts = list()
    for text in tqdm(texts, desc="Cleaning:", disable=not show_progress):

        if clean_ftfy:
            text - ftfy.fix_text(text)

        texts = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

        new_text = []
        for t in text.split():
            if strip_user_handles:
                t = user_placeholder if t.startswith("@") and len(t) > 1 else t

            if strip_urls:
                t = url_placeholder if t.startswith("http") else t

            new_text.append(t)

        new_texts.append(" ".join(new_text))

    return new_texts


@beartype
def retrieve_context(tweet_ids):
    pass


class Hopper:
    def __init__(self):
        self.twarc = Twarc2(bearer_token=os.environ["BEARER_TOKEN"])

    def extract_hop(self, tweet_ids: pd.Series):
        non_na = tweet_ids.loc[~tweet_ids.isna()]

        lookups = self.twarc.tweet_lookup(
            non_na.values, expansions=["referenced_tweets.id"]
        )

        new_data = list()
        for lup in lookups:
            for t in lup["data"]:
                new_data.append(
                    {
                        "id": t["id"],
                        "text": ftfy.fix_text(
                            t["text"].replace("\n", " ")
                        ),  # text of the next hop
                        "next_hop_id": get_hop_id(t),  # tweet id of the next next hop
                    }
                )

        hop_df = pd.DataFrame(new_data).set_index("id").drop_duplicates()
        return hop_df
