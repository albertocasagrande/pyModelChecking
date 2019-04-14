"""
.. module:: CTLS.model_checking
   :synopsis: Provides model checking methods for the CTL* language.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""

from .language import *
from pyModelChecking.kripke import Kripke

from .parser import Parser

import sys

import pyModelChecking.CTL
import pyModelChecking.LTL

CTL = sys.modules['pyModelChecking.CTL']
LTL = sys.modules['pyModelChecking.LTL']


def _get_a_new_atomic_proposition_for(kripke, formula):
    f_str = '[{}]'.format(formula)
    f_atom = f_str
    atoms = kripke.labels()

    i = 0
    while f_atom in atoms:
        f_atom = '[{}({})]'.format(f_str, i)
        i += 1

    return f_atom


def _remove_state_subformulas(kripke, formula, fair_label=None):
    Lang = sys.modules[formula.__module__]

    if isinstance(formula, AtomicProposition):
        return formula

    if isinstance(formula, PathQuantifier):
        f_atom = _get_a_new_atomic_proposition_for(kripke, formula)
        for s in _checkQuantifiedFormula(kripke, formula, fair_label):
            kripke.labels(s).add(f_atom)

        return Lang.AtomicProposition(f_atom)

    if isinstance(formula, Formula):
        sfs = []
        for sf in formula.subformulas():
            sfs.append(_remove_state_subformulas(kripke, sf, fair_label))

        return formula.__class__(*sfs)

    raise TypeError('expected a CTL* state formula, got {}' % (formula))


def _checkQuantifiedFormula(kripke, formula, fair_label=None):

    subformula = _remove_state_subformulas(kripke, formula.subformula(0),
                                           fair_label)

    formula = formula.__class__(subformula)
    try:
        if fair_label is not None:
            formula = formula.cast_to(CTL)
            formula = (formula).get_equivalent_non_fair_formula(fair_label)

        return CTL.modelcheck(kripke, formula)
    except TypeError:
        if fair_label is not None:
            formula = formula.get_equivalent_non_fair_formula(fair_label)

        if (not isinstance(formula, A)):
            if (isinstance(formula, E)):
                formula = LNot(A(LNot(formula.subformula(0))))

            formula = _remove_state_subformulas(kripke, formula)

            return CTL.modelcheck(kripke, formula)

        return LTL.modelcheck(kripke, formula)


def modelcheck(kripke, formula, parser=None, F=None):
    ''' Model checks any CTL* formula on a Kripke structure.

    This method performs CTL* model checking of a formula on a given
    Kripke structure.

    :param kripke: a Kripke structure.
    :type kripke: Kripke
    :param formula: the formula to model check.
    :type formula: a type castable in a CTLS.Formula or a string representing
                   a CTLS formula
    :param parser: a parser to parse a string into a CTLS.Formula.
    :type parser: CTLS.Parser
    :param F: a list of fair states
    :type F: Container
    :returns: a list of the Kripke structure states that satisfy the formula.
    '''

    if isinstance(formula, str):
        if parser is None:
            parser = Parser()
        formula = parser(formula)

    if not isinstance(kripke, Kripke):
        raise TypeError('expected a Kripke structure, got {}'.format(kripke))

    try:
        kripkeC = kripke.clone()

        if F is not None:
            fair_label = kripkeC.label_fair_states(F)

            CTL_frml = _remove_state_subformulas(kripkeC, formula,
                                                 fair_label)

            CTL_frml = CTL_frml.get_equivalent_non_fair_formula(fair_label)
        else:
            CTL_frml = _remove_state_subformulas(kripkeC, formula)

        return CTL.modelcheck(kripkeC, CTL_frml)

    except TypeError as e:
        print(e)

        raise TypeError('expected a CTL* state formula, ' +
                        'got {}'.format(formula))
