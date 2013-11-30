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
##Edited By: Erin Fowler Nov 27, 2013
###########################################################################

from py2neo import node, rel
from py2neo import neo4j
import time
import random
import AgtJUtilityClass
import createWorld_BW
from AStarFunctions import *
from worldState_BW import *
import logging

#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

neo4j.authenticate("bw3.sb01.stations.graphenedb.com:24789",
                   "Bw3", "rPNUx8yavz6tFsY2sgUv")

graph_db = neo4j.GraphDatabaseService("http://bw3.sb01.stations.graphenedb.com:24789/db/data/")


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
        cfg= AgtJUtilityClass.reconstructCfg(self.state.getLocation())
        #then find index of that number to pass to move function
        
        srt = AgtJUtilityClass.convertNtoStr(str(getIndx))
        stp = AgtJUtilityClass.convertNtoStr(str(putIndx))
        mv="MOVE"+srt+"TO"+stp
        self.state.moveByRelation(mv)

    ################ goToNodeById(nodeID)  #####################
    # uses A star to calculate moves, and then loops until all
    # of those moves are made, calling makeMove(x,x)
    def goToNodeById(self,nodeID):
        
        init= AgtJUtilityClass.reconstructCfg(self.state.getLocation())
        goal= AgtJUtilityClass.reconstructCfg(nodeID)
        #note--HEURISTIC_LIST is in file AStarHeuristics.py
        path = findPath(init,goal,HEURISTIC_LIST[2])
        path = path[1:-1]
        path = path.split(")(")
        #make the moves, just dequeue from our path queue
        for x in path:
            if x!= '':
                a=x.split(",")
                indxGet=AgtJUtilityClass.untranslateMv(a[0].strip(),AgtJUtilityClass.reconstructCfg(self.state.getLocation()))
                indxSet=AgtJUtilityClass.untranslateMv(a[1].strip(),AgtJUtilityClass.reconstructCfg(self.state.getLocation()))
                self.makeMove(indxGet,indxSet)


    ################# goToNodeByConfig(cfg) ######################
    def goToNodeByConfig(self,cfg):
        cfID = createWorld_BW.genCfgId(cfg)
        self.goToNodeById(cfID)
        

    ################# putDownFunction(property)  #################
    # creates a new key "function", and function value for current node
    def putDownFunction(self,value):
        #note: 'function' is the key, value is the value for that key
        self.state.addPropertyToLocation('function',value)


    ################# putDownObject(property)  ####################
    # function creates a new property on current node, which is
    def putDownObject(self,value):
        #note: 'object' is a key in node, value is value for that key
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

    #****************searchBWforProp()*******************************
    #Action:  will search blocks world nodes for objects
    #Returns: nothing, but can be made to return an object
    #****************************************************************
    def searchBWforObj(self):
       #check if agent is at central node
        central = '1a2a3a'
        cur = self.sensory_getCurrentLocation()
        print 'current',cur
        #if not already at central, get there
        if central != cur:
            self.goToNodeById(central)
        thing = self.peek('object')
        print 'object', thing
        #if thing isn't empty
        if thing != None:
            this = self.pickUp('object')
            print 'I have', this, '.  Awe-SOME!'
            #NOTE: answer should be in the form of a node id or the sack functions
            answer = raw_input('Where do you want me to put it? ')
            print 'OK.  Going to:', answer
            destination = self.goToNodeById(answer)
            where = self.sensory_getCurrentLocation()
            print 'I am here now.', where
            self.putDownObject(this)
            verify = self.peek('object')
            print 'I put it here in ',where, verify

        return

    #*****************searchBW()***********************************
    #Actions:  will move freely searching through BWn
    #Returns:  list of collected objects
    #**************************************************************
    def searchBW(self, genSeed=0):
        random.seed(genSeed)
        #list for objects
        objList =[]
        #check if agent is at central node
        #central = '1a2a3a'
        cur = self.sensory_getCurrentLocation()
        print 'current',cur
        thing = self.peek('object')
        print 'object', thing
        #if thing isn't none
        #while thing != None:
            #put it in the list
            #objList.append(thing)
            #print 'list', objList
            #keep looking for objects
            #curCfg = createWorld_BW.reconstructCfg(cur)
            #moves = createWorld_BW.genMvs(curCfg)
            #print 'moves', moves
            #get random index of move from list of moves
            #rIndex= random.randrange(len(moves))
            #print 'rIndex', rIndex
            #nxtCfg = createWorld_BW.mkNwCfg(moves[rIndex],curCfg)
            #print 'nxtCfg',nxtCfg
            #nxt=self.goToNodeByConfig(nxtCfg)
            #whr = self.sensory_getCurrentLocation()
            #print whr
        while thing == None:
            #keep looking for objects
            curCfg = createWorld_BW.reconstructCfg(cur)
            moves = createWorld_BW.genMvs(curCfg)
            print 'moves', moves
            #get random index of move from list of moves
            rIndex= random.randrange(len(moves))
            print 'rIndex', rIndex
            nxtCfg = createWorld_BW.mkNwCfg(moves[rIndex],curCfg)
            print 'nxtCfg',nxtCfg
            nxt=self.goToNodeByConfig(nxtCfg)
            whr = self.sensory_getCurrentLocation()
            print whr

        
        return objList 
        

