# pyModelChecking
pyModelChecking is a simple Python model checking package. Currently, it is able to represent 
[Kripke structures][Kripke] and [CTL][CTL] formulas and it provides [model checking][modelchecking] 
methods for them. In future, it will hopefully support [LTL][LTL], [CTL*][CTLS], and other temporal logics as well.

[Kripke]: https://en.wikipedia.org/wiki/Kripke_structure_%28model_checking%29
[CTL]: https://en.wikipedia.org/wiki/Computation_tree_logic
[modelchecking]: https://en.wikipedia.org/wiki/Model_checking
[LTL]: https://en.wikipedia.org/wiki/Linear_temporal_logic
[CTLS]: https://en.wikipedia.org/wiki/CTL*

### A simple example
```python
>>> from pyModelChecking import *

>>> K=Kripke(S=[0,1,2,3],
...          R=[(0,1),(1,2),(2,2),(3,3)],
...          L={0: set(['p']), 1:set(['p','q']),3:set(['p'])})

>>> from pyModelChecking.CTL import *

>>> phi=AU(True,Or('q',Not(EX('p'))))

>>> print phi

A(True U (q or not (EX p)))

>>>  modelcheck(K,phi)

set([0, 1, 2])

```

### Copyright and license

pyModelChecking
Copyright (C) 2015  Alberto Casagrande <acasagrande@units.it>

pyModelChecking is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
