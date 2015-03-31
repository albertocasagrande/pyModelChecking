#!/usr/bin/env python

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

from .ordering import Ordering

def BDDsons_and_BDD(A,B,operator,ordering,result_cache):
    low=boolean_function(A.low,B,operator,ordering,result_cache)
    high=boolean_function(A.high,B,operator,ordering,result_cache)
    return BDD(A.var,low,high)

def BDD_and_BDDsons(A,B,operator,ordering,result_cache):
    low=boolean_function(A,B.low,operator,ordering,result_cache)
    high=boolean_function(A,B.high,operator,ordering,result_cache)
    return BDD(B.var,low,high)

def BDDsons_and_BDDsons(A,B,operator,ordering,result_cache):
    low=boolean_function(A.low,B.low,operator,ordering,result_cache)
    high=boolean_function(A.high,B.high,operator,ordering,result_cache)
    return BDD(A.var,low,high)

def boolean_function(A,B,operator,ordering,result_cache):
    if A not in result_cache:
        result_cache[A]=dict()

    if B in result_cache[A]:
        return result_cache[A][B]

    result_cache[A][B]=boolean_function_compute(A,B,operator,ordering,
                                                            result_cache)

    return result_cache[A][B]

def boolean_function_compute(A,B,operator,ordering,result_cache):
    if isinstance(A,BDD_terminal):
        if isinstance(B,BDD_terminal):
            return BDD(operator(A.value,B.value))

        return BDD_and_BDDsons(A,B,operator,ordering,result_cache)

    if (isinstance(B,BDD_terminal) or
        ordering.in_order(A.var,B.var)):
        return BDDsons_and_BDD(A,B,operator,ordering,result_cache)

    if A.var==B.var:
        return BDDsons_and_BDDsons(A,B,operator,ordering,result_cache)

    if ordering.in_order(B.var,A.var):
        return BDD_and_BDDsons(A,B,operator,ordering,result_cache)

    raise RuntimeError('Unsupported configuration %s %s' % A, B)


class BDD(object):
    Tnodes={}

    def __new__(cls,*data):

        if len(data)==1:
            return BDD_terminal(data[0])

        if len(data)==3:
            return BDD_non_terminal(*data)

        raise RuntimeError(('passed %d parameters, but only ' % (len(data)))+
                            'BDD(value) for terminal node and '+
                            'BDD(var,low,high) for non terminal node '+
                            'have been implemented')

    def __hash__(self):
        return id(self)

    def reset(self):
        self.f_low=set([])
        self.f_high=set([])

    def variables(self):
        return set([node.var for node in self.nodes() if isinstance(node,BDD_non_terminal)])

    def __repr__(self):
        return self.__str__()

def find_isomorph(var,low,high):
    if len(low.f_low)<len(high.f_high):
        node_set=low.f_low
        lh_test=(lambda low,high: high is node.high)
    else:
        node_set=high.f_high
        lh_test=(lambda low,high: low is node.low)

    for node in node_set:
        if (isinstance(node,BDD_non_terminal) and
            var==node.var and lh_test(low,high)):
            return node

    return None


class BDD_non_terminal(BDD):
    def __new__(cls,var,low,high):
        for p in [low,high]:
            if not isinstance(p,BDD):
                raise TypeError('expected an BBD node, got %s'%(p))

        if low is high:
            return low

        node=find_isomorph(var,low,high)
        if node!=None:
            return node

        node=super(BDD,cls).__new__(cls)
        node.reset(var,low,high)

        return node

    def respect_ordering(self,O,checked=None):
        ''' Test whether a BDD respects an Ordering.

        :param O: the ordering to be tested
        :type O: Ordering
        :param checked: already checked nodes
        :type checked: set
        :returns: True if the variable of node is smaller that those of
                  node.low and node.high for any node in the subgraph rooted
                  in self, False otherwise
        :rtype: bool
        '''
        if not isinstance(O,Ordering):
            TypeError('expected an Ordering, got %s'%(O))

        if checked==None:
            checked=set()

        if self in checked:
            return True

        if self.var not in O:
            raise RuntimeError('%s in not in %s' % (self.var,O))

        for fathers in [self.f_low,self.f_high]:
            for father in fathers:
                if O.in_order(self.var,father.var):
                    return False

        if (self.high.respect_ordering(O,checked) and
                self.low.respect_ordering(O,checked)):
            checked.add(self)

            return True
            
        return False

    def reset(self,var,low,high):
        super(BDD_non_terminal,self).reset()

        self.var=var
        self.low=low
        self.high=high

        self.low.f_low.add(self)
        self.high.f_high.add(self)

    def nodes(self,visited=None):
        if visited==None:
            visited=set()

        if self in visited:
            return []

        visited.add(self)

        return ([self]+self.low.nodes(visited)+self.high.nodes(visited))

    def __invert__(self,result_cache=None):
        if result_cache==None:
            result_cache=dict()

        if self in result_cache:
            return result_cache[self]

        result_cache[self]=BDD_non_terminal(self.var,
                                            self.low.__invert__(result_cache),
                                            self.high.__invert__(result_cache))
        return result_cache[self]

    def __eq__(self,O):
        return (isinstance(O,BDD_non_terminal) and
                O.var==self.var and O.low==self.low and O.high==self.high)

    def __str__(self):
        repr=[]

        for succ, neg in [(self.low,'~'),(self.high,'')]:
            if isinstance(succ,BDD_terminal):
                if succ.value:
                    repr.append('%s%s' % (neg,self.var))
            else:
                repr.append('%s%s & %s' % (neg,self.var,succ))

        if len(repr)==2:
            return '(%s) | (%s)' % (repr[0],repr[1])

        return repr[0]

class BDD_terminal(BDD):
    Tnodes={}

    def __new__(cls,value):
        if not isinstance(value,bool):
            raise TypeError('expected a Boolean value, got %s'%(value))

        if value not in BDD_terminal.Tnodes:
            Tnode=super(BDD,cls).__new__(cls)
            Tnode.reset(value)

            BDD_terminal.Tnodes[value]=Tnode

        return BDD_terminal.Tnodes[value]

    def respect_ordering(self,O,checked=None):
        ''' Test whether a BDD respects an Ordering.

        :param O: the ordering to be tested
        :type O: Ordering
        :param checked: already checked nodes
        :type checked: set
        :returns: True
        :rtype: bool
        '''
        return True

    def reset(self,value):
        super(BDD_terminal,self).reset()
        self.value=value

    def __invert__(self,result_cache=None):
        if result_cache==None:
            result_cache=dict()

        if self in result_cache:
            return result_cache[self]

        result_cache[self]=BDD_terminal(not self.value)

        return result_cache[self]

    def nodes(self,visited=None):
        if visited==None:
            visited=set()

        if self in visited:
            return []

        visited.add(self)

        return [self]

    def __eq__(self,O):
        return (isinstance(O,BDD_terminal) and O.value==self.value)

    def __str__(self):
        return '%s' % (self.value)
