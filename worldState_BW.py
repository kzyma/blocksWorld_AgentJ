##########################################################################
##file: worldState_BW.py
##Author: Ken Zyma
##Project: Blocks World and Agency
##
##Dependencies: py2neo.py
##              neo4j data stored locally at...(localhost:7474/db/data)
##
##This file reports contains methods to report the current state of
##  blocks world.
###########################################################################


from py2neo import node, rel
from py2neo import neo4j
from py2neo import cypher
import logging

#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

class worldStateMachine:

    #current world State data
    location = ''
    node = ''

    ################ value semantics  ###################
    #constuct worldStateMachine object with initial location = center node
    def __init__(self):
        query = neo4j.CypherQuery(graph_db, "start n=node(1) return n")
        for record in query.stream():
            currentNode = record[0]
        self.node = currentNode
        self.location =  str(currentNode["id"])

    #################  getLocation()  ####################
    #return the current state location
    def getLocation(self):
        return self.location
       

    ##################  moveByRelation(mv)  ####################
    #this function takes a move as it's argument and queries the database based
    #on that move, if that move is legit it makes moves to the new node and
    #chnanges worldStateMachine's location to updated location.
    
    #****NOTE****: move MUST be in the form: MOVE_TO_, where _ is the index.The reason
    #for this is that these are the names of relations in the db.
    
    def moveByRelation(self,mv):        
        #query = 
        #start n=node(1)
        #match p=n-[relation:MOVEzeroTOone]->m
        #return m

        query = neo4j.CypherQuery(graph_db,"start n=node(1) match p=n-[relation:"+mv+"]->m return m")
        for record in query.stream():
            returnedNode = record[0]
        self.node = returnedNode
        self.location =  str(self.node["id"])



#devloper notes:
#Nov. 21st:
#   moveByRelation works nicely when the move
#   is possible, but throws a nasty, application breaking
#   exception when you try a move that does not exist, need to find
#   a better way to handle, maby with a try-catch block, where the exception
#   can be handled by calling function instead of blasting up to __main()__
#
