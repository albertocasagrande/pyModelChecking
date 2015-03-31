#!/usr/bin/env python

from .BDD import BDD
from .BDD import boolean_function as BDD_boolean_function
from .ordering import Ordering

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

class BooleanParser(object):
    '''
    A class to represent parsers of boolean functions.

    The objects of this class can parse strings representing Boolean functions
    are return the corresponding OBDD.

    '''

    def __init__(self,ordering):
        ''' Initialize a Boolean parser.

        :param ordering: an ordering for the variables to be parsed
        :type ordering: Ordering
        '''
        if not isinstance(ordering,Ordering):
            try:
                ordering=Ordering(ordering)
            except TypeError:
                raise TypeError('expected an Ordering of variables, got %s' % (ordering))

        self.ordering=ordering

    def consume_spaces(self,funct_str,i):
        ''' Consume the spaces of a string up to the next non-space character.

        :param funct_str: a string to be parsed
        :type funct_str: str
        :param i: the index of the first character to be parsed
        :type i: int
        :returns: the first non parsed index
        :rtype: int
        '''
        while i<len(funct_str) and funct_str[i]==' ':
            i+=1
        return i

    def operator_parse(self,funct_str,i):
        ''' Parse a Boolean operator from a string.

        :param funct_str: a string to be parsed
        :type funct_str: str
        :param i: the index of the first character to be parsed
        :type i: int
        :returns: a tuple (F,j) where F is one of the Boolean function
                  '&', '|', or '^' and j is the first non parsed index
        :rtype: a tuple (function,int)
        '''
        j=self.consume_spaces(funct_str,i)

        if j==len(funct_str):
            raise ParseError(funct_str,i)

        if funct_str[j]=='&':
            return ((lambda A,B: A&B),j+1)

        if funct_str[j]=='|':
            return ((lambda A,B: A|B),j+1)

        if funct_str[j]=='^':
            return ((lambda A,B: A^B),j+1)

        raise ParseError(funct_str,i)

    def variable_parse(self,funct_str,i):
        ''' Parse a Boolean variable from a string.

        :param funct_str: a string to be parsed
        :type funct_str: str
        :param i: the index of the first character to be parsed
        :type i: int
        :returns: a tuple (A,j) where A is an OBDD representing the parsed
                  variable and j is the first non parsed index
        :rtype: (OBDD,int)
        '''
        w=self.consume_spaces(funct_str,i)

        if w==len(funct_str) or not funct_str[w].isalpha():
            raise ParseError(funct_str,w)

        j=w
        while j<len(funct_str) and funct_str[j].isalpha():
            j+=1

        var=funct_str[w:j]

        for name, value in {'True': True, 'False': False}.items():
            if var==name:
                return (OBDD(self.ordering,BDD(value)),j)

        if var not in self.ordering:
            raise RuntimeError('variable %s in not in ordering %s' % (var,self.ordering))

        bdd=BDD(var,BDD(False),BDD(True))
        return (OBDD(self.ordering,bdd),j)

    def term_parse(self,funct_str,i):
        ''' Parse a Boolean term from a string.

        :param funct_str: a string to be parsed
        :type funct_str: str
        :param i: the index of the first character to be parsed
        :type i: int
        :returns: a tuple (A,j) where A is an OBDD representing the parsed
                  term and j is the first non parsed index
        :rtype: (OBDD,int)
        '''
        j=self.consume_spaces(funct_str,i)
        if j==len(funct_str):
            raise ParseError(funct_str,i)

        if funct_str[j]=='(':
            (A,j)=self.function_parse(funct_str,j+1)
            j=self.consume_spaces(funct_str,j)
            if j==len(funct_str) or funct_str[j]!=')':
                raise ParseError(funct_str,i)
            return (A,j+1)

        if funct_str[j]=='~':
            (A,j)=self.term_parse(funct_str,j+1)
            return (~A,j)

        return self.variable_parse(funct_str,j)

    def function_parse(self,funct_str,i):
        ''' Parse a Boolean function from a string.

        :param funct_str: a string to be parsed
        :type funct_str: str
        :param i: the index of the first character to be parsed
        :type i: int
        :returns: a tuple (A,j) where A is an OBDD representing the parsed
                  function and j is the first non parsed index
        :rtype: (OBDD,int)
        '''
        (A,j)=self.term_parse(funct_str,i)

        if j==len(funct_str) or funct_str[j]==')':
            return (A,j)

        (op,j)=self.operator_parse(funct_str,j)
        (B,j)=self.function_parse(funct_str,j)

        return (op(A,B),j)

    def parse(self,funct_str,i=0):
        ''' Parse a Boolean function from a string.

        :param funct_str: a string to be parsed
        :type funct_str: str
        :param i: the index of the first character to be parsed
        :type i: int
        :returns: an OBDD representing the parsed function
        :rtype: OBDD
        '''
        (obdd,i)=self.function_parse(funct_str,i)

        i=self.consume_spaces(funct_str,i)

        if i==len(funct_str):
            return obdd

        raise RuntimeError('unparsed suffix \'%s\'' % (funct_str[i:]))

def boolean_function(A,B,operator):
    ''' Apply a binray Boolean operator to two OBDD.

    :param A: an OBDD
    :type A: OBDD
    :param B: an OBDD
    :type B: OBDD
    :param operator: a binary boolean operator
    :type operator: function
    :returns: The OBDD obtained by applying the operator to the two OBDD
    :rtype: OBDD
    '''

    for O in [A,B]:
        if not isinstance(O,OBDD):
            raise TypeError('expected an OBDD, got %s' % (O))

    if A.ordering!=B.ordering:
        raise RuntimeError('Unsupported operation: %s and %s have different variable ordering' % (A,B))

    result_cache=dict()

    bdd=BDD_boolean_function(A.bdd,B.bdd,operator,A.ordering,result_cache)
    return OBDD(A.ordering, bdd,check_ordering=False)

class OBDD(object):
    '''
    A class to represent Ordered Binary Decision Diagrams (OBDDs).
    '''

    def __init__(self,ordering,bfunct,check_ordering=True):
        ''' Initialize an OBDD.

        :param ordering: an ordering for the variables to be parsed
        :type ordering: Ordering
        :param bfunct: either a BDD or a string that represents a binary
                function
        :type bfunct: str or function
        :param check_ordering: a Boolean flag: if bfunct is a BDD and this flag
                               is set to True, then this method check whether
                               the BDD respects the ordering
        :type check_ordering: bool
        '''
        if not isinstance(ordering,Ordering):
            try:
                ordering=Ordering(ordering)
            except TypeError:
                raise TypeError('expected an Ordering of variables, got %s' % (ordering))

        self.ordering=ordering

        if isinstance(bfunct,BDD):
            if check_ordering and not bfunct.respect_ordering(ordering):
                raise RuntimeError('the BDD %s does not respect %s' % (bfunct,ordering))

            self.bdd=bfunct
        else:
            if isinstance(bfunct,str):
                bparser=BooleanParser(ordering)
                self.bdd=(bparser.parse(bfunct)).bdd
            else:
                raise TypeError('expected a BDD or a str, got %s' % (bfunct))

    def variables(self):
        ''' Return the variables in an OBDD.

        :returns: the set of the variables represented in the OBDD
        :rtype: set
        '''
        return self.bdd.variables()

    def __eq__(self,A):
        ''' Check whether two OBDD are the same.

        :param A: either a BDD or an OBDD
        :type A: BDD or OBDD
        :returns: True if the two BDD are the same and respect the same
                  ordering, False otherwise
        :rtype: bool
        '''
        if isinstance(A,BDD):
            return self==OBDD(self.ordering,A)

        if isinstance(A,OBDD):
            return self.bdd is A.bdd and self.ordering==A.ordering

        raise TypeError('expected a BDD, got %s' % (A))

    def __req__(self,A):
        ''' Check whether two OBDD are the same.

        :param A: either a BDD or an OBDD
        :type A: BDD or OBDD
        :returns: True if the two BDD are the same and respect the same
                  ordering, False otherwise
        :rtype: bool
        '''
        return self==A

    def __and__(self,A):
        ''' Build the conjunction of two OBDD.

        :param A: an OBDD
        :type A: OBDD
        :returns: the OBDD that represents the logical conjunction of
                  the two OBDD
        :rtype: OBDD
        '''
        return boolean_function(self,A,(lambda a,b: a and b))

    def __or__(self,A):
        ''' Build the non-exclusive disjunction of two OBDD.

        :param A: an OBDD
        :type A: OBDD
        :returns: the OBDD that represents the logical non-exclusive disjunction
                  of the two OBDD
        :rtype: OBDD
        '''
        return boolean_function(self,A,(lambda a,b: a or b))

    def __xor__(self,A):
        ''' Build the exclusive disjunction of two OBDD.

        :param A: an OBDD
        :type A: OBDD
        :returns: the OBDD that represents the logical exclusive disjunction
                  of the two OBDD
        :rtype: OBDD
        '''
        return boolean_function(self,A,(lambda a,b: a ^ b))

    def __invert__(self):
        ''' Build the negation of an OBDD.

        :param A: an OBDD
        :type A: OBDD
        :returns: the OBDD that represents the logical negation of the OBDD
        :rtype: OBDD
        '''
        return OBDD(self.ordering,~self.bdd)

    def __str__(self):
        ''' Return a string that represents an OBDD

        :returns: a string that represents the OBDD
        :rtype: str
        '''
        return '%s'  %(self.bdd)

    def __repr__(self):
        ''' Return a string that represents an OBDD

        :returns: a string that represents the OBDD
        :rtype: str
        '''
        return '(\'%s\',%s)' % (self.bdd,self.ordering)
