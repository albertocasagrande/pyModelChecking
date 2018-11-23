Reactive Systems
****************

**Reactive systems** are systems that interact with their environment and
evolve over an infinite time horizon. This chapter presents a natural model
for them: Kripke structure.

.. _digraph:

Directed Graphs
===============

A **directed graph**, or **graph**, is pair :math:`(V,E)` where:

- :math:`V` is a finite set of *nodes*
- :math:`E \subseteq V \times V` is a set of *edges*

If :math:`(s,d) \in E`, then :math:`s` and :math:`d` are the *source* and the
*destination* of :math:`(s,d)`, respectively. The edge :math:`(s,d) \in E` is
said to *go from :math:`s` to :math:`d`*. If :math:`e \in E` goes either
from :math:`s` to :math:`d` or from :math:`d` to :math:`s`, then :math:`e`
is an edge **between** :math:`d` and :math:`s`. By extension,
an edge :math:`e \in E` goes from :math:`V_1 \subseteq S` to
:math:`V_2 \subseteq S` if there exists a pair of nodes
:math:`(v_1,v_2) \in V_1 \times V_2` such that :math:`(v_1,v_2) \in E`.
Analogously, :math:`e \in E` is between :math:`V_1` and :math:`V_2` if
it is either from :math:`V_1` to :math:`V_2` or from :math:`V_2` to :math:`V_1`.

The **reversed graph** of a graph :math:`(V,E)` is the graph :math:`(V,E')`
where :math:`E'={(d,s) | (s,d) \in E}`.

.. _subgraph:

A **subgraph** of a graph :math:`(V,E)` is a graph :math:`(V',E')` such that
:math:`V' \subseteq V` and :math:`E' \subseteq E \cap (V' \times V')`.
A subgraph :math:`(V',E')` of :math:`(V,E)` is a **proper subgraph** if
either :math:`V'\subsetneq V` or :math:`E'\subsetneq E`. A subgraph
:math:`G` of :math:`(V,E)` **respects** a set of nodes :math:`V' \subseteq V`
if :math:`G=(V',E \cap (V' \times V'))`.

.. _path:

A sequence, either finite or infinite, :math:`\pi=v_0 v_1 \ldots` is a **path**
for the graph :math:`(V,E)` if :math:`(v_i,v_{i+1}) \in E` for all :math:`v_i`
and :math:`v_{i+1}` in :math:`\pi`. The *lenght of a path* :math:`\pi`,
denoted by :math:`|\pi|`, is the size of the sequence.

It is easy to see that if :math:`\pi=v_0 \ldots v_n` and
:math:`\pi'=w_0 \ldots` are two paths for :math:`(V,E)` such that
:math:`(v_n,w_0) \in E`, then
:math:`\pi\cdot\pi'=v_0 \ldots v_n w_0 \ldots` is path for :math:`(V,E)`.

Let :math:`\pi`, :math:`\pi'`, and :math:`\pi''` be three paths such that
:math:`\pi=\pi'\cdot\pi''`. Then, :math:`\pi'` is a **prefix** of :math:`\pi`
and :math:`\pi''` is a **suffix** of :math:`\pi`.
We write :math:`\pi_i` to denote the suffix of :math:`\pi` for which
:math:`\pi=\pi' \cdot \pi_i` and :math:`|\pi'|=i` for some :math:`\pi'`.

If :math:`v_0 v_1 \ldots v_n` is a prefix for some path :math:`\pi` of
a graph :math:`(V,E)`, then we say that either
:math:`\pi` *starts* from :math:`v_0` and **reaches** :math:`v_n` or,
equivantely, :math:`v_n` is **reachable** from :math:`v_0` in
:math:`(V,E)`.

.. _scc:

Every :ref:`subgraph<subgraph>` :math:`(V',E')` of :math:`G` such that:

1. :math:`v` is reachable from :math:`v'` for all pairs :math:`v,v' \in V'` and
2. is not proper subgraph of any subgraph of :math:`G` that satisfies 1.

is a **strongly connected component** of :math:`G`. It is easy to see that the
the sets of nodes of each strongly connected component of a graph :math:`(V,E)`
is a partition of :math:`V`. A strongly connected component :math:`(V',E')`
is **trivial** if :math:`|V'|=1` and :math:`|E'|=0`.

.. _dag_tree:

---------------------------------
Directed Acyclic Graphs and Trees
---------------------------------

A **directed acyclic graph** or **DAG** is a directed graph whose
strongly connected components are all trivial.

A graph :math:`(V,E)` is **disconnected** if there exists a
:math:`V' \subseteq V` such that there are no edges between :math:`V'` and
:math:`V\setminus V'`. If a graph is not disconnected, then is **connected**.

A **directed tree** is a connected DAG :math:`(V,E)` whose subgraphs of the form
:math:`(V,E')`, where :math:`E' \subsetneq E`, are disconnected.

.. _kripke_structure:

Kripke Structures
=================

A **Kripke structure** is a :ref:`directed graph<digraph>`,
equipped with a set of initial nodes,
such that every node is source of some edge and it is labeled by a
set of *atomic propositions* [CGP00]_.
The nodes of Kripke structure are called *states*.

A Kripke structure is a tuple :math:`(S,S_0,R,L)` such that:

- :math:`S` is a finite set of states
- :math:`S_0\subseteq S` is a set of *initial states*
- :math:`R\subseteq S\times S` is a set of *transitions* such that
  for all :math:`s \in S` there exists a :math:`(s,s') \in R` for some
  :math:`s' \in S`
- :math:`L:S \rightarrow AP` maps each state into a set of
  atomic propositions

Sometime, the set of initial states is omitted. In such cases, :math:`S` and
:math:`S_0` coincide.

A **computation** of a Kripke structure :math:`(S,S_0,R,L)` is an infinite
path of :math:`(S,R)` that starts from some :math:`s \in S_0`.
