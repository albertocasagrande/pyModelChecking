#!/usr/bin/env python

from pyModelChecking.CTL import *
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
        self.formulas=[True,'p',Atom('q')]

    def test_atomic_proposition(self):
        s='p'
        a=Atom(s)
        self.assertEquals(s,a)

        self.assertEquals(s,'%s' % (a))

        with self.assertRaises(TypeError):
            Atom(1)

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
            s='%s %s' % (op_str, phi)
            self.assertEquals(s,'%s' % (op(phi)))
            if (equivalent_restricted_op!=None and isinstance(phi,Formula)):
                self.assertEquals(op(phi).get_equivalent_restricted_formula(),
                                    equivalent_restricted_op(phi))

    def test_not(self):
        self.generic_test_unaryop(Not,'not',(lambda phi: (phi.get_equivalent_restricted_formula()).negate_and_simplify()))

    def test_AF(self):
        self.generic_test_unaryop(AF,'AF',(lambda phi: Not(EG((phi.get_equivalent_restricted_formula()).negate_and_simplify()))))

    def test_EF(self):
        self.generic_test_unaryop(EF,'EF',(lambda phi: EU(True,phi.get_equivalent_restricted_formula())))

    def test_AG(self):
        self.generic_test_unaryop(AG,'AG',(lambda phi: Not(EU(True,(phi.get_equivalent_restricted_formula()).negate_and_simplify()))))

    def test_EG(self):
        self.generic_test_unaryop(EG,'EG',(lambda phi: EG(phi.get_equivalent_restricted_formula())))

    def generic_test_binaryop(self,op,middle_op_str,equivalent_restricted_op=None,prefix_op_str=''):
        i=0
        for phi in self.formulas:
            for psi in self.formulas:
                s='%s(%s %s %s)' % (prefix_op_str, phi,middle_op_str,psi)
                self.assertEquals(s,'%s' % (op(phi,psi)))
                if (equivalent_restricted_op!=None  and isinstance(psi,Formula) and isinstance(phi,Formula)):
                    self.assertEquals(op(phi,psi).get_equivalent_restricted_formula(),
                                        equivalent_restricted_op(phi,psi))

    def test_AU(self):
        self.generic_test_binaryop(AU,'U',
                        (lambda phi,psi: Not(Or(EU((psi.get_equivalent_restricted_formula()).negate_and_simplify(),
                                              Not(Or(phi.get_equivalent_restricted_formula(),
                                                     psi.get_equivalent_restricted_formula()))
                                            ),EG((psi.get_equivalent_restricted_formula()).negate_and_simplify())))),prefix_op_str='A')

    def test_EU(self):
        self.generic_test_binaryop(EU,'U',
                        (lambda phi,psi: EU(phi.get_equivalent_restricted_formula(),
                                            psi.get_equivalent_restricted_formula())),prefix_op_str='E')

    def test_AR(self):
        self.generic_test_binaryop(AR,'R',
                        (lambda phi,psi: Not(EU((phi.get_equivalent_restricted_formula()).negate_and_simplify(),
                                                (psi.get_equivalent_restricted_formula()).negate_and_simplify()))),prefix_op_str='A')

    def test_ER(self):
        self.generic_test_binaryop(ER,'R',
                        (lambda phi,psi: Or(EU(psi.get_equivalent_restricted_formula(),
                                              Not(Or((phi.get_equivalent_restricted_formula()).negate_and_simplify(),
                                                     (psi.get_equivalent_restricted_formula()).negate_and_simplify()))
                                            ),EG(psi.get_equivalent_restricted_formula()))),prefix_op_str='E')

    def test_or(self):
        self.generic_test_binaryop(Or,'or',(lambda phi,psi: Or(phi.get_equivalent_restricted_formula(),
                                                               psi.get_equivalent_restricted_formula())))

    def test_and(self):
        self.generic_test_binaryop(And,'and',(lambda phi,psi: Not(Or((phi.get_equivalent_restricted_formula()).negate_and_simplify(),
                                                                     (psi.get_equivalent_restricted_formula()).negate_and_simplify()))))

    def test_imply(self):
        self.generic_test_binaryop(Imply,'-->',(lambda phi,psi: Or((phi.get_equivalent_restricted_formula()).negate_and_simplify(),
                                                                   psi.get_equivalent_restricted_formula())))

#    def test_U(self):
#        self.generic_test_binaryop(U,'U',(lambda phi,psi: U(phi.get_equivalent_restricted_formula(),
#                                                            psi.get_equivalent_restricted_formula())))

#    def test_R(self):
#        self.generic_test_binaryop(R,'R',(lambda phi,psi: Not(U(Not(phi.get_equivalent_restricted_formula()),
#                                                                Not(psi.get_equivalent_restricted_formula())))))


if __name__ == '__main__':
    unittest.main()
