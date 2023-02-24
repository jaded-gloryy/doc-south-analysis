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
created_dict = {}

author_attr = {"class":"indent2"}
title_attr = {"span clas":"italic"}
year_string =  "(beween parens)"