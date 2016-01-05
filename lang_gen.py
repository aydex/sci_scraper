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
