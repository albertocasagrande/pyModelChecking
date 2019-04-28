************************************
Encoding Formulas and Model Checking
************************************

`pyModelChecking` provides a user friendly support for building
:ref:`CTL*<CTLS>`, :ref:`CTL<CTL>` and :ref:`LTL<LTL>` formulas. Each of these
languages corresponds to a `pyModelChecking`'s sub-module which implements
all the classes required to encode the corresponding formulas.

Propositional logic is also supported by `pyModelChecking` as a shared
basis for all the possible temporal logics.

.. _propositional_encoding:

Propositional Logics
====================

Propositional logics support is provided by including the
`pyModelChecking.language` sub-module. This sub-module allows to
represents atomic propositions and Boolean values through the
:class:`pyModelChecking.formula.AtomicProposition` and
:class:`pyModelChecking.formula.Bool` classes, respectively.

.. code-block:: Python

    >>> from pyModelChecking.PL import *
    >>> AtomicProposition('p')

    p

    >>> Bool(True)

    true

Moreover, the :mod:`pyModelChecking.PL` sub-module
implements the logic operators :math:`\land`, :math:`\lor`, :math:`\rightarrow`
and :math:`\neg` by mean of the classes
:class:`pyModelChecking.PL.And`, :class:`pyModelChecking.PL.Or`,
:class:`pyModelChecking.PL.Imply` and
:class:`pyModelChecking.PL.Not`, respectively. These classes
automatically wrap strings and Boolean values as objects of the classes
:class:`pyModelChecking.PL.AtomicProposition` and
:class:`pyModelChecking.PL.Bool`, respectively. All cited classes are 
subclasses of the class :class:`pyModelChecking.PL.Formula`.

.. code-block:: Python

    >>> And('p', true)
 
    (p and true)

    >>> And('p', true, 'p')

    (p and true and p)

    >>> f = Imply('q','p')
    >>> And('p', f, Imply(Not(f), Or('q','s', f)))

    (p and (q --> p) and (not (q --> p) --> (q or s or (q --> p))))

    >>> Imply('p', 'q', 'p')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: __init__() takes exactly 3 arguments (4 given)

In order to simplify formula encoding, the operators `~`, `&`, and `|` --i.e., 
:meth:`pyModelChecking.PL.__not__`, 
:meth:`pyModelChecking.PL.__and__`, and 
:meth:`pyModelChecking.PL.__or__`-- were 
overwritten to be used as shortcuts to :class:`pyModelChecking.PL.Not`, 
:class:`pyModelChecking.PL.And`, and :class:`pyModelChecking.PL.Or` 
constructors, respectively. At least one of the operator parameters should 
be an object of the class :class:`pyModelChecking.PL.Formula`.

.. code-block:: Python

    >>> AtomicProposition('p') & True

    (p and true)

    >>> True & AtomicProposition('p')

    (true and p)

    >>> f = 'p' & Bool(True)
    >>> f 

    (p and true)

    >>> True & 'p' & Bool(True)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unsupported operand type(s) for &: 'bool' and 'str'

    >>> 'p' & Bool(True) & 'p'

    ((p and true) and p)

    >>> ~('p' & Bool(True)) | And(~f,'b')

    (not (p and true) or (not (p and true) and b))

For user convenience, the function :func:`pyModelChecking.PL.LNot`
is also provided. This function returns a formula that is equivalent to the 
logic negation of the parameter and minimises the number of outermost 
:math:`\neg`.

.. code-block:: Python

    >>> f = Not(Not(Not(And('p',Not('q')))))
    >>> f

    not not not (p and not q)

    >>> LNot(f)

    (p and not q)

    >>> LNot(Not(f))

    not (p and not q)

    >>> LNot(LNot(f))

    not (p and not q)

Parsing Formulas
----------------

The module :mod:`pyModelChecking.PL` also provides a parsing class
:class:`pyModelChecking.PL.Parser` for propositional formula. 
Its objects read a formula from a string and, when it is possible, 
translate it into the corresponding :class:`pyModelChecking.PL.Formula` 
objects.

.. code-block:: Python

    >>> p = Parser()

    >>> p('p and true')

    (p and true)

    >>> p('(~p and q) --> ((q | p))')

    ((not p and q) --> (q or p))

A complete description of the parser grammar is contained in class attribute  
:attr:`pyModelChecking.PL.Parser.grammar`

.. code-block:: Python

    >>> print(p.grammar)

        s_formula: "true"     -> true
                 | "false"    -> false
                 | a_prop
                 | "(" s_formula ")"

        u_formula: ("not"|"~") u_formula  -> not_formula
                 | "(" b_formula ")"
                 | s_formula

        b_formula: u_formula
                 | u_formula ( ("or"|"|") u_formula )+ -> or_formula
                 | u_formula ( ("and"|"&") u_formula )+ -> and_formula
                 | u_formula ("-->") u_formula -> imply_formula

        a_prop: /[a-zA-Z_][a-zA-Z_0-9]*/ -> string
              | ESCAPED_STRING           -> e_string

        formula: b_formula

        %import common.ESCAPED_STRING
        %import common.WS
        %import WS


.. _TL_encoding:
 
Temporal Logics Implementation
==============================

CTL* formulas can be defined by using the
:mod:`pyModelChecking.CTLS` sub-module.

.. code-block:: Python

    >>> from pyModelChecking.CTLS import *

Path quantifiers :math:`A` and :math:`E` as well as temporal operators
:math:`X`, :math:`F`, :math:`G`, :math:`U` and :math:`R`  are provided as
classes (see :ref:`CTLS sub-module<ctls_api>` for more details).
As in the case of propositional logics, these classes wrap strings and
Boolean values as objects of the classes
:class:`pyModelChecking.CTLS.language.AtomicProposition` and
:class:`pyModelChecking.CTLS.language.Bool`, respectively.

.. code-block:: Python

    >>> phi = A(G(
    ...         Imply(And(Not('Close'),
    ...                   'Start'),
    ...               A(Or(G(Not('Heat')),
    ...                    F(Not('Error')))))
    ...         ))
    >>> phi

    A(G(((not Close and Start) --> A((G(not Heat) or F(not Error))))))

As far as parsing capabilities and siplifying syntax concern, 
:mod:`pyModelChecking.CTLS` has the same facilities 
:mod:`pyModelChecking.PL` had and implements :math:`CTL*` specific 
version of both class :class:`pyModelChecking.CTLS.Parser` and 
operators `~`, `&`, and `|`. 

.. code-block:: Python
   
   >>> p=Parser()
   >>> p('G(not Heat)') | p('A(F(not Error))')

   (G(not Heat) or A(F(not Error)))

Model Checking Formulas
=======================

The sub-module also implements the CTL* model checking and fair model checking
algorithms described in [CGP00]_.

.. code-block:: Python

    >>> from pyModelChecking import Kripke
    >>> K = Kripke(R=[(0, 1), (0, 2), (1, 4), (4, 1), (4, 2), (2, 0),
    ...               (3, 2), (3, 0), (3, 3), (6, 3), (2, 5), (5, 6)],
    ...            L={0: set(), 1: set(['Start', 'Error']), 2: set(['Close']),
    ...               3: set(['Close', 'Heat']),
    ...               4: set(['Start', 'Close', 'Error']),
    ...               5: set(['Start', 'Close']),
    ...               6: set(['Start', 'Close', 'Heat'])})
    >>> modelcheck(K, psi)

    set([0, 1, 2, 3, 4, 5, 6])

    >>> modelcheck(K, psi, F=[6])

    set([])

It is also possible to model check a string representation of a CTL* formula by
either passing an object of the class :class:`pyModelChecking.CTLS.Parser`
or leaving the remit of creating such an object to the function
:func:`pyModelChecking.CTLS.modelcheck`.

.. code-block:: Python

    >>> modelcheck(K, psi_str)

    set([0, 1, 2, 3, 4, 5, 6])

    >>> modelcheck(K, psi_str, parser=parser)

    set([0, 1, 2, 3, 4, 5, 6])

Analogous functionality are provided for :ref:`CTL<CTL>` and :ref:`LTL<LTL>`
by the sub-modules :mod:`pyModelChecking.CTL` and
:mod:`pyModelChecking.LTL`, respectively.
