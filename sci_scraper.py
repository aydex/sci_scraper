#!/usr/bin/env python

############# Imports ###################
import requests
from lxml import html

from lang_gen import LangGen

############# Scientific Scraper ########

site = "http://en.wikipedia.org/wiki/Physical_constant";

gen = LangGen();

page = requests.get(site);
root = html.fromstring(page.content);

section = find_section(root, "Table_of_universal_constants")[0];
table = section.getparent().getnext();


def find_section(node, name):
    return node.xpath('//h2/span[@id="' + name + '"]');


def scrape_table(node):
    if node.tag != 'table':
        raise ValueError('Not a table node');
    first_row = table.getchildren()[0];

    column_names = pull_table_column_names(first_row);

    for row in table.getchildren()[1:]:
        for el in row:
            print el.text


def pull_table_column_names(first_row):
    column_names = [];
    for i in first_row:
        name = i.text.strip();
        while name == "" and len(i) > 0:
            name = i.getchildren()[0].text.strip();
        if name != "":
            column_names.append(name);
    return column_names;


class LangGen:
    """
    Class for generating simple code in certain 
    languages. 
    """

    def __init__(self):
        pass

    _content = [];
    _header = [];

    class Language:
        """
        Enum of the different languages. 
        """

        def __init__(self):
            pass

        PYTHON = 1;
        FORTRAN = 2;
        JAVA = 3;
        C = 4;

    class Content:
        """
        Enum representing different content types:
            ENUM = (id, number_of_arguments)
        """

        def __init__(self):
            pass

        COMMENT = (1, 1);
        # Args:
        #   - String: text
        DECLARATION = (2, 3);
        # Args:
        #   - String: datatype
        #   - String: name of variable
        #   - String: value of variable
        FUNCTION = (3, 2);
        # Args:
        #   - String: function name
        #   - List: function args

    class Generator:
        """
        Class for generating language specific text
        lines from generic structure. 
        """

        def __init__(self, language):
            self.language = language;

        def generate(self, line):
            content = line[0]
            args = line[1];
            if self.language == LangGen.Language.FORTRAN:
                if content == LangGen.Content.COMMENT:
                    out = "! " + args[0];
                elif content == LangGen.Content.DECLARATION:
                    out = args[0] + " :: " + args[1] + " = " + args[2];
                elif content == LangGen.Content.FUNCTION:
                    out = args[0] + "(";
                    out.join(arg + ", " for arg in args[1]);
                    out = out[:-2];
                    out += ")"

            return out

    def add_line(self, content, args):
        element = (content, args);
        self._content.append(element);

    def output(self, language):
        gen = LangGen.Generator(language);
        out = [gen.generate(line) for line in self._content];
        return out;
