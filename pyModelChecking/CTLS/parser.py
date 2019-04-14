from lark import Lark, Transformer


class AST_to_TemporalLogics(Transformer):
    ''' A class to transform AST into temporal logics.

    This class implements a Lark's transformer to turn AST reprensenting
    temporal logics formulas into the corresponding temporal formula
    '''

    def __init__(self, lang):
        super(AST_to_TemporalLogics, self).__init__()

        self.__lang__ = lang

    def a_prop(self, subformula):
        return subformula[0]

    def string(self, s):
        return self.__lang__.AtomicProposition(s[0])

    def e_string(self, s):
        return self.__lang__.AtomicProposition(s[0][1:-1])

    def forall_formula(self, subformulas):
        return self.__lang__.A(*subformulas)

    def exists_formula(self, subformulas):
        return self.__lang__.E(*subformulas)

    def or_formula(self, subformulas):
        return self.__lang__.Or(*subformulas)

    def and_formula(self, subformulas):
        return self.__lang__.And(*subformulas)

    def imply_formula(self, subformulas):
        return self.__lang__.Imply(*subformulas)

    def not_formula(self, subformulas):
        return self.__lang__.Not(*subformulas)

    def next_formula(self, subformulas):
        return self.__lang__.X(*subformulas)

    def globally_formula(self, subformulas):
        return self.__lang__.G(*subformulas)

    def eventually_formula(self, subformulas):
        return self.__lang__.F(*subformulas)

    def until_formula(self, subformulas):
        return self.__lang__.U(*subformulas)

    def release_formula(self, subformulas):
        return self.__lang__.R(*subformulas)

    def true(self, subformula):
        return self.__lang__.Bool(True)

    def false(self, subformula):
        return self.__lang__.Bool(False)

    def p_formula(self, subformula):
        return subformula[0]

    def s_formula(self, subformula):
        return subformula[0]

    def u_formula(self, subformula):
        return subformula[0]

    def formula(self, subformula):
        return subformula[0]


class Parser(object):
    ''' A class to parse a temporal logics formula.

    Every object of this class instanciates a Lark's parser to parse a
    string reprensenting CTLS formulas into the corresponding pyModelChecking's
    CTLS formulas.
    '''

    grammar = r"""
        a_prop: /[a-zA-Z_][a-zA-Z_0-9]*/ -> string
              | ESCAPED_STRING           -> e_string

        s_formula: "true"     -> true
                 | "false"    -> false
                 | a_prop
                 | "A" u_formula  -> forall_formula
                 | "E" u_formula  -> exists_formula
                 | "(" s_formula ")"

        u_formula: "X" u_formula  -> next_formula
                  | "F" u_formula  -> eventually_formula
                  | "G" u_formula  -> globally_formula
                  | "not" u_formula -> not_formula
                  | "(" p_formula ")"
                  | s_formula

        p_formula: u_formula
                 | u_formula ( "or" u_formula )+ -> or_formula
                 | u_formula ( "and" u_formula )+ -> and_formula
                 | u_formula "-->" u_formula -> imply_formula
                 | u_formula "U" u_formula -> until_formula
                 | u_formula "R" u_formula -> release_formula

        formula: p_formula

        %import common.ESCAPED_STRING
        %import common.WS
        %ignore WS
        """

    def __init__(self):
        import pyModelChecking.CTLS as CTLS

        self._parser = Lark(Parser.grammar, start='formula', parser='lalr',
                            transformer=AST_to_TemporalLogics(CTLS))

    def __call__(self, string):
        ''' Parses a string and returns the equivalent formula

        This method parses a string and returns the equivalent temporal
        formula.

        :param name: a string representing a formula.
        :type name: str
        :returns: a temporal formula.
        :rtype: a temporal formula type
        '''

        return self._parser.parse(string)
