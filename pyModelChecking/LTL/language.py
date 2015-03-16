#!/usr/bin/env python

import sys
import inspect
import pyModelChecking.CTLS as CTLS

'''
This module represents the LTL language.

The **Linear Time Logic** or **LTL** is a subset of the temporal language CTL*.
LTL formulas have the form "A rho" where "rho" is a *path formula* and a LTL
path formula is either:
 - an atomic proposition
 - one of the formulas "not phi", "phi or psi", "phi and psi", "X phi", "F phi",
   "G phi", "phi U psi", or "phi R psi" where phi and psi are path formulas.
Since the temporal operator "F", "G", and "R" can be expressed by using "U",
the LTL restricted language that allows only path formulas having the form
"p", "not phi", "phi or psi", "X phi", or "phi U psi" is equivalent to the
full LTL (e.g., see [Clarke2000]_).


[Clarke2000] Edmund M. Clarke, Jr., Orna Grumberg, and Doron A. Peled. 2000. Model Checking. MIT Press, Cambridge, MA, USA.
'''

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"


class Formula(CTLS.Formula):
    '''
    A class representing LTL formulas.

    '''
    pass

class PathFormula(CTLS.Formula):
    def __init__(self,*phi):
        self.wrap_subformulas(phi,PathFormula)

class X(PathFormula,CTLS.X):
    pass

class F(PathFormula,CTLS.F):
    pass

class G(PathFormula,CTLS.G):
    pass

class U(PathFormula,CTLS.U):
    pass

class R(PathFormula,CTLS.R):
    pass

class Atom(CTLS.Atom,PathFormula):
    pass

class Bool(CTLS.Bool,PathFormula):
    pass

class Not(PathFormula,CTLS.Not):
    pass

class Or(PathFormula,CTLS.Or):
    pass

class And(PathFormula,CTLS.And):
    pass

class Imply(PathFormula,CTLS.Imply):
    pass

class StateFormula(Formula):
    def __init__(self,*phi):
        self.wrap_subformulas(phi,PathFormula)

class A(StateFormula,CTLS.A):
    pass

alphabet=CTLS.get_alphabet(__name__)
