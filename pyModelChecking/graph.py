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

        :param self: the DiGraph object that should be initializated
        :type self: DiGraph
        :param V: a collection of nodes
        :type V: a collection
        :param E: a collection of edges
        :type E: a collection
        '''
        self._nodes=set()
        if V!=None:
            self._nodes.update(V)

        self._next=dict()

        if E!=None:
            try:
                for src,dst in E:
                    if src in self._next:
                        self._next[src].add(dst)
                    else:
                        self._next[src]=set([dst])
                        self._nodes.add(src)

                    self._nodes.add(dst)
            except:
                raise RuntimeError(('E=\'%s\' must be a container ' % (E))+
                                   'of pairs.')

    def add_node(self,v):
        ''' Add a new node to a DiGraph

        :param self: the DiGraph object
        :type self: DiGraph
        :param v: a node
        '''
        if v in self._nodes:
            raise RuntimeError(('v=\'%s\' is already a node ' % (v))+
                                'of this DiGraph' )
        self._nodes.add(v)

    def add_edge(self,src,dst):
        ''' Add a new edge to a DiGraph

        :param self: the DiGraph object
        :type self: DiGraph
        :param src: the source node of the edge
        :param dst: the destination node of the edge
        '''
        if src not in self._nodes:
            self.add_node(src)
        else:
            if dst in self._next[src]:
                raise RuntimeError(('(%s,%s) is already an edge ' % (src,dst))+
                                    'of this DiGraph' )

        if dst not in self._nodes:
            self.add_node(dst)

        if src not in self._next:
            self._next[src]=set()

        self._next[src].add(dst)

    def sources(self):
        ''' Return the sources of a DiGraph.

        The *sources* of a DiGraph G are the nodes that are sources of some
        edges in G itself.
        :param self: the DiGraph object
        :type self: DiGraph
        :returns: a list of all the nodes that are sources of some edges
        :rtype: list
        '''
        return set(self._next.keys())

    def nodes(self):
        ''' Return the nodes of a DiGraph

        :param self: the DiGraph object
        :type self: DiGraph
        :returns: the set of nodes
        :rtype: set
        '''
        return self._nodes

    def next(self,src):
        ''' Return the next of a node

        Given a DiGraph (V,E) and one of its node v, the *next* of v in (V,E)
        is the set of all those nodes that are destination of some edges whose
        source is v itself i.e., (V,E).next(s)={v' | (v,v') in E}.
        :param self: the DiGraph object
        :type self: DiGraph
        :returns: the set of nodes {v' | (v,v') in E}
        :rtype: set
        '''
        if src not in self._nodes:
            raise RuntimeError(('src=\'%s\' is not a node ' % (src))+
                                'of this DiGraph' )
        if src not in self._next:
            return set()
        return self._next[src]

    def edges(self):
        ''' Return the edges of a DiGraph

        :param self: the DiGraph object
        :type self: DiGraph
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

        :param self: the DiGraph object
        :type self: DiGraph
        :returns: a copy of the DiGraph
        :rtype: DiGraph
        '''
        nDG=DiGraph()

        nDG._nodes=set(self._nodes)

        nDG._next=dict()
        for src, dsts in self._next.items():
            nDG._next[src]=set(dsts)

        return nDG

    def __str__(self):
        ''' Return a string that represents a DiGraph

        :param self: the DiGraph object
        :type self: DiGraph
        :returns: a string that represents the DiGraph
        :rtype: str
        '''
        return '(V=%s,E=%s)' % (self._nodes,self.edges())

    def get_subgraph(self,nodes):
        ''' Build the subgraph that respects a set of nodes

        A *subgraph* of a DiGraph (V,E) is a DiGraph (V',E') such that V' is
        a subset of V and E' is a subset of E. The *subgraph that respects V'*
        is the subgraph (V',(V'xV')&E).
        :param self: the DiGraph object
        :type self: DiGraph
        :param nodes: a set of nodes
        :type nodes: set
        :returns: the subgraph that respects :nodes
        :rtype: DiGraph
        '''
        E=[]

        for (s,d) in self.edges():
            if s in nodes and d in nodes:
                E.append((s,d))

        return DiGraph(E=E)

    def get_reversed_graph(self):
        ''' Build the reversed graph

        The *reversed graph* of a DiGraph (V,E) is the DiGraph (V,E')
        where E'={(dst,src) | (src,dst) in E}.
        :param self: the DiGraph object
        :type self: DiGraph
        :returns: the reversed graph
        :rtype: DiGraph
        '''
        rE=[]

        for (s,d) in self.edges():
            rE.append((d,s))

        return DiGraph(V=self._nodes,E=rE)

def compute_strongly_connected_components(G):
    ''' Compute the strongly connected components of a DiGraph

    The node *v' is reachable from v in (V,E)* iff either:
    1. v is v' or
    2. there exists an edge (v,v'') in E in such that v' is reachable from
       v in (V,E).
    A *strong connected component* of (V,E) is a maximal subgraph (V',E') of
    (V,E) such that, for any pair or vertices v,v' in V', v is reachable
    from v' and v' is reachable from v in (V',E').
    This method uses the Tarjan's algorithm ([Tarjan]_) to compute all the strongly
    connected components of a DiGraph.
    [Tarjan] Tarjan, R. E. 1972. "Depth-first search and linear graph algorithms",
             SIAM Journal on Computing 1 (2): 146-160
    :param G: the DiGraph object
    :type G: DiGraph
    :returns: a list whose elements are the sets of nodes of the strongly
                connected components of the DiGraph
    :rtype: list
    '''
    def popStack(stack,stackSet):
        v=stack.pop()
        stackSet.remove(v)
        return v

    def pushStack(v,stack,stackSet):
        stackSet.add(v)
        stack.append(v)

    def _Tarjan(G,v,disc,lowlink,stack,stackSet,time, SCCs):
        if v in disc:
            return time

        disc[v]=time
        lowlink[v]=time
        pushStack(v,stack,stackSet)
        time+=1

        for w in G.next(v):
            if w not in disc:
                time=_Tarjan(G,w,disc,lowlink,stack,stackSet,time,SCCs)
                lowlink[v]=min(lowlink[v],lowlink[w])
            else:
                if w in stackSet:
                    lowlink[v]=min(lowlink[v],disc[w])

        if lowlink[v]==disc[v]:
            w=popStack(stack,stackSet)
            scc=set([w])
            while v!=w:
                w=popStack(stack,stackSet)
                scc.add(w)
            SCCs.append(frozenset(scc))

        return time

    if not isinstance(G,DiGraph):
        raise TypeError('%s is not a DiGraph'  % (G))

    SCCs=[]

    disc=dict()
    lowlink=dict()
    stackSet=set()
    stack=[]

    time=0
    for v in G.nodes():
        if v not in disc:
            time=_Tarjan(G,v,disc,lowlink,stack,stackSet,time,SCCs)

    return SCCs


if __name__=='__main__':
    G0=DiGraph(V=['a','b','c'],
              E=[('a','c'),('c','c'),('a','b')])
    print(G0)

    G1=DiGraph(V=['a','b','c'],
             E=[('a','c'),('c','c'),('a','b'),('b','a')])

    print(G1)
    print(G1.get_reversed_edges_graph())
    print(G1.compute_strongly_connected_components())
