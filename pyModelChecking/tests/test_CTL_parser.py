from pyModelChecking.CTL import *
from pyModelChecking.parser import UnexpectedToken, UnexpectedCharacters

import unittest
import lark


class TestCTLParser(unittest.TestCase):
    def setUp(self):
        self.same_formulas = [(Bool(True), "true"),
                              (Bool(False), "false"),
                              (Not(True), "not true"),
                              (AF(EG('q')), "A F E G q"),
                              (Imply(AF(EG('q')), AG('p')),
                               "A F E G q --> A G p"),
                              (AG(Imply(And(Not('Close'), 'Start'),
                                        Or(AG(Not('Heat')),
                                           EF(Not('Error'))))),
                               "A G ((not Close and Start) --> " +
                               "((A G not Heat) or (E F not Error)))")]

        self.wrong_formulas = [("p and", UnexpectedToken),
                               ("A U and G", UnexpectedToken),
                               ("A a --> +", UnexpectedToken),
                               ("true\nfalse", UnexpectedToken),
                               ("A (F G q --> E G p)", UnexpectedToken),
                               ("A G ((not Close and Start) --> A " +
                               "((G not Heat) or (F not Error)))",
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
