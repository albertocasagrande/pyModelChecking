from ..parser import Parser as BaseParser
from ..parser import AST_to_Logics


class AST_to_PropositionalLogics(AST_to_Logics):
    ''' A class to transform AST into a propositional formula.

    This class implements a Lark's transformer to turn AST reprensenting
    propositional logics formulas into the corresponding propositional formula.
    '''

    def __init__(self, lang):
        super(AST_to_PropositionalLogics, self).__init__(lang)

    def a_prop(self, subformula):
        return subformula[0]

    def string(self, s):
        return self.__lang__.AtomicProposition(str(s[0]))

    def e_string(self, s):
        return self.__lang__.AtomicProposition(str(s[0])[1:-1])

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

    def b_formula(self, subformula):
        return subformula[0]

    def s_formula(self, subformula):
        return subformula[0]

    def u_formula(self, subformula):
        return subformula[0]

    def formula(self, subformula):
        return subformula[0]


class Parser(BaseParser):
    ''' A class to parse a propositional formula.

    Every object of this class instanciates a Lark's parser to parse a
    string reprensenting propositional formulas into the corresponding
    pyModelChecking's formulas.
    '''

    grammar = r"""
        s_formula: "{}"     -> true
                 | "{}"    -> false
                 | a_prop
                 | "(" s_formula ")"

        u_formula: {} u_formula  -> not_formula
                 | "(" b_formula ")"
                 | s_formula

        b_formula: u_formula
                 | u_formula ( {} u_formula )+ -> or_formula
                 | u_formula ( {} u_formula )+ -> and_formula
                 | u_formula {} u_formula -> imply_formula

        a_prop: /[a-zA-Z_][a-zA-Z_0-9]*/ -> string
              | ESCAPED_STRING           -> e_string

        formula: b_formula

        %import common.ESCAPED_STRING
        %import common.WS
        %ignore WS
        """

    def __init__(self, language=None):
        if language is None:
            import pyModelChecking.PL as PL

            language = PL

        AST_to_PL = AST_to_PropositionalLogics

        super(Parser, self).__init__(grammar=Parser.grammar,
                                     language=language,
                                     AST_Transformer=AST_to_PL)


def init_submodule():
    from .language import symbols, alphabet

    def format_symbols_for(operator):
        return '({})'.format('|'.join(['\"{}\"'.format(s)
                                       for s in alphabet[operator].symbols]))

    Parser.grammar = Parser.grammar.format(alphabet['Bool'].symbols[True],
                                           alphabet['Bool'].symbols[False],
                                           format_symbols_for('Not'),
                                           format_symbols_for('Or'),
                                           format_symbols_for('And'),
                                           format_symbols_for('Imply'))


init_submodule()
