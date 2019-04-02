import ast

from .BDD import BDDNode
from .BDD import apply as BDDapply
from .ordering import *


def parse_args(args_node):
    return Ordering([id(arg) for arg in args_node.args])


def parse_name(ordering, node):
    if node.id == 'True':
        return OBDD(BDDNode(True), ordering)
    if node.id == 'False':
        return OBDD(BDDNode(False), ordering)

    return OBDD(BDDNode(node.id, BDDNode(False), BDDNode(True)), ordering)


def parse_binary_unary_op(ordering, node):
    if (isinstance(node.op, ast.Not) or isinstance(node.op, ast.Invert)):

        return ~parse_binary_expr(ordering, node.operand)


def parse_binary_op(ordering, node):
    if isinstance(node.op, ast.BitAnd):
        return (parse_binary_expr(ordering, node.left) &
                parse_binary_expr(ordering, node.right))

    if isinstance(node.op, ast.BitOr):
        return (parse_binary_expr(ordering, node.left) |
                parse_binary_expr(ordering, node.right))

    raise SyntaxError('expected a binary operator, got a ' +
                      '{}'.format(node.op.__class__))


def parse_binary_binary_op(ordering, node):
    if isinstance(node.op, ast.And):
        result = OBDD(BDDNode(True), ordering)
        for arg in node.values:
            result = result & parse_binary_expr(ordering, arg)

        return result

    if isinstance(node.op, ast.Or):
        result = OBDD(BDDNode(False), ordering)
        for arg in node.values:
            result = result | parse_binary_expr(ordering, arg)

        return result

    raise SyntaxError('expected a binary operator, got a ' +
                      '{}'.format(node.op.__class__))


def parse_binary_expr(ordering, node):
    if isinstance(node, ast.BinOp):
        return parse_binary_op(ordering, node)

    if isinstance(node, ast.BoolOp):
        return parse_binary_binary_op(ordering, node)

    if isinstance(node, ast.UnaryOp):
        return parse_binary_unary_op(ordering, node)

    if isinstance(node, ast.Name):
        return parse_name(ordering, node)

    if isinstance(node, ast.Num):
        if node.n in [0, 1]:
            return OBDD(BDDNode(node.n), ordering)

        raise SyntaxError('expected a binary expression, got number ' +
                          '{}'.format(node.n))

    raise SyntaxError('expected a binary expression, got a ' +
                      '{}'.format(node.__class__))


class BinaryParser(object):
    '''
    A class to represent parsers of binary functions.

    The objects of this class can parse strings representing binary functions
    are return the corresponding OBDD.

    '''

    def __init__(self, ordering):
        ''' Initialize a binary parser.

        :param ordering: an ordering for the variables to be parsed
        :type ordering: Ordering
        '''
        if not isinstance(ordering, Ordering):
            try:
                ordering = Ordering(ordering)
            except TypeError:
                raise TypeError('expected an Ordering of variables, got ' +
                                '{}'.format(ordering))

        self.ordering = ordering

    @staticmethod
    def parse_function(binary_funct):
        ''' Parse a binary function.

        :param ordering: an ordering for the variables to be parsed
        :type ordering: Ordering
        '''
        st = ast.parse(binary_funct)

        try:
            args_node = st.body[0].value.args

            body_node = st.body[0].value.body

        except Exception:
            raise SyntaxError('expected a binary lambda function, got ' +
                              '{}'.format(binary_funct))

        ordering = parse_args(args_node)
        return parse_binary_expr(ordering, body_node)

    def parse(self, binary_expr):
        st = ast.parse(binary_expr)
        try:
            binary_expr_node = st.body[0].value
        except Exception:
            raise SyntaxError('expected a binary expression, got ' +
                              '{}'.format(binary_expr))

        return parse_binary_expr(self.ordering, binary_expr_node)


class OBDD(object):
    '''
    A class to represent Ordered Binary Decision Diagrams (OBDDs).
    '''

    def __init__(self, bfunct, ordering=None, check_ordering=True):
        ''' Initialize an OBDD.

        :param bfunct: either a BDDNode,  a string that represents a binary
                expression,  or a string that represent a binary function in
                lambda notation
        :type bfunct: str or function
        :param ordering: an ordering for the variables to be parsed
        :type ordering: Ordering
        :param check_ordering: a binary flag: if bfunct is a BDDNode and this
                               flag is set to True,  then this method check
                               whether the BDDNode respects the ordering
        :type check_ordering: bool
        '''
        if ordering is None:
            obdd = BinaryParser.parse_function(bfunct)
            self.ordering = obdd.ordering
            self.root = obdd.root

            return

        if not isinstance(ordering, Ordering):
            try:
                ordering = Ordering(ordering)
            except TypeError:
                raise TypeError('expected an Ordering of variables, got ' +
                                '{}'.format(ordering))

        self.ordering = ordering

        if isinstance(bfunct, BDDNode):
            if check_ordering and not bfunct.respect_ordering(ordering):
                raise ValueError('the BDDNode {} '.format(bfunct) +
                                 'does not respect {}'.format(ordering))

            self.root = bfunct
        else:
            if isinstance(bfunct, str):
                bparser = BinaryParser(ordering)
                self.root = (bparser.parse(bfunct)).root
            else:
                raise TypeError('expected a BDDNode or a str, got ' +
                                '{}'.format(bfunct))

    def restrict(self, var, value):
        ''' Partially evaluate the binary function encoded by an OBDD.

        :param var: name of the variable to be set
        :type var: str
        :param value: value to be set
        :type value: bool or int
        :returns: the OBDD representing the partial evaluation of :math:`f`
                  with :param var: set to :param value: where :math:`f` is
                  the function encoded by current object
        :rtype: OBDD
        '''
        return OBDD(self.root.restrict(var, value), self.ordering)

    def variables(self):
        ''' Return the variables in an OBDD.

        :returns: the set of the variables represented in the OBDD
        :rtype: set
        '''
        return self.root.variables()

    def __eq__(self, A):
        ''' Check whether two OBDD are the same.

        :param A: either a BDDNode,  an OBDD,  a binary,  or a Boolean value
        :type A: BDDNode,  OBDD,  binary,  or Boolean value
        :returns: True if the two OBDD are the same and respect the same
                  ordering,  False otherwise
        :rtype: bool
        '''
        if isinstance(A, BDDNode):
            return self == OBDD(A, self.ordering)

        if isinstance(A, OBDD):
            return self.root is A.root and self.ordering == A.ordering

        if A in set([0, 1, True, False]):
            return self == OBDD(BDDNode(A), self.ordering)

        raise TypeError('expected an OBDD, got %s' % (A))

    def __req__(self, A):
        ''' Check whether two OBDD are the same.

        :param A: either a BDDNode,  an OBDD,  a binary,  or a Boolean value
        :type A: BDDNode,  OBDD,  binary,  or Boolean value
        :returns: True if the two OBDD are the same and respect the same
                  ordering,  False otherwise
        :rtype: bool
        '''
        return self == A

    def apply(self, operator, B):
        ''' Apply a binary binary operator to two OBDD.

        :param operator: a binary boolean operator
        :type operator: function
        :param A: an OBDD
        :type A: OBDD
        :param B: an OBDD
        :type B: OBDD
        :returns: The OBDD obtained by applying the operator to the two OBDD
        :rtype: OBDD
        '''

        if not isinstance(B, OBDD):
            raise TypeError('expected an OBDD, got {}'.format(B))

        if self.ordering != B.ordering:
            raise RuntimeError('Unsupported operation: {}'.format(self) +
                               ' and {} '.format(B) +
                               'have different variable ordering')

        result_cache = dict()

        bdd = BDDapply(operator, self.root, B.root, self.ordering,
                       result_cache)
        return OBDD(bdd, self.ordering, check_ordering=False)

    def __and__(self, A):
        ''' Build the conjunction of two OBDD.

        :param A: an OBDD
        :type A: OBDD
        :returns: the OBDD that represents the logical conjunction of
                  the two OBDD
        :rtype: OBDD
        '''
        return self.apply((lambda a, b: a and b), A)

    def __or__(self, A):
        ''' Build the non-exclusive disjunction of two OBDD.

        :param A: an OBDD
        :type A: OBDD
        :returns: the OBDD that represents the logical non-exclusive
                  disjunction of the two OBDD
        :rtype: OBDD
        '''
        return self.apply((lambda a, b: a or b), A)

    def __xor__(self, A):
        ''' Build the exclusive disjunction of two OBDD.

        :param A: an OBDD
        :type A: OBDD
        :returns: the OBDD that represents the logical exclusive disjunction
                  of the two OBDD
        :rtype: OBDD
        '''
        return self.apply((lambda a, b: a ^ b), A)

    def __invert__(self):
        ''' Build the negation of an OBDD.

        :param A: an OBDD
        :type A: OBDD
        :returns: the OBDD that represents the logical negation of the OBDD
        :rtype: OBDD
        '''
        return OBDD(~self.root, self.ordering)

    def __str__(self):
        ''' Return a string that represents an OBDD

        :returns: a string that represents the OBDD
        :rtype: str
        '''
        if isinstance(self.ordering, ListOrdering):
            result = 'lambda'
            sep = ' '
            for var in self.ordering.get_list():
                result += '{}{}'.format(sep, var)
                sep = ','

            return result+': {}'.format(self.root)

        return '{}'.format(self.root)

    def __repr__(self):
        ''' Return a string that represents an OBDD

        :returns: a string that represents the OBDD
        :rtype: str
        '''
        return '{}'.format(str(self))
