###########################################################################
##file: createWorld_BW.py
##Author: Ken Zyma, Erin Fowler, Dr. Rieksts
##      *code adapted from Dr. Rieksts "Blocks World" is notated by an (*)
##
##Dependencies: py2neo.py
##
##This file contains all methods to create a blocksWorld(n) configuration
##  and add them to neo4j data file.
############################################################################

from py2neo import node, rel
from py2neo import neo4j
import logging

#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

from copy import copy
from copy import deepcopy
import math
import bisect
import time
import random

#the following should be un-commented when neo4j is running on your local machine, port 7474
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")


#next is provided a sample of how to run on a remote server (check out Graphene, which was
#       suggested to us by Nigel Small, http://www.graphenedb.com/

#neo4j.authenticate("address/of/remote/site")
#graph_db = neo4j.GraphDatabaseService("address/of/remote/site")



#generateRnadomConfig generates a random configuration
#of the size of n and a random width
def generateRandomConfig(n):
        width = random.randint(1,2)
        l=range(1,n+1)
        config=[]
        for x in range(width):
                config.append([])
        for x in range(len(l)):
                config[random.randint(0,width-1)].append(l.pop())
        #protect agains empty list being returned
        if [] in config:
                config.remove([])
        return config
#(*)
def numbize(nList):
        num=0
        for n in nList:
                num*=100
                num+=n
        return num

#(*)
def genCfgId(cfg):
        nL=map(numbize,cfg)
        nL.sort()
        cfId=''
        for n in nL:
                cfId+=str(n)+'a'
        return cfId

#(*)
def genMvs(cfg):
        src=[x for x in range(len(cfg))]
        dests=[]
        for indx in src:
                idst = copy(src)
                if len(cfg[indx])>1:
                        idst[indx]=-1
                else:
                        idst.remove(indx)
                dests.append(idst)
        return [(src[a],dests[a][b]) for a in range(len(src)) for b in range(len(dests[a]))]

#re-build the BW cfg from an id
#this function is used mainly to ensure iniformity across generating configurations. For example...
#  [[1,2],[3]]==[[3],[1,2]], so we do not want to store both!
def reconstructCfg(nodeID):
        cfg=[]
        i=1
        while i<len(nodeID):
            current=nodeID[(i-1):i]
            temp=[]
            while current!='a':
                if (current != '0'):
                    temp.append(int(current))
                i = i+1
                current=nodeID[(i-1):i]
            cfg.append(temp)
            i = i+1
        return cfg

#(*)
def mkNwCfg(mv,cfg):
        newCfg=deepcopy(cfg)
        frm=mv[0]
        to=mv[1]
        mvBlk=newCfg[frm].pop()
        if to>-1:
                newCfg[to].append(mvBlk)
        else:
                newCfg.append([mvBlk])
        if newCfg[frm]==[]:
                del newCfg[frm]
        return newCfg

#(*)
# changes: added the re-formatting and node contents altered to fit this problem
def makNd(cfg1,mv,root):
        #first need to re-reformat the cfg into common format
        cfg_id = genCfgId(cfg1)
        cfg_formatted= reconstructCfg(cfg_id)
        return {'cfg':cfg_formatted,'nid':cfg_id,'mv':mv,'root':root}
#(*)
def xpdNd(node):
        cfg=node['cfg']
        mvs = genMvs(cfg)
        nodes = []
        for x in mvs:
            nwCfg = mkNwCfg(x,cfg)
            newNode=makNd(nwCfg,x,node["nid"])
            nodes.append(newNode)
        return nodes

#generates center Node in the form [[0],[1],...[n]]
def generateCenterNode(n):
    i=[]
    for x in range(1,n+1):
        n = []
        n.append(x)
        i.append(n)
    return i

#convert 1 to One, 2 to Two, ect
#*note* this is a workaround, neo4j does not allow any numbers
#       as relation names
def convertNtoStr(n):
        n=str(n)
        return {
        '1': "one",
        '2': "two",
        '3': "three",
        '4': "four",
        '5': "five",
        '6': "six",
        '7': "seven",
        '8': "eight",
        '9': "nine",
        '0': "zero",
        '-1': "table",
        }.get(n,"none") 


def findIndexById(nid,List):
        return List.index(nid)
        
#Generate the Blocks World on the location named at the top of of this document "graph_db=..."
def generateBW(n):
        
        #list of New nodes that need to be expanded
        NeedToXpndList = []
        NeedToXpndListID = []
        #list of all nodes created and parrell indx'd node list for Neo2J
        nodesID = []
        nodesAndRelsN2J = []
        Nodes=[]
        nodesN2J = []
        relsN2J = []
        
        #generate central node/initial node
        CntCfg = generateCenterNode(n)
        CntNode = makNd(CntCfg,None,None)
        nodesID.append(CntNode['nid'])
        nodesN2J.append(node(id=CntNode["nid"]))
        NeedToXpndList.append(CntNode)
        NeedToXpndListID.append(CntNode['nid'])
        
        
        #until all nodes that need to be expanded are expanded, continue...
        while([] != (NeedToXpndListID)):
                
                NeedToXpndListID.pop()
                xpndNode = xpdNd(NeedToXpndList.pop())
                
                for x in xpndNode:
                        if (x['nid'] not in nodesID):
                                NeedToXpndList.append(x)
                                NeedToXpndListID.append(x['nid'])
                                nodesID.append(x['nid'])
                                nodesN2J.append(node(id=x["nid"]))
                        temp= xpdNd(x)
                        for y in temp:
                                Nodes.append(y)

        tempNodes = []
        for i in nodesN2J:
                if i not in tempNodes:
                        tempNodes.append(i)
        nodesN2J=tempNodes
                
        for x in Nodes:
                #create relationship string for mv
                temp= x["mv"]
                move="MOVE"+convertNtoStr(str(temp[0]))+"TO"+convertNtoStr(str(temp[1]))
                #create the relationship
                indxOfRoot = findIndexById(x["root"],nodesID)
                indxOfCurrent = findIndexById(x["nid"],nodesID)
                #append relation to nodesAndRels
                relsN2J.append(rel(indxOfRoot,move,indxOfCurrent))

        nodesAndRelsN2J = nodesN2J + relsN2J
        args = str(nodesAndRelsN2J).strip('[]')

        tempRels = []
        for i in relsN2J:
                if i not in tempRels:
                        tempRels.append(i)
                        
        nodesAndRelsN2J = tempNodes + tempRels            
        i= nodesAndRelsN2J
        #python has max length passed by parameter to a function, so a pointer is passed below 
        graph_db.create(*i)
              
