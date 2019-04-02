from pyModelChecking.kripke import *
import unittest


class TestKripke(unittest.TestCase):

    def setUp(self):
        self.S = set([0, 1, 3])
        self.S0 = set([0, 1, 6])
        self.R = set([(0, 2), (2, 2), (0, 1), (1, 0), (3, 2)])

        self.L = {1: set(['p', 'q']), 2: set(['p', 'q']), 3: set(['q'])}

        self.K = Kripke(self.S, self.S0, self.R, self.L)

    def test_init(self):
        S = set(self.S)
        for (s, d) in self.R:
            S.add(s)
            S.add(d)

        self.assertEqual(set(self.K.states()), S)

        with self.assertRaises(RuntimeError):
            Kripke(self.S, self.S0, self.R | set([(2, 4)]), self.L)

    def test_nodes(self):
        S = self.S | set([2])

        self.assertEqual(set(self.K.states()), S)

    def test_edges(self):
        self.assertEqual(set(self.K.transitions()), self.R)

    def test_labels(self):
        AP = set()
        for ap in self.L.values():
            AP.update(ap)

        self.assertEqual(self.K.labels(), AP)

        for v in set(self.K.states())-set(self.L.keys()):
            self.assertEqual(self.K.labels(v), set())

        for v in set(self.L.keys()):
            self.assertEqual(self.K.labels(v), self.L[v])

        with self.assertRaises(RuntimeError):
            self.K.labels('a')

    def test_next(self):

        for s in self.K.nodes():
            N = set()
            for (p, q) in self.K.edges_iter():
                if s == p:
                    N.add(q)

            self.assertEqual(self.K.next(s), N)

        with self.assertRaises(RuntimeError):
            self.K.next('a')


if __name__ == '__main__':
    unittest.main()
