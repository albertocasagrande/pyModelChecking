#!/usr/bin/env python

from language import *
from pyModelChecking.graph import compute_strongly_connected_components
from pyModelChecking.kripke import Kripke
from pyModelChecking.CTL import *

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
            Lformula=set()

            Lphi=modelcheck(kripke,formula.phi,L)

            for v in kripke.states()-Lphi:
                Lformula.add(v)

            L[formula]=Lformula

        return L[formula]

    def checkEX(kripke,formula,L):
        if formula not in L:
            Lformula=set()

            Lphi=modelcheck(kripke,formula.phi,L)

            for (src,dst) in kripke.transitions():
                if dst in Lphi:
                    Lformula.add(src)

            L[formula]=Lformula

        return L[formula]

    def checkOr(kripke,formula,L):
        if formula not in L:
            Lformula=set()

            Lphi=[]
            for subformula in formula.phi:
                Lphi.append(modelcheck(kripke,subformula,L))

            for v in Lphi[0]|Lphi[1]:
                Lformula.add(v)

            L[formula]=Lformula

        return L[formula]

    def checkEU(kripke,formula,L):
        if formula not in L:
            Lformula=set()

            Lphi=[]
            for subformula in formula.phi:
                Lphi.append(modelcheck(kripke,subformula,L))

            subgraph=kripke.get_subgraph(Lphi[0])
            subgraph=subgraph.get_reversed_graph()

            for v in Lphi[0]:
                for w in kripke.next(v)&Lphi[1]:
                    subgraph.add_edge((w,v))

            T=Lphi[1]

            for v in T:
                Lformula.add(v)

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
            Lformula=set()

            Lphi=modelcheck(kripke,formula.phi,L)

            subgraph=kripke.get_subgraph(Lphi)
            subgraph=subgraph.get_reversed_graph()
            SCCs=compute_strongly_connected_components(subgraph)

            T=set()
            for scc in SCCs:
                v = next(iter(scc))
                if len(scc)>1 or v in subgraph.next(v):
                    T.add(v)

            Lformula.update(T)

            while len(T)!=0:
                w=T.pop()
                for v in subgraph.next(w):
                    if v not in Lformula:
                        T.add(v)
                        Lformula.add(v)

            L[formula]=Lformula

        return L[formula]

    def check(kripke,formula,L):
        if isinstance(formula,EG):
            return checkEG(kripke,formula,L)

        if isinstance(formula,EU):
            return checkEU(kripke,formula,L)

        if isinstance(formula,EX):
            return checkEX(kripke,formula,L)

        if isinstance(formula,Not):
            return checkNot(kripke,formula,L)

        if isinstance(formula,Or):
            return checkOr(kripke,formula,L)

        if (isinstance(formula,Bool) or
            isinstance(formula,bool)):
            if formula==Bool(True):
                Lformula=kripke.states()
                L[Bool(True)]=Lformula
            else:
                Lformula=set()
                L[Bool(False)]=Lformula

            return Lformula

        if isinstance(formula,Atom):
            return checkAtom(kripke,formula,L)

        EGUX_op=formula.get_equivalent_EGUX_operator()

        if isinstance(formula,UnaryOperator):
            alter_formula=EGUX_op(formula.phi)
        else: #is a BinaryOperator
            if isinstance(formula,BinaryOperator):
                alter_formula=EGUX_op(formula.phi[0],formula.phi[1])
            else:
                raise RuntimeError('%s is an unknown CTLFormula subclass' %
                                    (formula.__class__))

        Lalter_formula=check(kripke,alter_formula,L)

        L[formula]=Lalter_formula

        return Lalter_formula

    if L==None:
        L=dict()

    if not isinstance(formula,CTLFormula):
        raise RuntimeError('%s is not a CTL formula' % (formula))

    if not isinstance(kripke,Kripke):
        raise RuntimeError('%s is not a Kripke structure' % (kripke))

    return check(kripke,formula,L)
