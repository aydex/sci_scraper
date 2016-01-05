#!/usr/bin/env python

############# Imports ###################

############# Math HTML parser ##########


def html_math_parse(tree):
    output = [];
    process(tree, output);
    return output;


def process(node, output):
    print(node.tag);
    string = extract_text(node);
    if string != None:
        output.append(string);
    for child in node.getchildren():
        process(child, output);
    string = extract_tail(node);
    if string != None:
        output.append(string);


def extract_text(node):
    if (node == None or node.text == None or node.text.strip() == ""):
        return None;
    if node.tag == 'sup':
        return '^{' + node.text + '}';
    else:
        return node.text.strip();


def extract_tail(node):
    if (node == None or node.tail == None or node.tail.strip() == ""):
        return None;
    return node.tail.strip();
