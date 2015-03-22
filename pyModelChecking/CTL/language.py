#!/usr/bin/env python

import sys

if 'pyModelChecking.CTLS' not in sys.modules:
    import pyModelChecking.CTLS

CTLS=sys.modules['pyModelChecking.CTLS']

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

    __desc__='CTL formula'

class PathFormula(Formula):
    '''
    A class representing CTL path formulas.

    '''

    __desc__='CTL path formula'

    def is_a_state_formula(self):
        return False

    def __init__(self,*phi):
        self.wrap_subformulas(phi,StateFormula)

class X(PathFormula,CTLS.X):
    '''
    A class representing CTL X-formulas.

    '''

    def __str__(self):
        return 'X %s' % (self._subformula[0])

class F(PathFormula,CTLS.F):
    '''
    A class representing CTL F-formulas.

    '''

    def __str__(self):
        return 'F %s' % (self._subformula[0])

class G(PathFormula,CTLS.G):
    '''
    A class representing CTL G-formulas.

    '''

    def __str__(self):
        return 'G %s' % (self._subformula[0])

class U(PathFormula,CTLS.U):
    '''
    A class representing CTL U-formulas.

    '''

    pass

class R(PathFormula,CTLS.R):
    '''
    A class representing CTL R-formulas.

    '''

    pass

class StateFormula(Formula):
    '''
    A class representing CTL state formulas.

    '''

    __desc__='CTL state formula'

    def is_a_state_formula(self):
        return True

    def __init__(self,*phi):
        self.wrap_subformulas(phi,StateFormula)

class AtomicProposition(CTLS.AtomicProposition,StateFormula):
    '''
    A class representing CTL atomic propositions.

    '''

    pass

class Bool(CTLS.Bool,StateFormula):
    '''
    A class representing CTL Boolean atomic propositions.

    '''

    pass

class Not(StateFormula,CTLS.Not):
    '''
    A class representing CTL negations.

    '''

    pass

class Or(StateFormula,CTLS.Or):
    '''
    A class representing CTL disjunctions.

    '''

    pass

class And(StateFormula,CTLS.And):
    '''
    A class representing CTL conjunctions.

    '''

    pass

class Imply(StateFormula,CTLS.Imply):
    '''
    A class representing CTL implications.

    '''

    pass

class A(StateFormula,CTLS.A):
    '''
    A class representing CTL A-formulas.

    '''

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

        raise TypeError('%s is not a CTL formula' % (self))

    def __str__(self):
        return 'A%s' % (self._subformula[0])

class E(StateFormula,CTLS.E):
    '''
    A class representing CTL E-formulas.

    '''

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

        raise TypeError('%s is not a CTL formula' % (self))

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
