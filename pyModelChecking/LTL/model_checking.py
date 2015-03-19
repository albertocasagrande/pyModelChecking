#!/usr/bin/env python

from language import *
from pyModelChecking.graph import DiGraph,compute_strongly_connected_components
from pyModelChecking.kripke import Kripke
import pyModelChecking.CTLS as CTLS

import sys

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

def get_closure(formula):
    closure=set()
    T=[formula]

    Lang=sys.modules[formula.__module__]
    while len(T)>0:
        phi=T.pop()
        if phi not in closure:
            closure.add(phi)
            T.append(phi.negate_and_simplify())
            if isinstance(phi,CTLS.X):
                T.append(phi.subformula(0))
            else:
                if (isinstance(phi,CTLS.Not) and
                    isinstance(phi.subformula(0),X)):
                    sf=phi.subformula(0).subformula(0)
                    T.append(Lang.X(sf.negate_and_simplify()))
                else:
                    if isinstance(phi,CTLS.Or):
                        T.append(phi.subformula(0))
                        T.append(phi.subformula(1))
                    else:
                        if isinstance(phi,CTLS.U):
                            T.append(phi.subformula(0))
                            T.append(phi.subformula(1))
                            T.append(Lang.X(phi))
                        else:
                            if not (isinstance(phi,CTLS.Not) or
                                    isinstance(phi,CTLS.AtomicProposition) or
                                    isinstance(phi,CTLS.Bool)):
                                raise TypeError('%s is not LTL path ' % (phi) +
                                                'formula restricted to "or", '+
                                                '"not", "U" and "X"')

    return closure

class TableuAtom(set):
    def __init__(self,state,formulas=None):
        self.state=state
        if (formulas==None):
            formulas=set()

        super(TableuAtom,self).__init__(formulas)

    def __or__(self,A):
        if (isinstance(A,TableuAtom)):
            if self.state!=A.state:
                raise RuntimeError('%s and %s have different states' % (self,A))
            return self|set(A)

        return TableuAtom(self.state,super(TableuAtom,self).__or__(A))

    def __ror__(self,A):
        return self | A

    def __and__(self,A):
        if (isinstance(A,TableuAtom)):
            if self.state!=A.state:
                raise RuntimeError('%s and %s have different states' % (self,A))
            return self&set(A)

        return TableuAtom(self.state,super(TableuAtom,self).__and__(A))

    def __rand__(self,A):
        return self & A

    def copy(self):
        return TableuAtom(self.state,set(self))

    def __str__(self):
        return '(%s,%s)' % (self.state,set(self))

    def __repr__(self):
        return str(self)

class Tableu(DiGraph):
    @staticmethod
    def __build_atoms__(K,closure):
        A=[]
        for state in K.states():
            A.append(TableuAtom(state))

        for phi in sorted(list(closure),key=lambda a: a.height):
            Lang=sys.modules[phi.__module__]
            neg_phi=phi.negate_and_simplify()

            A_tail=[]
            if isinstance(phi,Bool):
                for atom in A:
                    atom.add(phi)
            else:
                if isinstance(phi,AtomicProposition):
                    for atom in A:
                        if phi in K.labels(atom.state):
                            atom.add(phi)
                        else:
                            atom.add(neg_phi)

            if (isinstance(phi,Or)):
                sf=phi.subformulas()
                neg_sf=[p.negate_and_simplify() for p in sf]

                for atom in A:
                    if (sf[0] in atom or sf[1] in atom):
                        atom.add(phi)
                    else:
                        atom.add(neg_phi)

            if (isinstance(phi,Not) and
                isinstance(phi.subformula(0),X)):
                sf=phi.subformula(0).subformula(0)

                for atom in A:
                    if phi.subformula(0) not in atom:
                        if phi not in atom:
                            new_atom=atom|set([phi,Lang.X(sf.negate_and_simplify())])
                            A_tail.append(new_atom)
                            atom.add(phi.subformula(0))
                        else:
                            atom.add(Lang.X(sf.negate_and_simplify()))

            if isinstance(phi,U):
                sf=phi.subformulas()
                neg_sf=[p.negate_and_simplify() for p in sf]

                for atom in A:
                    if (sf[1] in atom):
                        atom.add(phi)
                        A_tail.append(atom|set([Lang.X(phi)]))
                    else:
                        if (sf[0] in atom):
                            A_tail.append(atom|set([phi,Lang.X(phi)]))
                        atom.add(neg_phi)
                    atom.add(Lang.Not(Lang.X(phi)))

            A.extend(A_tail)

            if phi!=Lang.Not(True):
                for atom in A:
                    if phi not in atom and neg_phi not in atom:
                        A.append(atom|set([phi]))
                        atom.add(neg_phi)

        return A

    def __init__(self,K,formula=None,closure=None):
        def respect_Xs(Xs_in_closure,s_atom,d_atom):
            for phi in Xs_in_closure:
                if (phi.subformula(0) in d_atom) ^ (phi in s_atom):
                    return False

            return True

        def build_state_dict(atoms):
            state_dict={}
            for i in range(len(atoms)):
                if atoms[i].state not in state_dict:
                    state_dict[atoms[i].state]=[i]
                else:
                    state_dict[atoms[i].state].append(i)

            return state_dict

        if closure==None:
            if formula==None:
                raise RuntimeError('either closure or formula must be provided')
            closure=get_closure(formula)

        Xs_in_closure=set([p for p in closure if isinstance(p,X) ])

        self.atoms=Tableu.__build_atoms__(K,closure)
        state_dict=build_state_dict(self.atoms)

        super(Tableu,self).__init__(V=range(len(closure)))
        for (s,d) in K.edges():
            for s_i in state_dict[s]:
                for d_i in state_dict[d]:
                    if respect_Xs(Xs_in_closure,self.atoms[s_i],self.atoms[d_i]):
                        self.add_edge(s_i,d_i)

    def __str__(self):
        return '(V=%s,E=%s,A=%s)' % (self.nodes(),self.edges(),self.atoms)

def modelcheck(kripke,formula):

    def is_non_trivial_self_fulfilling(T,C,closure):
        i_atom=next(C.__iter__())
        if len(C)>1 or i_atom in T.next(i_atom):
            formulas=set()
            for i in C:
                formulas.update(T.atoms[i])

            for f in closure:
                if isinstance(f,CTLS.U):
                    if (f in formulas)^(f.subformula(1) in formulas):
                        return False

            return True

        return False

    if not isinstance(formula,Formula):
        try:
            formula=formula.cast_to(sys.modules[__name__])
        except:
            raise RuntimeError('%s is not a LTL formula' % (formula))

    if not isinstance(formula,StateFormula):
        raise RuntimeError('%s is not a LTL state formula' % (formula))

    if not isinstance(kripke,Kripke):
        raise RuntimeError('%s is not a Kripke structure' % (kripke))

    Lang=sys.modules[formula.__module__]
    p_formula=Not(formula.subformula(0)).get_equivalent_restricted_formula()

    closure=get_closure(p_formula)
    T=Tableu(kripke,closure=closure)

    stack=[]
    for C in compute_strongly_connected_components(T):
        if is_non_trivial_self_fulfilling(T,C,closure):
            stack.extend(C)

    T_reversed=T.get_reversed_graph()
    R=set([])
    while len(stack)>0:
        i_atom=stack.pop()
        if i_atom not in R:
            R.add(i_atom)
            for next_i in T_reversed.next(i_atom):
                stack.append(next_i)

    return kripke.states()-set([T.atoms[i].state for i in R if p_formula in T.atoms[i] ])
