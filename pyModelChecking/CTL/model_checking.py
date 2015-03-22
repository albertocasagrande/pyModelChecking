#!/usr/bin/env python

from .language import *
from pyModelChecking.graph import compute_strongly_connected_components
from pyModelChecking.kripke import Kripke

import sys

if 'pyModelChecking.CTLS' not in sys.modules:
    import pyModelChecking.CTLS

CTLS=sys.modules['pyModelChecking.CTLS']

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

def init_formula_in(formula,L):
    if formula not in L:
        L[formula]=set()

def checkAtomicProposition(kripke,formula,L):
    if formula not in L:
        Lformula=set()
        for v in kripke.states():
            if formula.name in kripke.labels(v):
                Lformula.add(v)

        L[formula]=Lformula

    return L[formula]

def checkNot(kripke,formula,L):
    if formula not in L:
        Lphi=checkStateFormula(kripke,formula.subformula(0),L)

        Lformula=set()
        for v in kripke.states()-Lphi:
            Lformula.add(v)

        L[formula]=Lformula

    return L[formula]

def checkEX(kripke,formula,L):
    if formula not in L:

        p_formula=formula.subformula(0)
        Lphi=checkStateFormula(kripke,p_formula.subformula(0),L)

        Lformula=set()
        for (src,dst) in kripke.transitions():
            if dst in Lphi:
                Lformula.add(src)

        L[formula]=Lformula

    return L[formula]

def checkOr(kripke,formula,L):
    if formula not in L:
        Lphi=[]
        for i in range(2):
            subformula=formula.subformula(i)
            Lphi.append(checkStateFormula(kripke,subformula,L))

        Lformula=set()
        for v in Lphi[0]|Lphi[1]:
            Lformula.add(v)

        L[formula]=Lformula

    return L[formula]

def checkEU(kripke,formula,L):
    if formula not in L:
        Lphi=[]
        p_formula=formula.subformula(0)
        for i in range(2):
            Lphi.append(checkStateFormula(kripke,p_formula.subformula(i),L))

        subgraph=kripke.get_subgraph(Lphi[0])
        subgraph=subgraph.get_reversed_graph()

        for v in Lphi[0]:
            for w in kripke.next(v)&Lphi[1]:
                try:
                    subgraph.add_edge(w,v)
                except:
                    pass

        T=Lphi[1]

        L[formula]=subgraph.get_reachable_set_from(Lphi[1])

    return L[formula]

def checkEG(kripke,formula,L):
    if formula not in L:
        p_formula=formula.subformula(0)
        Lphi=checkStateFormula(kripke,p_formula.subformula(0),L)

        subgraph=kripke.get_subgraph(Lphi)
        subgraph=subgraph.get_reversed_graph()
        SCCs=compute_strongly_connected_components(subgraph)

        T=set()
        for scc in SCCs:
            v = next(iter(scc))
            if len(scc)>1 or v in subgraph.next(v):
                T.add(v)

        L[formula]=subgraph.get_reachable_set_from(T)

    return L[formula]

def checkStateFormula(kripke,formula,L):
    if isinstance(formula,CTLS.Not):
        return checkNot(kripke,formula,L)

    if isinstance(formula,CTLS.Or):
        return checkOr(kripke,formula,L)

    if (isinstance(formula,CTLS.Bool) or
        isinstance(formula,bool)):
        Lang=sys.modules[formula.__module__]
        if formula==Bool(True):
            Lformula=kripke.states()
            L[Lang.Bool(True)]=Lformula
        else:
            Lformula=set()
            L[Lang.Bool(False)]=Lformula

        return Lformula

    if isinstance(formula,CTLS.AtomicProposition):
        return checkAtomicProposition(kripke,formula,L)

    if isinstance(formula,CTLS.E):
        p_formula=formula.subformula(0)
        if isinstance(p_formula,CTLS.G):
            return checkEG(kripke,formula,L)

        if isinstance(p_formula,CTLS.U):
            return checkEU(kripke,formula,L)

        if isinstance(p_formula,CTLS.X):
            return checkEX(kripke,formula,L)

    restr_f=formula.get_equivalent_restricted_formula()

    Lalter_formula=checkStateFormula(kripke,restr_f,L)

    L[formula]=Lalter_formula

    return Lalter_formula

def modelcheck(kripke,formula):

    if not isinstance(formula,Formula):
        try:
            formula=formula.cast_to(sys.modules[__name__])
        except:
            raise TypeError('expected a CTL state formula, got %s' % (formula))

    if not isinstance(formula,StateFormula):
        raise TypeError('expected a CTL state formula, got %s' % (formula))

    if not isinstance(kripke,Kripke):
        raise TypeError('expected a Kripke structure, got %s' % (kripke))

    return checkStateFormula(kripke,formula,L=dict())
