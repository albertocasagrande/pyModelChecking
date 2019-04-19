from ..parser import Parser as BaseParser
from ..CTLS.parser import AST_to_TemporalLogics


class Parser(BaseParser):
    grammar = r"""
        s_formula: "{}"     -> true
                 | "{}"    -> false
                 | a_prop
                 | {} p_formula       -> forall_formula
                 | {} p_formula       -> exists_formula
                 | {} s_formula       -> not_formula
                 | "(" u_formula ")"

        u_formula: s_formula
                  | s_formula ( {} s_formula )+      -> or_formula
                  | s_formula ( {} s_formula )+      -> and_formula
                  | s_formula {} s_formula           -> imply_formula

        p_formula: {} s_formula  -> next_formula
                 | {} s_formula  -> eventually_formula
                 | {} s_formula  -> globally_formula
                 | s_formula {} s_formula -> until_formula
                 | s_formula {} s_formula -> release_formula
                 | "(" p_formula ")"

        a_prop: /[a-zA-Z_][a-zA-Z_0-9]*/ -> string
              | ESCAPED_STRING           -> e_string

        formula: p_formula | u_formula

        %import common.ESCAPED_STRING
        %import common.WS
        %ignore WS
        """

    def __init__(self, language=None):
        if language is None:
            import pyModelChecking.CTL as CTL

            language = CTL

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
                                           format_symbols_for('Not'),
                                           format_symbols_for('Or'),
                                           format_symbols_for('And'),
                                           format_symbols_for('Imply'),
                                           format_symbols_for('X'),
                                           format_symbols_for('F'),
                                           format_symbols_for('G'),
                                           format_symbols_for('U'),
                                           format_symbols_for('R'))


init_submodule()
