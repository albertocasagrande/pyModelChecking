#!/usr/bin/env python

'''
.. _kripke:

Kripke Structures
=================

A **Kripke structure** is a :ref:`total directed graph<total_digraph>`
equipped with a set of initial nodes and a labelling function that maps each
node into the set of atomic propositions that hold in the node itself.
The nodes of Kripke structure are called *states*.

Kripke structure
  A Kripke structure is a tuple :math:`(S,S_0,R,L)` such that:

  - :math:`S` is a finite set of states
  - :math:`S_0\\subseteq S` is a set of *initial states*
  - :math:`R\\subseteq S\\times S` is a set of *transitions* such that
    for all :math:`s \in S` there exists a :math:`(s,s') \in R` for some
    :math:`s' \in S`
  - :math:`L:S \\rightarrow AP` maps each state into a set of
    *atomic propositions*

'''

from .graph import DiGraph
from .graph import compute_strongly_connected_components

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

    A Kripke structure is a directed graph equipped with a set of initial
    nodes, S0, and a labelling function that maps each node into the set of
    atomic propositions that hold in the node itself. The nodes of Kripke
    structure are called *states*.
    '''

    def __init__(self,S=None,S0=None, R=None,L=None):
        ''' Initialize a new Kripke structure

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
            self.S0=set(self.nodes())&set(S0)

        pots=set(self.nodes())-set(self.sources())
        if pots:
            raise RuntimeError(('R=\'%s\' must be total, while it ' % (R))+
                                ('does not contains the states %s' % (pots)))

        if L==None:
            L=dict()

        if not isinstance(L,dict):
            raise RuntimeError('L=\'%s\' must be a dictionary' % (L))

        self._labels=dict()
        for state in self.nodes():
            if state in L:
                try:
                    self._labels[state]=set(L[state])
                except:
                    raise RuntimeError(('L=\'%s\' must be a ' % (L)) +
                                        'dictionary that labels each state '+
                                        'with a set of atomic propositions' )
            else:
                self._labels[state]=set()

    def labelling_function(self):
        ''' Return the labelling function

        :returns: the labelling function
        :rtype: dict
        '''
        return self._labels

    def replace_labelling_function(self,L):
        ''' Replace the labelling function

        :param L: a new labelling function for this Kripke structure
        :type L: dict
        :returns: the former labelling function
        :rtype: dict
        '''
        old_L=self._labels

        self._labels=L

        for s in self.states():
            if s not in self._labels:
                self._labels[s]=set()

        return old_L

    def labels(self, state=None):
        ''' Get the atomic propositions labelling either a state or the whole structure

        :param state: either a state of the Kripke structure or None
        :returns: the atomic propositions that label either:
        1. *state*, whenever a parameter *state* is passed
        2. at least one state of the Kripke structure, otherwise
        :rtype: set
        '''
        if state!=None:
            if state not in self.nodes():
                raise RuntimeError(('state=\'%s\' is not a state ' % (state))+
                                    'of this Kripke structure')
            return self._labels[state]

        AP=set()
        for ap in self._labels.values():
            AP.update(ap)

        return AP

    def states(self):
        ''' Return the states of a Kripke structure

        :returns: the states of the Kripke structure
        :rtype: set
        '''
        return self.nodes()

    def next(self,src):
        ''' Return the next of a state

        Given a Kripke structure K=(S,S0,R,L) and one of its state s, the *next*
        of s in K is the set of all thos states that are destination of
        some edges whose source is s itself i.e., K.next(s)={s' | (s,s') in R}.

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

        :returns: the set of edges of the Kripke structure
        :rtype: set
        '''
        return self.edges()

    def copy(self):
        ''' Copy a Kripke structure

        :returns: a copy of the Kripke structure
        :rtype: Kripke
        '''
        L=dict()
        for state, AP in self._labels.items():
            L[state]=set(AP)

        return Kripke(self.states(),self.S0,self.transitions(),L)

    def get_substructure(self,V):
        ''' Return the sub-structure that respects a set of states

        The sub-structure of a Kripke structure :math:`(V',E',L')` that
        respects a set of states :math:`V` is the Kripke structure
        :math:`(V,E,L)` where :math:`E=E'\cap(V \times V)` and
        :math:`L(v)=L'(v)` for all :math:`s in V`.

        :param V: a set of states
        :type V: set
        :returns: the sub-structure that respects :param:`V`
        :rtype: Kripke
        '''

        S=V&set(self.states())
        S0=V&self.S0
        E=[(s,d) for (s,d) in self.transitions() if s in V and d in V]
        L={s:S for s, S in self._next.items() if s in V }

        return Kripke(S,S0,E,L)

    def get_fair_states(self,F):
        ''' Return a set of states from which leaves a fair path.

        :param F: a container of fairness constraints
        :type F: a container
        :returns: the set of states from which leaves a fair path
        :rtype: set
        '''

        def is_a_fair_SCC(self,scc,F):
            v = next(iter(scc))
            if len(scc)==1 or v not in self.next(v):
                return False

            for P in F:
                if not set(scc)&P:
                    return False

            return True

        F_set=set()
        for SCC in compute_strongly_connected_components(self):
            if is_a_fair_SCC(self,SCC,F):
                F_set.update(SCC)

        R_graph=self.get_reversed_graph()

        return R_graph.get_reachable_set_from(F_set)

    def label_fair_states(self,F):
        ''' Label all the fair states by a new atomic proposition.

        This method labels all the states from which a fair path exists by using
        a new atomic proposition that means "there exists a fair path from
        here". The new label is returned.
        :returns: a new label that means "there exists a fair path from here"
        :rtype: str
        '''
        labels=self.labels()
        i=0
        f_label='fair'
        while f_label in labels:
            f_label='fair%d' % (i)
            i+=1

        for s in self.get_fair_states(F):
            self._labels[s].add(f_label)

        return f_label

    def __str__(self):
        ''' Return a string that represents a Kripke structure.

        :returns: a string that represents the Kripke
        :rtype: str
        '''
        return '(S=%s,S0=%s,R=%s,L=%s)' % (self.states(),self.S0,self.transitions(),self._labels)
