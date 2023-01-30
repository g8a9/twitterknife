import os

from beartype import beartype
from beartype.typing import List
from twarc.client2 import Twarc2


class Hopper:
    @beartype
    def __init__(self, bearer_token: str):
        self.twarc = Twarc2(bearer_token=bearer_token)

    @beartype
    def get_hop_id(self, tweet: dict):
        """Get the tweet id of the next hop in the tree."""
        if "referenced_tweets" in tweet and isinstance(
            tweet["referenced_tweets"], list
        ):
            if tweet["referenced_tweets"][0]["type"] == "replied_to":
                hop_id = tweet["referenced_tweets"][0]["id"]
                return hop_id
        return None

    @beartype
    def extract_hop(self, tweet_ids: List[int]):
        lookups = self.twarc.tweet_lookup(
            tweet_ids, expansions=["referenced_tweets.id"]
        )

        new_data = list()
        for lup in lookups:
            for t in lup["data"]:
                new_data.append(
                    {
                        "id": t["id"],
                        "text": t["text"],  # text of the next hop
                    }
                )

        return new_data
