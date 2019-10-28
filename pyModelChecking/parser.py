from lark import Lark, Transformer, exceptions


class AST_to_Logics(Transformer, object):
    ''' A class to transform AST into a propositional formula.

    This class implements a Lark's transformer to turn AST reprensenting
    propositional logics formulas into the corresponding propositional formula.
    '''

    def __init__(self, lang):
        super(AST_to_Logics, self).__init__()

        self.__lang__ = lang

    def or_formula(self, subformulas):
        return self.__lang__.Or(*subformulas)

    def and_formula(self, subformulas):
        return self.__lang__.And(*subformulas)

    def imply_formula(self, subformulas):
        return self.__lang__.Imply(*subformulas)

    def not_formula(self, subformulas):
        return self.__lang__.Not(*subformulas)

    def true(self, subformula):
        return self.__lang__.Bool(True)

    def false(self, subformula):
        return self.__lang__.Bool(False)


class ParserError(Exception):
    ''' A class to represent parser errors. '''

    def __init__(self, string, pos):
        self.string = string
        self.pos = pos

    def __str__(self):
        return 'Parser Error: \n\n{}\n{}^\n'.format(self.string, ' '*self.pos)


class UnexpectedToken(ParserError):
    def __init__(self, string, pos):
        super(UnexpectedToken, self).__init__(string, pos)


class UnexpectedCharacters(ParserError):
    def __init__(self, string, pos):
        super(UnexpectedCharacters, self).__init__(string, pos)


class Parser(object):
    ''' A class to parse a propositional formula.

    Every object of this class instanciates a Lark's parser to parse a
    string reprensenting propositional formulas into the corresponding
    pyModelChecking's formulas.
    '''

    def __init__(self, grammar, language, AST_Transformer):
        self._parser = Lark(grammar, start='formula', parser='lalr',
                            transformer=AST_Transformer(language))

    def __call__(self, string):
        ''' Parses a string and returns the equivalent formula

        This method parses a string and returns the equivalent formula.

        :param name: a string representing a formula.
        :type name: str
        :returns: a formula.
        :rtype: a temporal formula type
        :raises: objects of either :py:exception:UnexpectedToken or
                 :py:exception:UnexpectedCharacters
        '''
        try:
            return self._parser.parse(string)
        except exceptions.UnexpectedToken as e:
            ex_class = UnexpectedToken
            pos = int(e.pos_in_stream)
        except exceptions.UnexpectedCharacters as e:
            ex_class = UnexpectedCharacters
            pos = int(e.pos_in_stream)

        raise ex_class(string, pos)
