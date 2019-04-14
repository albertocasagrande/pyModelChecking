"""
.. module:: CTL.model_checking
   :synopsis: Provides model checking methods for the CTL language.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""

from .language import *
from pyModelChecking.graph import compute_SCCs
from pyModelChecking.kripke import Kripke

import pyModelChecking.CTLS

from .parser import Parser

import sys

CTLS = sys.modules['pyModelChecking.CTLS']


def _init_formula_in(formula, L):
    if formula not in L:
        L[formula] = set()


def _checkAtomicProposition(kripke, formula, L):
    if formula not in L:
        Lformula = set()
        for v in kripke.states():
            if formula.name in kripke.labels(v):
                Lformula.add(v)

        L[formula] = Lformula

    return L[formula]


def _checkNot(kripke, formula, L):
    if formula not in L:
        Lphi = _checkStateFormula(kripke, formula.subformula(0), L)

        Lformula = set()
        for v in kripke.states():
            if v not in Lphi:
                Lformula.add(v)

        L[formula] = Lformula

    return L[formula]


def _checkEX(kripke, formula, L):
    if formula not in L:

        p_formula = formula.subformula(0)
        Lphi = _checkStateFormula(kripke, p_formula.subformula(0), L)

        Lformula = set()
        for (src, dst) in kripke.transitions_iter():
            if dst in Lphi:
                Lformula.add(src)

        L[formula] = Lformula

    return L[formula]


def _checkOr(kripke, formula, L):
    if formula not in L:
        Lphi = []
        for i in range(2):
            subformula = formula.subformula(i)
            Lphi.append(_checkStateFormula(kripke, subformula, L))

        Lformula = set()
        for v in (Lphi[0] | Lphi[1]):
            Lformula.add(v)

        L[formula] = Lformula

    return L[formula]


def _checkEU(kripke, formula, L):
    if formula not in L:
        Lphi = []
        p_formula = formula.subformula(0)
        for i in range(2):
            Lphi.append(_checkStateFormula(kripke, p_formula.subformula(i), L))

        subgraph = kripke.get_subgraph(Lphi[0])
        subgraph = subgraph.get_reversed_graph()

        for v in Lphi[0]:
            for w in (kripke.next(v) & Lphi[1]):
                try:
                    subgraph.add_edge(w, v)
                except Exception:
                    pass

        T = Lphi[1]

        L[formula] = subgraph.get_reachable_set_from(Lphi[1])

    return L[formula]


def _checkEG(kripke, formula, L):
    if formula not in L:
        p_formula = formula.subformula(0)
        Lphi = _checkStateFormula(kripke, p_formula.subformula(0), L)

        subgraph = kripke.get_subgraph(Lphi)
        subgraph = subgraph.get_reversed_graph()
        SCCs = compute_SCCs(subgraph)

        T = set()
        for scc in SCCs:
            v = next(iter(scc))
            if len(scc) > 1 or v in subgraph.next(v):
                T.update(scc)

        L[formula] = subgraph.get_reachable_set_from(T)

    return L[formula]


def _checkStateFormula(kripke, formula, L):
    if isinstance(formula, CTLS.Not):
        return _checkNot(kripke, formula, L)

    if isinstance(formula, CTLS.Or):
        return _checkOr(kripke, formula, L)

    if (isinstance(formula, CTLS.Bool) or isinstance(formula, bool)):
        Lang = sys.modules[formula.__module__]
        if formula == Bool(True):
            Lformula = set(kripke.states())
            L[Lang.Bool(True)] = Lformula
        else:
            Lformula = set()
            L[Lang.Bool(False)] = Lformula

        return Lformula

    if isinstance(formula, CTLS.AtomicProposition):
        return _checkAtomicProposition(kripke, formula, L)

    if isinstance(formula, CTLS.E):
        p_formula = formula.subformula(0)
        if isinstance(p_formula, CTLS.G):
            return _checkEG(kripke, formula, L)

        if isinstance(p_formula, CTLS.U):
            return _checkEU(kripke, formula, L)

        if isinstance(p_formula, CTLS.X):
            return _checkEX(kripke, formula, L)

    restr_f = formula.get_equivalent_restricted_formula()

    Lalter_formula = _checkStateFormula(kripke, restr_f, L)

    L[formula] = Lalter_formula

    return Lalter_formula


def modelcheck(kripke, formula, parser=None, F=None):
    ''' Model checks any CTL formula on a Kripke structure.

    This method performs CTL model checking of a formula on a given
    Kripke structure.

    :param kripke: a Kripke structure.
    :type kripke: Kripke
    :param formula: the formula to model check.
    :type formula: a type castable in a CTL.Formula or a string representing
                   a CTL formula
    :param parser: a parser to parse a string into a CTL.Formula.
    :type parser: CTL.Parser
    :param F: a list of fair states
    :type F: Container
    :returns: a list of the Kripke structure states that satisfy the formula.
    '''

    if isinstance(formula, str):
        if parser is None:
            parser = Parser()
        formula = parser(formula)

    if not isinstance(formula, Formula):
        try:
            formula = formula.cast_to(sys.modules[__name__])
        except Exception:
            raise TypeError('expected a CTL state formula, ' +
                            'got {}'.format(formula))

    if not isinstance(formula, StateFormula):
        raise TypeError('expected a CTL state formula, got {}'.format(formula))

    if not isinstance(kripke, Kripke):
        raise TypeError('expected a Kripke structure, got {}'.format(kripke))

    if F is not None:
        kripke = kripke.clone()

        fair_label = kripke.label_fair_states(F)

        formula = formula.get_equivalent_non_fair_formula(fair_label)

    return _checkStateFormula(kripke, formula, L=dict())
