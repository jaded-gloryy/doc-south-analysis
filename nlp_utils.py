"""
This module contains utility functions for natural language processing

"""
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from textblob import TextBlob



def tokenize_words(str):
    """
    tokenize words with textblob
    """
    tokenized_words = []
    blob = TextBlob(str).words
    useless_words = stopwords.words("english") + ["" , " ", "\n"]
    for word in blob:
        if word not in useless_words:
            tokenized_words.append(word)

    return tokenized_words

