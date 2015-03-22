#!/usr/bin/env python

from language import *
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

def copy_labelling(L):
    copy={}

    for state, S in L:
        copy[state]=set(S)

    return copy

def checkAtomicProposition(kripke,formula):
    Lformula=set()
    for v in kripke.states():
        if formula.name in kripke.labels(v):
            Lformula.add(v)

    return Lformula

def checkBool(kripke,formula):
    if formula._value:
        return set(kripke.states())

    return set()

def checkNot(kripke,formula):
    Lphi=checkStateFormula(kripke,formula.subformula(0))

    Lformula=set()
    for v in kripke.states()-Lphi:
        Lformula.add(v)

    return Lformula

def checkOr(kripke,formula):
    Lphi=[]
    for i in range(2):
        subformula=formula.subformula(i)
        Lphi.append(checkStateFormula(kripke,subformula))

    Lformula=set()
    for v in Lphi[0]|Lphi[1]:
        Lformula.add(v)

    return Lformula

def get_a_new_atomic_proposition_for(kripke,formula):
    f_str='[%s]' % (formula)
    f_atom=f_str
    atoms=kripke.labels()

    i=0
    while f_atom in atoms:
        f_atom='[%s(%d)]' % (f_str,i)
        i+=1

    return f_atom

def remove_state_subformulas(kripke,formula):
    Lang=sys.modules[formula.__module__]

    if isinstance(formula,Lang.AtomicProposition):
        return formula

    if isinstance(formula,Not):
        return Lang.Not(remove_state_subformulas(kripke,formula.subformula(0)))

    if isinstance(formula,Or):
        return Lang.Or(remove_state_subformulas(kripke,formula.subformula(0)),
                  remove_state_subformulas(kripke,formula.subformula(1)))

    if isinstance(formula,U):
        return Lang.U(remove_state_subformulas(kripke,formula.subformula(0)),
                 remove_state_subformulas(kripke,formula.subformula(1)))

    if isinstance(formula,E):
        f_atom=get_a_new_atomic_proposition_for(kripke,formula)
        for s in checkEPathFormula(kripke,formula):
            kripke.labels(s).add(f_atom)

        return Lang.AtomicProposition(f_atom)

def checkEPathFormula(kripke,formula):
    try:
        return CTL.modelcheck(kripke,formula)
    except TypeError:
        pass

    LTL_path_formula=remove_state_subformulas(kripke,formula.subformula(0))

    return LTL.checkE_path_formula(kripke,LTL_path_formula)

def checkStateFormula(kripke, formula):
    try:
        if isinstance(formula,Bool):
            return checkBool(kripke,formula)

        if isinstance(formula,AtomicProposition):
            return checkAtomicProposition(kripke,formula)

        if isinstance(formula,Not):
            return checkNot(kripke,formula)

        if isinstance(formula,Or):
            return checkOr(kripke,formula)

        if isinstance(formula,E):
            return checkEPathFormula(kripke,formula)

    except TypeError:
        raise TypeError('%s is not a CTL* state formula' % (formula))

    raise TypeError('%s is not a restricted CTL* state formula' % (formula))

def modelcheck(kripke,formula):

    if not isinstance(kripke,Kripke):
        raise TypeError('expected a Kripke structure, got %s' % (kripke))

    try:
        restricted_formula=formula.get_equivalent_restricted_formula()

        return checkStateFormula(kripke.copy(),restricted_formula)
    except TypeError:
        raise TypeError('expected a CTL* state formula, got %s' % (formula))
