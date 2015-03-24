'''
This package represents the CTL language and provides model checking methods for it.

The **Computational Tree Language** or **CTL** is a subset of the temporal
language CTL* ([BMP83]_,[CE81]_,[CE80]_). In CTL, beside the standard
logical operators "not", "and", "or", and "implies" each occurence of the
two path quantifiers "A" and "E" should be coupled to one of the temporal
operators "X", "G", "F", "U", or "R". More formally, we distinguish CTL
*state formulas* (i.e., formulas that are evaluated in a single state)
from CTL *path formulas* (i.e., formulas that are evaluated over an
infinite path).

A CTL state formula is either:
- an atomic proposition
- "not phi", "phi or psi", "phi and psi", or "phi implies psi" where
  both "phi" and "psi" are CTL state formulas
- "A phi" or "E phi" if "phi" is a CTL path formula

A CTL path formula is either "X phi", "F phi", "G phi", "phi U psi", or
"phi R psi" where "phi" and "psi" are CTL state formulas.

Despite the apperent syntatic complexity of CTL, any possible property
definable in it can be expressed by a CTL formula whose syntax is restricted
to the use of "not", "or", and "E" coupled to either "X", "U", or "G" (e.g.,
see [Clarke2000]_).

[BMP83] M. Ben-Ari, Z. Manna, A. Pnueli. The temporal logic of branching
        time. Acta Informatica 20(1983): 207-226
[CE81]  E. M. Clarke, E. A. Emerson. "Design and synthesis of
        synchronization skeletons using branching time temporal logic." In
        Logic of Programs: Workshop. LNCS 131. Springer, 1981.
[CE80]  E. M. Clarke, E. A. Emerson. "Characterizing correcteness properties
        of parallel programs using fixpoints." In Automata, Languages, and
        Programming. LNCS 85:169-181. Springer 1980.
[CGP00] E. M. Clarke, O. Grumberg, D. A. Peled. "Model Checking" MIT Press,
        Cambridge, MA, USA. 2000.
'''

from .language import *
from .model_checking import modelcheck
from pyModelChecking.CTLS import LNot as LNot
