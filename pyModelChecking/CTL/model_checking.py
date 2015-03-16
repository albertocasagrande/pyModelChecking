#!/usr/bin/env python

from language import *
from pyModelChecking.graph import compute_strongly_connected_components
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

def modelcheck(kripke,formula,L=None):
    def init_formula_in(formula,L):
        if formula not in L:
            L[formula]=set()

    def checkAtom(kripke,formula,L):
        if formula not in L:
            Lformula=set()
            for v in kripke.states():
                if formula.name in kripke.labels(v):
                    Lformula.add(v)

            L[formula]=Lformula

        return L[formula]

    def checkNot(kripke,formula,L):
        if formula not in L:
            Lphi=modelcheck(kripke,formula.subformula(0),L)

            Lformula=set()
            for v in kripke.states()-Lphi:
                Lformula.add(v)

            L[formula]=Lformula

        return L[formula]

    def checkEX(kripke,formula,L):
        if formula not in L:

            p_formula=formula.subformula(0)
            Lphi=modelcheck(kripke,p_formula.subformula(0),L)

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
                Lphi.append(modelcheck(kripke,subformula,L))

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
                Lphi.append(modelcheck(kripke,p_formula.subformula(i),L))

            subgraph=kripke.get_subgraph(Lphi[0])
            subgraph=subgraph.get_reversed_graph()

            for v in Lphi[0]:
                for w in kripke.next(v)&Lphi[1]:
                    try:
                        subgraph.add_edge(w,v)
                    except:
                        pass

            T=Lphi[1]

            Lformula=set(T)
            while len(T)!=0:
                w=T.pop()
                for v in subgraph.next(w):
                    if v not in Lformula:
                        T.add(v)
                        Lformula.add(v)

            L[formula]=Lformula

        return L[formula]

    def checkEG(kripke,formula,L):
        if formula not in L:
            p_formula=formula.subformula(0)
            Lphi=modelcheck(kripke,p_formula.subformula(0),L)

            subgraph=kripke.get_subgraph(Lphi)
            subgraph=subgraph.get_reversed_graph()
            SCCs=compute_strongly_connected_components(subgraph)

            T=set()
            for scc in SCCs:
                v = next(iter(scc))
                if len(scc)>1 or v in subgraph.next(v):
                    T.add(v)

            Lformula=set(T)
            while len(T)!=0:
                w=T.pop()
                for v in subgraph.next(w):
                    if v not in Lformula:
                        T.add(v)
                        Lformula.add(v)

            L[formula]=Lformula

        return L[formula]

    def check(kripke,formula,L):
        if isinstance(formula,CTLS.Not):
            return checkNot(kripke,formula,L)

        if isinstance(formula,CTLS.Or):
            return checkOr(kripke,formula,L)

        if (isinstance(formula,CTLS.Bool) or
            isinstance(formula,bool)):
            if formula==Bool(True):
                Lformula=kripke.states()
                L[Bool(True)]=Lformula
            else:
                Lformula=set()
                L[Bool(False)]=Lformula

            return Lformula

        if isinstance(formula,CTLS.Atom):
            return checkAtom(kripke,formula,L)

        if isinstance(formula,CTLS.E):
            p_formula=formula.subformula(0)
            if isinstance(p_formula,CTLS.G):
                return checkEG(kripke,formula,L)

            if isinstance(p_formula,CTLS.U):
                return checkEU(kripke,formula,L)

            if isinstance(p_formula,CTLS.X):
                return checkEX(kripke,formula,L)

        restr_f=formula.get_equivalent_restricted_formula()

        Lalter_formula=check(kripke,restr_f,L)

        L[formula]=Lalter_formula

        return Lalter_formula

    if L==None:
        L=dict()

    old_formula=None
    if not isinstance(formula,Formula):
        try:
            old_formula=formula
            formula=formula.cast_to(sys.modules[__name__])
        except:
            raise RuntimeError('%s is not a CTL formula' % (formula))

    if not isinstance(formula,StateFormula):
        raise RuntimeError('%s is not a CTL state formula' % (formula))

    if not isinstance(kripke,Kripke):
        raise RuntimeError('%s is not a Kripke structure' % (kripke))

    S=check(kripke,formula,L)

    if old_formula!=None:
        L[old_formula]=S

    return S
