#!/usr/bin/env python

############# Imports ###################
import requests
import re

from lang_gen import LangGen

############# Scientific Scraper ########

gen = LangGen()

site = "http://physics.nist.gov/cuu/Constants/Table/allascii.txt"

page = requests.get(site)
text = str(page.text)
lines = text[text.find('\n', text.find('----------')) + 1 : ].split('\n')
print len(lines)

dict = {}

for line in lines:
    elements = re.split('  +', line)
    name = elements[0] #ad
    dict[name] = elements[1:]


