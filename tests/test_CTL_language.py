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

    def generic_test_unaryop(self,op,op_str,equivalent_EGUX_operator=None):
        i=0
        for phi in self.formulas:
            s='%s %s' % (op_str, phi)
            self.assertEquals(s,'%s' % (op(phi)))
            if (equivalent_EGUX_operator!=None):
                self.assertEquals(equivalent_EGUX_operator(phi),
                                    op.get_equivalent_EGUX_operator()(phi))

    def test_not(self):
        self.generic_test_unaryop(Not,'not',(lambda phi: Not(phi)))

    def test_AF(self):
        self.generic_test_unaryop(AF,'AF',(lambda phi: Not(EG(Not(phi)))))

    def test_EF(self):
        self.generic_test_unaryop(EF,'EF',(lambda phi: EU(True,phi)))

    def test_AG(self):
        self.generic_test_unaryop(AG,'AG',(lambda phi: Not(EU(True,Not(phi)))))

    def test_EG(self):
        self.generic_test_unaryop(EG,'EG',(lambda phi: EG(phi)))

    def generic_test_binaryop(self,op,middle_op_str,equivalent_EGUX_operator,prefix_op_str=''):
        i=0
        for phi in self.formulas:
            for psi in self.formulas:
                s='%s(%s %s %s)' % (prefix_op_str, phi,middle_op_str,psi)
                self.assertEquals(s,'%s' % (op(phi,psi)))
                self.assertEquals(equivalent_EGUX_operator(phi,psi),
                                  op.get_equivalent_EGUX_operator()(phi,psi))

    def test_or(self):
        self.generic_test_binaryop(Or,'or',(lambda phi,psi: Or(phi,psi)))


if __name__ == '__main__':
    unittest.main()
