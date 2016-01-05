#!/usr/bin/python

from lang_gen import LangGen

a = LangGen()
com = LangGen.Content.COMMENT
dec = LangGen.Content.DECLARATION
fun = LangGen.Content.FUNCTION
lang = LangGen.Language.FORTRAN

a.add_line(com, ["test"])
a.add_line(dec, ["integer", "var", "100"])
a.add_line(fun, ["open", ["file_name", "flag"]])
print(a.output(lang))


