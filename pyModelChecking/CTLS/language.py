#!/usr/bin/env python

import sys
import inspect

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"


class Formula(object):
    '''
    A class representing CTL* formulas.

    '''

    __desc__='CTL* formula'

    def __init__(self,*phi):
        self.wrap_subformulas(phi,sys.modules[self.__module__].Formula)

    def wrap_subformulas(self,subformulas,FormulaClass):

        Lang=sys.modules[self.__module__]

        self._subformula=[]
        self.height=0

        for phi in subformulas:
            if isinstance(phi,bool):
                self._subformula.append(Lang.Bool(phi))
            else:
                if isinstance(phi,str):
                    self._subformula.append(Lang.AtomicProposition(phi))
                else:
                    if isinstance(phi,FormulaClass):
                        self._subformula.append(phi)
                        self.height=max(self.height,phi.height+1)
                    else:
                        if ((not isinstance(phi,Lang.Formula)) and
                                isinstance(phi,Formula)):
                            psi=phi.cast_to(Lang)

                            if isinstance(psi,FormulaClass):
                                self._subformula.append(psi)
                                self.height=max(self.height,psi.height+1)
                            else:
                                raise TypeError('expected a %s, got the %s %s' %
                                                (FormulaClass.__desc__,
                                                 phi.__desc__,phi))
                        else:
                            raise TypeError('expected a %s, got the %s %s' %
                                                (FormulaClass.__desc__,
                                                 phi.__desc__,phi))

    def copy(self):
        return self.__class__(*[sf.copy() for sf in self._subformula])

    def __hash__(self):
        return str(self).__hash__()

    def __cmp__(self,other):
        self_str=str(self)
        other_str=str(other)
        if (self_str<other_str):
            return -1

        if (self_str>other_str):
            return 1

        return 0

    def subformula(self,idx):
        return self._subformula[idx]

    def subformulas(self):
        return self._subformula

    def is_a_state_formula(self):
        raise RuntimeError('%s.is_a_state_formula() not implemented yet' % (self.__class__))

    def negate_and_simplify(self):
        if isinstance(self,sys.modules[self.__module__].Not):
            return self.subformula(0)
        return sys.modules[self.__module__].Not(self)

    def cast_to(self,Lang):
        if isinstance(self,Bool):
            return Lang.Bool(bool(self._value))
        if isinstance(self,AtomicProposition):
            return Lang.AtomicProposition(str(self.name))

        symbol_name=self.__class__.__name__
        if symbol_name not in Lang.alphabet:
            raise TypeError(('%s is not in the alphabet ' % (symbol_name))+
                            ('of %s, thus %s is ' % (Lang.__name__,self))+
                            ('not a %s formula' % (self,Lang.__name__)))

        subformulas=[]
        for subformula in self.subformulas():
            subformulas.append(Formula.cast_to(subformula,Lang))

        return Lang.alphabet[symbol_name](*subformulas)

    def __repr__(self):
        return str(self)

class AlphabeticSymbol(object):
    pass

class AtomicProposition(Formula,AlphabeticSymbol):
    '''
    The class representing atomic propositionic propositions.

    '''
    def __init__(self,name):
        ''' Initialize a CTL* atomic proposition.

        This method builds a CTL* atomic propositionic proposition.

        :param name: the name of the atomic proposition that should be represented.
        :type name: str
        '''
        if not isinstance(name,str):
            raise TypeError('name=\'%s\' must be a string' % (name))
        self.name=str(name)
        self.height=0

    def copy(self):
        return self.__class__(str(self.name))

    def get_equivalent_restricted_formula(self):
        return self.copy()

    def subformula(self,idx):
        raise TypeError('AtomicPropositions have not subformulas.')

    def subformulas(self):
        return []

    def is_a_state_formula(self):
        return True

    def __str__(self):
        return '%s' % (self.name)

class Bool(AtomicProposition):
    '''
    The class of Boolean atomic propositions.

    '''

    def __init__(self,value):
        ''' Initialize a Boolean atomic proposition.

        This method builds either a True or a False atomic proposition.

        :param value: the boolean atomic proposition that should be represented.
        :type value: bool

        '''
        if not isinstance(value,bool):
            raise TypeError('\'%s\' must be boolean value' % (value))
        self._value=value
        self.height=0

    def copy(self):
        ''' Copy the current object.

        :returns: a copy of the current object.
        :rtype: pyModelChecking.CTLS.Bool

        '''
        return self.__class__(bool(self._value))

    def subformula(self,idx):
        raise TypeError('Bools have not subformulas.')

    def __str__(self):
        ''' Return a string depicting the Boolean atomic proposition.

        :returns: a string depicting the current Boolean atomic proposition.
        :rtype: str
        '''
        return '%s' % (self._value)

class Not(Formula,AlphabeticSymbol):

    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.Not
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()

        return subformula.negate_and_simplify()

    def is_a_state_formula(self):
        return self.subformula(0).is_a_state_formula()

    def __str__(self):
        return 'not %s' % (self._subformula[0])

class A(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.Not
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()

        Lang=sys.modules[self.__module__]
        return Lang.Not(Lang.E(subformula.negate_and_simplify()))

    def is_a_state_formula(self):
        return True

    def __str__(self):
        return 'A(%s)' % (self._subformula[0])

class E(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.E
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()

        Lang=sys.modules[self.__module__]
        return Lang.E(subformula)

    def is_a_state_formula(self):
        return True

    def __str__(self):
        return 'E(%s)' % (self._subformula[0])

class X(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.X
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()

        Lang=sys.modules[self.__module__]
        return Lang.X(subformula)

    def is_a_state_formula(self):
        return False

    def __str__(self):
        return 'X(%s)' % (self._subformula[0])

class F(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.U
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()

        Lang=sys.modules[self.__module__]
        return Lang.U(True,subformula)

    def is_a_state_formula(self):
        return False

    def __str__(self):
        return 'F(%s)' % (self._subformula[0])

class G(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.Not
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()

        Lang=sys.modules[self.__module__]
        return Lang.Not(Lang.U(True,subformula.negate_and_simplify()))

    def is_a_state_formula(self):
        return False

    def __str__(self):
        return 'G(%s)' % (self._subformula[0])

class Or(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.Or
        '''
        subformulas=[p.get_equivalent_restricted_formula() for p in self._subformula]

        Lang=sys.modules[self.__module__]
        return Lang.Or(*subformulas)

    def is_a_state_formula(self):
        for sf in self.subformulas():
            if not sf.is_a_state_formula():
                return False

        return True

    def __str__(self):
        return '(%s or %s)' % (self._subformula[0],self._subformula[1])

class And(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.Not
        '''
        subformulas=[]
        for p in self._subformula:
            equi_p=p.get_equivalent_restricted_formula()
            subformulas.append(equi_p.negate_and_simplify())

        Lang=sys.modules[self.__module__]
        return Lang.Not(Lang.Or(*subformulas))

    def is_a_state_formula(self):
        for sf in self.subformulas():
            if not sf.is_a_state_formula():
                return False

        return True

    def __str__(self):
        return '(%s and %s)' % (self._subformula[0],self._subformula[1])

class Imply(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.Not
        '''
        equiv_sf0=self.subformula(0).get_equivalent_restricted_formula()

        Lang=sys.modules[self.__module__]
        return Lang.Or(equiv_sf0.negate_and_simplify(),
                    self.subformula(1).get_equivalent_restricted_formula())

    def is_a_state_formula(self):
        for sf in self.subformulas():
            if not sf.is_a_state_formula():
                return False

        return True

    def __str__(self):
        return '(%s --> %s)' % (self._subformula[0],self._subformula[1])

class U(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.U
        '''
        subformulas=[]
        for p in self._subformula:
            subformulas.append(p.get_equivalent_restricted_formula())

        Lang=sys.modules[self.__module__]
        return Lang.U(*subformulas)

    def is_a_state_formula(self):
        return False

    def __str__(self):
        return '(%s U %s)' % (self._subformula[0],self._subformula[1])

class R(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return an equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.

        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: pyModelChecking.CTLS.Not
        '''
        subformulas=[]
        for p in self._subformula:
            equi_p=p.get_equivalent_restricted_formula()
            subformulas.append(equi_p.negate_and_simplify())

        Lang=sys.modules[self.__module__]
        return Lang.Not(Lang.U(*subformulas))

    def is_a_state_formula(self):
        return False

    def __str__(self):
        return '(%s R %s)' % (self._subformula[0],self._subformula[1])

def get_alphabet(name):
    alphabet={}
    for name, obj in inspect.getmembers(sys.modules[name], inspect.isclass):
        if obj!=AlphabeticSymbol and issubclass(obj,AlphabeticSymbol):
            alphabet[name]=obj

    return alphabet


alphabet=get_alphabet(__name__)
