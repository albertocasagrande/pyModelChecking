"""A simple Python Model Checking package

.. moduleauthor:: Alberto Casagrande <acasagrande@units.it>

"""

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015-2020"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__release__ = "1.3"
__subrelease__ = "3"
__version__ = __release__+"."+__subrelease__
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

from .kripke import *
from .language import *

name = "pyModelChecking"
