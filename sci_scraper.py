#!/usr/bin/env python

############# Imports ###################
import requests
from lxml import html

from lang_gen import LangGen

############# Scientific Scraper ########

site = "http://en.wikipedia.org/wiki/Physical_constant"

gen = LangGen()

page = requests.get(site)
root = html.fromstring(page.content)


def find_section(node, name):
    return node.xpath('//h2/span[@id="' + name + '"]')


section = find_section(root, "Table_of_universal_constants")[0]
table = section.getparent().getnext()


def scrape_table(node):
    if node.tag != 'table':
        raise ValueError('Not a table node')
    first_row = table.getchildren()[0]

    column_names = pull_table_column_names(first_row)

    for row in table.getchildren()[1:]:
        for el in row:
            print el.text


def pull_table_column_names(first_row):
    column_names = []
    for i in first_row:
        name = i.text.strip()
        while name == "" and len(i) > 0:
            name = i.getchildren()[0].text.strip()
        if name != "":
            column_names.append(name)
    return column_names
