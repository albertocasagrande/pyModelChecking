from lark import Lark

from ..CTLS.parser import Parser as CLTS_Parser
from ..CTLS.parser import AST_to_TemporalLogics


class Parser(CLTS_Parser):
    grammar = r"""
        formula: "A" u_formula      -> forall_formula

        a_prop: /[a-zA-Z_][a-zA-Z_0-9]*/ -> string
              | ESCAPED_STRING           -> e_string

        p_formula: "(" (or_formula
                        |and_formula
                        |imply_formula
                        |until_formula
                        |release_formula
                        |u_formula) ")"

        u_formula: "true"            -> true
                | "false"            -> false
                | a_prop
                | p_formula
                | "not" u_formula    -> not_formula
                | "X" u_formula      -> next_formula
                | "F" u_formula      -> eventually_formula
                | "G" u_formula      -> globally_formula

        or_formula: u_formula ( "or" u_formula )+
        and_formula: u_formula ( "and" u_formula )+
        imply_formula: u_formula "-->" u_formula
        until_formula: u_formula "U" u_formula
        release_formula: u_formula "R" u_formula

        %import common.ESCAPED_STRING
        %import common.WS
        %ignore WS
        """

    def __init__(self):
        import pyModelChecking.LTL as LTL

        self._parser = Lark(Parser.grammar, start='formula', parser='lalr',
                            transformer=AST_to_TemporalLogics(LTL))
