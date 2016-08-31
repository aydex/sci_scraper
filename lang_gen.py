#!/usr/bin/env python

############# Imports ###################


############# Lamguage Generator ########
class LangGen:
    """
    Class for generating simple code in certain 
    languages. 
    """

    def __init__(self):
        pass

    _content = []

    class Language:
        """
        Enum of the different languages.
        """

        def __init__(self):
            pass

        PYTHON = 1
        FORTRAN = 2
        JAVA = 3
        C = 4

    class ContentType:
        """
        Enum representing different content types:
            CONTENT_TYPE = (id, number_of_arguments)
        """

        def __init__(self):
            pass

        EMPTY = (1,0)
        # Args: (none)
        COMMENT = (2, 1)
        # Args:
        #   - String: text
        DECLARATION = (3, 3)
        # Args:
        #   - String: datatype
        #   - String: name of variable
        #   - String: value of variable
        FUNCTION = (4, 2)
        # Args:
        #   - String: function name
        #   - List: function args

    class Generator:
        """
        Class for generating language specific text
        lines from generic structure.
        """

        def __init__(self, language):
            self.language = language

        def generate(self, line):
            content_type = line[0]
            args = line[1]
            if (self.language == LangGen.Language.FORTRAN):
                if (content_type == LangGen.ContentType.EMPTY):
                    out = ''
                if (content_type == LangGen.ContentType.COMMENT):
                    out = "! " + args[0]
                elif (content_type == LangGen.ContentType.DECLARATION):
                    # Some datatypes might have special declarations (e.g. string requires "")
                    out = args[0] + " :: " + args[1] + " = " + args[2]
                elif (content_type == LangGen.ContentType.FUNCTION):
                    out = args[0] + "(" + ", ".join(args[1]) + ")"
            return out

    def add_line(self, content_type, args):
        element = (content_type, args)
        self._content.append(element)

    def output(self, language):
        gen = LangGen.Generator(language)
        out = [gen.generate(line) for line in self._content]
        return out

