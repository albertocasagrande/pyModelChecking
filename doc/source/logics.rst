***************
Temporal Logics
***************

.. _CTLS:

Computational Tree Logic*
=========================

The **Computational Tree Language**\ * or **CTL**\ * is a the temporal logic
that describes the properties of computation trees over Kripke structures
([CE81]_, [CES86]_). Beside a set of atomic propostions and the standard
logical operators :math:`\neg`, :math:`\land`, :math:`\lor`, and
:math:`\rightarrow`, the alphabet of CTL* contains the two path quantifiers
:math:`\mathbf{A}` ("for all paths") and :math:`\mathbf{E}` ("for some path") and the five
temporal operators :math:`\mathbf{X}` ("at the next step"), :math:`\mathbf{G}` ("globally"),
:math:`F` ("in the future"), :math:`\mathbf{U}` ("until"), and :math:`\mathbf{R}` ("release").

------
Syntax
------

Any CTL* formula is either a *state formula* (i.e., a formula that are
evaluated in a single state) or a *path formula* (i.e., a formula whose
truth value depend on an infinite path).

A CTL* state formula is either:

- :math:`\top` or :math:`\bot`
- an atomic proposition
- :math:`\neg\varphi_1`, :math:`\varphi_1 \land \varphi_2`,
  :math:`\varphi_1 \lor \varphi_2`, or
  :math:`\varphi_1 \rightarrow \varphi_2` where both :math:`\varphi_1` and
  :math:`\varphi_2` are CTL* state formulas
- :math:`\mathbf{A} \psi` or :math:`\mathbf{E} \psi` where :math:`\psi` is a CTL* path
  formula

A CTL* path formula is either:

- a state formula
- :math:`\neg\psi_1`, :math:`\psi_1 \land \psi_2`, :math:`\psi_1 \lor \psi_2`,
  or :math:`\psi_1 \rightarrow \psi_2` where both :math:`\psi_1` and
  :math:`\psi_2` are CTL* path formulas
- :math:`\mathbf{X} \psi_1`, :math:`\mathbf{F} \psi_1`, :math:`\mathbf{G} \psi_1`,
  :math:`\psi_1 \mathbf{U} \psi_2`, or
  :math:`\psi_1 \mathbf{R} \psi_2` where both :math:`\psi_1` and :math:`\psi_2`
  are CTL* path formulas

.. _CTLS_semantics:

---------
Semantics
---------
The semantics of CTL* formulas are given with respect to a
:ref:`Kripke structure<kripke_structure>`. If :math:`K` is a Kripke structure,
:math:`s` one of its states, and :math:`\varphi` a state formula,
we write :math:`K,s \models \varphi` (to be read ":math:`K` and :math:`s`
satisfy :math:`\varphi`") meaning that :math:`\varphi` holds at state
:math:`s` in :math:`K`. Analogously, If :math:`K` is a Kripke structure,
:math:`\pi` one of its computations, and :math:`\psi` a path formula,
we write :math:`K,\pi \models \psi` meaning that :math:`\psi` holds
along :math:`\pi` in :math:`K`.

Let :math:`K` be the Kripke structure :math:`(S,S_0,R,L)`;
the relation :math:`\models` is defined recursively as follows:

- :math:`K,s \models \top` and :math:`K,s \not\models \bot` for any state
  :math:`s \in S`
- if :math:`p \in AP`, then :math:`K,s \models p`
  :math:`\Longleftrightarrow` :math:`p \in L(s)`
- :math:`K,s \models \neg\varphi`
  :math:`\Longleftrightarrow` :math:`K,s \not\models \varphi`
- :math:`K,s \models \varphi_1 \land \varphi_2` :math:`\Longleftrightarrow`
  :math:`K,s \models \varphi_1` and :math:`K,s \models \varphi_2`
- :math:`K,s \models \varphi_1 \lor \varphi_2` :math:`\Longleftrightarrow`
  :math:`K,s \models \varphi_1` or :math:`K,s \models \varphi_2`
- :math:`K,s \models \varphi_1 \rightarrow \varphi_2`
  :math:`\Longleftrightarrow`
  :math:`K,s \not\models \varphi_1` or :math:`K,s \models \varphi_2`
- :math:`K,s \models \mathbf{A} \varphi`
  :math:`\Longleftrightarrow` :math:`K,\pi \models \varphi`
  for any computation :math:`\pi` of :math:`K` that starts from :math:`s`
- :math:`K,s \models \mathbf{E} \varphi`
  :math:`\Longleftrightarrow` :math:`K,\pi \models \varphi`
  for some computation :math:`\pi` of :math:`K` that starts
  from :math:`s`
- :math:`K,\pi \models \psi`
  :math:`\Longleftrightarrow` :math:`K,s \models \psi`, where
  :math:`\pi` is a computation of :math:`K` that starts from :math:`s`
- :math:`K,\pi \models \neg\psi`
  :math:`\Longleftrightarrow` :math:`K,\pi \not\models \psi`
- :math:`K,\pi \models \psi_1 \land \psi_2` :math:`\Longleftrightarrow`
  :math:`K,\pi \models \psi_1` and :math:`K,\pi \models \psi_2`
- :math:`K,\pi \models \psi_1 \lor \psi_2` :math:`\Longleftrightarrow`
  :math:`K,\pi \models \psi_1` or :math:`K,\pi \models \psi_2`
- :math:`K,\pi \models \psi_1 \rightarrow \psi_2` :math:`\Longleftrightarrow`
  :math:`K,\pi \not\models \psi_1` or :math:`K,\pi \models \psi_2`
- :math:`K,\pi \models \mathbf{X} \psi`
  :math:`\Longleftrightarrow` :math:`K,\pi_1 \models \psi`
- :math:`K,\pi \models \mathbf{F} \psi`
  :math:`\Longleftrightarrow` :math:`K,\pi_i \models \psi`
  for some :math:`i \in \mathbb{N}`
- :math:`K,\pi \models \mathbf{G} \psi` :math:`\Longleftrightarrow`
  :math:`K,\pi_i \models \psi` for all :math:`i \in \mathbb{N}`
- :math:`K,\pi \models \psi_1 \mathbf{U} \psi_2`
  :math:`\Longleftrightarrow` there exists an
  :math:`i \in \mathbb{N}` such that :math:`K,\pi_i \models \psi_2`
  and :math:`K,\pi_j \models \psi_1` for all :math:`j \in [0,i-1]`
- :math:`K,\pi \models \psi_1 \mathbf{R} \psi_2` :math:`\Longleftrightarrow` for all
  :math:`i \in \mathbb{N}`, if :math:`K,\pi_j \not\models \psi_1`
  for all :math:`j \in [0,i-1]`, then :math:`K,\pi_i \models \psi_2`


Whenever :math:`K,\sigma \models \psi` :math:`\Longleftrightarrow`
:math:`K,\sigma \models \varphi` for any :math:`\sigma` and
and any :math:`K`, we say that :math:`\psi` and
:math:`\varphi` are **equivalent** and we write
:math:`\varphi \equiv \psi`.

Two set of formulas :math:`\mathcal{F}` and
and any :math:`\mathbf{G}` are **equivalent** if
any formula :math:`\mathbf{G}` has an equivalent formula
in :math:`\mathcal{F}` and vice versa.

-----------------
Restricted Syntax
-----------------

It is easy to prove that :math:`\bot`, :math:`\mathbf{F} \psi`, :math:`\mathbf{G} \psi`,
:math:`\varphi \mathbf{R} \psi`, :math:`\mathbf{A} \varphi`, :math:`\varphi \land \psi`,
and :math:`\varphi \rightarrow \psi` are equivalent to
:math:`\neg \top`, :math:`\top \mathbf{U} \psi`, :math:`\neg (\top \mathbf{U} \neg \psi)`,
:math:`\neg (\neg \varphi \mathbf{U} \neg \psi)`, :math:`\neg \mathbf{E} \neg \varphi`,
:math:`\neg (\varphi \lor \psi)`, and :math:`\neg \varphi \lor \psi`,
respectively. Thus, the CTL* language whose alphabet is restricted to
:math:`\neg`, :math:`\lor`, :math:`\mathbf{X}`, :math:`\mathbf{U}`, :math:`\mathbf{A}`, :math:`\top`,
and atomic propositions is equivalent to the full CTL* language
(e.g., see [CGP00]_).

.. _CTL:

Computational Tree Logic
========================

The **Computational Tree Language** or **CTL** is a subset of :ref:`CTL*<CTLS>`
([BMP83]_, [CE81]_, [CE80]_). In CTL, each occurence of the
two path quantifiers :math:`\mathbf{A}` and :math:`\mathbf{E}` should be
coupled to one of the temporal
operators :math:`\mathbf{X}`, :math:`\mathbf{G}`, :math:`\mathbf{F}`, :math:`\mathbf{U}`, or :math:`\mathbf{U}`.

------
Syntax
------

More formally, a CTL state formula is either:

- :math:`\top` or :math:`\bot`
- an atomic proposition
- :math:`\neg \varphi_1`, :math:`\varphi_1 \land \varphi_2`,
  :math:`\varphi_1 \lor \varphi_2`, or :math:`\varphi_1 \rightarrow \varphi_2`,
  where both :math:`\varphi_1` and :math:`\varphi_2` are CTL state formulas
- :math:`\mathbf{A} \psi` or :math:`\mathbf{E} \psi` where :math:`\varphi` is a CTL path
  formula

A CTL path formula is either :math:`\mathbf{X} \varphi_1`,
:math:`\mathbf{F} \varphi_1`,
:math:`\mathbf{G} \varphi_1`, :math:`\varphi_1 \mathbf{U} \varphi_2`, or
:math:`\varphi_1 \mathbf{R} \varphi_2` where both :math:`\varphi_1` and
:math:`\varphi_2` are CTL state formulas.

---------
Semantics
---------
CTL has the same :ref:`semantics of CTL*<CTLS_semantics>`.

-----------------
Restricted Syntax
-----------------

Despite the apperent syntatic complexity of CTL, any possible property
definable in it can be expressed by a CTL formula whose syntax is restricted
to the use of :math:`\top`, :math:`\neg`, :math:`\lor`, and :math:`\mathbf{E}` coupled to
either :math:`\mathbf{X}`, :math:`\mathbf{U}`, or :math:`\mathbf{G}` (e.g., see [CGP00]_).
As a matter of the facts, it is easy to prove that:

- :math:`\bot \equiv \neg \top`
- :math:`\varphi_1 \land \varphi_2 \equiv \neg (\neg \varphi_1 \lor \neg \varphi_2)`
- :math:`\varphi_1 \rightarrow \varphi_2 \equiv \neg \varphi_1 \lor \varphi_2`
- :math:`\mathbf{A}\mathbf{X} \varphi \equiv \neg \mathbf{E}\mathbf{X} (\neg \varphi)`
- :math:`\mathbf{E}F \varphi \equiv \mathbf{E}(\top \mathbf{U} \varphi)`
- :math:`\mathbf{A}\mathbf{G} \varphi \equiv \neg \mathbf{E}(\top \mathbf{U} \neg \varphi)`
- :math:`\mathbf{A}F \varphi \equiv \neg \mathbf{E}\mathbf{G} (\neg \varphi)`
- :math:`\mathbf{A}(\varphi_1 \mathbf{U} \varphi_2) \equiv \neg (\mathbf{E} ((\neg \varphi_2) \mathbf{U} \neg (\varphi_1 \lor \varphi_2) ) \lor \mathbf{E}\mathbf{G}(\neg \varphi_2))`
- :math:`\mathbf{A}(\varphi_1 \mathbf{R} \varphi_2) \equiv \neg \mathbf{E} ((\neg \varphi_1) \mathbf{U} (\neg \varphi_2))`
- :math:`\mathbf{E}(\varphi_1 \mathbf{R} \varphi_2) \equiv (\mathbf{E} (\varphi_2 \mathbf{U} (\neg \varphi_1 \lor \neg \varphi_2) ) \lor \mathbf{E}\mathbf{G}(\varphi_2))`

.. _LTL:

Linear Time Logic
=================

The **Linear Time Logic** or **LTL** is a subset of of :ref:`CTL*<CTLS>`
([P77]_).

------
Syntax
------

LTL formulas have the form :math:`A \rho` where :math:`\rho`
is a LTL path formula and a LTL path formula is either:

- :math:`\top` or :math:`\bot`
- an atomic proposition
- :math:`\neg \varphi_1`, :math:`\varphi_1 \land \varphi_2`,
  :math:`\varphi_1 \lor \varphi_2`, or :math:`\varphi_1 \rightarrow \varphi_2`,
  where both :math:`\varphi_1` and :math:`\varphi_2` are LTL path formulas
- :math:`\mathbf{X} \varphi_1`, :math:`\mathbf{F} \varphi_1`,
  :math:`\mathbf{G} \varphi_1`, :math:`\varphi_1 \mathbf{U} \varphi_2`, or
  :math:`\varphi_1 \mathbf{R} \varphi_2` where both :math:`\varphi_1` and
  :math:`\varphi_2` are LTL path formulas.

---------
Semantics
---------
LTL has the same :ref:`semantics of CTL*<CTLS_semantics>`.

-----------------
Restricted Syntax
-----------------

It is easy to prove that:

- :math:`\psi_1 \land \psi_2 \equiv \neg (\neg \psi_1 \lor \neg \psi_2)`
- :math:`\psi_1 \rightarrow \psi_2 \equiv \neg \psi_1 \lor \psi_2`
- :math:`\mathbf{F} \psi \equiv \top \mathbf{U} \psi`
- :math:`\mathbf{G} \psi \equiv \neg (\top \mathbf{U} \neg \psi)`
- :math:`\psi_1 \mathbf{R} \psi_2 \equiv \neg ((\neg \psi_1) \mathbf{U} (\neg \psi_2))`

Hence, the LTL restricted language that allows
exclusively the path formulas whose operators are
:math:`\neg`, :math:`\lor`, :math:`\mathbf{X}`, or :math:`\mathbf{U}`
is equivalent to the full LTL language (e.g., see [CGP00]_).

.. [P77] A. Pnueli. "The temporal logic of programs." In Proceedings of the
   18th Annual Symposium of Foundations of Computer Science (FOCS),
   1977, 46-57
.. [BMP83] M. Ben-Ari, Z. Manna, A. Pnueli. The temporal logic of branching
   time. Acta Informatica 20(1983): 207-226
.. [CE81] E. M. Clarke, E. A. Emerson. "Design and synthesis of
   synchronization skeletons using branching time temporal logic." In
   Logic of Programs: Workshop. LNCS 131. Springer, 1981.
.. [CE80] E. M. Clarke, E. A. Emerson. "Characterizing correcteness properties
   of parallel programs using fixpoints." In Automata, Languages, and
   Programming. LNCS 85:169-181. Springer 1980.
.. [CES86] E. M. Clarke, E. A. Emerson, A. P. Sistla. "Automatic verification
   of finite-state concurrent systems using temporal logic specifications."
   ACM Transactions on Programming Languages and
   Systems 8(2): 244-263. 1986.
.. [CGP00] E. M. Clarke, O. Grumberg, D. A. Peled. "Model Checking" MIT Press,
   Cambridge, MA, USA. 2000.
