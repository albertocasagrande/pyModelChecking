"""
.. module:: LTL.language
   :synopsis: Represents the LTL language.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""

import pyModelChecking.CTLS

from ..language import LNot
from ..language import get_alphabet

import sys

CTLS = sys.modules['pyModelChecking.CTLS']

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015-2018"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"


class Formula(CTLS.Formula):
    '''
    A class representing LTL formulas.

    '''

    __desc__ = 'LTL formula'


class PathFormula(Formula, CTLS.PathFormula):
    '''
    A class representing LTL path formulas.

    '''

    __desc__ = 'LTL path formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, PathFormula)


class X(PathFormula, CTLS.X):
    '''
    A class representing LTL X-formulas.

    '''

    pass


class F(PathFormula, CTLS.F):
    '''
    A class representing LTL F-formulas.

    '''

    pass


class G(PathFormula, CTLS.G):
    '''
    A class representing LTL G-formulas.

    '''

    pass


class U(PathFormula, CTLS.U):
    '''
    A class representing LTL U-formulas.

    '''

    pass


class R(PathFormula, CTLS.R):
    '''
    A class representing LTL R-formulas.

    '''

    pass


class AtomicProposition(CTLS.AtomicProposition, PathFormula):
    '''
    A class representing LTL atomic propositions.

    '''

    pass


class Bool(CTLS.Bool, PathFormula):
    '''
    A class representing LTL Boolean atomic propositions.

    '''

    pass


class Not(PathFormula, CTLS.Not):
    '''
    A class representing LTL negations.

    '''

    pass


class Or(PathFormula, CTLS.Or):
    '''
    A class representing LTL disjunctions.

    '''

    pass


class And(PathFormula, CTLS.And):
    '''
    A class representing LTL conjunctions.

    '''

    pass


class Imply(PathFormula, CTLS.Imply):
    '''
    A class representing LTL implications.

    '''

    pass


class StateFormula(Formula, CTLS.StateFormula):
    '''
    A class representing LTL state formulas.

    '''

    __desc__ = 'LTL state formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, PathFormula)


class A(StateFormula, CTLS.A):
    '''
    A class representing LTL A-formulas.

    '''
    pass


alphabet = get_alphabet(__name__)
