"""Top-level package for Twitterknife."""

__author__ = """Giuseppe Attanasio"""
__email__ = "giuseppeattanasio6@gmail.com"
__version__ = "0.1.0"

from .processing import clean_texts, get_base_info, parse_jsonl
from .text_analysis import association_rules_mining, find_topics, frequent_word_sets
