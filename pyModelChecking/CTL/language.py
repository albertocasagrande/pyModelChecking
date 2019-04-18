"""
.. module:: CTL.language
   :synopsis: Represents the CTL language.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""

import sys

from ..language import LNot
from ..language import get_alphabet, get_symbols

import pyModelChecking.CTLS

CTLS = sys.modules['pyModelChecking.CTLS']


class Formula(CTLS.Formula):
    '''
    A class representing CTL formulas.

    '''

    __desc__ = 'CTL formula'


class StateFormula(Formula, CTLS.StateFormula):
    '''
    A class representing CTL* state formulas.

    '''

    __desc__ = 'CTL state formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, StateFormula)


class PathFormula(Formula, CTLS.PathFormula):
    '''
    A class representing CTL* path formulas.

    '''

    __desc__ = 'CTL path formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, StateFormula)


class X(CTLS.X, PathFormula):
    '''
    A class representing CTL X-formulas.

    '''

    def __str__(self):
        return 'X {}'.format(self._subformula[0])


class F(CTLS.F, PathFormula):
    '''
    A class representing CTL F-formulas.

    '''

    def __str__(self):
        return 'F {}'.format(self._subformula[0])


class G(CTLS.G, PathFormula):
    '''
    A class representing CTL G-formulas.

    '''

    def __str__(self):
        return 'G {}'.format(self._subformula[0])


class U(CTLS.U, PathFormula):
    '''
    A class representing CTL U-formulas.

    '''

    pass


class R(CTLS.R, PathFormula):
    '''
    A class representing CTL R-formulas.

    '''

    pass


class AtomicProposition(CTLS.AtomicProposition, StateFormula):
    '''
    A class representing CTL atomic propositions.

    '''

    pass


class Bool(CTLS.Bool, StateFormula):
    '''
    A class representing CTL Boolean atomic propositions.

    '''

    pass


class Not(CTLS.Not, StateFormula):
    '''
    A class representing CTL negations.

    '''

    pass


class Or(CTLS.Or, StateFormula):
    '''
    A class representing CTL disjunctions.

    '''

    pass


class And(CTLS.And, StateFormula):
    '''
    A class representing CTL conjunctions.

    '''

    pass


class Imply(CTLS.Imply, StateFormula):
    '''
    A class representing CTL implications.

    '''

    pass


class A(CTLS.A, StateFormula):
    '''
    A class representing CTL A-formulas.

    '''

    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`\land`,
        :math:`\\rightarrow`, :math:`A`, :math:`F`, and :math:`R` and is
        equivalent to this formula.

        :param self: this formula
        :type self: CTL.E
        :returns: a formula that avoids :math:`\land`, :math:`\\rightarrow`,
                  :math:`A`, :math:`F`, and :math:`R` and is equivalent to
                  this formula
        :rtype: CTL.StateFormula
        '''

        p_formula = self.subformula(0)
        sf0 = p_formula.subformula(0).get_equivalent_restricted_formula()
        neg_sf0 = LNot(sf0)
        if (isinstance(p_formula, CTLS.X)):
            return Not(EX(neg_sf0))

        if (isinstance(p_formula, CTLS.F)):
            return Not(EG(neg_sf0))

        if (isinstance(p_formula, CTLS.G)):
            return Not(EU(True, neg_sf0))

        sf1 = p_formula.subformula(1).get_equivalent_restricted_formula()
        neg_sf1 = LNot(sf1)
        if (isinstance(p_formula, CTLS.U)):
            return Not(Or(EU(neg_sf1, Not(Or(sf0, sf1))), EG(neg_sf1)))

        if (isinstance(p_formula, CTLS.R)):
            return Not(EU(neg_sf0, neg_sf1))

        raise TypeError('{} is not a CTL formula'.format(self))

    def get_equivalent_non_fair_formula(self, fairAP):
        p_formula = self.subformula(0)
        sf0 = p_formula.subformula(0).get_equivalent_non_fair_formula(fairAP)
        neg_sf0 = LNot(sf0)
        if (isinstance(p_formula, CTLS.X)):
            return Not(EX(And(neg_sf0, fairAP)))

        if (isinstance(p_formula, CTLS.F)):
            return Not(EG(And(neg_sf0, fairAP)))

        if (isinstance(p_formula, CTLS.G)):
            return Not(EU(True, And(neg_sf0, fairAP)))

        sf1 = p_formula.subformula(1).get_equivalent_non_fair_formula(fairAP)
        neg_sf1 = LNot(sf1)
        if (isinstance(p_formula, CTLS.U)):
            return Not(Or(EU(neg_sf1, And(Not(Or(sf0, sf1)), fairAP)),
                          EG(And(neg_sf1, fairAP))))

        if (isinstance(p_formula, CTLS.R)):
            return Not(EU(neg_sf0, And(neg_sf1, fairAP)))

        raise TypeError('{} is not a CTL formula'.format(self))

    def __str__(self):
        return 'A{}'.format(self._subformula[0])

    def __init__(self, phi):
        self.wrap_subformulas([phi], sys.modules[self.__module__].PathFormula)


class E(CTLS.E, StateFormula):
    '''
    A class representing CTL E-formulas.

    '''

    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`\land`,
        :math:`\\rightarrow`, :math:`A`, :math:`F`, and :math:`R` and is
        equivalent to this formula.

        :param self: this formula
        :type self: CTL.E
        :returns: a formula that avoids :math:`\land`, :math:`\\rightarrow`,
                  :math:`A`, :math:`F`, and :math:`R` and is equivalent to
                  this formula
        :rtype: CTL.StateFormula
        '''

        p_formula = self.subformula(0)
        sf0 = p_formula.subformula(0).get_equivalent_restricted_formula()
        if (isinstance(p_formula, CTLS.X)):
            return EX(sf0)

        if (isinstance(p_formula, CTLS.F)):
            return EU(True, sf0)

        if (isinstance(p_formula, CTLS.G)):
            return EG(sf0)

        sf1 = p_formula.subformula(1).get_equivalent_restricted_formula()
        if (isinstance(p_formula, CTLS.U)):
            return EU(sf0, sf1)

        if (isinstance(p_formula, CTLS.R)):
            neg_sf1 = LNot(sf1)
            neg_sf0 = LNot(sf0)

            return Or(EU(sf1, Not(Or(neg_sf0, neg_sf1))), EG(sf1))

        raise TypeError('{} is not a CTL formula'.format(self))

    def get_equivalent_non_fair_formula(self, fairAP):
        p_formula = self.subformula(0)
        sf0 = p_formula.subformula(0).get_equivalent_non_fair_formula(fairAP)
        if (isinstance(p_formula, CTLS.X)):
            return EX(And(sf0, fairAP))

        if (isinstance(p_formula, CTLS.F)):
            return EU(True, And(sf0, fairAP))

        if (isinstance(p_formula, CTLS.G)):
            return EG(And(sf0, fairAP))

        sf1 = p_formula.subformula(1).get_equivalent_non_fair_formula(fairAP)
        if (isinstance(p_formula, CTLS.U)):
            return EU(sf0, And(sf1, fairAP))

        if (isinstance(p_formula, CTLS.R)):
            neg_sf1 = LNot(sf1)
            neg_sf0 = LNot(sf0)

            return Or(EU(sf1, And(Not(Or(neg_sf0, neg_sf1))), fairAP),
                      EG(And(sf1, fairAP)))

        raise TypeError('{} is not a CTL formula'.format(self))

    def __str__(self):
        return 'E{}'.format(self._subformula[0])

    def __init__(self, phi):
        self.wrap_subformulas([phi], sys.modules[self.__module__].PathFormula)


def AX(psi):
    ''' A shortcut to build :math:`A(X(\psi))`.

    This method returns the formula :math:`A(X(\psi))` where :math:`\psi` is
    the method parameter.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :returns: the formula :math:`A(X(\psi))`
    :rtype: CTL.StateFormula
    '''
    return A(X(psi))


def EX(psi):
    ''' A shortcut to build :math:`E(X(\psi))`.

    This method returns the formula :math:`E(X(\psi))` where :math:`\psi` is
    the method parameter.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :returns: the formula :math:`E(X(\psi))`
    :rtype: CTL.StateFormula
    '''
    return E(X(psi))


def AF(psi):
    ''' A shortcut to build :math:`E(X(\psi))`.

    This method returns the formula :math:`E(X(\psi))` where :math:`\psi` is
    the method parameter.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :returns: the formula :math:`E(X(\psi))`
    :rtype: CTL.StateFormula
    '''
    return A(F(psi))


def EF(psi):
    ''' A shortcut to build :math:`E(F(\psi))`.

    This method returns the formula :math:`E(F(\psi))` where :math:`\psi` is
    the method parameter.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :returns: the formula :math:`E(F(\psi))`
    :rtype: CTL.StateFormula
    '''
    return E(F(psi))


def AG(psi):
    ''' A shortcut to build :math:`A(G(\psi))`.

    This method returns the formula :math:`A(G(\psi))` where :math:`\psi` is
    the method parameter.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :returns: the formula :math:`A(G(\psi))`
    :rtype: CTL.StateFormula
    '''
    return A(G(psi))


def EG(psi):
    ''' A shortcut to build :math:`E(G(\psi))`.

    This method returns the formula :math:`E(G(\psi))` where :math:`\psi` is
    the method parameter.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :returns: the formula :math:`E(G(\psi))`
    :rtype: CTL.StateFormula
    '''
    return E(G(psi))


def AU(psi, phi):
    ''' A shortcut to build :math:`A(U(\psi, \phi))`.

    This method returns the formula :math:`A(U(\psi, \phi))` where
    :math:`\psi` and :math:`\phi` are the method parameters.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :param phi: a state formula
    :type phi: CTL.StateFormula
    :returns: the formula :math:`A(U(\psi, \phi))`
    :rtype: CTL.StateFormula
    '''
    return A(U(psi, phi))


def EU(psi, phi):
    ''' A shortcut to build :math:`E(U(\psi, \phi))`.

    This method returns the formula :math:`E(U(\psi, \phi))` where
    :math:`\psi` and :math:`\phi` are the method parameters.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :param phi: a state formula
    :type phi: CTL.StateFormula
    :returns: the formula :math:`E(U(\psi, \phi))`
    :rtype: CTL.StateFormula
    '''
    return E(U(psi, phi))


def AR(psi, phi):
    ''' A shortcut to build :math:`A(R(\psi, \phi))`.

    This method returns the formula :math:`A(R(\psi, \phi))` where
    :math:`\psi` and :math:`\phi` are the method parameters.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :param phi: a state formula
    :type phi: CTL.StateFormula
    :returns: the formula :math:`A(R(\psi, \phi))`
    :rtype: CTL.StateFormula
    '''
    return A(R(psi, phi))


def ER(psi, phi):
    ''' A shortcut to build :math:`E(R(\psi, \phi))`.

    This method returns the formula :math:`E(R(\psi, \phi))` where
    :math:`\psi` and :math:`\phi` are the method parameters.

    :param psi: a state formula
    :type psi: CTL.StateFormula
    :param phi: a state formula
    :type phi: CTL.StateFormula
    :returns: the formula :math:`E(R(\psi, \phi))`
    :rtype: CTL.StateFormula
    '''
    return E(R(psi, phi))


alphabet = get_alphabet(__name__)
symbols = get_symbols(alphabet)
