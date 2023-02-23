"""
Scrape a website for stylized text, read it into a DF
"""
from bs4 import BeautifulSoup
import requests

def scrape_website(url, params):
    """
    Scrape a website for text.

    Inputs: 
        Url
        {params}: dict of patterns to look for 

    Output: 
        {dict}: "column_name":[values]
    """
    html_doc = requests.get(url=url).text
    soup = BeautifulSoup(html_doc, "html.parser")
