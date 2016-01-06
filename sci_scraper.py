#!/usr/bin/env python

############# Imports ###################
import os

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

#dict = {}

for line in lines:
    if len(line.strip()) > 0:
        elements = re.split('  +', line)
        name = re.sub("(\.|\{(.*?)\}|\{|\}|\)|\(|,)", '', elements[0])
        elements[1] = re.sub("(\.\.\.)", '', elements[1])
        name = name.lower().strip()
        name = re.sub("(-|_| |/|\\|)", '_', name)
        elements[1] = elements[1].replace(' ', '')
        elements[1] = elements[1].replace('e', 'd')
        elements[2] = elements[2].replace('e', 'd')
        #dict[name] = elements[1:]
        #gen.add_line(dec, ["real", name, dict[name][0]])
        gen.add_line(dec, ["real(8)", name, elements[1]])


if not os.path.exists("output"):
    os.makedirs("output")

f = open('output/test.f', 'w+')
for line in gen.output(lang):
    f.write(line + '\n')

f.close()

