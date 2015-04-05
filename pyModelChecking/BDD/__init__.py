'''
This module represents the OBDD.

Oredered Binary Decision Diagrams are data structures to represent binary
functions.

[CGP00] E. M. Clarke, O. Grumberg, D. A. Peled. "Model Checking" MIT Press,
        Cambridge, MA, USA. 2000.
'''


from .BDD import BDDNode
from .ordering import Ordering
from .OBDD import OBDD
#from .OBDD import BooleanParser
