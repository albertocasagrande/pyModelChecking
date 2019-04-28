from pyModelChecking import Kripke
from pyModelChecking.CTLS import *

import unittest


class TestCTLSModelChecking(unittest.TestCase):
    def setUp(self):
        self.problems = [(Kripke(R=[(0, 0), (0, 1), (1, 2), (2, 2)],
                                 L={0: set([]),
                                    1: set(['p']),
                                    2: set(['q'])}),
                          [(Bool(True), set([0, 1, 2]), None),
                           (Bool(False), set([]), None),
                           (Not(True), set([]), None),
                           (A(F(G('q'))), set([1, 2]), None),
                           (A(Imply(F(G('q')), E(G('p')))), set([]), None)]),
                         (Kripke(R=[(0, 1), (0, 2), (1, 4), (4, 1), (4, 2),
                                    (2, 0), (3, 2), (3, 0), (3, 3), (6, 3),
                                    (2, 5), (5, 6)],
                                 L={0: set(),
                                    1: set(['Start', 'Error']),
                                    2: set(['Close']),
                                    3: set(['Close', 'Heat']),
                                    4: set(['Start', 'Close', 'Error']),
                                    5: set(['Start', 'Close']),
                                    6: set(['Start', 'Close', 'Heat'])}),
                          [(A(G(Imply(And(Not('Close'), 'Start'),
                                      A(Or(G(Not('Heat')), F(Not('Error'))))))
                              ), set([0, 1, 2, 3, 4, 5, 6]), None),
                           (A(G(Imply(And(Not('Close'), 'Start'),
                                      A(Or(G(Not('Heat')), F(Not('Error'))))))
                              ), set([]), set([6]))])]

    def test_modelchecking(self):
        for kripke, instances in self.problems:
            for formula, solution, Fconstraints in instances:
                S = modelcheck(kripke, formula, F=Fconstraints)

                self.assertEqual(set(S), solution)


if __name__ == '__main__':
    unittest.main()
