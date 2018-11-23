
.. _model_checking:

**************
Model Checking
**************

Model checking is a technique to establish the set of states in Kripke
structure that satisfy a given temporal formula. More formally, provided
a Kripke structure :math:`K=(S,S_0,R,L)` and a temporal formula
:math:`\varphi`, model checking aims to identify
:math:`S' \subseteq S` such that

.. math::

   K,s_i \models \varphi

for all :math:`s_i \in S'`.

Model checking problem for :ref:`CTL*<CTLS>`, :ref:`CTL<CTL>` and
:ref:`LTL<LTL>` is decidable even though the time complexity of the
algorithm is logics dependent: the complexities of the :ref:`CTL<CTL>`,
:ref:`LTL<LTL>` and :ref:`CTL*<CTLS>` decision
procedures are :math:`O(|\varphi| * (|S|+|R|))`,
:math:`O(2^{O(|\varphi|)} * (|S|+|R|))` and
:math:`O(2^{O(|\varphi|)} * (|S|+|R|))`, respectively.

Fair Model Checking
===================

A *fair Kripke structure* is a Kripke structure :math:`(S, S_0, R, L)`
added with a set of *fair states* :math:`F \subseteq S`. A *fair path*
for it is an infinite path that passes through all the fair states infinitely
often.

*Fair model checking* only considers fair paths.
A *fair state* is a path from which at least one fair path originates.
