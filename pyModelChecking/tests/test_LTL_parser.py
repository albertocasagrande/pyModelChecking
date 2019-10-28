from pyModelChecking.LTL import *
from pyModelChecking.parser import UnexpectedToken, UnexpectedCharacters

import unittest
import lark


class TestLTLParser(unittest.TestCase):
    def setUp(self):
        self.same_formulas = [(Bool(True), "true"),
                              (Bool(False), "false"),
                              (Not(True), "not true"),
                              (A(F(G('q'))), "A F G q"),
                              (A(Imply(F(G('q')), X('p'))),
                               "A (F G q --> X p)"),
                              (A(G(Imply(And(Not('Close'), 'Start'),
                                         Or(G(Not('Heat')),
                                            F(Not('Error')))))),
                               "A G ((not Close and Start) --> " +
                               "((G not Heat) or (F not Error)))")]

        self.wrong_formulas = [("p and", UnexpectedToken),
                               ("A U and G", UnexpectedToken),
                               ("A a --> +", UnexpectedToken),
                               ("true\nfalse", UnexpectedToken),
                               ("A (F G q --> E G p)", UnexpectedToken),
                               ("A G ((not Close and Start) --> " +
                                "A ((G not Heat) or (F not Error)))",
                                UnexpectedToken)]

    def test_parser(self):
        parser = Parser()
        for psi, phi_str in self.same_formulas:
            phi = parser(phi_str)

            self.assertEqual(phi, psi)

        for phi_str, ErrorType in self.wrong_formulas:
            with self.assertRaises(ErrorType):
                phi = parser(phi_str)


if __name__ == '__main__':
    unittest.main()
