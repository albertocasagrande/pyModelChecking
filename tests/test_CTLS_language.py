#!/usr/bin/env python

from pyModelChecking.CTLS import *
import unittest

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

class TestFormulas(unittest.TestCase):
    def setUp(self):
        self.formulas=[True,'p',AtomicProposition('q')]

    def test_atomic_proposition(self):
        s='p'
        a=AtomicProposition(s)
        self.assertEquals(s,a)

        self.assertEquals(s,'%s' % (a))

        with self.assertRaises(TypeError):
            AtomicProposition(1)

    def test_boolean(self):
        b=False
        a=Bool(b)
        self.assertEquals(b,a)

        self.assertEquals(a,'%s' % (b))

        with self.assertRaises(TypeError):
            Bool('a')

    def generic_test_unaryop(self,op,op_str,equivalent_restricted_op=None):
        i=0
        for phi in self.formulas:
            s='%s(%s)' % (op_str, phi)
            self.assertEquals(s,'%s' % (op(phi)))
            if (equivalent_restricted_op!=None and isinstance(phi,Formula)):
                self.assertEquals(op(phi).get_equivalent_restricted_formula(),
                                  equivalent_restricted_op(phi))

    def test_not(self):
        for phi in self.formulas:
            self.assertEquals('not %s' % (phi),'%s' % (Not(phi)))
            if (isinstance(phi,Formula)):
                self.assertEquals(Not(phi).get_equivalent_restricted_formula(),
                                 (phi.get_equivalent_restricted_formula()).negate_and_simplify())

    def test_A(self):
        self.generic_test_unaryop(A,'A',(lambda phi: Not(E((phi.get_equivalent_restricted_formula()).negate_and_simplify()))))

    def test_E(self):
        self.generic_test_unaryop(E,'E',(lambda phi: E(phi.get_equivalent_restricted_formula())))

    def test_G(self):
        self.generic_test_unaryop(G,'G',(lambda phi: Not(F(phi.negate_and_simplify())).get_equivalent_restricted_formula()))

    def test_F(self):
        self.generic_test_unaryop(F,'F',(lambda phi: U(True,phi.get_equivalent_restricted_formula())))

    def test_X(self):
        self.generic_test_unaryop(X,'X',(lambda phi: X(phi.get_equivalent_restricted_formula())))

    def generic_test_binaryop(self,op,middle_op_str,equivalent_restricted_op=None):
        i=0
        for phi in self.formulas:
            for psi in self.formulas:
                s='(%s %s %s)' % (phi,middle_op_str,psi)
                self.assertEquals(s,'%s' % (op(phi,psi)))
                if (equivalent_restricted_op!=None and isinstance(psi,Formula) and isinstance(phi,Formula) ):
                    self.assertEquals(op(phi,psi).get_equivalent_restricted_formula(),
                                        equivalent_restricted_op(phi,psi))

    def test_U(self):
        self.generic_test_binaryop(U,'U',(lambda phi,psi: U(phi.get_equivalent_restricted_formula(),
                                                            psi.get_equivalent_restricted_formula())))

    def test_R(self):
        self.generic_test_binaryop(R,'R',(lambda phi,psi: Not(U((phi.get_equivalent_restricted_formula()).negate_and_simplify(),
                                                                (psi.get_equivalent_restricted_formula()).negate_and_simplify()))))

    def test_or(self):
        self.generic_test_binaryop(Or,'or',(lambda phi,psi: Or(phi.get_equivalent_restricted_formula(),
                                                               psi.get_equivalent_restricted_formula())))

    def test_and(self):
        self.generic_test_binaryop(And,'and',(lambda phi,psi: Not(Or((phi.get_equivalent_restricted_formula()).negate_and_simplify(),
                                                                     (psi.get_equivalent_restricted_formula()).negate_and_simplify()))))

    def test_imply(self):
        self.generic_test_binaryop(Imply,'-->',(lambda phi,psi: Or((phi.get_equivalent_restricted_formula()).negate_and_simplify(),
                                                                   psi.get_equivalent_restricted_formula())))

if __name__ == '__main__':
    unittest.main()
