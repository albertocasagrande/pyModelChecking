from lark import Lark

from ..CTLS.parser import Parser as CLTS_Parser
from ..CTLS.parser import AST_to_TemporalLogics


class Parser(CLTS_Parser):
    grammar = r"""
        a_prop: /[a-zA-Z_][a-zA-Z_0-9]*/ -> string
              | ESCAPED_STRING           -> e_string

        s_formula: "true"     -> true
                 | "false"    -> false
                 | a_prop
                 | "A" p_formula  -> forall_formula
                 | "E" p_formula  -> exists_formula
                 | "not" s_formula -> not_formula
                 | "(" u_formula ")"

        u_formula: s_formula
                  | s_formula ( "or" s_formula )+ -> or_formula
                  | s_formula ( "and" s_formula )+ -> and_formula
                  | s_formula "-->" s_formula -> imply_formula

        p_formula: "X" s_formula  -> next_formula
                 | "F" s_formula  -> eventually_formula
                 | "G" s_formula  -> globally_formula
                 | s_formula "U" s_formula -> until_formula
                 | s_formula "R" s_formula -> release_formula
                 | "(" p_formula ")"

        formula: p_formula | u_formula

        %import common.ESCAPED_STRING
        %import common.WS
        %ignore WS
        """

    def __init__(self):
        import pyModelChecking.CTL as CTL

        self._parser = Lark(Parser.grammar, start='formula', parser='lalr',
                            transformer=AST_to_TemporalLogics(CTL))
