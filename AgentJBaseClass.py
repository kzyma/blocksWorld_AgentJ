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
##
###########################################################################


from py2neo import node, rel
from py2neo import neo4j
import logging

#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

#get database
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

class AgentJBase:

    #def __init__(self):
        

    #state parameter is type worldStateMachine
    def sensory_getCurrentLocation(self,state):
        return state.getLocation()

    #move Agent by: start: index of block you want to move
    #               stop:  index of location you want to move it
    def makeMove(self,start,stop,state):    
        srt = self.convertNtoStr(str(start))
        stp = self.convertNtoStr(str(stop))
        mv="MOVE"+srt+"TO"+stp
        state.moveByRelation(mv)


#############classes utility functions##################
    #these should all be moved to a new class, i am just lazy right now...
        
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



##################### UNIT TEST #################################
# this is meant to test code and show how our objects could     #
# possiblty interact to eventually create our main application  #
#                                                               #

from worldState_BW import *
import unittest

BW = worldStateMachine()
Agent = AgentJBase()

print 'Current Starting Location of Agent is:'
print Agent.sensory_getCurrentLocation(BW)

print 'Agent wants to MOVE (indx 0) TO (indx 1)'
Agent.makeMove(0,1,BW)
print Agent.sensory_getCurrentLocation(BW)
