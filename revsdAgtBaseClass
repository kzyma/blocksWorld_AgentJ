##########################################################################
##
##file: AgentJBaseClass.py
##Author: Ken Zyma
##Project: Blocks World and Agency
##
##Dependencies: py2neo.py
##              neo4j data stored locally at...(localhost:7474/db/data)
##
##This file contains low level basic functionality for agent in blocks world
##  implemented through neo4j
##Edited by: Erin Fowler Nov 26. 2013
##Changes Made: removed utility functions and put in separate class
###########################################################################


from py2neo import node, rel
from py2neo import neo4j
from AStarFunctions import*
import AgtJUtilityClass
import logging

#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

#get database
#graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
neo4j.authenticate("bwn.sb01.stations.graphenedb.com:24789",
                   "BWn", "n6xcosUgxSWJBnM4lc94")

graph_db = neo4j.GraphDatabaseService("http://bwn.sb01.stations.graphenedb.com:24789/db/data/")

#*NOTE*: argument 'state' is of type worldStateMachine

class AgentJBase:

    #def __init__(self):

    ###############  sensory_getCurrentLocation  #################
    #return current location of Agent
    def sensory_getCurrentLocation(self,state):
        return state.getLocation()


    ################ makeMov(getIndx,putIndx,state)  ###############
    #move Agent by: getIndx: number you want to move
    #               putIndx:  index of location you want to move it
    def makeMove(self,getIndx,putIndx,state):
        
        #Translate the index that number is at
        #first build configuration from currentlocation ID
        cfg= AgtJUtilityClass.reconstructCfg(state.getLocation())
        #then find index of that number to pass to move function
        
        srt = AgtJUtilityClass.convertNtoStr(str(getIndx))
        stp = AgtJUtilityClass.convertNtoStr(str(putIndx))
        mv="MOVE"+srt+"TO"+stp
        state.moveByRelation(mv)

    ################ goToNodeById(nodeID,state)  #####################
    def goToNodeById(self,nodeID,state):
        
        init= AgtJUtilityClass.reconstructCfg(state.getLocation())
        goal= AgtJUtilityClass.reconstructCfg(nodeID)
        #note--HEURISTIC_LIST is in file AStarHeuristics.py
        path = findPath(init,goal,HEURISTIC_LIST[2])
        path = path[1:-1]
        path = path.split(")(")
        #make the moves, just dequeue from our path queue
        for x in path:
            if x!= '':
                a=x.split(",")
                indxGet=AgtJUtilityClass.untranslateMv(a[0].strip(),AgtJUtilityClass.reconstructCfg(state.getLocation()))
                indxSet=AgtJUtilityClass.untranslateMv(a[1].strip(),AgtJUtilityClass.reconstructCfg(state.getLocation()))
                self.makeMove(indxGet,indxSet,state)


    ################# goToNodeByConfig(cfg,state) #####################
    def goToNodeByConfig(self,cfg,state):
        cfID = AgtJUtilityClass.genCfgId(cfg)
        self.goToNodeById(cfID,state)
        

    ################# putDownFunction(property,state)  #################
    # function creates a new property on current node, which is
    # named function='value'
    def putDownFunction(self,value,state):
        state.addPropertyToLocation('function',value)


    ################# putDownObject(property,state)  ###################
    # function creates a new property on current node, which is
    # named Object='value'
    def putDownObject(self,value,state):
        state.addPropertyToLocation('object',value)

    ################# pickUp(property,state)  ##########################
    # function return value from given property from node
    # NOTE..this does delete that property from node
    def pickUp(self,property,state):
        t = state.getValueOfPropertyAtLocation(property)
        state.deletePropertyFromLocation(property)
        return t

    ################# peek(property,state)  ############################
    # function returns value for the property from node
    # NOTE..this does NOT delete that property from the node
    def peek(self,property,state):
        t= state.getValueOfPropertyAtLocation(property)
        return t

    ################# examineContents(property,state)  ##################
    # function returns ALL PROPERTIES on node
    def examineLocation(self,state):
         return 0 #NOT COMPLETED YET<---------------

    ################ evaluateItem(item)  ################################
    # evalauates item passed in and returns result
    # items means value
    def evaluateItem(self,item):
        return eval(item)


####################### UNIT TEST ###############################
# this is meant to test code and show how our objects could     #
# possiblty interact to eventually create our main application  #
#                                                               #

from worldState_BW import *
import unittest

BW = worldStateMachine()
Agent = AgentJBase()

print 'Current Starting Location of Agent is:'
print Agent.sensory_getCurrentLocation(BW)

print 'Agent  MOVE (indx 1) TO (indx 2)'
Agent.makeMove(1,2,BW)
print 'Agents current Location:'
print Agent.sensory_getCurrentLocation(BW)

print 'go to node by id 1a2a3a'
Agent.goToNodeById('1a2a3a',BW)
print 'Agents current Location:'
print Agent.sensory_getCurrentLocation(BW)

#print 'go to configuration [[1,3,2]]'
#cfg=[[1,3,2]]
#Agent.goToNodeByConfig(cfg,BW)
#print Agent.sensory_getCurrentLocation(BW)

#print 'go to configuration [[1],[2],[3]]'
#cfg=[[1],[2],[3]]
#Agent.goToNodeByConfig(cfg,BW)
#print Agent.sensory_getCurrentLocation(BW)

#print 'go to configuration [[1,2,3]]'
#cfg=[[1,2,3]]
#Agent.goToNodeByConfig(cfg,BW)
#print Agent.sensory_getCurrentLocation(BW)

#print 'go to configuration [[1],[3,2]]'
#cfg=[[1],[3,2]]
#Agent.goToNodeByConfig(cfg,BW)
#print Agent.sensory_getCurrentLocation(BW)

#print 'go to configuration [[3],[1,2]]'
#cfg=[[3],[1,2]]
#Agent.goToNodeByConfig(cfg,BW)
#print Agent.sensory_getCurrentLocation(BW)

#print 'go to configuration [[1],[2],[3]]'
#cfg=[[1],[2],[3]]
#Agent.goToNodeByConfig(cfg,BW)
#print Agent.sensory_getCurrentLocation(BW)

