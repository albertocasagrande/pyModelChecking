from pyModelChecking.graph import *
import unittest


class TestDiGraph(unittest.TestCase):

    def setUp(self):
        self.V = set([0, 1, 3, 4])
        self.E = set([(0, 2), (2, 2), (0, 1), (1, 0)])

        self.G = DiGraph(self.V, self.E)

    def test_init(self):
        V = set(self.V)
        for (s, d) in self.E:
            V.add(s)
            V.add(d)

        self.assertEqual(set(self.G.nodes()), V)

    def test_nodes(self):
        V = (self.V | set([2]))

        self.assertEqual(set(self.G.nodes()), V)

    def test_edges(self):
        self.assertEqual(set(self.G.edges_iter()), self.E)

    def test_add_node(self):

        V = (set(self.G.nodes()) | set([5]))

        self.G.add_node(5)

        self.assertEqual(set(self.G.nodes()), V)

        with self.assertRaises(RuntimeError):
            self.G.add_node(0)

    def test_add_edge(self):

        E = set(self.G.edges_iter()) | set([(0, 3)])
        V = set(self.G.nodes()) | set([0, 3])

        self.G.add_edge(0, 3)

        self.assertEqual(set(self.G.nodes()), V)
        self.assertEqual(set(self.G.edges_iter()), E)

        self.G.add_edge(0, 6)

        E = E | set([(0, 6)])
        V = V | set([0, 6])

        self.assertEqual(set(self.G.nodes()), V)
        self.assertEqual(set(self.G.edges_iter()), E)

        with self.assertRaises(RuntimeError):
            self.G.add_edge(0, 6)

    def test_sources(self):
        S = set()
        for (s, d) in self.G.edges_iter():
            S.add(s)

        self.assertEqual(set(self.G.sources()), S)

    def test_next(self):

        for s in set(self.G.nodes()):
            N = set()
            for (p, q) in self.G.edges_iter():
                if s == p:
                    N.add(q)

            self.assertEqual(self.G.next(s), N)

    def test_reversed(self):
        rG = self.G.get_reversed_graph()

        rE = []
        for (s, d) in self.G.edges_iter():
            rE.append((d, s))

        self.assertEqual(set(rE), set(rG.edges_iter()))
        self.assertEqual(set(self.G.nodes()), set(rG.nodes()))

    def test_subgraph(self):
        Vp = set([0, 1, 4, 5])
        SG = self.G.get_subgraph(Vp)

        GE = set(self.G.edges_iter())
        self.assertEqual(Vp & set(self.G.nodes()), set(SG.nodes()))
        for (s, d) in SG.edges_iter():
            self.assertIn(s, Vp)
            self.assertIn(d, Vp)

            self.assertIn((s, d), GE)

    def test_strongly_connected_components(self):
        SCCs = set([frozenset([0, 1]), frozenset([2]), frozenset([3]),
                    frozenset([4])])

        list_SCCs = [frozenset(s) for s in compute_SCCs(self.G)]
        computed_SCCs = set(list_SCCs)

        self.assertEqual(computed_SCCs, SCCs)


if __name__ == '__main__':
    unittest.main()
