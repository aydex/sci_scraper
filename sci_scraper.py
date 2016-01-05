#!/usr/bin/env python

############# Imports ###################
import requests

from lang_gen import LangGen

############# Scientific Scraper ########

gen = LangGen()

site = "http://physics.nist.gov/cuu/Constants/Table/allascii.txt"

page = requests.get(site)
text = page.text
print(text)


