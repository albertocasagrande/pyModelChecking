#!/usr/bin/env python

from pyModelChecking.BDD import *

import unittest

__author__ = "Alberto Casagrande"
__copyright__ = "Copyright 2015"
__credits__ = ["Alberto Casagrande"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alberto Casagrande"
__email__ = "acasagrande@units.it"
__status__ = "Development"

class TestOBDD(unittest.TestCase):
    def setUp(self):
        self.a=BDD('a',BDD(False),BDD(True))
        self.b=BDD('a',BDD(True),BDD(False))
        self.c=BDD('c',self.b,BDD(False))
        self.d=BDD('b',BDD(True),BDD(False))

        self.ordering=['c','a']

    def test_BDD(self):
        self.assertEquals('%s' % (self.a),'a')
        self.assertEquals('%s' % (self.b),'~a')
        self.assertEquals('%s' % (self.c),'~c & ~a')
        self.assertEquals('%s' % (self.d),'~b')
        self.assertEquals(self.a.variables(),set(['a']))
        self.assertEquals(self.b.variables(),set(['a']))
        self.assertEquals(self.c.variables(),set(['a','c']))
        self.assertEquals(self.d.variables(),set(['b']))

    def test_OBDD(self):
        oa=OBDD(self.ordering,self.a)
        ob=OBDD(self.ordering,self.c)

        self.assertEquals('%s' % (oa),'a')
        self.assertEquals('%s' % (ob),'~c & ~a')
        self.assertEquals('%s' % (~ob),'(~c & a) | (c)')
        self.assertEquals('%s' % (oa&ob),'False')
        self.assertEquals('%s' % (oa|ob),'(~c) | (c & a)')
        self.assertEquals('%s' % (~(oa&ob)|(oa|ob)),'True')

        self.assertEquals(oa.variables(),set(['a']))
        self.assertEquals(ob.variables(),set(['a','c']))

        with self.assertRaises(RuntimeError):
            OBDD(self.ordering,self.d)

    def test_OBDD_parser(self):
        oa=OBDD(self.ordering,self.a)
        ob=OBDD(self.ordering,self.c)

        parser=BooleanParser(self.ordering)

        for obdd in [oa,ob,~ob,oa&ob, oa|ob, ~(oa&ob)|(oa|ob)]:
            self.assertEquals(parser.parse('%s' % (obdd)),obdd)

        for (a,b) in [('a & ~a','False'),('a | ~a','True'),('~a | c','~(a & ~c)'),
                  ('~~~~a','a'),('~(~a|~c)','a&c')]:
            self.assertEquals(parser.parse(a),parser.parse(b))

        with self.assertRaises(RuntimeError):
            parser.parse('a|~b')

        with self.assertRaises(RuntimeError):
            OBDD(self.ordering,'a|~b')

if __name__ == '__main__':
    unittest.main()
