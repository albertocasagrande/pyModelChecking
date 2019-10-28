"""
.. module:: LTL.model_checking
   :synopsis: Provides model checking methods for the LTL language.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""

from .language import *
from pyModelChecking.graph import DiGraph
from pyModelChecking.graph import compute_SCCs
from pyModelChecking.kripke import Kripke
from pyModelChecking.CTLS import LNot as LNot

from .parser import Parser

import sys

# if 'pyModelChecking.CTLS' not in sys.modules:
import pyModelChecking.CTLS

LTL = sys.modules[__name__]
CTLS = sys.modules['pyModelChecking.CTLS']


def _get_closure(formula):
    closure = set()
    T = [formula]

    Lang = sys.modules[formula.__module__]
    while len(T) > 0:
        phi = T.pop()
        if phi not in closure:
            closure.add(phi)
            T.append(LNot(phi))
            if isinstance(phi, CTLS.X):
                T.append(phi.subformula(0))
            else:
                if (isinstance(phi, CTLS.Not) and
                        isinstance(phi.subformula(0), CTLS.X)):
                    sf = phi.subformula(0).subformula(0)
                    T.append(Lang.X(LNot(sf)))
                else:
                    if isinstance(phi, CTLS.Or):
                        T.append(phi.subformula(0))
                        T.append(phi.subformula(1))
                    else:
                        if isinstance(phi, CTLS.U):
                            T.append(phi.subformula(0))
                            T.append(phi.subformula(1))
                            T.append(Lang.X(phi))
                        else:
                            if not (isinstance(phi, CTLS.Not) or
                                    isinstance(phi, CTLS.AtomicProposition) or
                                    isinstance(phi, CTLS.Bool)):
                                raise TypeError('expected a LTL path ' +
                                                'formula  restricted to ' +
                                                '"or",  "not",  ' +
                                                '"U" and "X", got ' +
                                                '{}'.format(phi))

    return closure


class _TableuAtom(set):
    def __init__(self, state, formulas=None):
        self.state = state
        if (formulas is None):
            formulas = set()

        super(_TableuAtom, self).__init__(formulas)

    def __or__(self, A):
        if (isinstance(A, _TableuAtom)):
            if self.state != A.state:
                raise RuntimeError('{} and {}'.format(self, A) +
                                   ' have different states')
            return self | set(A)

        return _TableuAtom(self.state, super(_TableuAtom, self).__or__(A))

    def __ror__(self, A):
        return self | A

    def __and__(self, A):
        if (isinstance(A, _TableuAtom)):
            if self.state != A.state:
                raise RuntimeError('{} and {}'.format(self, A) +
                                   ' have different states')
            return self & set(A)

        return _TableuAtom(self.state, super(_TableuAtom, self).__and__(A))

    def __rand__(self, A):
        return self & A

    def clone(self):
        return _TableuAtom(self.state, set(self))

    def __str__(self):
        return '(%s, %s)' % (self.state, set(self))

    def __repr__(self):
        return str(self)


def _does_respect_Xs(Xs_in_closure, s_atom, d_atom):
    for phi in Xs_in_closure:
        if (phi.subformula(0) in d_atom) ^ (phi in s_atom):
            return False

    return True


def _build_state_dict(atoms):
    state_dict = {}
    for i in range(len(atoms)):
        if atoms[i].state not in state_dict:
            state_dict[atoms[i].state] = [i]
        else:
            state_dict[atoms[i].state].append(i)

    return state_dict


def _build_atoms(K, closure):
    A = []
    for state in K.states():
        A.append(_TableuAtom(state))

    # this is to avoid issues with the "not X" case
    cl_list = sorted(list(closure), key=(lambda a: a.height
                                     if not (isinstance(a, CTLS.Not) and
                                             isinstance(a.subformula(0), CTLS.X))
                                     else a.height-1))

    for phi in cl_list:
        Lang = sys.modules[phi.__module__]

        if phi != Lang.Not(True) and phi != Lang.Bool(False):
            neg_phi = LNot(phi)

            A_tail = []
            if isinstance(phi, CTLS.Bool):
                for atom in A:
                    atom.add(phi)
            else:
                if isinstance(phi, CTLS.AtomicProposition):
                    for atom in A:
                        if phi in K.labels(atom.state):
                            atom.add(phi)
                        else:
                            atom.add(neg_phi)

            if (isinstance(phi, CTLS.Or)):
                sf = phi.subformulas()

                for atom in A:
                    if sum([f in atom for f in sf]):
                        atom.add(phi)
                    else:
                        atom.add(neg_phi)

            if (isinstance(phi, CTLS.Not) and
                    isinstance(phi.subformula(0), CTLS.X)):
                sf = phi.subformula(0).subformula(0)

                for atom in A:
                    if phi.subformula(0) not in atom:
                        if phi not in atom:
                            new_atom = atom | set([phi, Lang.X(LNot(sf))])
                            A_tail.append(new_atom)
                            atom.add(phi.subformula(0))
                        else:
                            atom.add(Lang.X(LNot(sf)))

            if isinstance(phi, CTLS.U):
                sf = phi.subformulas()

                for atom in A:
                    if (sf[1] in atom):
                        atom.add(phi)
                        A_tail.append(atom | set([Lang.X(phi)]))
                    else:
                        if (sf[0] in atom):
                            A_tail.append(atom | set([phi, Lang.X(phi)]))
                        atom.add(neg_phi)
                    atom.add(Lang.Not(Lang.X(phi)))

            A.extend(A_tail)

            for atom in A:
                if phi not in atom and neg_phi not in atom:
                    A.append(atom | set([phi]))
                    atom.add(neg_phi)

    return A


class _Tableu(DiGraph):
    def __init__(self, K, formula=None, closure=None):
        if closure is None:
            if formula is None:
                raise RuntimeError('either closure or formula ' +
                                   'must be provided')
            closure = _get_closure(formula)

        Xs_in_closure = set([p for p in closure if isinstance(p, CTLS.X)])

        self.atoms = _build_atoms(K, closure)
        state_dict = _build_state_dict(self.atoms)

        super(_Tableu, self).__init__(V=range(len(self.atoms)))
        for (s, d) in K.edges_iter():
            for s_i in state_dict[s]:
                for d_i in state_dict[d]:
                    if _does_respect_Xs(Xs_in_closure,
                                        self.atoms[s_i], self.atoms[d_i]):
                        self.add_edge(s_i, d_i)

    def __str__(self):
        return '(V = {}, E = {}, A = {})'.format(self.nodes(),
                                                 self.edges_iter(),
                                                 self.atoms)


def _is_non_trivial_self_fulfilling(T, C, closure):
    i_atom = next(C.__iter__())
    if len(C) > 1 or i_atom in T.next(i_atom):
        formulas = set()
        for i in C:
            formulas.update(T.atoms[i])

        for f in closure:
            if isinstance(f, CTLS.U):
                if (f in formulas) ^ (f.subformula(1) in formulas):
                    return False

        return True

    return False


def _checkE_path_formula(kripke, p_formula):

    closure = _get_closure(p_formula)
    T = _Tableu(kripke, closure=closure)

    in_ntsf = []

    for C in compute_SCCs(T):
        if _is_non_trivial_self_fulfilling(T, C, closure):
            in_ntsf.extend(C)

    T_reversed = T.get_reversed_graph()
    R = T_reversed.get_reachable_set_from(in_ntsf)

    return set([T.atoms[i].state for i in R if p_formula in T.atoms[i]])


def modelcheck(kripke, formula, parser=None, F=None):
    ''' Model checks any LTL formula on a Kripke structure.

    This method performs LTL model checking of a formula on a given
    Kripke structure.

    :param kripke: a Kripke structure.
    :type kripke: Kripke
    :param formula: the formula to model check.
    :type formula: a type castable in a LTL.Formula or a string representing
                   a LTL formula
    :param parser: a parser to parse a string into a LTL.Formula.
    :type parser: LTL.Parser
    :param F: a list of fair states
    :type F: Container
    :returns: a list of the Kripke structure states that satisfy the formula.
    '''

    if isinstance(formula, str):
        if parser is None:
            parser = Parser()
        formula = parser(formula)

    if not (isinstance(formula, CTLS.A)):
        raise TypeError('expected a LTL state formula, got {}'.format(formula))

    if not isinstance(kripke, Kripke):
        raise TypeError('expected a Kripke structure, got {}'.format(kripke))

    try:
        p_formula = LNot(formula.subformula(0))
        p_formula = p_formula.get_equivalent_restricted_formula()

        if F is not None:
            kripke = kripke.clone()

            fair_label = kripke.label_fair_states(F)

            p_formula = p_formula.get_equivalent_non_fair_formula(fair_label)
            p_formula = And(fair_label, p_formula)

        return set(kripke.states())-_checkE_path_formula(kripke, p_formula)
    except TypeError:
        raise TypeError('expected a LTL formula, got {}'.format(formula))
