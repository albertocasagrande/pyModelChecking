from ..parser import Parser as BaseParser
from ..CTLS.parser import AST_to_TemporalLogics


class Parser(BaseParser):
    grammar = r"""
        formula: s_formula | p_formula

        s_formula: "{}" u_formula      -> forall_formula

        p_formula: u_formula ( "{}" u_formula )+   -> or_formula
                 | u_formula ( "{}" u_formula )+   -> and_formula
                 | u_formula "{}" u_formula        -> imply_formula
                 | u_formula "{}" u_formula        -> until_formula
                 | u_formula "{}" u_formula        -> release_formula
                 | u_formula

        u_formula: "{}"                -> true
                 | "{}"                -> false
                 | a_prop
                 | "(" p_formula ")"
                 | "{}" u_formula      -> not_formula
                 | "{}" u_formula      -> next_formula
                 | "{}" u_formula      -> eventually_formula
                 | "{}" u_formula      -> globally_formula

        a_prop: /[a-zA-Z_][a-zA-Z_0-9]*/ -> string
              | ESCAPED_STRING           -> e_string

        %import common.ESCAPED_STRING
        %import common.WS
        %ignore WS
        """

    def __init__(self, language=None):
        if language is None:
            import pyModelChecking.LTL as LTL

            language = LTL

        super(Parser, self).__init__(grammar=Parser.grammar,
                                     language=language,
                                     AST_Transformer=AST_to_TemporalLogics)


def init_submodule():
    from .language import symbols, alphabet

    Parser.grammar = Parser.grammar.format(alphabet['A'].symbol,
                                           alphabet['Or'].symbol,
                                           alphabet['And'].symbol,
                                           alphabet['Imply'].symbol,
                                           alphabet['U'].symbol,
                                           alphabet['R'].symbol,
                                           alphabet['Bool'].symbols[True],
                                           alphabet['Bool'].symbols[False],
                                           alphabet['Not'].symbol,
                                           alphabet['X'].symbol,
                                           alphabet['F'].symbol,
                                           alphabet['G'].symbol)


init_submodule()
