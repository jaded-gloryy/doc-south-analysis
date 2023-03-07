"""
This module contains utility functions for natural language processing using the NLTK library.

"""
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize

def list_to_blob(word_list):
    """
    Function to convert a list of words into a str.
    Input:
        [word_list]
    Output:
        "text_blob"
    """    
    string_form = list_to_str(word_list)

    return TextBlob(string_form)

def list_to_str(word_list):
    """
    Function to convert a list of words into a str.
    Input:
        [word_list]
    Output:
        "str"
    """    
    string_form = " ".join(word_list)

    return string_form

def remove_stopwords(str, additional_stop_words=None):
    """
    Function to remove stopwords from a string.
    Input:
        "str"; text to remove stopwords from
        [additional_stop_words]; extra words or characters to remove outside of NLTK's stopwords
    Output:
        [word_list]; all words excluding stopwords
    """
    word_list = []
    useless_words = stopwords.words("english")
    if additional_stop_words:
        useless_words = useless_words + additional_stop_words

    str = str.lower()
    blob_list = TextBlob(str).words
    for word in blob_list:
        if word not in useless_words:
            word_list.append(word)

    return word_list


def tokenize_words(word_list):
    """
    Function to tokenize a string.
    Input:
        [word_list]
    Output:
        [tokenized_words]
    """
    string_form = list_to_str(word_list)

    return word_tokenize(string_form)


def get_word_counts(word_list):
    """
    Get word counts from a list of words.
    Input:
        [word_list]
    Output:
        {word_count dictionary}
    """
    blob_form = list_to_blob(word_list)

    return blob_form.word_counts

def lemmatize_words(word_list):
    """
    Function to get a list of root words.
    Input:
        [word_list]
    Output:
        [lemmatized_list]; list of root words
    """

    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_list = [wordnet_lemmatizer.lemmatize(word) for word in word_list]

    return lemmatized_list