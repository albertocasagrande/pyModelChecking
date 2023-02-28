"""
.. module:: kripke
   :synopsis: A module to represent Kripke structures

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""


from .graph import DiGraph
from .graph import compute_SCCs

from .__init__ import __release__


class Kripke(DiGraph):
    r'''
    A class to represent Kripke structures.

    A Kripke structure is a directed graph equipped with a set of initial
    nodes, S0, and a labelling function that maps each node into the set of
    atomic propositions that hold in the node itself. The nodes of Kripke
    structure are called *states*.
    '''

    def __init__(self, S=None, S0=None, R=None, L=None):
        r''' Initialize a new Kripke structure

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
        super(Kripke, self).__init__(S, R)

        if S0 is None:
            self.S0 = set()
        else:
            self.S0 = set(self.nodes()) & set(S0)

        pots = set(self.nodes())-set(self.sources())
        if pots:
            raise RuntimeError('R=\'{}\' '.format(R) +
                               'is supposed be total (see Kripke ' +
                               'definition at ' +
                               'https://pymodelchecking.readthedocs.io/en/' +
                               'v'+__release__ +
                               '/models.html#kripke-structures), ' +
                               'but it does not contains as sources ' +
                               'the nodes {}'.format(pots))

        if L is None:
            L = dict()

        if not isinstance(L, dict):
            raise RuntimeError('L=\'%s\' must be a dictionary' % (L))

        self._labels = dict()
        for state in self.nodes():
            if state in L:
                try:
                    self._labels[state] = set(L[state])
                except Exception:
                    raise RuntimeError(('L=\'{}\' must be a '.format(L)) +
                                       'dictionary that labels each state ' +
                                       'with a set of atomic propositions')
            else:
                self._labels[state] = set()

    def labelling_function(self):
        r''' Return the labelling function

        :returns: the labelling function
        :rtype: dict
        '''
        return self._labels

    def replace_labelling_function(self, L):
        r''' Replace the labelling function

        :param L: a new labelling function for this Kripke structure
        :type L: dict
        :returns: the former labelling function
        :rtype: dict
        '''
        old_L = self._labels

        self._labels = L

        for s in self.states():
            if s not in self._labels:
                self._labels[s] = set()

        return old_L

    def labels(self, state=None):
        r''' Get the atomic propositions

        This method gets the atomic propositions labelling either a
        state or the whole structure.

        :param state: either a state of the Kripke structure or None
        :returns: the atomic propositions that label either a
                  *state*, whenever a parameter *state* is passed, or
                  at least one state of the Kripke structure, otherwise
        :rtype: set
        '''
        if state is not None:
            if state not in self.nodes():
                raise RuntimeError(('state=\'{}\' is '.format(state)) +
                                   'not a state of this Kripke structure')
            return self._labels[state]

        AP = set()
        for ap in self._labels.values():
            AP.update(ap)

        return AP

    def states(self):
        r''' Return the states of a Kripke structure

        :returns: the states of the Kripke structure
        :rtype: set
        '''
        return self.nodes()

    def next(self, src):
        r''' Return the next of a state

        Given a Kripke structure :math:`K=(S,S0,R,L)` and one of its state
        :math:`s`, the *next* of :math:`s` in :math:`K` is the set of all
        those states that are destination of some edges whose source is
        :math:`s` itself i.e., :math:`K.next(s)=\{s' | (s,s') \in R\}`.

        :returns: the set of nodes :math:`\{s' | (s,s') \in R\}`
        :rtype: set
        '''
        try:
            return super(Kripke, self).next(src)
        except Exception:
            raise RuntimeError(('src=\'{}\' is not a state '.format(src)) +
                               'of this Kripke structure')

    def transitions_iter(self):
        r''' Return an interator of the edges of a Kripke structure

        :returns: an interator of the set of edges of the Kripke structure
        :rtype: iterator
        '''
        return self.edges_iter()

    def transitions(self):
        r''' Return the edges of a Kripke structure

        :returns: the set of edges of the Kripke structure
        :rtype: set
        '''
        return self.edges()

    def clone(self):
        r''' Clone a Kripke structure

        :returns: a clone of the current Kripke structure
        :rtype: Kripke
        '''
        L = dict()
        for state, AP in self._labels.items():
            L[state] = set(AP)

        return Kripke(self.states(), self.S0, self.transitions(), L)

    def get_substructure(self, V):
        r''' Return the sub-structure that respects a set of states

        The sub-structure of a Kripke structure :math:`(V',E',L')` that
        respects a set of states :math:`V` is the Kripke structure
        :math:`(V,E,L)` where :math:`E=E'\cap(V \times V)` and
        :math:`L(v)=L'(v)` for all :math:`s \in V`.

        :param V: a set of states
        :type V: set
        :returns: the sub-structure that respects V
        :rtype: Kripke
        '''

        S = V & set(self.states())
        S0 = V & self.S0
        E = [(s, d) for (s, d) in self.transitions_iter() if s in V and d in V]
        L = {s: S for s, S in self._next.items() if s in V}

        return Kripke(S, S0, E, L)

    def get_fair_states(self, F):
        r''' Return a set of states from which leaves a fair path.

        :param F: a container of fairness constraints
        :type F: a container
        :returns: the set of states from which leaves a fair path
        :rtype: set
        '''

        def is_a_fair_SCC(self, scc, F):
            v = next(iter(scc))
            if len(scc) == 1 or v not in self.next(v):
                return False

            for P in F:
                if not set(scc) & P:
                    return False

            return True

        F_set = set()
        for SCC in compute_SCCs(self):
            if is_a_fair_SCC(self, SCC, F):
                F_set.update(SCC)

        R_graph = self.get_reversed_graph()

        return R_graph.get_reachable_set_from(F_set)

    def label_fair_states(self, F):
        r''' Label all the fair states by a new atomic proposition.

        This method labels all the states from which a fair path exists by
        using a new atomic proposition that means "there exists a fair path
        from here". The new label is returned.

        :param F: a container of fairness constraints
        :type F: a container
        :returns: a new label that means "there exists a fair path from here"
        :rtype: str
        '''
        labels = self.labels()
        i = 0
        f_label = 'fair'
        while f_label in labels:
            f_label = 'fair{}'.format(i)
            i += 1

        for s in self.get_fair_states(F):
            self._labels[s].add(f_label)

        return f_label

    def __str__(self):
        r''' Return a string that represents a Kripke structure.

        :returns: a string that represents the Kripke
        :rtype: str
        '''
        return '(S={},S0={},R={},L={})'.format(self.states(),
                                               self.S0,
                                               list(self.transitions()),
                                               self._labels)
