#!/usr/bin/env python

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

class DiGraph(object):
    '''
    A class to represent directed graphs.

    A *directed graph* is a couple (V,E) where V is a set of vertices and E
    is a set of edges (i.e., pairs of vertices). If (s,d) in E, then s and d
    are said *source* and *destination* of (s,d).
    '''

    def __init__(self,V=None,E=None):
        ''' Initialize a new DiGraph

        :param V: a collection of nodes
        :type V: a collection
        :param E: a collection of edges
        :type E: a collection
        '''

        self._next=dict()
        if V!=None:
            for v in V:
                self._next[v]=set()

        if E!=None:
            try:
                for src,dst in E:
                    if src in self._next:
                        self._next[src].add(dst)
                    else:
                        self._next[src]=set([dst])

                    if dst not in self._next:
                        self._next[dst]=set()
            except:
                raise RuntimeError(('E=\'%s\' must be a container ' % (E))+
                                   'of pairs.')

    def add_node(self,v):
        ''' Add a new node to a DiGraph

        :param self: the DiGraph object
        :type self: DiGraph
        :param v: a node
        '''
        if v in self._next:
            raise RuntimeError(('v=\'%s\' is already a node ' % (v))+
                                'of this DiGraph' )
        self._next[v]=set()

    def add_edge(self,src,dst):
        ''' Add a new edge to a DiGraph

        :param src: the source node of the edge
        :param dst: the destination node of the edge
        '''
        if src not in self._next:
            self._next[src]=set()
        else:
            if dst in self._next[src]:
                raise RuntimeError(('(%s,%s) is already an edge ' % (src,dst))+
                                    'of this DiGraph' )

        if dst not in self._next:
            self.add_node(dst)

        self._next[src].add(dst)

    def sources(self):
        ''' Return the sources of a DiGraph.

        The *sources* of a DiGraph G are the nodes that are sources of some
        edges in G itself.

        :returns: a list of all the nodes that are sources of some edges
        :rtype: list
        '''
        srcs=set()
        for src, dsts in self._next.items():
            if len(dsts)>0:
                srcs.add(src)

        return srcs

    def nodes(self):
        ''' Return the nodes of a DiGraph

        :returns: the set of nodes
        :rtype: set
        '''
        return set(self._next.keys())

    def next(self,src):
        ''' Return the next of a node

        Given a DiGraph :math:`(V,E)` and one of its node v, the
        *next* of :math:`v \in V` is the set of all those nodes :math:`v'` that
        are destination of some edge :math:`(v,v') \in E`.

        :returns: the set of nodes :math:`{v' | (v,v') in E}`
        :rtype: set
        '''
        if src not in self._next:
            raise RuntimeError(('src=\'%s\' is not a node ' % (src))+
                                'of this DiGraph' )

        return self._next[src]

    def edges(self):
        ''' Return the edges of a DiGraph

        :returns: the set of edges of the DiGraph
        :rtype: set
        '''
        E=set()
        for src, dsts in self._next.items():
            for dst in dsts:
                E.add((src,dst))

        return E

    def copy(self):
        ''' Copy a DiGraph

        :returns: a copy of the DiGraph
        :rtype: DiGraph
        '''
        nDG=DiGraph()

        nDG._next=dict()
        for src, dsts in self._next.items():
            nDG._next[src]=set(dsts)

        return nDG

    def __str__(self):
        ''' Return a string that represents a DiGraph

        :returns: a string that represents the DiGraph
        :rtype: str
        '''
        return '(V=%s,E=%s)' % (self.nodes(),self.edges())

    def get_subgraph(self,nodes):
        ''' Build the subgraph that respects a set of nodes

        :returns: the subgraph that respects :param nodes:
        :rtype: DiGraph
        '''
        E=[]

        for (s,d) in self.edges():
            if s in nodes and d in nodes:
                E.append((s,d))

        return DiGraph(E=E)

    def get_reversed_graph(self):
        ''' Build the reversed graph

        :returns: the reversed graph
        :rtype: DiGraph
        '''
        rE=[]

        for (s,d) in self.edges():
            rE.append((d,s))

        return DiGraph(V=self.nodes(),E=rE)

    def get_reachable_set_from(self,nodes):
        ''' Compute the reachable set

        :param nodes: the set of nodes from which the reachability
        should be evaluated
        :type nodes: a container of nodes
        :returns: the set of the reachable nodes
        :rtype: set
        '''
        queue=list(nodes)
        R=set(nodes)

        while queue:
            s=queue.pop()
            for d in self.next(s):
                if d not in R:
                    R.add(d)
                    queue.append(d)

        return R

def compute_strongly_connected_components(G):
    ''' Compute the strongly connected components of a DiGraph

    This method implements a non-recursive version of the
    Nuutila and Soisalon-Soinen's algorithm ([ns94]_) to compute the
    strongly connected components of a DiGraph.

    ..[ns94] E. Nuutila and E. Soisalon-Soinen. "On finding the strongly
             connected components in a directed graph.",Information Processing
             Letters 49(1): 9-14, (1994)

    :param G: the DiGraph object
    :type G: DiGraph
    :returns: a generator of a list whose elements are the sets of
                nodes of the strongly connected components of the DiGraph
    :rtype: list
    '''

    if not isinstance(G,DiGraph):
        raise TypeError('%s is not a DiGraph'  % (G))

    disc=dict()
    lowlink=dict()
    in_a_scc=set()
    scc_stack=[]
    time=0

    for s in G.nodes():
        if s not in in_a_scc:
            stack=[s]
            while stack:
                v=stack[-1]
                if v not in disc:
                    time=time+1
                    disc[v]=time

                di=iter(G.next(v))
                try:
                    d=next(di)
                    while (d in disc):
                        d=next(di)
                    stack.append(d)
                except:
                    d=None

                if stack[-1]!=d:
                    lowlink[v]=disc[v]
                    for w in G.next(v):
                        if w not in in_a_scc:
                            if disc[w]>disc[v]:
                                lowlink[v]=min([lowlink[v],lowlink[w]])
                            else:
                                lowlink[v]=min([lowlink[v],disc[w]])
                    stack.pop()

                    if lowlink[v]==disc[v]:
                        in_a_scc.add(v)
                        scc=set([v])
                        while scc_stack and disc[scc_stack[-1]]>disc[v]:
                            k=scc_stack.pop()
                            in_a_scc.add(k)
                            scc.add(k)
                        yield scc
                    else:
                        scc_stack.append(v)

if __name__=='__main__':
    G0=DiGraph(V=['a','b','c'],
              E=[('a','c'),('c','c'),('a','b')])
    print(G0)

    G1=DiGraph(V=['a','b','c'],
             E=[('a','c'),('c','c'),('a','b'),('b','a')])

    print(G1)
    print(G1.get_reversed_edges_graph())
    print(G1.compute_strongly_connected_components())
