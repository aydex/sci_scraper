#!/usr/bin/env python

############# Imports ###################
import requests
import re

from lang_gen import LangGen

############# Scientific Scraper ########

gen = LangGen()
com = LangGen.Content.COMMENT
dec = LangGen.Content.DECLARATION
fun = LangGen.Content.FUNCTION
lang = LangGen.Language.FORTRAN

site = "http://physics.nist.gov/cuu/Constants/Table/allascii.txt"

page = requests.get(site)
text = str(page.text)
lines = text[text.find('\n', text.find('----------')) + 1 : ].split('\n')
#del lines[-1]
print len(lines)

dict = {}

for line in lines:
    if len(line.strip()) > 0:
        elements = re.split('  +', line)
        name = re.sub("(\.|\{(.*?)\}|\{|\}|\)|\(|,)", '', elements[0])
        elements[1] = re.sub("(\.\.\.)", '', elements[1])
        name = name.lower().strip()
        name = re.sub("(-|_| |/|\\|)", '_', name)
        elements[1] = elements[1].replace(' ', '')
        dict[name] = elements[1:]
        gen.add_line(dec, ["string", name, dict[name][0]])
        print elements[1]

print len(dict.keys())
print(gen.output(lang))
