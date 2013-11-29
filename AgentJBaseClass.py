##########################################################################
##
##file: AgentJBaseClass.py
##Author: Ken Zyma, Erin Fowler
##Project: Blocks World and Agency
##
##Dependencies: py2neo.py
##              neo4j 
##
##This file contains low level basic functionality for agent in blocks world
##  implemented through neo4j
##
###########################################################################

from py2neo import node, rel
from py2neo import neo4j
from AStarFunctions import*
from worldState_BW import *
import logging
from GUIApp import *

#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

#get database / if you are not using a local server you
#will have to authenticate and change the location.
#THE SAME MUST ALSO BE DONE IN WORLDSTATE_BW.py
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")


class AgentJBase:

    #delcaration needed for referencing state in entire class
    state=''
        
    def __init__(self):
        #create an instance of state
        self.state = worldStateMachine()

    ###############  sensory_getCurrentLocation  #################
    #return current location of Agent
    def sensory_getCurrentLocation(self):
        return self.state.getLocation()


    ################ makeMov(getIndx,putIndx)  ###############
    #move Agent by:
    #        getIndx:  index of location you want to move top of stack
    #       putIndx:  index of location you want to move top of stack
    def makeMove(self,getIndx,putIndx):
        
        #Translate the index that number is at
        #first build configuration from currentlocation ID
        cfg= self.reconstructCfg(self.state.getLocation())
        #then find index of that number to pass to move function
        
        srt = self.convertNtoStr(str(getIndx))
        stp = self.convertNtoStr(str(putIndx))
        mv="MOVE"+srt+"TO"+stp
        self.state.moveByRelation(mv)

    ################ goToNodeById(nodeID)  #####################
    # uses A star to calculate moves, and then loops until all
    # of those moves are made, calling makeMove(x,x)
    def goToNodeById(self,nodeID):
        
        init= self.reconstructCfg(self.state.getLocation())
        goal= self.reconstructCfg(nodeID)
        #note--HEURISTIC_LIST is in file AStarHeuristics.py
        path = findPath(init,goal,HEURISTIC_LIST[2])
        path = path[1:-1]
        path = path.split(")(")
        #make the moves, just dequeue from our path queue
        for x in path:
            if x!= '':
                a=x.split(",")
                indxGet=self.untranslateMv(a[0].strip(),self.reconstructCfg(self.state.getLocation()))
                indxSet=self.untranslateMv(a[1].strip(),self.reconstructCfg(self.state.getLocation()))
                self.makeMove(indxGet,indxSet)


    ################# goToNodeByConfig(cfg) ######################
    def goToNodeByConfig(self,cfg):
        cfID = self.genCfgId(cfg)
        self.goToNodeById(cfID)
        

    ################# putDownFunction(property)  #################
    # function creates a new property on current node, which is
    # named function='value'
    def putDownFunction(self,value):
        self.state.addPropertyToLocation('function',value)


    ################# putDownObject(property)  ####################
    # function creates a new property on current node, which is
    # named Object='value'
    def putDownObject(self,value):
        self.state.addPropertyToLocation('object',value)

    ################# pickUp(property,state)  #####################
    # function return value from given property from node
    # NOTE..this does delete that property from node
    def pickUp(self,property):
        t = self.state.getValueOfPropertyAtLocation(property)
        self.state.deletePropertyFromLocation(property)
        return t

    ################# peek(property,state)  ########################
    # function returns value for the property from node
    # NOTE..this does NOT delete that property from the node
    def peek(self,property):
        t= self.state.getValueOfPropertyAtLocation(property)
        return t

    ################# examineContents(property)  ####################
    # function returns ALL PROPERTIES on node
    def examineLocation(self):
         return 0 #NOT COMPLETED YET<---------------

    ################ evaluateItem(item)  ############################
    # evalauates item passed in and returns result
    def evaluateItem(self,item):
        return eval(item)

#################### Non-Member Functions #############################
        
    def convertNtoStr(self,n):
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

    #re-build the BW cfg from it's id
    def reconstructCfg(self,nodeID):
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

    def untranslateMv(self,a,node):
        #take care of special case--table
        if (a=="-1"):
            return -1
        #all other cases
        for i in node:
            if int(a) in i:
                return node.index(i)

    def numbize(self,nList):
        num=0
        for n in nList:
                num*=100
                num+=n
        return num

    def genCfgId(self,cfg):
        nL=map(self.numbize,cfg)
        nL.sort()
        cfId=''
        for n in nL:
                cfId+=str(n)+'a'
        return cfId
