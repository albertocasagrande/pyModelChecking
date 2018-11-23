*****************************
Logics and Model Checking API
*****************************

The implementations of specific languages and their model checking routines
are contained in *pyModelChecking* sub-modules. CTL*, CTL, and LTL
are handled by :ref:`CTLS sub-module<ctls_api>`, :ref:`CTL sub-module<ctl_api>`
and :ref:`LTL sub-module<ltl_api>`, respectively.

.. _ctls_api:

CTLS sub-module API
===================

It represents :ref:`CTL* formulas<CTLS>` and provides model checking methods for them.

.. automodule:: pyModelChecking.CTLS
    :members:
    :undoc-members:
    :show-inheritance:

Language
--------

.. automodule:: pyModelChecking.CTLS.language
    :members:
    :undoc-members:
    :show-inheritance:

Model Checking
--------------

.. automodule:: pyModelChecking.CTLS.model_checking
    :members:
    :undoc-members:
    :show-inheritance:

.. _ctl_api:

CTL sub-module API
==================

It represents :ref:`CTL formulas<CTL>` and provides model checking methods for them.

.. automodule:: pyModelChecking.CTL
    :members:
    :undoc-members:
    :show-inheritance:

Language
--------

.. automodule:: pyModelChecking.CTL.language
    :members:
    :undoc-members:
    :show-inheritance:

Model Checking
--------------

.. automodule:: pyModelChecking.CTL.model_checking
    :members:
    :undoc-members:
    :show-inheritance:

.. _ltl_api:

LTL sub-module API
==================

It represents :ref:`LTL formulas<LTL>` and provides model checking methods for them.

.. automodule:: pyModelChecking.LTL
    :members:
    :undoc-members:
    :show-inheritance:

Language
--------

.. automodule:: pyModelChecking.LTL.language
    :members:
    :undoc-members:
    :show-inheritance:

Model Checking
--------------

.. automodule:: pyModelChecking.LTL.model_checking
    :members:
    :undoc-members:
    :show-inheritance:
