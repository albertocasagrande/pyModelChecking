class Ordering(object):
    '''
    A class representing variable ordering.

    '''

    def __new__(cls, ordering):
        if isinstance(ordering, list):
            return ListOrdering(ordering)

        TypeError('unsupported ordering %s' % (ordering))

    def __eq__(self, ordering):
        raise RuntimeError('not implemented')

    def __ne__(self, ordering):
        return not (self == ordering)

    def in_order(self, x, y):
        raise RuntimeError('not implemented')

    def cmp(self, x, y):
        raise RuntimeError('not implemented')

    def __contains__(self, var):
        raise RuntimeError('not implemented')


class FunctionOrdering(Ordering):
    '''
    A class representing variable ordering specified by a function.

    '''

    def __new__(cls, ordering):
        return super(Ordering, cls).__new__(cls)

    def __init__(self, ordering):
        if not isinstance(ordering, function):
            TypeError('expected a function, got %s' % (ordering))

        self.ordering = ordering

    def __eq__(self, ordering):
        if not isinstance(ordering, FunctionalOrdering):
            return False

        return self.ordering is ordering.ordering

    def in_order(self, x, y):
        return self.ordering(x, y)

    def __contains__(self, var):
        return True

    def cmp(self, x, y):
        if x == y:
            return 0

        if self.in_order(x, y):
            return -1

        return 1

    def __str__(self):
        return '%s' % (self.ordering)


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


class ListOrdering(Ordering):
    '''
    A class representing variable ordering specified by a list.

    '''

    def __new__(cls, ordering):
        return super(Ordering, cls).__new__(cls)

    def __init__(self, ordering):
        if not isinstance(ordering, list):
            TypeError('expected a list, got %s' % (ordering))

        self.ordering = dict()

        i = 0
        for obj in ordering:
            if obj in self.ordering:
                raise RuntimeError('%s is repeated in %s' % (obj, ordering))
            self.ordering[obj] = i
            i += 1

    def __eq__(self, ordering):
        if not isinstance(ordering, ListOrdering):
            return False

        return self.ordering == ordering.ordering

    def in_order(self, x, y):
        return self.cmp(x, y) < 0

    def __contains__(self, var):
        return var in self.ordering

    def cmp(self, x, y):
        return self.ordering[x]-self.ordering[y]

    def get_list(self):
        return sorted(self.ordering.keys(), 
                      key=cmp_to_key((lambda x, y: self.cmp(x, y))))

    def __str__(self):
        return '%s' % (self.get_list())
