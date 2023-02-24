"""
This function scrapes a website and returns a dict. Add specific tag or attrs
to params dict.
TODO: make sure strainer can accept tags AND attrs.
"""

from utils import get_html, build_soup

# Change these as needed
url = "https://docsouth.unc.edu/neh/religiouscontent.html"
target_attr={"class":"text_inside"}
target_tag = ""

# belongs in MAIN
params = {"tag":target_tag, "attribute":target_attr}
html_doc = get_html(url=url)

target_soup = build_soup(html_doc=html_doc,params=params)

#next, traverse through new soup
# for each indent2, read through
created_dict = {"theme":[], "alt_theme":[], "author":[], "title":[], "year":[], "page":[]}

theme_attr = {"class":"heading2"}
author_attr = {"class":"indent2"} # tag 
title_attr = {"class":"italic"} # tag is span
year_string = """ (between parens)""" # " (year), "
# page has a hyperlink. grab page numbers and hyperlinks ("pages", "links")
pages = () # link attr href=" some_link" pages p

#structure of parse
# for every class = heading2
    # for every class=indent2
    # if class= indenthead exists: add an alternate theme
    # else: add None to alternate theme (or ""?)
        #theme attr = theme (each time), add to dict["author"]
        # get author, add to dict["author"]
            # remove trailing space. Then remove trailing comma
        # get title, add to dict["title"]
        # get yr, add to dict["yr"]
        # get page and link, add to dict["page"]

# maybe make this script into a function...I need the resulting dict for analysis
