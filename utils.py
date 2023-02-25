from bs4 import BeautifulSoup, SoupStrainer, NavigableString, Tag
import requests

def isNavigableString(element):
    """
    Returns true if element is type NavigableString
    """
    return isinstance(element, NavigableString)

def isTag(element):
    """
    Returns true if element is type NavigableString
    """
    return isinstance(element, Tag)

def strain_tags(tag=None,attrs=None):
    """
    Define what tags or attribute to parse from a BeautifulSoup object.
    
    Inputs:
    "tag": html tag
    {attrs}: {"attribute":"value"}

    Output: SoupStrainer object
        
    """
    if tag:
        strainer = SoupStrainer(tag)
    else:
        strainer = SoupStrainer(attrs=attrs)
    return strainer

def get_html(url):
    """
    Get a html document from a url.

    Input: 
        Url

    Output: 
        <html_doc>
    """
    html_doc = requests.get(url=url).text
    return html_doc

def build_soup(html_doc, params=None):
    """
    Shrink the scope of an html doc for more targeted parsing.
    Inputs:
        <html>
        params
    Output: 
        BeautifulSoup object
    """
    tag_parse = params.get("tag")
    attr_parse = params.get("attribute")

    if tag_parse:
        strainer = strain_tags(tag=tag_parse)
    elif attr_parse:
        strainer = strain_tags(attrs=attr_parse)
    else: 
        strainer = None
    
    soup = BeautifulSoup(html_doc, "html.parser", parse_only=strainer)

    return soup

