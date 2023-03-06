"""
This module contains utility functions for natural language processing

"""
from nltk.corpus import stopwords
from textblob import TextBlob

def tokenize_words(str):
    """
    tokenize words with textblob
    """
    tokenized_words = []
    blob = TextBlob(str)
    useless_words = stopwords.words("english") + "" + " " + "\n"
    for word in str:
        if str not in useless_words:
            tokenized_words.append(str)

    return tokenized_words