"""
.. module:: language
   :synopsis: Represents formulas and logics.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""

import sys
import inspect


class Formula(object):
    ''' A class to represent formulas.

    Formulas are represented as nodes in labelled trees: leaves are terminal
    symbols (e.g., atomic propositions and Boolean values), while internal
    nodes correspond to operators and quantifiers. The ariety of internal nodes
    depends on the kind of operator or quantifier must be represented.
    For instance, the arity of a node representing the formula
    :math:`not (p \lor True)` is one because the formula has exclusively one
    sub-formula, i.e., :math:`p \lor True`. On the contrary, this last formula
    has two sub-formulas, i.e., :math:`p` and  :math:`True`, thus, the node
    representing it has two sons.
    '''

    __desc__ = 'formula'

    def __init__(self, *phi):
        self.wrap_subformulas(phi, sys.modules[self.__module__].Formula)

    def wrap_subformulas(self, subformulas, FormulaClass):
        ''' Replaces subformulas of the current object

        This method replaces the subformulas of the current object by
        using the :class:`FormulaClass` objects representing the
        elements of :param subformulas:.

        :param self: this object
        :type self: Formula
        :param subformulas: the set of objects to be used as model for the
            replacement
        :type subformulas: Container
        :param FormulaClass: the final class of the new subformulas
        :type FormulaClass: class
        '''

        def err_msg(phi):
            return ('expected a {}, '.format(FormulaClass.__desc__) +
                    'got the {} {}'.format(phi.__desc__, phi))

        Lang = sys.modules[self.__module__]

        self._subformula = []
        self.height = 0

        for phi in subformulas:
            if isinstance(phi, bool):
                self._subformula.append(Lang.Bool(phi))
            else:
                if not isinstance(phi, FormulaClass):
                    if (isinstance(phi, Lang.Formula) or
                            not isinstance(phi, Formula)):

                        raise TypeError(err_msg(phi))

                    phi = phi.cast_to(Lang)

                    if not isinstance(phi, FormulaClass):
                        raise TypeError(err_msg(phi))

                self._subformula.append(phi)
                self.height = max(self.height, phi.height+1)

    def clone(self):
        ''' Clones a formula

        :returns: a clone of the current formula
        :rtype: Formula
        '''
        return self.__class__(*[sf.clone() for sf in self._subformula])

    def __and__(self, obj):
        Lang = sys.modules[self.__module__]

        return Lang.And(self, obj)

    def __rand__(self, obj):
        Lang = sys.modules[self.__module__]

        return Lang.And(obj, self)

    def __or__(self, obj):
        Lang = sys.modules[self.__module__]

        return Lang.Or(self, obj)

    def __ror__(self, obj):
        Lang = sys.modules[self.__module__]

        return Lang.Or(obj, self)

    def __invert__(self):
        Lang = sys.modules[self.__module__]

        return Lang.Not(self)

    def __hash__(self):
        return str(self).__hash__()

    def __eq__(self, other):
        return str(self) == str(other)

    def __cmp__(self, other):
        self_str = str(self)
        other_str = str(other)
        if (self_str < other_str):
            return -1

        if (self_str > other_str):
            return 1

        return 0

    def subformula(self, i):
        ''' Returns the :math:`i`-th subformula.

        :param i: the index of the subformula to be returned
        :type i: Integer
        :returns: returns the :math:`i`-th subformula of the current formula
        :rtype: Formula
        '''
        return self._subformula[i]

    def subformulas(self):
        ''' Returns the list of all the subformulas.

        :returns: returns the list of the subformulas of the current formula
        :rtype: list
        '''
        return self._subformula

    def __repr__(self):
        return str(self)


class Bool(Formula):
    '''
    The class of Boolean values.

    '''

    symbols = {True: 'true',
               False: 'false'}

    def __init__(self, value):
        ''' Initialize a Boolean value.

        This method builds either a True or a False value.

        :param value: the boolean value.
        :type value: bool

        '''
        if not isinstance(value, bool):
            raise TypeError('\'{}\' must be boolean value'.format(value))
        self._value = value
        self.height = 0

    def clone(self):
        ''' Clones an atomic proposition

        :returns: a clone of the current Bool value
        :rtype: Bool
        '''
        return self.__class__(bool(self._value))

    def subformula(self, i):
        ''' Returns the :math:`i`-th subformula.

        :param i: the index of the subformula to be returned
        :type i: Integer
        :raise TypeError: Boolean values have not subformulas
        '''
        raise TypeError('Bools have not subformulas.')

    def subformulas(self):
        ''' Returns the list of all the subformulas.

        :returns: returns the empty list of the subformulas of the current
            formula
        :rtype: list
        '''
        return []

    def __hash__(self):
        return str(self).__hash__()

    def __eq__(self, other):

        if isinstance(other, bool):
            return self._value == other

        if isinstance(other, Bool):
            return self._value == other._value

        return False

    def __str__(self):
        ''' Return a string depicting the Boolean value.

        :returns: a string depicting the current Boolean value.
        :rtype: str
        '''
        return Bool.symbols[self._value]


class AlphabeticSymbol(object):
    pass


class LogicOperator(Formula):
    '''
    A class to represent logic operator such as :math:`\land` or :math:`\lor`.

    '''
    def __str__(self):
        if len(self._subformula) == 1:
            return '{} {}'.format(self.__class__.symbols[0],
                                  self._subformula[0])
        else:
            sep = ' {} '.format(self.__class__.symbols[0])
            return '({})'.format(sep.join([str(f) for f in self._subformula]))


class Not(LogicOperator, AlphabeticSymbol):
    '''
    Represents logic negation.

    '''

    symbols = ['not', '~']

    def __init__(self, phi):
        super(Not, self).__init__(phi)


class Or(LogicOperator, AlphabeticSymbol):
    '''
    Represents logic non-exclusive disjunction.

    '''
    symbols = ['or', '|']


class And(LogicOperator, AlphabeticSymbol):
    '''
    Represents logic conjunction.

    '''
    symbols = ['and', '&']


class Imply(LogicOperator, AlphabeticSymbol):
    '''
    Represents logic implication.

    '''
    symbols = ['-->']

    def __init__(self, phi, psi):
        super(Imply, self).__init__(phi, psi)


def get_alphabet(name):
    alphabet = {}
    for name, obj in inspect.getmembers(sys.modules[name], inspect.isclass):
        if obj != AlphabeticSymbol and issubclass(obj, AlphabeticSymbol):
            alphabet[name] = obj

    return alphabet


def get_symbols(alphabet):
    symbols = list()

    for name, c in alphabet.items():
        if name == 'Bool':
            symbols.extend(Bool.symbols.values())
        else:
            if name != 'AtomicProposition':
                symbols.extend(c.symbols)

    return symbols


def LNot(formula):
    ''' Logical Not - Returns an equivalent formula that does not begin
    with two negations.

    This method negates the parameter and removes all the pairs of negations at
    the begin of the obtained formula.

    :param formula: a formula
    :type formula: Formula
    :returns: a formula equivalent to the parameter that does not begin with
        two negations
    :rtype: Formula
    '''

    if isinstance(formula, Not):
        if isinstance(formula.subformula(0), Not):
            return LNot(formula.subformula(0).subformula(0))
        return formula.subformula(0)

    return sys.modules[formula.__module__].Not(formula)


alphabet = get_alphabet(__name__)
symbols = get_symbols(alphabet)
