#!/usr/bin/env python

from pyModelChecking import Kripke
from pyModelChecking.CTL import *
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

class TestCTLModelChecking(unittest.TestCase):
    def setUp(self):
        self.problems=[(EG(And(Or(Not('p'),'q'),EF(And('q',Not('p'))))),set([0,1,3]))]
        self.K=Kripke(S=[0,1,2,3],
                      R=[(0,1),(1,2),(2,2),(1,3),(3,3)],
                      L={0:set(['p','q']),
                         1:set(['q']),
                         2:set(['p']),
                         3:set(['q'])})

    def test_modelchecking(self):
        for formula,solution in self.problems:
            S=modelcheck(self.K,formula)

            self.assertEquals(S,solution)

if __name__ == '__main__':
    unittest.main()
