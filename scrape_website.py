"""
This module contains utility functions for parsing data and constructing a dictionary from 
the contents of a website: http://docsouth.unc.edu/neh
"""

from utils import get_html, get_soup, isNavigableString, isTag, is_list
import re

def clean_up_text(str):
    """
    Remove html tags and
    """
    text = str
    tag_query_pattern = "(\<.*?\>)"
    weird_stuff = "(\&.*?\;)"
    replace_with = " "
    text = re.sub(tag_query_pattern,replace_with, text)
    text = re.sub(weird_stuff,replace_with, text)
    weird_stuff = ["\n"]
    for each in weird_stuff:
        text = text.replace(each," ")
    return text

def get_pages_from_url(urls, pages):
    """
    Get text from a webpage, given page numbers.
    Input:
        [urls]
        [pages]
    Output:
        [texts]
    """

    all_texts = []
    for i in range(len(list(urls))):
        a_url = urls[i]
        page_ref = pages[i]
        url_text = get_html(a_url)

        current_text = ""
        for a_pg in page_ref:
            specific_page = "Page " + a_pg
            start_position = url_text.find(specific_page)
            new_soup = url_text[start_position+len(specific_page):]
            end_position = new_soup.find("Page ")

            specified_text = new_soup[:end_position]
            current_text += specified_text
        all_texts.append(current_text)

    return all_texts


def get_page_num(tag):
    """
    Get page num from tag text
    Input:
        <tag>
    Output:
        "page_num"
    """
    has_text = tag.text.strip("Page ") if tag.text else False
    # if has_text and has_text.isnumeric():
    #     return int(has_text)
    # else: 
    return has_text

def is_range(str):
    """
    Input:
        "str"
    Output:
        Boolean
    """
    return True if str.find("-") != -1 else False

def get_range(str_range):
    """
    Input:
        "str" like "num-num"
    Output:
        ["num", "num", "num"]
    """
    range_list = []
    temp = str_range.split("-")

    for i in range(int(temp[0]),int(temp[1])+1):
        range_list.append(str(i))

    return range_list


def get_page_list(pages):
    """
    Input:
        "str"
    Output:
        ["str"]
    """
    if is_list(pages) and is_range(pages):
        page_range = []
        page_list = pages.split(",")
        for page in page_list:
            if is_range(page):
                page_range += get_range(page)
            else:
                page_range.append(page)
        # page_range.append(temp_list)
        return page_range
    elif is_range(pages):
        page_range = get_range(pages)
    elif is_list(pages):
        page_range = pages.split(",")
    else:
        page_range = [pages]
    return page_range


def combine_url(base_url, specific_url):
    """
    Combine a base url with an extension.
    Input:
        "base_url";
        "specific_url" or [specific_url];
    Output:
        "full_url"; if input is a str
        [full_urls]; if input is a list
    """
    urls = []
    if type(specific_url) == str:
        return base_url + specific_url
    
    else:
        for url in specific_url:
            
            full_url = base_url + url
            urls.append(full_url)
        return urls


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

def scrape_data(url, filter=None):
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
    custom_dict = {"theme":[], "alt_theme":[], "author":[], "title":[], "year":[], "page_numbers":[], "page_link":[]}
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
            
            custom_dict["theme"].append(current_theme)
            custom_dict["alt_theme"].append(current_alt_theme)
            custom_dict["author"].append(author)
            custom_dict["title"].append(title)
            custom_dict["year"].append(year)
            custom_dict["page_numbers"].append(page_range)
            custom_dict["page_link"].append(page_link)

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