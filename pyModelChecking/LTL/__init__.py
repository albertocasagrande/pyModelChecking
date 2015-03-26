'''
This module represents the LTL language and provides model checking methods for it.

The **Linear Time Logic** or **LTL** is a subset of the temporal language
CTL* ([P77]_). LTL formulas have the form "A rho" where "rho" is a LTL
*path formula* and a LTL path formula is either:
 - an atomic proposition
 - "not phi", "phi or psi", "phi and psi", "phi implies psi", "X phi",
   "F phi", "G phi", "phi U psi", or "phi R psi" where "phi" and "psi"
   are LTL path formulas.

Since the temporal operator "F", "G", and "R" can be expressed by using
"U" and "not", the LTL restricted language that allows only path
formulas having the form "p", "not phi", "phi or psi", "X phi", or
"phi U psi" is equivalent to the full LTL language (e.g., see
[Clarke2000]_).


[P77]   A. Pnueli. "The temporal logic of programs." In Proceedings of the
        18th Annual Symposium of Foundations of Computer Science (FOCS),
        1977, 46-57.
[CGP00] E. M. Clarke, O. Grumberg, D. A. Peled. "Model Checking" MIT Press,
        Cambridge, MA, USA. 2000.
'''

from .language import *
from .model_checking import modelcheck
from pyModelChecking.CTLS import LNot as LNot
