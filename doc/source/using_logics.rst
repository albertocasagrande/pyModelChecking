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

    >>> from pyModelChecking.formula import *
    >>> AtomicProposition('p')

    p

    >>> Bool(True)

    True

Moreover, the `pyModelChecking.language` sub-module
implements the logic operators :math:`\land`, :math:`\lor`, :math:`\rightarrow`
and :math:`\neg` by mean of the classes
:class:`pyModelChecking.formula.And`, :class:`pyModelChecking.formula.Or`,
:class:`pyModelChecking.formula.Imply` and
:class:`pyModelChecking.formula.Not`, respectively. These classes
automatically wrap strings and Boolean values as objects of the classes
:class:`pyModelChecking.formula.AtomicProposition` and
:class:`pyModelChecking.formula.Bool`, respectively.

.. code-block:: Python

    >>> And('p', True)

    (p and True)

    >>> And('p', True, 'p')

    (p and True and p)

    >>> f = Imply('q','p')
    >>> And('p', f, Imply(Not(f), Or('q','s', f)))

    (p and (q --> p) and (not (q --> p) --> (q or s or (q --> p))))

    >> Imply('p', 'q', 'p')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: __init__() takes exactly 3 arguments (4 given)

For user convenience, the function :py:meth:`pyModelChecking.formula.LNot`
is also provided. This function returns a formula equivalent to logic
negation of the parameter and minimise the number of outermost :math:`\neg`.

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


.. _TL_encoding:

Temporal Logics Encoding
========================

CTL* formulas can be defined by using the
:py:mod:`pyModelChecking.CTLS` sub-module.

.. code-block:: Python

    >>> from pyModelChecking.CTLS import *

Path quantifiers :math:`A` and :math:`E` as well as temporal operators
:math:`X`, :math:`F`, :math:`G`, :math:`U` and :math:`R`  are provided as
classes (see ref:`CTLS sub-module<ctls_api>` for more details).
As in the case of propositional logics, these classes wrap strings and
Boolean values as objects of the classes
:class:`pyModelChecking.CTLS.language.AtomicProposition` and
:class:`pyModelChecking.CTLS.language.Bool`, respectively.

.. code-block:: Python

    >>> f = A(G(
    ...         Imply(And(Not('Close'),
    ...                   'Start'),
    ...               A(Or(G(Not('Heat')),
    ...                    F(Not('Error')))))
    ...         ))
    >>> f

    A(G(((not Close and Start) --> A((G(not Heat) or F(not Error))))))


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
    >>> modelcheck(K, f)

    set([0, 1, 2, 3, 4, 5, 6])

    >>> modelcheck(K, f, F=[6])

    set([])

Analogous functionality are provided for :ref:`CTL<CTL>` and :ref:`LTL<LTL>`
by the sub-modules :py:mod:`pyModelChecking.CTL` and
:py:mod:`pyModelChecking.LTL`, respectively.
