# pyModelChecking
*pyModelChecking* is a small Python model checking package. Currently, it is 
able to represent [Kripke structures][Kripke], [CTL][CTL], [LTL][LTL], and 
[CTL*][CTLS] formulas and it provides [model checking][modelchecking] methods 
for LTL, CTL, and CTL*. In future, it will hopefully support symbolic model 
checking.

[Kripke]: https://en.wikipedia.org/wiki/Kripke_structure_%28model_checking%29
[CTL]: https://en.wikipedia.org/wiki/Computation_tree_logic
[modelchecking]: https://en.wikipedia.org/wiki/Model_checking
[LTL]: https://en.wikipedia.org/wiki/Linear_temporal_logic
[CTLS]: https://en.wikipedia.org/wiki/CTL*

### Documentation

[Here][last_doc] you can find the *pyModelChecking* documenation. It contains:
* a brief introduction to Kripke structures, temporal logics and model checking
* the user manual and some examples
* the API manual  

[last_doc]: https://pymodelchecking.readthedocs.io/

### Examples

First of all, import all the functions and all the classes in the package.

```python
>>> from pyModelChecking import *
```

In order to represent a Kripke structure use the `Kripke` class.

```
>>> K=Kripke(R=[(0,0),(0,1),(1,2),(2,2),(3,3)],
...          L={0: set(['p']), 1:set(['p','q']),3:set(['p'])})
```

CTL can be represented by importing the `CTL` module.

```python
>>> from pyModelChecking.CTL import *

>>> phi=AU(True,Or('q',Not(EX('p'))))

>>> print(phi)

A(True U (q or not (EX p)))
```

Whenever a non-CTL formula is built, an exception is thrown.

```python
>>> psi=A(F(G('p')))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "pyModelChecking/CTL/language.py", line 42, in __init__
    self.wrap_subformulas(phi,StateFormula)
  File "pyModelChecking/CTLS/language.py", line 59, in wrap_subformulas
    phi.__desc__,phi))
TypeError: expected a CTL state formula, got the CTL path formula G p
```

It is also possible to parse a string representing a CTL formula by using 
the `Parser` class in the module `CTL`.

```python
>>> parser = Parser()

>>> psi = parser("A(true U (q or not E X p))")

>>> print(psi)

A(True U (q or not EX p))

>>> print(psi.__class__)

<class 'pyModelChecking.CTL.language.A'>
```

The function `modelcheck` in the module `CTL` finds the states of Kripke 
structure that model a given CTL formula.

```python
>>>  modelcheck(K,phi)

set([1, 2])
```

The formula `AFG p`, which we tried to build above, is a LTL formula. The 
`LTL` module can be used to represent and model check it on any Kripke 
structure.

```python
>>> from pyModelChecking.LTL import *

>>> psi=A(F(G('p')))

>>> print(psi)

A(G(F(p))

>>> modelcheck(K,psi)

set([3])
```

Strings representing formulas in the opportune language can be used as a 
parameter of the model checking function too.

```python
>>> modelcheck(K,'A G F p')

set([3])
```

The module `CTLS` is meant to deal with CTL* formulas. It can also combine and 
model checks CTL and LTL formulas.

```python
>>> from pyModelChecking.CTLS import *

>>> eta=A(F(E(U(True,Imply('p',Not('q'))))))

>>> print(eta,eta.__class__)

(A(F(E((True U (p --> not q))))), <class 'pyModelChecking.CTLS.language.A'>)

>>> rho=A(G(And(X('p'),'p')))

>>> print(rho,rho.__class__)

(A(G((X(p) and p))), <class 'pyModelChecking.CTLS.language.A'>)

>>> gamma=And(phi, psi)

>>> print(gamma,gamma.__class__)

(A(True U (q or not (EX p))) and A(G(F(p)))), <class 'pyModelChecking.CTLS.language.And'>)

>>> modelcheck(K,eta)

set([0, 1, 2, 3])

>>> modelcheck(K, psi)

set([3])

>>> modelcheck(K, gamma)

set([])

```

Whenever a CTL* formula is a CTL formula (LTL formula), CTL (LTL) model 
checking can be applied to it.

```python
>>> import pyModelChecking.CTL as CTL

>>> CTL.modelcheck(K,eta)

set([0, 1, 2, 3])

>>> CTL.modelcheck(K,rho)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "pyModelChecking/CTL/model_checking.py", line 183, in modelcheck
    raise RuntimeError('%s is not a CTL formula' % (formula))
RuntimeError: A(G((X(p) and p))) is not a CTL formula

>>> import pyModelChecking.LTL as LTL

>>> LTL.modelcheck(K,rho)

set([3])
```

### Copyright and license

pyModelChecking
Copyright (C) 2015-2019  Alberto Casagrande <acasagrande@units.it>

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
