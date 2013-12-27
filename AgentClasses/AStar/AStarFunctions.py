##file: AStarFunctions.py
##Author: Ken Zyma
##Project: Block World, A*, A* heuristics
##
##Dependents: BlocksWorldHeurstics.py
##
##This file includes all optimized functions for a* blocks world project.

from copy import copy
from copy import deepcopy
import math
import bisect
from AStarHeuristics import *
import time
import random

#to use Heuristic, simply use index of HEURISTIC_LIST.
# example: HEURISTIC_LIST[1] = zerOrTwoMoveHeuristic
HEURISTIC_LIST = [DijkstraAlgorithm,zerOrTwoMoveHeuristic,zerOrTwoMoveVersionTwoHeuristic]

#generateRnadomConfig generates a random configuration
#of the size of n and a set width.
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

def numbize(nList):
        num=0
        for n in nList:
                num*=100
                num+=n
        return num

def genCfgId(cfg):
        nL=map(numbize,cfg)
        nL.sort()
        cfId=''
        for n in nL:
                cfId+=str(n)+'a'
        return cfId


def destsOf(cfg):
        rr=[x for x in range(len(cfg))]
        mList=[]
        for indx in range(len(cfg)):
                irr = copy(rr)
                irr[indx]=-1
                mList.append(irr)
        return mList

def genMvs(cfg,gcfg):
        src = isNotZero(cfg,gcfg)
        dests=[]
        for indx in src:
                idst = copy(src)
                if len(cfg[indx])>1:
                        idst[indx]=-1
                else:
                        idst.remove(indx)
                dests.append(idst)
        return [(src[a],dests[a][b]) for a in range(len(src)) for b in range(len(dests[a]))]

#make sure that we do not move zero-move blocks
def isNotZero(cfg,goal):
        retIndxList = []
        for i in range(len(cfg)):
                for j in range(len(goal)):
                        if ((cfg[i]!=goal[j])and(not i in retIndxList)):
                                retIndxList.append(i)
        return retIndxList


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


def insertKeyed(node,f,L,keysL,idsL):
        place=bisect.bisect_left(keysL,f)
        return L[:place]+[node]+L[place:],keysL[:place]+[f]+keysL[place:],idsL[:place]+[node['nid']]+idsL[place:]


def adGoods(nwNds,wl,wlfs,wlids,maxD):

        for nd in nwNds:
            if (not(nd['nid'] in wlids)):
                if (nd['f']<=maxD):
                        wl,wlfs,wlids=insertKeyed(nd,nd['f'],wl,wlfs,wlids)
            else:
                index = wlids.index(nd['nid'])
                if (nd['f']<wlfs[index]):
                    del wl[index]
                    del wlfs[index]
                    del wlids[index]
                    wl,wlfs,wlids=insertKeyed(nd,nd['f'],wl,wlfs,wlids)
        return wl,wlfs,wlids
    

def makNd(cfg1,g,h,mv):
        #construct/deconstruct code
        cfg_id=genCfgId(cfg1)
        cfg_formatted = reconstructCfg(cfg_id)
        return {'nid':cfg_id,'cfg':cfg_formatted,'path':mv,'g':g,'h':h,'f': g+h}

#re-build the BW cfg from it's id
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

def xpdNd(node,gcfg,h):
        cfg=node['cfg']
        g=node['g']
        currentPath = node['path']
        mvs = genMvs(cfg,gcfg)
        nodes = []
        for x in mvs:
            nwCfg = mkNwCfg(x,cfg)
            nodePath = currentPath + move(x,node['cfg'])
            newNode=makNd(nwCfg,g+1,h(nwCfg,gcfg),nodePath)
            nodes.append(newNode)
        return nodes

def move(mv,node):
        #translate to VALUE of top of index, or -1 if table
        a = findIndex(mv[0],node)
        b = findIndex(mv[1],node)
        return "("+str(a)+","+str(b)+")"
 

def findIndex(a,node):
        if a != -1:
                return node[a][-1]
        else:
                return -1

def computeMaxPath(cfg,goal):
        zerM = numOfZeroMoves(cfg,goal)
        x = (2*(n(cfg)))-len(cfg)-len(goal)-zerM+wrongBase(cfg,goal)
        return x

def findPath(icfg,gcfg,h):
        WL=[]
        WLfs=[]
        WLids=[]
        maxWL = 0
        numOfLoops = 0
        path = ''
        goalId=genCfgId(gcfg)
        iNode = makNd(icfg,0,h(icfg,gcfg),path)
        curNode=iNode
        start=time.clock()
        #compute the max Path Length
        maxD = computeMaxPath(icfg,gcfg)
        while curNode['nid'] != goalId:
                t2=time.clock()
                elapse=t2-start
                if (elapse>30):
                        return 'FAILED, time>30.',0,maxWL,numOfLoops
                #update number of loops run
                numOfLoops += 1
                #update to find the maximum waitlist
                if(len(WL)>maxWL):
                        maxWL = len(WL)
                #xpand to all nodes within 1 move
                newNodes=xpdNd(curNode,gcfg,h)
                #if nodes is not already represented, add to WL
                WL,WLfs,WLids=adGoods(newNodes,WL,WLfs,WLids,maxD)
                curNode=WL[0]
                WL.remove(WL[0])
                WLfs.remove(WLfs[0])
                WLids.remove(WLids[0])
        return curNode['path']#,curNode['g'],maxWL,numOfLoops

def runBlocksWorldSearch(icfg,gcfg,h):
        print 'icfg: ',icfg
        print 'gcfg: ',gcfg
        path,l,WL,loops = findPath(icfg,gcfg,h)
        print 'Heuristic Used:',h.__name__
        print 'max WL:',WL
        print '# of loops:',loops
        print path
        print 'length is:',l
