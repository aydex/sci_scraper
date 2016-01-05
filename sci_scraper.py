#!/usr/bin/env python

############# Imports ###################
import requests

from lang_gen import LangGen

############# Scientific Scraper ########

gen = LangGen()

site = "http://physics.nist.gov/cuu/Constants/Table/allascii.txt"

page = requests.get(site)
text = str(page.text)
lines = text[text.find('\n', text.find("----------")) + 1 : ].split('\n')
print len(lines)



