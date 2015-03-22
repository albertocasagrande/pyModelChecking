'''
This module represents the CTL* language.

The Computational Tree Language* or CTL* is a the temporal logic that
describes the properties of computation trees over Kripke structures
([CE81],[CES86]). Beside a set of atomic propostions and the standard
logical operators "not", "and", "or", and "implies", the alphabet of CTL*
contains the two path quantifiers "A" ("for all paths") and "E" ("for some
path") and the five temporal operators "X" ("at the next step"), "G"
("globally"), "F" ("in the future"), "U" ("until"), and "R" ("release").

Any CTL* formula is either a *state formula* (i.e., a formula that are
evaluated in a single state) or a *path formula* (i.e., a formula whose
truth value depend on an infinite path).

A CTL* state formula is either:
- an atomic proposition
- "not phi", "phi and psi", "phi or psi", or "phi implies psi" where both
  "phi" and "psi" are CTL* state formulas
- "A phi" or "E phi" where "phi" is a CTL* path formula

A CTL* path formula is either:
- a state formula
- "not phi", "phi and psi", "phi or psi", or "phi implies psi" where both
  "phi" and "psi" are CTL* path formulas
- "X phi", "F phi", "G phi", "phi U psi", or "phi R psi" where "phi"
  and "psi" are CTL path formulas

Since the temporal operator "F", "G", and "R" can be expressed by using
"U" and "not" and the formula "A phi" is equivalent to "not E not phi",
the CTL* language restricted to "not", "or", "X", "U", and "A" is
equivalent to the full CTL* language (e.g., see [CGP00]).


[CE81]  E. M. Clarke, E. A. Emerson. "Design and synthesis of
        synchronization skeletons using branching time temporal logic." In
        Logic of Programs: Workshop. LNCS 131. Springer, 1981.
[CES86] E. M. Clarke, E. A. Emerson, A. P. Sistla. "Automatic verification
        of finite-state concurrent systems using temporal logic
        specifications." ACM Transactions on Programming Languages and
        Systems 8(2): 244-263. 1986.
        synchronization skeletons using branching time temporal logic." In
        Logic of Programs: Workshop. LNCS 131. Springer, 1981.
[CGP00] E. M. Clarke, O. Grumberg, D. A. Peled. "Model Checking" MIT Press,
        Cambridge, MA, USA. 2000.
'''

from .language import *
from .model_checking import modelcheck
