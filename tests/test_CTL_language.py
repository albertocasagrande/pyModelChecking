from pyModelChecking.CTL import *
import unittest

from .test_CTLS_language import formula_into_str


class TestFormulas(unittest.TestCase):
    def setUp(self):
        self.formulas = [True, 'p', AtomicProposition('q'), AF(EG('q')),
                         AG('p'), EF('p'), AX('p'), AU('q', 'p'), ER('q', 'p'),
                         Imply(AF(EG('q')), AG('p')),
                         AG(Imply(And(Not('Close'), 'Start'),
                                  Or(AG(Not('Heat')), EF(Not('Error')))))]

    def test_simplified_syntax(self):
        formulas = [(And(True, 'p'), Bool(True) & 'p'),
                    (Not(And(True, 'p')), ~(Bool(True) & 'p')),
                    (And(Not(True), 'p'), ~Bool(True) & 'p'),
                    (Or(True, Not('p')), Bool(True) | Not('p')),
                    (Or(True, Not('p')), True | Not('p')),
                    (Or(AG(True), Not(EX('p'))), AG(True) | ~EX('p'))]

        for old_syntax, new_syntax in formulas:
            self.assertEqual(old_syntax, new_syntax)

    def test_atomic_proposition(self):
        s = 'p'
        a = AtomicProposition(s)
        self.assertEqual(s, a)

        self.assertEqual(s, '{}'.format(a))

        with self.assertRaises(TypeError):
            AtomicProposition(1)

    def test_boolean(self):
        for b in [False, True]:
            a = Bool(b)
            self.assertEqual(b, a)
            self.assertEqual(a, b)

        with self.assertRaises(TypeError):
            Bool('a')

    def generic_test_unaryop(self, op, op_str, equivalent_restricted_op=None):
        i = 0
        for phi in self.formulas:
            s = '{} {}'.format(op_str, formula_into_str(phi))
            self.assertEqual(s, '{}'.format(op(phi)))
            if (equivalent_restricted_op is not None and
                    isinstance(phi, Formula)):
                self.assertEqual(op(phi).get_equivalent_restricted_formula(),
                                 equivalent_restricted_op(phi))

    def test_not(self):
        formula = (lambda phi: LNot(phi.get_equivalent_restricted_formula()))
        self.generic_test_unaryop(Not, 'not', formula)

    def test_AF(self):
        formula = (lambda phi:
                   Not(EG(LNot(phi.get_equivalent_restricted_formula()))))
        self.generic_test_unaryop(AF, 'AF', formula)

    def test_EF(self):
        formula = (lambda phi:
                   EU(True, phi.get_equivalent_restricted_formula()))
        self.generic_test_unaryop(EF, 'EF', formula)

    def test_AG(self):
        formula = (lambda phi:
                   Not(EU(True,
                          LNot(phi.get_equivalent_restricted_formula()))))
        self.generic_test_unaryop(AG, 'AG', formula)

    def test_EG(self):
        formula = (lambda phi: EG(phi.get_equivalent_restricted_formula()))
        self.generic_test_unaryop(EG, 'EG', formula)

    def generic_test_binaryop(self, op, middle_op_str,
                              equivalent_restricted_op=None,
                              prefix_op_str=''):
        i = 0
        for phi in self.formulas:
            for psi in self.formulas:
                s = '{}({} {} {})'.format(prefix_op_str, formula_into_str(phi),
                                          middle_op_str, formula_into_str(psi))
                self.assertEqual(s, '{}'.format(op(phi, psi)))
                if (equivalent_restricted_op is not None and
                        isinstance(psi, Formula) and isinstance(phi, Formula)):

                    formula = op(phi, psi).get_equivalent_restricted_formula()
                    self.assertEqual(formula,
                                     equivalent_restricted_op(phi, psi))

    def test_AU(self):
        formula = (lambda phi, psi:
                   Not(Or(EU(LNot(psi.get_equivalent_restricted_formula()),
                             Not(Or(phi.get_equivalent_restricted_formula(),
                                    psi.get_equivalent_restricted_formula()))),
                          EG(LNot(psi.get_equivalent_restricted_formula())))))
        self.generic_test_binaryop(AU, 'U', formula, prefix_op_str='A')

    def test_EU(self):
        formula = (lambda phi, psi:
                   EU(phi.get_equivalent_restricted_formula(),
                      psi.get_equivalent_restricted_formula()))

        self.generic_test_binaryop(EU, 'U', formula, prefix_op_str='E')

    def test_AR(self):
        formula = (lambda phi, psi:
                   Not(EU(LNot(phi.get_equivalent_restricted_formula()),
                          LNot(psi.get_equivalent_restricted_formula()))))
        self.generic_test_binaryop(AR, 'R', formula, prefix_op_str='A')

    def test_ER(self):
        subformula = (lambda phi, psi:
                      Not(Or(LNot(phi.get_equivalent_restricted_formula()),
                             LNot(psi.get_equivalent_restricted_formula()))))
        formula = (lambda phi, psi:
                   Or(EU(psi.get_equivalent_restricted_formula(),
                         subformula(phi, psi)),
                      EG(psi.get_equivalent_restricted_formula())))
        self.generic_test_binaryop(ER, 'R', formula, prefix_op_str='E')

    def test_or(self):
        formula = (lambda phi, psi:
                   Or(phi.get_equivalent_restricted_formula(),
                      psi.get_equivalent_restricted_formula()))
        self.generic_test_binaryop(Or, 'or', formula)

    def test_and(self):
        formula = (lambda phi, psi:
                   Not(Or(LNot(phi.get_equivalent_restricted_formula()),
                          LNot(psi.get_equivalent_restricted_formula()))))
        self.generic_test_binaryop(And, 'and', formula)

    def test_imply(self):
        formula = (lambda phi, psi:
                   Or(LNot(phi.get_equivalent_restricted_formula()),
                      psi.get_equivalent_restricted_formula()))

        self.generic_test_binaryop(Imply, '-->', formula)


if __name__ == '__main__':
    unittest.main()
