#!/usr/bin/env python

from graph import DiGraph

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

class Kripke(DiGraph):
    '''
    A class to represent Kripke structures.

    A Kripke structure is a directed graph equipped with a set of initial nodes,
    S0, and a labelling function that maps each node in the set of atomic
    propositions that hold in the node itself. The nodes of Kripke structure
    are called *states*.
    '''

    def __init__(self,S=None,S0=None, R=None,L=None):
        ''' Initialize a new Kripke structure

        :param self: the Kripke object that should be initializated
        :type self: Kripke
        :param S: a collection of states
        :type S: a collection
        :param S0: a collection of initial states
        :type S0: a collection
        :param R: a collection of edges
        :type R: a collection
        :param L: a labelling function that maps each state in the set of
                    atomic propositions that hold in the state itself.
        :type L: dict
        '''
        super(Kripke,self).__init__(S,R)

        if S0==None:
            self.S0=set()
        else:
            self.S0=set(self._nodes)&set(S0) #set(super(Kripke,self)._nodes)&set(S0)

        pots=self._nodes-set(self._next.keys())
        if len(pots)>0:
            raise RuntimeError(('R=\'%s\' must be total, while it ' % (R))+
                                ('does not contains the states %s' % (pots)))

        if L==None:
            L=dict()

        if not isinstance(L,dict):
            raise RuntimeError('L=\'%s\' must be a dictionary' % (L))

        self._labels=dict()
        for state in self._nodes:
            if state in L:
                try:
                    self._labels[state]=set(L[state])
                except:
                    raise RuntimeError(('L=\'%s\' must be a ' % (L)) +
                                        'dictionary that labels each state '+
                                        'with a set of atomic propositions' )
            else:
                self._labels[state]=set()

    def labels(self, state=None):
        ''' Get the atomic propositions labelling either a state or the whole structure

        :param self: the Kripke object
        :type self: Kripke
        :param state: either a state of the Kripke structure or None
        :returns: the atomic propositions that label either:
        1. *state*, whenever a parameter *state* is passed
        2. at least one state of the Kripke structure, otherwise
        :rtype: set
        '''
        if state!=None:
            if state not in self._nodes:
                raise RuntimeError(('state=\'%s\' is not a state ' % (state))+
                                    'of this Kripke structure')
            return self._labels[state]

        AP=set()
        for ap in self._labels.values():
            AP.update(ap)

        return AP

    def states(self):
        ''' Return the states of a Kripke structure

        :param self: the Kripke object
        :type self: Kripke
        :returns: the states of the Kripke structure
        :rtype: set
        '''
        return self.nodes()

    def next(self,src):
        ''' Return the next of a state

        Given a Kripke structure K=(S,S0,R,L) and one of its state s, the *next*
        of s in K is the set of all thos states that are destination of
        some edges whose source is s itself i.e., K.next(s)={s' | (s,s') in R}.
        :param self: the Kripke object
        :type self: Kripke
        :returns: the set of nodes {s' | (s,s') in R}
        :rtype: set
        '''
        try:
            return super(Kripke,self).next(src)
        except:
            raise RuntimeError(('src=\'%s\' is not a state ' % (src))+
                                'of this Kripke structure' )

    def transitions(self):
        ''' Return the edges of a Kripke structure

        :param self: the Kripke object
        :type self: Kripke
        :returns: the set of edges of the Kripke structure
        :rtype: set
        '''
        return self.edges()

    def copy(self):
        ''' Copy a Kripke structure

        :param self: the Kripke object
        :type self: Kripke
        :returns: a copy of the Kripke structure
        :rtype: Kripke
        '''
        L=dict()
        for state, AP in self._labels.items():
            L[state]=set(AP)

        return Kripke(self.states(),self.S0,self.transitions,L)

    def __str__(self):
        ''' Return a string that represents a Kripke structure

        :param self: the Kripke object
        :type self: Kripke
        :returns: a string that represents the Kripke
        :rtype: str
        '''
        return '(S=%s,S0=%s,R=%s,L=%s)' % (self.states(),self.S0,self.transitions(),self._labels)


if __name__=='__main__':
#    K=Kripke(S=['a','b','c'],
#             R=[('a','c'),('c','c'),('a','b')],
#             L={'a': set(['p','q'])})

    K=Kripke(S=['a','b','c'],
             R=[('a','c'),('c','c'),('a','b'),('b','a')],
             L={'a': set(['p','q'])})

    print(K)
