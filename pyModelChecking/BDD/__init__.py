'''
This module represents the OBDD.

Binary Decision Diagrams (BDDs) and Ordered Binary Decision Diagrams (OBDDs)
are data structures to represent binary functions [Bryant86]_.

## Binary Decision Diagrams

BDD nodes can be either **terminal** or **non-terminal** nodes.
Terminal nodes are labelled by a *binary value* and they are not source of any
edge. If `t` is a terminal node, we write `t.value` to denote the value of `t`.
Non-terminal nodes are labelled by a *variable* name and they
are source of two edges called *low* and *high*. If `n` is a non-terminal
node, we write `n.var`, `n.low`, and `n.high` to denote the variable name,
the edge low, and the edge high of the node `n`.

Any terminal node `t` represents the binary function `t.value`, while
any non-terminal node `n` encodes the binary function
`(~n.var & f_l) | (n.var & f_h)` where `f_l` and `f_h` are the binary
functions associated to `n.low` and `n.high`, respectively.

A BDD **respects a variable ordering <** whenever `n.var` < `n.low.var`
for all non-terminal nodes `n` and `n.low` and `n.var` < `n.high.var`
for all non-terminal nodes `n` and `n.high`.

## Ordered Binary Decision Diagrams

The logical equivalence of two binary functions can be reduced to the
existence of an isomorphism between the BDD encoding them under three conditions:

1. the two BDDs respect the same variable ordering;
2. `n.low` and `n.high` are different nodes for any non-terminal node `n` in
   both the BDDs;
3. for each of the BDDs and for all pairs of nodes in it, there is no
   isomophism between them.

OBDDs are BDDs equipped of a variable ordering and satisfying condition 2. and 3.

Whenever two binary functions `f_1` and `f_2` are stored as OBDD and they share
the same variable ordering, it is possible to:
* test logical equivalence between `f_1` and `f_2` in time O(1);
* compute the OBDD that represents:
  * the bitwise negation of the formula `f_1` in time O(|f_1|);
  * the bitwise binary combinations of the functions `f_1` and `f_2` in time O(|f_1|+|f_2|).

.. [Bryant86] Randal E. Bryant. "Graph-Based Algorithms for Boolean Function Manipulation".
              IEEE Transactions on Computers, C-35(8):677–691, 1986.

[digraph]: https://en.wikipedia.org/wiki/Directed_graph
'''


from .BDD import BDDNode
from .ordering import Ordering
from .OBDD import OBDD
#from .OBDD import BooleanParser
