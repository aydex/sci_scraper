#!/usr/bin/env python

############# Imports ###################
import os

import requests
import re

from lang_gen import LangGen

############# Scientific Scraper ########

#### Parameters ####
site = "http://physics.nist.gov/cuu/Constants/Table/allascii.txt"
pad_length = len('__00__u')
length_limit = 63
####################


header = """! ###################### MODULE ##################"
! Physical constants module
! 
! Contains a list of physical constants, 
! automatically  scraped from:
! http://physics.nist.gov/cuu/Constants/Table/
! allascii.txt
! 
! Each constant is given 4 entries of the form:
!   real(wp), param    :: NAME    = value
!   real(wp), param    :: NAME__U = uncertainty
!   char(len=*), param :: NAME__S = name string
!   char(len=*), param :: NAME__N = unit string
! 
! ################################################
module phys_constants

implicit none

public

"""

footer = "\nend module\n"

gen = LangGen()
emp = LangGen.ContentType.EMPTY
com = LangGen.ContentType.COMMENT
dec = LangGen.ContentType.DECLARATION
fun = LangGen.ContentType.FUNCTION
lang = LangGen.Language.FORTRAN

page = requests.get(site)
text = str(page.text)
lines = text[text.find('\n', text.find('----------')) + 1:].split('\n')


def parse_var_name(string):
    # Remove paranthesis
    string = re.sub('\(.*\)', '', string)

    # Remove decimal numbers
    string = re.sub('[0-9]+\.[0-9]+', '', string)

    # Substitue separator chars with underscore
    string = re.sub('[\-|_| |\\\\]+', '_', string)

    # Substitute forward slash with _per_
    string = re.sub('/+', '_per_', string)

    # Remove any invalid characters that remain
    string = re.sub('[^a-zA-Z0-9_]', '', string)

    # Remove leading and trailing underscores
    string = re.sub('^_+', '', string)
    string = re.sub('_+$', '', string)

    # Pad leading numbers with "n_"
    string = re.sub('(^[0-9]+)', 'n_\\1', string)

    # Remove any multiple of underscores
    string = re.sub('_+', '_', string)

    # Upper case for Fortran parameter
    string = string.upper()

    return string

def parse_number(value):
    # Remove invalid characters
    value = re.sub('[^0-9e\-\.]', '', value)
    value = re.sub('e{2,}', '', value)
    value = re.sub('\-{2,}', '', value)
    value = re.sub('\.{2,}', '', value)

    # Check if valid number
    try:
        float(value)

        # 'd' for Fortran double precision float 
        value = value.replace('e', 'd')

        return value

    except ValueError:
        print('Parse error on value: ' + value)
        return None

name_list = []
dupl_dict = {}

for line in lines:
    if (len(line.strip()) > 0):
        elements = re.split('  +', line)

        # Extract strings
        name_string = elements[0].strip()
        value_string = elements[1].strip()
        unc_string = elements[2].strip()
        unit_string = elements[3].strip()

        # Process name string
        name = parse_var_name(name_string)
        if (len(name) + pad_length > length_limit):
            name = name[:length_limit - pad_length]
        if (name in dupl_dict):
            dupl_dict[name] += 1
        else:
            dupl_dict[name] = 0

        # Process value string
        value = parse_number(value_string)

        # Process uncertainty string
        if (unc_string == '(exact)'):
            unc = '0'
        else:
            unc = parse_number(unc_string)

        # Process unit string
        if (unit_string == ''):
            unit = '1'
        else:
            unit = unit_string

        # Check valid
        if (value == None or unc == None):
            continue

        name_list.append((name, value, unc, name_string, unit))

def add_element(name, value, unc, string, unit):
    gen.add_line(dec, ['real(wp), parameter', name, value])
    gen.add_line(dec, ['real(wp), parameter', name + '__U', unc])
    gen.add_line(dec, ['character(len=*), parameter', name + '__S', '\"' + string + '\"'])
    gen.add_line(dec, ['character(len=*), parameter', name + '__N', '\"' + unit + '\"'])
    gen.add_line(emp, [])

iter_dict = {}
for element in name_list:
    name = element[0]
    if (dupl_dict[name] != 0):
        if (name in iter_dict):
            iter_dict[name] += 1
        else:
            iter_dict[name] = 1
        name = name + '__' + str(iter_dict[name])
    add_element(name, element[1], element[2], element[3], element[4])


if not os.path.exists("output"):
    os.makedirs("output")

f = open('output/test.f', 'w+')
f.write(header)
for line in gen.output(lang):
    f.write(line + '\n')
f.write(footer)

f.close()

