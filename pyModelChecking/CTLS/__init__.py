"""
.. module:: CTLS
   :synopsis: Represents the CTL* language and provides model
              checking methods for it.

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>
"""

from .language import *
from .model_checking import modelcheck

from ..language import LNot

from .parser import Parser
