"""
This module contains utility functions for constructing a dictionary from 
the contents of a website. 
"""

from utils import get_html, get_soup, isNavigableString, isTag
import re

def custom_filter(tag):
    """
    Filter to check if a tag meets function criteria.

    Input:
        <html_tag>
    Output:
        Boolean
    """
    is_div = tag.name == 'div'
    has_class_attr = tag.get('class') if tag.get('class') else None
    has_class_heading2 = has_class_attr and tag.get('class')[0] == "heading2"
    has_class_indent2 = has_class_attr and tag.get('class')[0] == "indent2"
    
    return is_div and has_class_attr and has_class_heading2 or has_class_indent2

def scrape_data(url, filter):
    """
    Given a url, filter a html document for specifed tags.

    Input:
        url
    Output:
        [html tags]; list of tags fitting the custom filter
    """
    html_doc = get_html(url=url)
    soup = get_soup(html_doc=html_doc)
    tag_list = soup.find_all(filter)
    return tag_list

def build_dict(tag_list):
    """
    Build a dictionary from 

    Input:
        [tags]; list of tags to parse
    Output:
        {custom_dict}; dictionary
    TODO: 
    1. Make this function extensible by feeding custom_dict params
    2. Separate theme logic in a fcn, separate indent2 logic into fcn
    3. Make append function(accept list of keys)
    4. Pass in specific constructor (is_a, get) params when creating dict

    """
    custom_dict = {"theme":[], "alt_theme":[], "author":[], "title":[], "year":[], "page":[]}
    current_theme = None
    current_alt_theme = None

    for i in range(len(tag_list)):
        tag = tag_list[i]
        if tag.get('class')[0] == "heading2":
            current_theme = tag.contents[1]
            current_alt_theme = None if len(tag.contents) <= 2 else tag.contents[2]
        elif tag.get('class')[0] == "indent2":
            author = get_author(tag.contents[0])
            title = get_title(tag.find(is_title))
            year = get_year(is_year(tag))
            page_range = get_page_range(is_page_range(tag))
            page_link = get_page_link(is_page_link(tag))
            page = (page_range, page_link)
            
            custom_dict["theme"].append(current_theme)
            custom_dict["alt_theme"].append(current_alt_theme)
            custom_dict["author"].append(author)
            custom_dict["title"].append(title)
            custom_dict["year"].append(year)
            custom_dict["page"].append(page)

    return custom_dict

def get_author(element):
    isNavStr = isNavigableString(element)
    if isNavStr:
        return element.string.strip(" ,")

def is_title(element):
    title = element.get("class")[0] == "italic"
    return title
    
def get_title(element):
    is_Tag = isTag(element)
    if is_Tag:
        return element.get_text()

def is_year(element):
    regex_str = re.compile("\(([^)]+)\)")
    return element.find(text=regex_str)

def get_year(element):
    isNavStr = isNavigableString(element)
    if isNavStr:
        return element.string.strip(" ,()")

def is_page_range(element):
    is_page = element.find("a")
    return is_page

def get_page_range(element):
    """
    TODO: Add logic for converting str to range
    """
    is_Tag = isTag(element)
    if is_Tag:
        return element.get_text().strip(" p")

def is_page_link(element):
    is_page_link = element.find("a")
    if is_page_link:
        return is_page_link.attrs["href"] 

def get_page_link(element):
    """
    TODO: Add logic for comverting str to range
    """
    is_string = True if type(element) == str else False
    if is_string:
        return element

# if __name__ == "main":