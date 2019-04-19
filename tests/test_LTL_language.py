from pyModelChecking.LTL import *
import unittest


def formula_into_str(phi):
    if isinstance(phi, bool):
        return str(phi).lower()
    return str(phi)


class TestFormulas(unittest.TestCase):
    def setUp(self):
        self.formulas = [True, 'p', AtomicProposition('q'),
                         G('p'), F('p'), X('p'), U('q', 'p'), R('q', 'p')]

    def test_simplified_syntax(self):
        formulas = [(And(True, 'p'), Bool(True) & 'p'),
                    (Not(And(True, 'p')), ~(Bool(True) & 'p')),
                    (And(Not(True), 'p'), ~Bool(True) & 'p'),
                    (Or(True, Not('p')), Bool(True) | Not('p')),
                    (Or(True, Not('p')), True | Not('p')),
                    (A(Or(True, Not(X('p')))), A(True | ~X('p')))]

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
            s = '{}({})'.format(op_str, formula_into_str(phi))
            self.assertEqual(s, '{}'.format(op(phi)))
            if (equivalent_restricted_op is not None and
                    isinstance(phi, Formula)):
                self.assertEqual(op(phi).get_equivalent_restricted_formula(),
                                 equivalent_restricted_op(phi))

    def test_not(self):
        for phi in self.formulas:
            self.assertEqual('not {}'.format(formula_into_str(phi)),
                             '{}'.format(Not(phi)))
            if (isinstance(phi, Formula)):
                not_formula = Not(phi).get_equivalent_restricted_formula()
                lnot_formula = LNot(phi.get_equivalent_restricted_formula())
                self.assertEqual(not_formula, lnot_formula)

    def test_G(self):
        formula = (lambda phi:
                   Not(F(LNot(phi)).get_equivalent_restricted_formula()))
        self.generic_test_unaryop(G, 'G', formula)

    def test_F(self):
        formula = (lambda phi:
                   U(True, phi.get_equivalent_restricted_formula()))
        self.generic_test_unaryop(F, 'F', formula)

    def test_X(self):
        formula = (lambda phi: X(phi.get_equivalent_restricted_formula()))
        self.generic_test_unaryop(X, 'X', formula)

    def generic_test_binaryop(self, op, middle_op_str,
                              equivalent_restricted_op=None):
        i = 0
        for phi in self.formulas:
            phi_str = formula_into_str(phi)
            for psi in self.formulas:
                s = '({} {} {})'.format(phi_str,
                                        middle_op_str,
                                        formula_into_str(psi))
                self.assertEqual(s, '{}'.format(op(phi, psi)))
                if (equivalent_restricted_op is not None and
                        isinstance(psi, Formula) and
                        isinstance(phi, Formula)):

                    formula = op(phi, psi).get_equivalent_restricted_formula()

                    self.assertEqual(formula,
                                     equivalent_restricted_op(phi, psi))

    def test_U(self):
        formula = (lambda phi, psi: U(phi.get_equivalent_restricted_formula(),
                                      psi.get_equivalent_restricted_formula()))
        self.generic_test_binaryop(U, 'U', formula)

    def test_R(self):
        formula = (lambda phi, psi:
                   Not(U(LNot(phi.get_equivalent_restricted_formula()),
                         LNot(psi.get_equivalent_restricted_formula()))))
        self.generic_test_binaryop(R, 'R', formula)

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
