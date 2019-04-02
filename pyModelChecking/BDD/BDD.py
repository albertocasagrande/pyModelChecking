from weakref import WeakSet
from .ordering import Ordering


def BDDsons_and_BDD(operator, A, B, ordering, r_cache):
    low = apply(operator, A.low, B, ordering, r_cache)
    high = apply(operator, A.high, B, ordering, r_cache)
    return BDDNonTerminalNode(A.var, low, high)


def BDD_and_BDDsons(operator, A, B, ordering, r_cache):
    low = apply(operator, A, B.low, ordering, r_cache)
    high = apply(operator, A, B.high, ordering, r_cache)
    return BDDNonTerminalNode(B.var, low, high)


def BDDsons_and_BDDsons(operator, A, B, ordering, r_cache):
    low = apply(operator, A.low, B.low, ordering, r_cache)
    high = apply(operator, A.high, B.high, ordering, r_cache)
    return BDDNonTerminalNode(A.var, low, high)


def apply(operator, A, B, ordering, r_cache):
    if A not in r_cache:
        r_cache[A] = dict()

    if B in r_cache[A]:
        return r_cache[A][B]

    r_cache[A][B] = compute(operator, A, B, ordering, r_cache)

    return r_cache[A][B]


def compute(operator, A, B, ordering, r_cache):
    if isinstance(A, BDDTerminalNode):
        if isinstance(B, BDDTerminalNode):
            return BDDTerminalNode(operator(A.value, B.value))

        return BDD_and_BDDsons(operator, A, B, ordering, r_cache)

    if (isinstance(B, BDDTerminalNode) or ordering.in_order(A.var, B.var)):
        return BDDsons_and_BDD(operator, A, B, ordering, r_cache)

    if A.var == B.var:
        return BDDsons_and_BDDsons(operator, A, B, ordering, r_cache)

    if ordering.in_order(B.var, A.var):
        return BDD_and_BDDsons(operator, A, B, ordering, r_cache)

    raise RuntimeError('Unsupported configuration %s %s' % A,  B)


def descendents(root, checked=None):
    if checked is None:
        checked = set()

    desc = set()
    stack = [root]

    while stack:
        node = stack.pop()
        if node not in desc and node not in checked:
            desc.add(node)

            if (isinstance(node, BDDNonTerminalNode)):
                stack.append(node.low)
                stack.append(node.high)

    return desc


def ancestors(leaf, checked=None):
    if checked is None:
        checked = set()

    anc = set()
    stack = [leaf]

    while stack:
        node = stack.pop()
        if node not in anc and node not in checked:
            anc.add(node)

            stack.extend((node.f_low | node.f_high-checked)-anc)

    return anc


class BDDNode(object):
    '''
    A class to represent Binary Decision Diagram (BDD) nodes.
    '''
    def __new__(cls, *data):
        if len(data) == 1:
            return BDDTerminalNode(data[0])

        if len(data) == 3:
            return BDDNonTerminalNode(*data)

        raise RuntimeError('passed {} parameters, '.format(len(data)) +
                           'but only  BDDNode(value) for terminal node and ' +
                           'BDDNode(var, low, high) for non terminal node ' +
                           'have been implemented')

    def __hash__(self):
        ''' Compute a hash for a BDDNode

        :returns: the id of `self`
        :rtype: int
        '''
        return id(self)

    def restrict(self, var, value):
        ''' Partially evaluate the binary function encoded by a BDD.

        :param var: name of the variable to be set
        :type var: str
        :param value: value to be set
        :type value: bool or int
        :returns: the BDDNode representing the partial evaluation of
                  :math:`f` with :param var: set to :param value: where
                  :math:`f` is the function encoded by the object
        :rtype: BDDNode
        '''
        if isinstance(value, int):
            if value == 1:
                value = True
            if value == 0:
                value = False

        if not (isinstance(var, str) and isinstance(value, bool)):
            raise TypeError('expected a pair (str, bool), ' +
                            'got ({}, {})'.format(var.__class__,
                                                  value.__class__))

        return cache_restrict(self, var, value, dict())

    def __reset__(self):
        self.f_low = WeakSet()
        self.f_high = WeakSet()

    def descendents(self):
        ''' Computes the descendents of this node.

        :returns: the set of nodes that have the current object as ancestor
        :rtype: set of :class:`BDDNode`
        '''
        return descendents(self, set())

    def ancestors(self):
        ''' Computs the ancestors of this node.

        :returns: the set of nodes that have the current object as descendent
        :rtype: set of :class:`BDDNode`
        '''
        return ancestors(self, set())

    @staticmethod
    def nodes():
        ''' Return all the BDD nodes stored in memory.

        :returns: all the BDD nodes that are stored in memory
        :rtype: set of `BDDNode`
        '''
        return BDDNode(0).ancestors() | BDDNode(1).ancestors()

    def variables(self):
        ''' Return the variables contained into a BDD.

        :returns: all the variable that label some the descendents of this node
        :rtype: set of str
        '''
        return set([node.var for node in self.descendents()
                    if isinstance(node, BDDNonTerminalNode)])

    def __repr__(self):
        return self.__str__()


def find_isomorph(var, low, high):
    if len(low.f_low) < len(high.f_high):
        node_set = low.f_low
        lh_test = (lambda low, high: high is node.high)
    else:
        node_set = high.f_high
        lh_test = (lambda low, high: low is node.low)

    for node in node_set:
        if (isinstance(node, BDDNonTerminalNode) and var == node.var and
                lh_test(low, high)):
            return node

    return None


def cache_restrict(bdd, var, value, r_cache):
    if bdd in r_cache:
        return r_cache[bdd]

    r_cache[bdd] = compute_restrict(bdd, var, value, r_cache)

    return r_cache[bdd]


def compute_restrict(bdd, var, value, r_cache):
    if isinstance(bdd, BDDTerminalNode):
        return bdd

    if bdd.var == var:
        if value:
            return cache_restrict(bdd.high, var, value, r_cache)
        else:
            return cache_restrict(bdd.low, var, value, r_cache)
    else:
        low = cache_restrict(bdd.low, var, value, r_cache)
        high = cache_restrict(bdd.high, var, value, r_cache)

        return BDDNonTerminalNode(bdd.var, low, high)


class BDDNonTerminalNode(BDDNode):
    def __new__(cls, var, low, high):
        for p in [low, high]:
            if not isinstance(p, BDDNode):
                raise TypeError('expected an BBD node, got {}'.format(p))

        if low is high:
            return low

        node = find_isomorph(var, low, high)
        if node is not None:
            return node

        node = super(BDDNode, cls).__new__(cls)
        node.__reset__(var, low, high)

        return node

    def respect_ordering(self, O, checked=None):
        ''' Test whether a BDDNode respects an ordering.

        :param O: the ordering to be tested
        :type O: Ordering
        :param checked: already checked nodes
        :type checked: set
        :returns: True if and only if the variable of `node` is smaller that
                  those of `node.low` and `node.high` for any node in the
                  subgraph rooted in this object
        :rtype: bool
        '''
        if not isinstance(O, Ordering):
            TypeError('expected an Ordering, got {}'.format(O))

        if checked is None:
            checked = set()

        if self in checked:
            return True

        if self.var not in O:
            raise RuntimeError('%s in not in %s' % (self.var, O))

        for son in [self.low, self.high]:
            if (isinstance(son, BDDNonTerminalNode) and
                    not O.in_order(self.var, son.var)):
                return False

        if (self.high.respect_ordering(O, checked) and
                self.low.respect_ordering(O, checked)):
            checked.add(self)

            return True

        return False

    def __reset__(self, var, low, high):
        ''' Reset the value of a BDDNonTerminalNode.

        :param var: variable name
        :type var: str
        :param low: the low BDDNode
        :type low: BDDNode
        :param high: the high BDDNode
        :type high: BDDNode
        '''
        super(BDDNonTerminalNode, self).__reset__()

        self.var = var
        self.low = low
        self.high = high

        self.low.f_low.add(self)
        self.high.f_high.add(self)

    def __invert__(self, r_cache=None):
        ''' Invert the binary function represented by a BDDNode.

        :param r_cache: a dictionary that caches already computed results
        :type r_cache: dict or None
        :returns: the BDDNode representing the function `1-f` where `f` is the
                  function depicted by `self`
        :rtype: BDDNode
        '''
        if r_cache is None:
            r_cache = dict()

        if self in r_cache:
            return r_cache[self]

        r_cache[self] = BDDNonTerminalNode(self.var,
                                           self.low.__invert__(r_cache),
                                           self.high.__invert__(r_cache))
        return r_cache[self]

    def __hash__(self):
        return id(self)

    def __eq__(self, O):
        ''' Test the equivalence of two BDDs.

        :param O: a BDD node
        :type O: BDDNode
        :returns: `True` if the two BDDs rooted in `self` and `O` are
                  isomorph,  `False`,  otherwise
        :rtype: bool
        '''
        return self is O

    def __str__(self):
        ''' Produce a string that represents a BDD.

        :returns: a string that represents the BDD rooted in `self`
        :rtype: str
        '''
        repr = []

        for succ,  neg in [(self.low, '~'), (self.high, '')]:
            if isinstance(succ, BDDTerminalNode):
                if succ.value:
                    repr.append('%s%s' % (neg, self.var))
            else:
                repr.append('%s%s & %s' % (neg, self.var, succ))

        if len(repr) == 2:
            return '(%s) | (%s)' % (repr[0], repr[1])

        return repr[0]


class BDDTerminalNode(BDDNode):
    Tnodes = {}

    def __new__(cls, value):
        if not (value in set([0, 1, False, True])):
            raise TypeError('expected a value among [0, 1, False, True], ' +
                            'got {}'.format(value))

        if value not in BDDTerminalNode.Tnodes:
            node = super(BDDNode, cls).__new__(cls)

            # reset the node and set the node value
            node.__reset__(value)

            BDDTerminalNode.Tnodes[value] = node

        return BDDTerminalNode.Tnodes[value]

    def respect_ordering(self, O, checked=None):
        ''' Test whether a BDDNode respects an Ordering or not.

        :param O: the ordering to be tested
        :type O: Ordering
        :param checked: already checked nodes
        :type checked: set
        :returns: True
        :rtype: bool
        '''
        return True

    def __reset__(self, value):
        ''' Reset the value of a BDDTerminalNode.

        :param value: the new value
        :type value: bool
        '''
        super(BDDTerminalNode, self).__reset__()
        self.value = value

    def __invert__(self, r_cache=None):
        ''' Invert the binary function represented by a BDDNode.

        :param r_cache: a dictionary that caches already computed results
        :type r_cache: dict or None
        :returns: the BDDNode representing the function `1-f` where `f` is the
                  function depicted by `self`
        :rtype: BDDNode
        '''
        if r_cache is None:
            r_cache = dict()

        if self in r_cache:
            return r_cache[self]

        r_cache[self] = BDDTerminalNode(not self.value)

        return r_cache[self]

    def __hash__(self):
        return id(self)

    def __eq__(self, O):
        ''' Test the equivalence of two BDDs.

        :param O: a BDD node
        :type O: BDDNode
        :returns: `True` if the two BDDs rooted in `self` and `O` are
                  isomorph,  `False`,  otherwise
        :rtype: bool
        '''
        return self is O

    def __str__(self):
        if self.value:
            return '1'
        return '0'
