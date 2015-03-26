#!/usr/bin/env python

from .language import *
from pyModelChecking.kripke import Kripke

import sys

if 'pyModelChecking.CTL' not in sys.modules:
    import pyModelChecking.CTL

CTL=sys.modules['pyModelChecking.CTL']

if 'pyModelChecking.LTL' not in sys.modules:
    import pyModelChecking.LTL

LTL=sys.modules['pyModelChecking.LTL']

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

def get_a_new_atomic_proposition_for(kripke,formula):
    f_str='[%s]' % (formula)
    f_atom=f_str
    atoms=kripke.labels()

    i=0
    while f_atom in atoms:
        f_atom='[%s(%d)]' % (f_str,i)
        i+=1

    return f_atom

def remove_state_subformulas(kripke,formula,fair_label=None):
    Lang=sys.modules[formula.__module__]

    if isinstance(formula,AtomicProposition):
        return formula

    if isinstance(formula,PathQuantifier):
        f_atom=get_a_new_atomic_proposition_for(kripke,formula)
        for s in checkQuantifiedFormula(kripke,formula,fair_label):
            kripke.labels(s).add(f_atom)

        return Lang.AtomicProposition(f_atom)

    if isinstance(formula,Formula):
        sfs=[]
        for sf in formula.subformulas():
            sfs.append(remove_state_subformulas(kripke,sf,fair_label))

        return formula.__class__(*sfs)

    raise TypeError('expected a CTL* state formula, got %s' % (formula))

def checkQuantifiedFormula(kripke,formula,fair_label=None):

    subformula=remove_state_subformulas(kripke,formula.subformula(0),fair_label)

    formula=formula.__class__(subformula)
    try:
        if fair_label!=None:
            formula=(formula.cast_to(CTL)).get_equivalent_non_fair_formula(fair_label)

        return CTL.modelcheck(kripke,formula)
    except TypeError:
        if fair_label!=None:
            formula=formula.get_equivalent_non_fair_formula(fair_label)

        if (not isinstance(formula,A)):
            if (isinstance(formula,E)):
                formula=LNot(A(LNot(formula.subformula(0))))

            formula=remove_state_subformulas(kripke,formula)

            return CTL.modelcheck(kripke,formula)

        return LTL.modelcheck(kripke,formula)

def modelcheck(kripke,formula,F=None):

    if not isinstance(kripke,Kripke):
        raise TypeError('expected a Kripke structure, got %s' % (kripke))

    try:
        kripkeC=kripke.copy()

        if F!=None:
            fair_label=kripkeC.label_fair_states(F)

            CTL_formula=remove_state_subformulas(kripkeC,formula,fair_label)

            CTL_formula=CTL_formula.get_equivalent_non_fair_formula(fair_label)
        else:
            CTL_formula=remove_state_subformulas(kripkeC,formula)

        return CTL.modelcheck(kripkeC,CTL_formula)

    except TypeError:
        raise TypeError('expected a CTL* state formula, got %s' % (formula))
