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
<<<<<<< HEAD
##
=======
>>>>>>> 3cfc162332e14ff23593dc176000cf9190a236b4
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
import time
import random
from random import choice
import logging


#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

neo4j.authenticate("bw3.sb01.stations.graphenedb.com:24789",
                   "Bw3", "rPNUx8yavz6tFsY2sgUv")

graph_db = neo4j.GraphDatabaseService("http://bw3.sb01.stations.graphenedb.com:24789/db/data/")

#neo4j.authenticate("bw3.sb01.stations.graphenedb.com:24789",
                  # "Bw3", "rPNUx8yavz6tFsY2sgUv")

#graph_db = neo4j.GraphDatabaseService("http://bw3.sb01.stations.graphenedb.com:24789/db/data/")


class AgentJBase():

    #delcaration needed for referencing state in entire class
    state=''
    currentlyHolding = ["Map Of BW"]
        
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
        
##        print 'object', thing
##        #if thing isn't empty
##        if thing != None:
##            this = self.pickUp('object')
##            print 'I have', this, '.  Awe-SOME!'
##            #NOTE: answer should be in the form of a node id or the sack functions
##            answer = raw_input('Where do you want me to put it? ')
##            print 'OK.  Going to:', answer
##            destination = self.goToNodeById(answer)
##            where = self.sensory_getCurrentLocation()
##            print 'I am here now.', where
##            self.putDownObject(this)
##            verify = self.peek('object')
##            print 'I put it here in ',where, verify
##
##        return

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

####################### functions for Agent output ###########################
    
    ################# examineContents(property)  ####################
    # function returns ALL PROPERTIES on node
    def examineLocation(self):
        
        if((self.peek('object')!=None)):
            replies = ["I found some kind of object, its a(n): "+self.peek('object'),
                   "Look what I found..a(n) "+self.peek('object'),
                   "Okay, I stumbled on a(n) "+self.peek('object')]
            return choice(replies)
        elif((self.peek('function')!=None)):
            return "I found this: "+self.peek('function')+" ...wonder what it does"
        else:
             return "Nothing of interest here!"

    ################ goToNode(cfg) ##################################
    # calls goToNodeByCfg(self,cfg) and returns location as cfg
    def goToNode(self,cfg):
        self.goToNodeByConfig(cfg)

        replies = ['okay, Im here. ','I made it. ', 'What a trip!, but I made it .',
                   'Im here. ','Im here, what next amigo? ']
        
        return choice(replies)

    ################ currentLocation() ###############################
    # returns Agents' current location
    def currentLocation(self):
        loc = self.sensory_getCurrentLocation()
        return "I am at "+str(reconstructCfg(loc))+" . "

    ################ error() ########################################
    #if no commands are found..return an error
    def error(self):

        replies = ["hmmm, I didnt get that, what did you want me to do? ",
                   "no entiendo. ",
                   "I have no idea what your talking about. ",
                   "Say again?",
                   "What did you want me to do again? ",
                   "Sorry, I dont understand. "]

        return choice(replies)

    ################ pickUp() #######################################
    #pick up object
    def pickItUp(self):
        ret = self.pickUp("object")
        #add that to what your carrying
        self.currentlyHolding.append(ret)
        if (ret != None):
            return "okay, i got it. "
        else:
            return "there is nothing to pick up. "

    #################### putDown() ##################################
    #puts down last object picked up
    def putItDown(self):
        
        try:
            value = self.currentlyHolding.pop()
        except:
            value = None
            
        if (value!=None):
            self.putDownObject(value)
            return "I put it down. "
        else:
            return "sorry...im not carrying anything. "

    ################# currentlyCarrying() #########################
    #reutrns object currently carrying
    def currentlyCarrying(self):
        if ((len(self.currentlyHolding))>0):
            string = "I am holding "
            holdingStr = ''
            for x in self.currentlyHolding:
                holdingStr = holdingStr+((str(x)+","))
            return (string+holdingStr+" . ")
        else:
            return 'im not holding anything. '

    ############### searchBwForAnyObject() ############################
    #scrape all of the world looking for any object
    def searchBwForAnyObject(self):
        ret = self.searchBWforObj()
        return 'I found a(n) '+ret+" . "

    ####################### help() ###################################
    # prompt for help with functions
    def help(self):
        replies = ['try asking for my current location. ',
                   'maby tell me to go to another configuration? ',
                   'I can search all of blocks world for something, just let me know. '
                   'I can search this node, just say the magic words. '] 
        return choice(replies)

<<<<<<< HEAD
#################### Non-Member Functions ##################################
        
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
    
    def generateCenterNode(n):
        i=[]
        for x in range(1,n+1):  
            n = []
            n.append(x)
            i.append(n)
        return i
=======
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
        

>>>>>>> 3cfc162332e14ff23593dc176000cf9190a236b4
