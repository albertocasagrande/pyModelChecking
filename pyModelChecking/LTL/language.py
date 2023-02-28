"""
.. module:: LTL.language
   :synopsis: Represents the LTL language.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""

import sys

from ..language import LNot
from ..language import get_alphabet, get_symbols

import pyModelChecking.CTLS

CTLS = sys.modules['pyModelChecking.CTLS']


class Formula(CTLS.Formula):
    r'''
    A class representing LTL formulas.

    '''

    __desc__ = 'LTL formula'


class PathFormula(Formula, CTLS.PathFormula):
    r'''
    A class representing LTL path formulas.

    '''

    __desc__ = 'LTL path formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, PathFormula)


class X(PathFormula, CTLS.X):
    r'''
    A class representing LTL X-formulas.

    '''

    pass


class F(PathFormula, CTLS.F):
    r'''
    A class representing LTL F-formulas.

    '''

    pass


class G(PathFormula, CTLS.G):
    r'''
    A class representing LTL G-formulas.

    '''

    pass


class U(PathFormula, CTLS.U):
    r'''
    A class representing LTL U-formulas.

    '''

    pass


class R(PathFormula, CTLS.R):
    r'''
    A class representing LTL R-formulas.

    '''

    pass


class AtomicProposition(CTLS.AtomicProposition, PathFormula):
    r'''
    A class representing LTL atomic propositions.

    '''

    pass


class Bool(CTLS.Bool, PathFormula):
    r'''
    A class representing LTL Boolean atomic propositions.

    '''

    pass


class Not(PathFormula, CTLS.Not):
    r'''
    A class representing LTL negations.

    '''

    pass


class Or(PathFormula, CTLS.Or):
    r'''
    A class representing LTL disjunctions.

    '''

    pass


class And(PathFormula, CTLS.And):
    r'''
    A class representing LTL conjunctions.

    '''

    pass


class Imply(PathFormula, CTLS.Imply):
    r'''
    A class representing LTL implications.

    '''

    pass


class StateFormula(Formula, CTLS.StateFormula):
    r'''
    A class representing LTL state formulas.

    '''

    __desc__ = 'LTL state formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, PathFormula)


class A(StateFormula, CTLS.A):
    r'''
    A class representing LTL A-formulas.

    '''
    pass


alphabet = get_alphabet(__name__)
symbols = get_symbols(alphabet)
