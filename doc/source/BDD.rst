Symbolic Representation
***********************

:ref:`Binary Decision Diagrams<BDD>` (BDDs) and
:ref:`Ordered Binary Decision Diagrams<OBDD>` (OBDDs)
are data structures to represent binary functions [Bryant86]_.

.. _BDD:

Binary Decision Diagrams
========================

BDDs are :ref:`directed graphs<digraph>` whose nodes can be either **terminal** or **non-terminal**.
Terminal nodes are labelled by a *binary value* and they are not source of any
edge. If :math:`t` is a terminal node, we write :math:`t.value` to denote the value of :math:`t`.
Non-terminal nodes are labelled by a *variable* name and they
are source of two edges called *low* and *high*. If :math:`n` is a non-terminal
node, we write :math:`n.var`, :math:`n.low`, and :math:`n.high` to denote the variable name,
the edge low, and the edge high of the node :math:`n`.

Any terminal node :math:`t` represents the binary function :math:`t.value`, while
any non-terminal node :math:`n` encodes the binary function
:math:`(\tilde{}n.var \& f_l) | (n.var \& f_h)` where :math:`f_l` and :math:`f_h` are the binary
functions associated to :math:`n.low` and :math:`n.high`, respectively.

A BDD **respects a variable ordering** :math:`<` whenever :math:`n.var < n.low.var`
for all non-terminal nodes :math:`n` and :math:`n.low` and :math:`n.var < n.high.var`
for all non-terminal nodes :math:`n` and :math:`n.high`.

.. _OBDD:

Ordered Binary Decision Diagrams
================================

The logical equivalence of two binary functions can be reduced to the
existence of an isomorphism between the BDD encoding them under three conditions:

1. the two BDDs respect the same variable ordering;
2. :math:`n.low` and :math:`n.high` are different nodes for any non-terminal node :math:`n` in
   both the BDDs;
3. for each of the BDDs and for all pairs of nodes in it, there is no
   isomophism between them.

OBDDs are BDDs equipped of a variable ordering and satisfying condition 2. and 3.

Whenever two binary functions :math:`f_1` and :math:`f_2` are stored as OBDD and they share
the same variable ordering, it is possible to:

* test logical equivalence between :math:`f_1` and :math:`f_2` in time :math:`O(1)`;
* compute the OBDD that represents:

  - the bitwise negation of the formula :math:`f_1` in time :math:`O(|f_1|)`;
  - the bitwise binary combinations of the functions :math:`f_1` and :math:`f_2` in time
    :math:`O(|f_1|+|f_2|)`.

.. [Bryant86] Randal E. Bryant. "Graph-Based Algorithms for Boolean Function
   Manipulation". IEEE Transactions on Computers, C-35(8):677–691, 1986.
