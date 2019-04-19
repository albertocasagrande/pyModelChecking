from ..PL.parser import AST_to_PropositionalLogics
from ..parser import Parser as BaseParser


class AST_to_TemporalLogics(AST_to_PropositionalLogics):
    ''' A class to transform AST into a CTLS temporal formula.

    This class implements a Lark's transformer to turn AST reprensenting
    temporal logics formulas into the corresponding temporal formulas.
    '''

    def __init__(self, lang):
        super(AST_to_TemporalLogics, self).__init__(lang)

    def forall_formula(self, subformulas):
        return self.__lang__.A(*subformulas)

    def exists_formula(self, subformulas):
        return self.__lang__.E(*subformulas)

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

    def p_formula(self, subformula):
        return subformula[0]


class Parser(BaseParser):
    ''' A class to parse a temporal logics formula.

    Every object of this class instanciates a Lark's parser to parse a string
    reprensenting CTLS formulas into the corresponding pyModelChecking's CTLS
    formulas.
    '''

    grammar = r"""
        s_formula: "{}"     -> true
                 | "{}"    -> false
                 | a_prop
                 | {} u_formula  -> forall_formula
                 | {} u_formula  -> exists_formula
                 | "(" s_formula ")"

        u_formula: {} u_formula  -> next_formula
                 | {} u_formula  -> eventually_formula
                 | {} u_formula  -> globally_formula
                 | {} u_formula  -> not_formula
                 | "(" p_formula ")"
                 | s_formula

        p_formula: u_formula
                 | u_formula ( {} u_formula )+ -> or_formula
                 | u_formula ( {} u_formula )+ -> and_formula
                 | u_formula {} u_formula -> imply_formula
                 | u_formula {} u_formula -> until_formula
                 | u_formula {} u_formula -> release_formula

        a_prop: /[a-zA-Z_][a-zA-Z_0-9]*/ -> string
              | ESCAPED_STRING           -> e_string

        formula: p_formula

        %import common.ESCAPED_STRING
        %import common.WS
        %ignore WS
        """

    def __init__(self, language=None):
        if language is None:
            import pyModelChecking.CTLS as CTLS

            language = CTLS

        super(Parser, self).__init__(grammar=Parser.grammar,
                                     language=language,
                                     AST_Transformer=AST_to_TemporalLogics)


def init_submodule():
    from .language import alphabet

    def format_symbols_for(operator):
        return '({})'.format('|'.join(['\"{}\"'.format(s)
                                       for s in alphabet[operator].symbols]))

    Parser.grammar = Parser.grammar.format(alphabet['Bool'].symbols[True],
                                           alphabet['Bool'].symbols[False],
                                           format_symbols_for('A'),
                                           format_symbols_for('E'),
                                           format_symbols_for('X'),
                                           format_symbols_for('F'),
                                           format_symbols_for('G'),
                                           format_symbols_for('Not'),
                                           format_symbols_for('Or'),
                                           format_symbols_for('And'),
                                           format_symbols_for('Imply'),
                                           format_symbols_for('U'),
                                           format_symbols_for('R'))


init_submodule()
