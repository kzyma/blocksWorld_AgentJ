##########################################################################
##
##file: AgentJBaseClass.py
##Author: Ken Zyma, Erin Fowler
##date: December 2013
##      
##This file contains low level basic functionality for agent in blocks world
##  named "Agent J".
##
###########################################################################

from py2neo import node, rel
from py2neo import neo4j
import time
import random
from AStar.AStarFunctions import *
from worldState_BW import *
import time
import random
from random import choice
import logging

class AgentJBase():
    #class data
    state=''
    currentlyHolding = ["Map Of BW"]

    ###################  no-arg constructor  ###################
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
        cfg= reconstructCfg(self.state.getLocation())
        #then find index of that number to pass to move function
        
        srt = convertNtoStr(str(getIndx))
        stp = convertNtoStr(str(putIndx))
        mv="MOVE"+srt+"TO"+stp
        self.state.moveByRelation(mv)

    ################ goToNodeById(nodeID)  #####################
    # uses A star to calculate moves, and then loops until all
    # of those moves are made, calling makeMove(x,x)
    def goToNodeById(self,nodeID):
        
        init= reconstructCfg(self.state.getLocation())
        goal= reconstructCfg(nodeID)
        #note--HEURISTIC_LIST is in file AStarHeuristics.py
        path = findPath(init,goal,HEURISTIC_LIST[2])
        path = path[1:-1]
        path = path.split(")(")
        #make the moves, just dequeue from our path queue
        for x in path:
            if x!= '':
                a=x.split(",")
                indxGet=untranslateMv(a[0].strip(),reconstructCfg(self.state.getLocation()))
                indxSet=untranslateMv(a[1].strip(),reconstructCfg(self.state.getLocation()))
                self.makeMove(indxGet,indxSet)


    ################# goToNodeByConfig(cfg) ######################
    def goToNodeByConfig(self,cfg):
        cfID = genCfgId(cfg)
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

    ################ evaluateItem(item)  ############################
    # evalauates item passed in and returns result
    def evaluateItem(self,item):
        return eval(item)

    ################# peek(property,state)  ########################
    # function returns value for the property from node
    # NOTE..this does NOT delete that property from the node
    def peek(self,property):
        t= self.state.getValueOfPropertyAtLocation(property)
        return t
    
    #****************searchBWforProp()*******************************
    #Action:  will search blocks world nodes for objects
    #Returns: nothing, but can be made to return an object
    #****************************************************************
    def searchBWforObj(self):
        random.seed(random.Random(int(round(time.time() * 1000))))
       #Go to Central Node
        #unfortunatly will need to change based on which size blocks world
        centralCfg = reconstructCfg(self.state.centerNodeCfg)
        self.goToNodeByConfig(centralCfg)
        #set initial 'thing' to look at central node and start loop
        thing = self.peek('object')
        
        while(thing==None):
            #move to a random adjacent node
            currentId = self.sensory_getCurrentLocation()
            currentCfg = reconstructCfg(currentId)
            moveState = 'bad'
            #find a good move
            while(moveState == 'bad'):
                move = random.randint(0,(len(currentCfg))-1)
                to = random.randint(0,(len(currentCfg))-1)
                if(move==to):
                    to = -1
                moveState = 'good'
                if(((len(currentCfg[move]))==1)and(to==-1)):
                    moveState = 'bad'
                
            #make the move
            self.makeMove(move,to)
            #check node
            thing = self.peek('object')
        return thing

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

#################### Non-Member Functions ##################################
        
def convertNtoStr(n):
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

def untranslateMv(a,node):
    #take care of special case--table
    if (a=="-1"):
        return -1
    #all other cases
    for i in node:
        if int(a) in i:
            return node.index(i)

def numbize(nList):
    num=0
    for n in nList:
            num*=100
            num+=n
    return num

def genCfgId(cfg):
    nL=map(self.numbize,cfg)
    nL.sort()
    cfId=''
    for n in nL:
            cfId+=str(n)+'a'
    return cfId
    
def generateCenterNode(n):
    i=[]
    for x in range(1,n+1):  
        n = []
        n.append(x)
        i.append(n)
    return i

def genCfgId(cfg):
        nL=map(numbize,cfg)
        nL.sort()
        cfId=''
        for n in nL:
                cfId+=str(n)+'a'
        return cfId
        
