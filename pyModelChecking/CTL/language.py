#!/usr/bin/env python

import sys
import inspect
import pyModelChecking.CTLS as CTLS

'''
This module represents the CTL language.

The **Computational Tree Language** or **CTL** is a subset of the temporal
language CTL*. In CTL, beside the standard logical operators "not", "and", and
"or", each occurence of the two path quantifiers "A" and "E" should be coupled
to one of the temporal operators "X", "G", "F", "U", or "R" and form one of the
10 possible CTL temporal operators. Despite this, "not", "or", and "E" coupled
to "X", "U", or "G" are sufficient to express any possible property definable
in CTL (e.g., see [Clarke2000]_).


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
    A class representing CTL formulas.

    '''
    pass

class PathFormula(Formula):
    def __init__(self,*phi):
        self.wrap_subformulas(phi,StateFormula)

class X(PathFormula,CTLS.X):
    def __str__(self):
        return 'X %s' % (self._subformula[0])

class F(PathFormula,CTLS.F):
    def __str__(self):
        return 'F %s' % (self._subformula[0])

class G(PathFormula,CTLS.G):
    def __str__(self):
        return 'G %s' % (self._subformula[0])

class U(PathFormula,CTLS.U):
    pass

class R(PathFormula,CTLS.R):
    pass

class StateFormula(Formula):
    def __init__(self,*phi):
        self.wrap_subformulas(phi,StateFormula)

class Atom(CTLS.Atom,StateFormula):
    pass

class Bool(CTLS.Bool,StateFormula):
    pass

class Not(StateFormula,CTLS.Not):
    def __str__(self):
        return 'not %s' % (self._subformula[0])

class Or(StateFormula,CTLS.Or):
    pass

class And(StateFormula,CTLS.And):
    pass

class Imply(StateFormula,CTLS.Imply):
    pass

class A(StateFormula,CTLS.A):
    def __init__(self,phi):
        self.wrap_subformulas([phi],PathFormula)

    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: A
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: StateFormula
        '''

        p_formula=self.subformula(0)
        sf0=p_formula.subformula(0).get_equivalent_restricted_formula()
        neg_sf0=sf0.negate_and_simplify()
        if (isinstance(p_formula,CTLS.X)):
            return Not(EX(neg_sf0))

        if (isinstance(p_formula,CTLS.F)):
            return Not(EG(neg_sf0))

        if (isinstance(p_formula,CTLS.G)):
            return Not(EU(True,neg_sf0))

        sf1=p_formula.subformula(1).get_equivalent_restricted_formula()
        neg_sf1=sf1.negate_and_simplify()
        if (isinstance(p_formula,CTLS.U)):
            return Not(Or(EU(neg_sf1,Not(Or(sf0,sf1))),EG(neg_sf1)))

        if (isinstance(p_formula,CTLS.R)):
            return Not(EU(neg_sf0,neg_sf1))

        raise RuntimeError('%s is not a CTL formula' %
                            (self))

    def __str__(self):
        return 'A%s' % (self._subformula[0])

class E(StateFormula,CTLS.E):
    def __init__(self,phi):
        self.wrap_subformulas([phi],PathFormula)

    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: E
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: StateFormula
        '''

        p_formula=self.subformula(0)
        sf0=p_formula.subformula(0).get_equivalent_restricted_formula()
        if (isinstance(p_formula,CTLS.X)):
            return EX(sf0)

        if (isinstance(p_formula,CTLS.F)):
            return EU(True,sf0)

        if (isinstance(p_formula,CTLS.G)):
            return EG(sf0)

        sf1=p_formula.subformula(1).get_equivalent_restricted_formula()
        if (isinstance(p_formula,CTLS.U)):
            return EU(sf0,sf1)

        if (isinstance(p_formula,CTLS.R)):
            neg_sf1=sf1.negate_and_simplify()
            neg_sf0=sf0.negate_and_simplify()

            return Or(EU(sf1,Not(Or(neg_sf0,neg_sf1))),EG(sf1))

        raise RuntimeError('%s is not a CTL formula' %
                            (self))

    def __str__(self):
        return 'E%s' % (self._subformula[0])

def AX(subformula):
    return A(X(subformula))

def EX(subformula):
    return E(X(subformula))

def AF(subformula):
    return A(F(subformula))

def EF(subformula):
    return E(F(subformula))

def AG(subformula):
    return A(G(subformula))

def EG(subformula):
    return E(G(subformula))

def AU(subformula0,subformula1):
    return A(U(subformula0,subformula1))

def EU(subformula0,subformula1):
    return E(U(subformula0,subformula1))

def AR(subformula0,subformula1):
    return A(R(subformula0,subformula1))

def ER(subformula0,subformula1):
    return E(R(subformula0,subformula1))

alphabet=CTLS.get_alphabet(__name__)
