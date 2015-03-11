#!/usr/bin/env python

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

class CTLFormula(object):
    '''
    A class representing CTL formulas.

    '''

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

class Atom(CTLFormula):
    '''
    The class representing CTL atoms.

    '''
    def __init__(self,name):
        ''' Initialize a CTL atom.

        This method builds a CTL atom.
        :param self: the Atom object that should be initializated.
        :type self: Atom
        :param name: the name of the atom that should be represented.
        :type name: str

        '''
        if not isinstance(name,str):
            raise TypeError('name=\'%s\' must be a string' % (name))
        self.name=str(name)

    def copy(self):
        return Atom(str(self.name))

    def __str__(self):
        return '%s' % (self.name)

class Bool(Atom):
    '''
    The class of CTL Boolean atoms.

    '''

    def __init__(self,value):
        ''' Initialize a CTL Boolean atom.

        This method builds either a True or a False CTL atom.
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
        return Bool(bool(self._value))

    def __str__(self):
        ''' Return a string depicting a CTL Boolean atom.

        :param self: the current object
        :type self: Bool
        :returns: a string depicting the current Boolean atom.
        :rtype: str

        '''
        return '%s' % (self._value)

class UnaryOperator(CTLFormula):
    def __init__(self,phi):
        if isinstance(phi,bool):
            self.phi=Bool(phi)
        else:
            if isinstance(phi,str):
                self.phi=Atom(phi)
            else:
                if isinstance(phi,CTLFormula):
                    self.phi=phi.copy()
                else:
                    raise RuntimeError('phi=\'%s\' must be a CTLFormula' % (phi))

class Not(UnaryOperator):
    def __init__(self,phi):
        super(Not,self).__init__(phi)

    ''' Return an operator equivalent to "not" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "not phi" in which "not" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes a CTL formula "phi" and returns the
               CTL formula "Not(phi)"
    :rtype: a function that takes a CTLformula and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi: Not(phi))

    def copy(self):
        return Not(self.phi.copy())

    def __str__(self):
        return 'not %s' % (self.phi)

class AX(UnaryOperator):
    def __init__(self,phi):
        super(AX,self).__init__(phi)

    ''' Return an operator equivalent to "AX" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "AX phi" in which "AX" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes a CTL formula "phi" and returns the
               CTL formula "Not(EX(Not(phi)))"
    :rtype: a function that takes a CTLformula and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi: Not(EX(Not(phi))))

    def copy(self):
        return AX(self.phi.copy())

    def __str__(self):
        return 'AX %s' % (self.phi)

class EX(UnaryOperator):
    def __init__(self,phi):
        super(EX,self).__init__(phi)

    ''' Return an operator equivalent to "EX" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "EX phi" in which "EX" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes a CTL formula "phi" and returns the
               CTL formula "EX(phi)"
    :rtype: a function that takes a CTLformula and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi: EX(phi))

    def copy(self):
        return EX(self.phi.copy())

    def __str__(self):
        return 'EX %s' % (self.phi)

class AG(UnaryOperator):
    def __init__(self,phi):
        super(AG,self).__init__(phi)

    ''' Return an operator equivalent to "AG" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "AG phi" in which "AG" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes a CTL formula "phi" and returns the
               CTL formula "Not(EU(True,Not(phi)))"
    :rtype: a function that takes a CTLformula and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi: Not(EU(True,Not(phi))))

    def copy(self):
        return AG(self.phi.copy())

    def __str__(self):
        return 'AG %s' % (self.phi)

class EG(UnaryOperator):
    def __init__(self,phi):
        super(EG,self).__init__(phi)

    ''' Return an operator equivalent to "EG" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "EG phi" in which "EG" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes a CTL formula "phi" and returns the
               CTL formula "EG(phi)"
    :rtype: a function that takes a CTLformula and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi: EG(phi))

    def copy(self):
        return EG(self.phi.copy())

    def __str__(self):
        return 'EG %s' % (self.phi)

class AF(UnaryOperator):
    def __init__(self,phi):
        super(AF,self).__init__(phi)

    ''' Return an operator equivalent to "AF" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "AF phi" in which "AF" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes a CTL formula "phi" and returns the
               CTL formula "Not(EG(Not(phi)))"
    :rtype: a function that takes a CTLformula and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi: Not(EG(Not(phi))))

    def copy(self):
        return AF(self.phi.copy())

    def __str__(self):
        return 'AF %s' % (self.phi)

class EF(UnaryOperator):
    def __init__(self,phi):
        super(EF,self).__init__(phi)

    ''' Return an operator equivalent to "EF" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "EF phi" in which "EF" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes a CTL formula "phi" and returns the
               CTL formula "EU(True,phi)"
    :rtype: a function that takes a CTLformula and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi: EU(True,phi))

    def copy(self):
        return EF(self.phi.copy())

    def __str__(self):
        return 'EF %s' % (self.phi)

class BinaryOperator(CTLFormula):
    def __init__(self,phi0,phi1):
        self.phi=[None]*2
        phi=[phi0,phi1]

        for i in range(2):
            if isinstance(phi[i],bool):
                self.phi[i]=Bool(phi[i])
            else:
                if isinstance(phi[i],str):
                    self.phi[i]=Atom(phi[i])
                else:
                    if isinstance(phi[i],CTLFormula):
                        self.phi[i]=phi[i].copy()
                    else:
                        raise RuntimeError('phi%d=\'%s\' must be a CTLFormula' %
                                            (i,phi1))

class Or(BinaryOperator):
    def __init__(self,phi0,phi1):
        super(Or,self).__init__(phi0,phi1)

    ''' Return an operator equivalent to "or" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "phi or psi" in which "or" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes two CTL formulas "phi" and "psi" and
               returns the CTL formula "phi or psi"
    :rtype: a function that takes two CTLformula's and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi0, phi1: Or(phi0,phi1))

    def copy(self):
        return Or(self.phi[0].copy(),self.phi[1].copy())

    def __str__(self):
        return '(%s or %s)' % (self.phi[0],self.phi[1])

class And(BinaryOperator):
    def __init__(self,phi0,phi1):
        super(And,self).__init__(phi0,phi1)

    ''' Return an operator equivalent to "and" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "phi and psi" in which "and" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes two CTL formulas "phi" and "psi" and
               returns the CTL formula "Not(Not(phi) or Not(psi))"
    :rtype: a function that takes two CTLformula's and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi0, phi1: Not(Or(Not(phi0),Not(phi1))))

    def copy(self):
        return Or(self.phi[0].copy(),self.phi[1].copy())

    def __str__(self):
        return '(%s and %s)' % (self.phi[0],self.phi[1])

class AU(BinaryOperator):
    def __init__(self,phi0,phi1):
        super(AU,self).__init__(phi0,phi1)

    ''' Return an operator equivalent to "AU" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "A(phi U psi)" in which "AU" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes two CTL formulas "phi" and "psi" and
               returns the CTL formula "Not(Or(EU(Not(psi),Not(Or(phi,psi))),EG(Not(psi))))"
    :rtype: a function that takes two CTLformula's and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi0, phi1: Not(Or(EU(Not(phi1),
                      Not(Or(phi0,phi1))),EG(Not(phi1)))))

    def copy(self):
        return AU(self.phi[0].copy(),self.phi[1].copy())

    def __str__(self):
        return 'A(%s U %s)' % (self.phi[0],self.phi[1])

class EU(BinaryOperator):
    def __init__(self,phi0,phi1):
        super(EU,self).__init__(phi0,phi1)

    ''' Return an operator equivalent to "EU" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "E(phi U psi)" in which "EU" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes two CTL formulas "phi" and "psi" and
               returns the CTL formula "E(phi U psi)"
    :rtype: a function that takes two CTLformula's and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi0, phi1: EU(phi0,phi1))

    def copy(self):
        return EU(self.phi[0].copy(),self.phi[1].copy())

    def __str__(self):
        return 'E(%s U %s)' % (self.phi[0],self.phi[1])

class AR(BinaryOperator):
    def __init__(self,phi0,phi1):
        super(AR,self).__init__(phi0,phi1)

    ''' Return an operator equivalent to "AR" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "A(phi R psi)" in which "AR" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes two CTL formulas "phi" and "psi" and
               returns the CTL formula "Not(EU(Not(phi),Not(psi)))"
    :rtype: a function that takes two CTLformula's and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi0,phi1: Not(EU(Not(phi0),Not(phi1))))

    def copy(self):
        return AR(self.phi[0].copy(),self.phi[1].copy())

    def __str__(self):
        return 'A(%s R %s)' % (self.phi[0],self.phi[1])

class ER(BinaryOperator):
    def __init__(self,phi0,phi1):
        super(ER,self).__init__(phi0,phi1)

    ''' Return an operator equivalent to "ER" in the EGUX syntax.

    This method returns a function that takes a CTL formula "phi" and returns
    a formula equivalent to "E(phi R psi)" in which "ER" is expressed by using
    exclusively the operators "not", "or", "EG", "EU", and "EX".
    :returns: a function that takes two CTL formulas "phi" and "psi" and
               returns the CTL formula "Or(EU(psi,Not(Or(Not(phi),Not(psi)))),EG(psi))"
    :rtype: a function that takes two CTLformula's and returns a CTLformula
    '''
    @staticmethod
    def get_equivalent_EGUX_operator():
        return (lambda phi0,phi1: Or(EU(phi1,Not(Or(Not(phi0),Not(phi1)))),
                                    EG(phi1)))

    def copy(self):
        return ER(self.phi[0].copy(),self.phi[1].copy())

    def __str__(self):
        return 'E(%s R %s)' % (self.phi[0],self.phi[1])

if __name__=='__main__':
    Phi=[EU(AX(Or(Not(Atom('p')), Not(False))), Not(True)),AR('p',Not('b'))]

    for phi in Phi:
        print(phi)
