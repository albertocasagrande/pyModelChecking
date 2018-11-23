**************************
Modelling Reactive Systems
**************************

.. _digraph_modelling:

Directed Graphs
===============

:ref:`Directed graphs<digraph>` can be represented in `pyModelChecking` by using
the class :class:`DiGraph` (see :ref:`Graph API<graph_api>`).

.. code-block:: Python

    >>> from pyModelChecking import *
    >>> G = DiGraph(V=['a',3],
    ...             E=[('a','a'), ('a','b')])
    >>> print(G)

    (V=['a', 3, 'b'], E=[('a', 'a'), ('a', 'b')])

    >>> G.nodes()

    ['a', 3, 'b']

    >>> G.edges()

    [('a','a'), ('a','b')]

    >>> G.add_edge('c','b')
    >>> G.nodes()

    ['a', 'c', 3, 'b']

    >>> G.edges()

    [('a', 'a'), ('a', 'b'), ('c', 'b')]


The same class provides methods to compute **reachable sets**,
**reversed graphs** and **subgraphs** of a given directed graph.

.. code-block:: Python

    >>> print(G.get_reversed_graph())

    (V=['a', 'c', 3, 'b'], E=[('a', 'a'), ('b', 'a'), ('b', 'c')])

    >>> print(G.get_subgraph(['a','b',3]))

    (V=['a', 3, 'b'], E=[('a', 'a'), ('a', 'b')])

    >>> print(G.get_reachable_set_from(['a', 3]))

    set(['a', 3, 'b'])

    >>> print(G.get_reachable_set_from(['d']))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "pyModelChecking/graph.py", line 203, in get_reachable_set_from
        for d in self.next(s):
      File "pyModelChecking/graph.py", line 120, in next
        'of this DiGraph')
    RuntimeError: src = 'd' is not a node of this DiGraph

`pyModelChecking` can also compute the strongly connected components of a
directed graph.

.. code-block:: Python

    >>> G.add_edge('b','a')
    >>> print(list(compute_strongly_connected_components(G)))
    [['a', 'b'], ['c'], [3]]


Refer to :ref:`Graph API<graph_api>` for more details.

Kripke Structures
=================

:ref:`Kripke structures<kripke_structure>` are representable by using the class
:class:`Kripke` (see :ref:`Kripke API<kripke_api>`).

.. code-block:: Python

    >>> from pyModelChecking import *
    >>> K = Kripke(S=[0, 1, 3],
    ...            R=[(0, 2), (2, 2), (0, 1), (1, 0), (3, 2)],
    ...            L={1: ['p', 'q'], 2: ['p', 'q'], 3: ['q']})
    >>> print(K)

    (S=[0, 1, 2, 3],S0=set([]),R=[(0, 1), (0, 2), (1, 0), (2, 2), (3, 2)],L={0: set([]), 1: set(['q', 'p']), 2: set(['q', 'p']), 3: set(['q'])})

The sets of Kripke's states and transitions can be obtained by using the
following syntax:

.. code-block:: Python

    >>> K.states()

    [0, 1, 2, 3]

    >>> K.transitions()

    [(0, 1), (0, 2), (1, 0), (2, 2), (3, 2)]

It is possible to get the successors of a given state with respect to the Kripke's transitions:

.. code-block:: Python

    >>> K.next(0)

    set([1, 2])

Finally, the API provides a method for getting the labels of Kripke's states.

.. code-block:: Python

    >>> K.labels()

    set(['q', 'p'])

    >>> K.labels(3)

    set(['q'])
