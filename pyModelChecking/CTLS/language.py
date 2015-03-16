#!/usr/bin/env python

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

import sys
import inspect
#import pyModelChecking.CTLS as CTLS

class Formula(object):
    '''
    A class representing formulas.

    '''
    def __init__(self,*phi):
        self.wrap_subformulas(phi,sys.modules[self.__module__].Formula)

    def wrap_subformulas(self,subformulas,FormulaClass):
        self._subformula=[]

        for phi in subformulas:
            if isinstance(phi,bool):
                self._subformula.append(Bool(phi))
            else:
                if isinstance(phi,str):
                    self._subformula.append(Atom(phi))
                else:
                    if isinstance(phi,FormulaClass):
                        self._subformula.append(phi)
                    else:
                        if ((not isinstance(phi,sys.modules[self.__module__].Formula)) and
                                isinstance(phi,Formula)):
                            psi=phi.cast_to(sys.modules[self.__module__])

                            if isinstance(psi,FormulaClass):
                                self._subformula.append(psi)
                            else:
                                raise TypeError('%s must be a %s' % (phi,FormulaClass.__name__))
                        else:
                            raise TypeError('%s must be a %s' % (phi,FormulaClass.__name__))

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

    def negate_and_simplify(self):
        if isinstance(self,sys.modules[self.__module__].Not):
            return self.subformula(0)
        return sys.modules[self.__module__].Not(self)

    def cast_to(self,lang_module):
        if isinstance(self,Bool):
            return lang_module.Bool(bool(self._value))
        if isinstance(self,Atom):
            return lang_module.Atom(str(self.name))

        symbol_name=self.__class__.__name__
        if symbol_name not in lang_module.alphabet:
            raise TypeError('%s is not a %s formula' % (self,lang_module.__name__))

        subformulas=[]
        for subformula in self.subformulas():
            subformulas.append(Formula.cast_to(subformula,lang_module))

        return lang_module.alphabet[symbol_name](*subformulas)

    def __repr__(self):
        return str(self)

class AlphabeticSymbol(object):
    pass

class Atom(Formula,AlphabeticSymbol):
    '''
    The class representing atoms.

    '''
    def __init__(self,name):
        ''' Initialize a CTL* atom.

        This method builds a CTL* atom.
        :param self: the Atom object that should be initializated.
        :type self: Atom
        :param name: the name of the atom that should be represented.
        :type name: str

        '''
        if not isinstance(name,str):
            raise TypeError('name=\'%s\' must be a string' % (name))
        self.name=str(name)

    def copy(self):
        return self.__class__(str(self.name))

    def get_equivalent_restricted_formula(self):
        return self.copy()

    def subformula(self,idx):
        raise TypeError('Atoms have not subformulas.')

    def subformulas(self):
        return []

    def __str__(self):
        return '%s' % (self.name)

class Bool(Atom):
    '''
    The class of Boolean atoms.

    '''

    def __init__(self,value):
        ''' Initialize a Boolean atom.

        This method builds either a True or a False atom.
        :param self: the Bool object that should be initializated.
        :type self: Bool
        :param value: the boolean atom that should be represented.
        :type value: bool

        '''
        if not isinstance(value,bool):
            raise TypeError('\'%s\' must be boolean value' % (value))
        self._value=value

    def copy(self):
        ''' Copy the current object.

        :param self: the current object.
        :type self: Bool
        :returns: a copy of the current object.
        :rtype: Bool

        '''
        return self.__class__(bool(self._value))

    def subformula(self,idx):
        raise TypeError('Bools have not subformulas.')

    def __str__(self):
        ''' Return a string depicting the Boolean atom.

        :param self: the current object
        :type self: Bool
        :returns: a string depicting the current Boolean atom.
        :rtype: str

        '''
        return '%s' % (self._value)

class Not(Formula,AlphabeticSymbol):

    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: Not
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: Not
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()
        return subformula.negate_and_simplify()

    def __str__(self):
        return 'not(%s)' % (self._subformula[0])

class A(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: A
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: Not
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()

        return sys.modules[self.__module__].Not(
                    sys.modules[self.__module__].E(subformula.negate_and_simplify()))


    def __str__(self):
        return 'A(%s)' % (self._subformula[0])

class E(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: E
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: E
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()

        return sys.modules[self.__module__].E(subformula)


    def __str__(self):
        return 'E(%s)' % (self._subformula[0])

class X(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: X
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: X
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()
        return sys.modules[self.__module__].X(subformula)

    def __str__(self):
        return 'X(%s)' % (self._subformula[0])

class F(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: F
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: U
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()
        return sys.modules[self.__module__].U(True,subformula)

    def __str__(self):
        return 'F(%s)' % (self._subformula[0])

class G(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: G
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: Not
        '''
        subformula=self.subformula(0).get_equivalent_restricted_formula()
        return sys.modules[self.__module__].Not(
                    sys.modules[self.__module__].U(True,subformula.negate_and_simplify()))

    def __str__(self):
        return 'G(%s)' % (self._subformula[0])

class Or(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: Or
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: Or
        '''
        subformulas=[p.get_equivalent_restricted_formula() for p in self._subformula]
        return sys.modules[self.__module__].Or(*subformulas)

    def __str__(self):
        return '(%s or %s)' % (self._subformula[0],self._subformula[1])

class And(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: And
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: Not
        '''
        subformulas=[]
        for p in self._subformula:
            equi_p=p.get_equivalent_restricted_formula()
            subformulas.append(equi_p.negate_and_simplify())

        return sys.modules[self.__module__].Not(
                    sys.modules[self.__module__].Or(*subformulas))

    def __str__(self):
        return '(%s and %s)' % (self._subformula[0],self._subformula[1])

class Imply(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: And
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: Not
        '''
        equiv_sf0=self.subformula(0).get_equivalent_restricted_formula()
        return sys.modules[self.__module__].Or(equiv_sf0.negate_and_simplify(),
                    self.subformula(1).get_equivalent_restricted_formula())

    def __str__(self):
        return '(%s --> %s)' % (self._subformula[0],self._subformula[1])

class U(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: U
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: U
        '''
        subformulas=[]
        for p in self._subformula:
            subformulas.append(p.get_equivalent_restricted_formula())

        return sys.modules[self.__module__].U(*subformulas)

    def __str__(self):
        return '(%s U %s)' % (self._subformula[0],self._subformula[1])

class R(Formula,AlphabeticSymbol):
    def get_equivalent_restricted_formula(self):
        ''' Return a equivalent formula in the restricted syntax.

        This method returns a formula that avoids "and", "implies", "A", "F",
        and "R" and that is equivalent to this formula.
        :param self: this formula
        :type self: R
        :returns: a formula that avoids "and", "implies", "A", "F", and "R" and
                  that is equivalent to this formula
        :rtype: Not
        '''
        subformulas=[]
        for p in self._subformula:
            equi_p=p.get_equivalent_restricted_formula()
            subformulas.append(equi_p.negate_and_simplify())

        return sys.modules[self.__module__].Not(
                    sys.modules[self.__module__].U(*subformulas))

    def __str__(self):
        return '(%s R %s)' % (self._subformula[0],self._subformula[1])

def get_alphabet(name):
    alphabet={}
    for name, obj in inspect.getmembers(sys.modules[name], inspect.isclass):
        if obj!=AlphabeticSymbol and issubclass(obj,AlphabeticSymbol):
            alphabet[name]=obj

    return alphabet

alphabet=get_alphabet(__name__)
