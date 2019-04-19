"""
.. module:: CTLS.language
   :synopsis: Represents the CTL* language.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""


from pyModelChecking import PL

from ..language import LNot
from ..language import get_alphabet
from pyModelChecking.PL import get_symbols

from ..language import AlphabeticSymbol

import sys


class Formula(PL.Formula):
    ''' A class to represent CTL* formulas.

    Formulas are represented as nodes in labelled trees: leaves are
    terminal symbols (e.g., atomic propositions and Boolean values),
    while internal nodes correspond to operators and quantifiers.
    The ariety of internal nodes depends on the kind of operator or
    quantifier must be represented. For instance, the arity of a node
    representing the formula :math:`not (A(p U q) \lor True)` is one because
    the formula has exclusively one sub-formula, i.e.,
    :math:`A(p U q) \lor True`. On the contrary, this last formula has
    two sub-formulas, i.e., :math:`A(p U q)` and  :math:`True`, thus, the node
    representing it has two sons.
    '''

    __desc__ = 'CTL* formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, sys.modules[self.__module__].Formula)

    def get_equivalent_non_fair_formula(self, fairAP):
        fair_sfs = [sf.get_equivalent_non_fair_formula(fairAP)
                    for sf in self._subformula]

        return self.__class__(*fair_sfs)

    def is_a_state_formula(self):
        ''' Returns True if and only if the object represents a state formula.

        This method should return True if and only if the current object
        represents a state formula. Since this is a general class meant to
        represent both state and path formulas, an implementation for this
        method cannot be provided. Thus, any call to it raise a
        :class:`RuntimeError`.

        :param self: this formula
        :type self: CTLS.Formula
        :raise RuntimeError: this method cannot be implemented by this general
            class
        '''
        raise RuntimeError('{}.is_a_state_formula() '.format(self.__class__) +
                           'not implemented yet')


class PathFormula(Formula):
    '''
    A class representing CTL* path formulas.

    '''

    __desc__ = 'CTL* path formula'

    def is_a_state_formula(self):
        ''' Returns True if and only if the object has type :class:`StateFormula`.

        This method returns True if and only if the current object has
        type :class:`CTLS.StateFormula`. Since this is a method of the
        class :class:`CTLS.PathFormula`, it always returns False.

        :param self: this formula
        :type self: CTLS.PathFormula
        :returns: False
        :rtype: bool
        '''
        return False

    def __init__(self, *phi):
        self.wrap_subformulas(phi, sys.modules[self.__module__].Formula)


class StateFormula(PathFormula):
    '''
    A class representing CTL* state formulas.

    '''

    __desc__ = 'CTL* state formula'

    def is_a_state_formula(self):
        ''' Returns True if and only if the object has type :class:`StateFormula`.

        This method returns True if and only if the current object has
        type :class:`CTLS.StateFormula`. Since this is a method of the
        class :class:`CTLS.StateFormula`, it always returns True.

        :param self: this formula
        :type self: CTLS.StateFormula
        :returns: True
        :rtype: bool
        '''
        return True

    def __init__(self, *phi):
        self.wrap_subformulas(phi, sys.modules[self.__module__].Formula)


class AtomicProposition(PL.AtomicProposition, StateFormula):
    '''
    The class representing atomic propositionic propositions.

    '''
    def __init__(self, name):
        ''' Initialize a CTL* atomic proposition.

        This method builds a CTL* atomic propositionic proposition.

        :param name: the name of the atomic proposition.
        :type name: str
        '''
        super(AtomicProposition, self).__init__(name)

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula. Since this is a method of the class
        :class:`CTLS.AtomicProposition`, a clone of the current object is
        always returned.

        :returns: a clone of the current atomic proposition.
        :rtype: CTLS.AtomicProposition
        '''
        return self.clone()

    def get_equivalent_non_fair_formula(self, fairAP):
        Lang = sys.modules[self.__module__]

        return Lang.And(self, fairAP)


class Bool(PL.Bool, AtomicProposition):
    '''
    The class of Boolean atomic propositions.

    '''

    def __init__(self, value):
        ''' Initialize a Boolean atomic proposition.

        This method builds either a True or a False atomic proposition.

        :param value: the boolean atomic proposition.
        :type value: bool

        '''
        super(Bool, self).__init__(value)


class TemporalOperator(PathFormula):
    '''
    A class to represent temporal operators such as :math:`R` or :math:`X`.

    '''
    def __str__(self):
        if len(self._subformula) == 1:
            return '{}({})'.format(self.__class__.symbols[0],
                                   self._subformula[0])
        else:
            sep = ' {} '.format(self.__class__.symbols[0])
            return '({})'.format(sep.join([str(f) for f in self._subformula]))


class PathQuantifier(StateFormula):
    '''
    A class to represent the path quantifiers :math:`A` or :math:`E`.

    '''

    def __init__(self, phi):
        self.wrap_subformulas([phi], Formula)

    def __str__(self):
        return '{}({})'.format(self.__class__.symbols[0], self._subformula[0])


class LogicOperator(Formula, PL.LogicOperator):
    '''
    A class to represent logic operator such as :math:`\land` or :math:`\lor`.

    '''

    def is_a_state_formula(self):
        ''' Returns True if and only if the object represents a state formula.

        This method returns True if and only if the current object represents
        a state formula.

        :param self: this formula
        :type self: CTLS.LogicOperator
        :returns: True if and only if the object represents a state formula.
        :rtype: bool
        '''
        for sf in self.subformulas():
            if not sf.is_a_state_formula():
                return False

        return True


class Not(LogicOperator, PL.Not):

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.Not
        '''
        subformula = self.subformula(0).get_equivalent_restricted_formula()

        return LNot(subformula)

    def is_a_state_formula(self):
        ''' Returns True if and only if the object represents a state formula.

        This method returns True if and only if the current object represents
        a state formula.

        :param self: this formula
        :type self: CTLS.Not
        :returns: True if and only if this formula is a state formula.
        :rtype: bool
        '''
        return self.subformula(0).is_a_state_formula()


class A(PathQuantifier, AlphabeticSymbol):
    '''
    A class representing CTL* A-formulas.

    '''

    symbols = ['A']

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.Not
        '''
        subformula = self.subformula(0).get_equivalent_restricted_formula()

        Lang = sys.modules[self.__module__]
        return Lang.Not(Lang.E(LNot(subformula)))

    def get_equivalent_non_fair_formula(self, fairAP):
        Lang = sys.modules[self.__module__]

        sf = self.subformula(0).get_equivalent_non_fair_formula(fairAP)

        return self.__class__(LNot(Lang.And(LNot(sf), fairAP)))


class E(PathQuantifier, AlphabeticSymbol):
    '''
    A class representing CTL* A-formulas.

    '''

    symbols = ['E']

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.E
        '''
        subformula = self.subformula(0).get_equivalent_restricted_formula()

        Lang = sys.modules[self.__module__]
        return Lang.E(subformula)

    def get_equivalent_non_fair_formula(self, fairAP):
        fair_sf = self.subformula(0).get_equivalent_non_fair_formula(fairAP)

        Lang = sys.modules[self.__module__]
        return Lang.E(Lang.And(fairAP, fair_sf))


class X(TemporalOperator, AlphabeticSymbol):
    symbols = ['X']

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and
                  is equivalent this formula
        :rtype: CTLS.X
        '''
        subformula = self.subformula(0).get_equivalent_restricted_formula()

        Lang = sys.modules[self.__module__]
        return Lang.X(subformula)


class F(TemporalOperator, AlphabeticSymbol):
    symbols = ['F']

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.U
        '''
        subformula = self.subformula(0).get_equivalent_restricted_formula()

        Lang = sys.modules[self.__module__]
        return Lang.U(True, subformula)


class G(TemporalOperator, AlphabeticSymbol):
    symbols = ['G']

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.Not
        '''
        subformula = self.subformula(0).get_equivalent_restricted_formula()

        Lang = sys.modules[self.__module__]
        return Lang.Not(Lang.U(True, LNot(subformula)))


class Or(LogicOperator, PL.Or):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.Or
        '''
        subformulas = [p.get_equivalent_restricted_formula()
                       for p in self._subformula]

        Lang = sys.modules[self.__module__]
        return Lang.Or(*subformulas)


class And(LogicOperator, PL.And):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.Not
        '''
        subformulas = []
        for p in self._subformula:
            equi_p = p.get_equivalent_restricted_formula()
            subformulas.append(LNot(equi_p))

        Lang = sys.modules[self.__module__]
        return Lang.Not(Lang.Or(*subformulas))


class Imply(LogicOperator, PL.Imply):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.Not
        '''
        equiv_sf0 = self.subformula(0).get_equivalent_restricted_formula()

        Lang = sys.modules[self.__module__]
        return Lang.Or(LNot(equiv_sf0),
                       self.subformula(1).get_equivalent_restricted_formula())


class U(TemporalOperator, AlphabeticSymbol):
    symbols = ['U']

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.U
        '''
        subformulas = []
        for p in self._subformula:
            subformulas.append(p.get_equivalent_restricted_formula())

        Lang = sys.modules[self.__module__]
        return Lang.U(*subformulas)


class R(TemporalOperator, AlphabeticSymbol):
    symbols = ['R']

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids :math:`A`, :math:`F`,
        :math:`R`, :math:`\land` and :math:`\\rightarrow` and is equivalent to
        this formula.

        :returns: a formula that avoids :math:`A`, :math:`F`, :math:`R`,
                  :math:`\land` and :math:`\\rightarrow` and is equivalent to
                  this formula
        :rtype: CTLS.Not
        '''
        subformulas = []
        for p in self._subformula:
            equi_p = p.get_equivalent_restricted_formula()
            subformulas.append(LNot(equi_p))

        Lang = sys.modules[self.__module__]
        return Lang.Not(Lang.U(*subformulas))


alphabet = get_alphabet(__name__)
symbols = get_symbols(alphabet)
