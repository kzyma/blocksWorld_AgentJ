##########################################################################
##file: createWorld_BW_test.py
##Author: Ken Zyma
##
##Dependencies: py2neo.py
##              neo4j data stored locally at...(localhost:7474/db/data)
##
##This file contains unit tests for createWorld_BW.py
##
## notes: dec. 26, 2013: generateBW() is ommitted due to testing complexity.
###########################################################################

import unittest
import sys
from createWorld_BW import *

class TestCreateWorld(unittest.TestCase):

    def test_numbize(self):
        n = numbize([])
        self.assertEqual(n,0)
        
        n = numbize([1])
        self.assertEqual(n,1)

        n = numbize([3,2])
        self.assertEqual(n,302)

        n = numbize([2,1,3])
        self.assertEqual(n,20103)

    
    def test_genCfgId(self):
        ID = genCfgId([[]])
        self.assertEqual(ID,'0a')

        ID = genCfgId([[1,2,3]])
        self.assertEqual(ID,'10203a')

        ID = genCfgId([[1,2,3],[4,5]])
        self.assertEqual(ID,'405a10203a')

        ID = genCfgId([[5,4],[3,1,2]])
        self.assertEqual(ID,'504a30102a')

    def test_genMvs(self):
        mvs = genMvs([[]])
        self.assertEqual(mvs,[])
        
        mvs = genMvs([[2], [1, 3]])
        self.assertEqual(mvs,[(0, 1), (1, 0), (1, -1)])

        mvs = genMvs([[1], [2], [3]])
        self.assertEqual(mvs,[(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)])

        mvs = genMvs([[1, 3, 2]])
        self.assertEqual(mvs,[(0, -1)])

    def test_reconstructCfg(self):
        cfg = reconstructCfg('0')
        self.assertEqual(cfg,[])

        cfg = reconstructCfg('1a2a3a')
        self.assertEqual(cfg,[[1], [2], [3]])

        cfg = reconstructCfg('3a201a')
        self.assertEqual(cfg,[[3], [2, 1]])

        cfg = reconstructCfg('102030405a')
        self.assertEqual(cfg,[[1,2,3,4,5]])

    def test_makNd(self):
        node = makNd([[1], [2], [3]],None,None)
        self.assertEqual(node,{'cfg': [[1], [2], [3]], 'mv': None, 'root': None, 'nid': '1a2a3a'})

        node = makNd([[1], [2, 3]],(2, 1),'1a2a3a')
        self.assertEqual(node,{'cfg': [[1], [2, 3]], 'mv': (2, 1), 'root': '1a2a3a', 'nid': '1a203a'})

        node = makNd([[2, 1, 3]],(0, 1), '3a201a')
        self.assertEqual(node,{'cfg': [[2, 1, 3]], 'mv': (0, 1), 'root': '3a201a', 'nid': '20103a'})        
        
    def test_xpdNd(self):
        xpndNode = xpdNd({'cfg': [[1], [2], [3]], 'mv': None, 'root': None, 'nid': '1a2a3a'})
        self.assertEqual(xpndNode,[{'cfg': [[3], [2, 1]], 'mv': (0, 1), 'root': '1a2a3a', 'nid': '3a201a'},
                                   {'cfg': [[2], [3, 1]], 'mv': (0, 2), 'root': '1a2a3a', 'nid': '2a301a'},
                                   {'cfg': [[3], [1, 2]], 'mv': (1, 0), 'root': '1a2a3a', 'nid': '3a102a'},
                                   {'cfg': [[1], [3, 2]], 'mv': (1, 2), 'root': '1a2a3a', 'nid': '1a302a'},
                                   {'cfg': [[2], [1, 3]], 'mv': (2, 0), 'root': '1a2a3a', 'nid': '2a103a'},
                                   {'cfg': [[1], [2, 3]], 'mv': (2, 1), 'root': '1a2a3a', 'nid': '1a203a'}])


    def test_generateCenterNode(self):
        cntr = generateCenterNode(0)
        self.assertEqual(cntr,[])

        cntr = generateCenterNode(2)
        self.assertEqual(cntr,[[1],[2]])

        cntr = generateCenterNode(3)
        self.assertEqual(cntr,[[1],[2],[3]])

    def test_convertNtoStr(self):
        self.assertEqual(convertNtoStr(1),"one")
        self.assertEqual(convertNtoStr(2),"two")
        self.assertEqual(convertNtoStr(3),"three")
        self.assertEqual(convertNtoStr(4),"four")
        self.assertEqual(convertNtoStr(5),"five")
        self.assertEqual(convertNtoStr(6),"six")
        self.assertEqual(convertNtoStr(7),"seven")
        self.assertEqual(convertNtoStr(8),"eight")
        self.assertEqual(convertNtoStr(9),"nine")
        self.assertEqual(convertNtoStr(-1),"table")
        self.assertEqual(convertNtoStr('foo'),"none")
        
    def test_findIndexById(self):
        l=['1a2a3a', '3a201a', '2a301a', '3a102a', '1a302a', '2a103a', '1a203a',
           '20301a', '10302a', '30201a', '10203a', '30102a', '20103a']
        self.assertEqual(findIndexById('3a201a',l),1)
        self.assertEqual(findIndexById('20103a',l),12)
        self.assertEqual(findIndexById('1a2a3a',l),0)

if __name__ == '__main__':
    unittest.main()




