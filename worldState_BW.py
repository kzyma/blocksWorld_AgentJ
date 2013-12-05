<<<<<<< HEAD
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
from GUIApp import *

#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

#graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

neo4j.authenticate("blocksworld5.sb01.stations.graphenedb.com:24789","blocksWorld5", "TZrxoHKHzmBVSwFoelLX")
graph_db = neo4j.GraphDatabaseService("http://blocksworld5.sb01.stations.graphenedb.com:24789/db/data/")

class worldStateMachine:

    #current world State data
    location = ''
    node = ''
    centerNodeCfg = ''

    ################# value semantics  #######################
    #constuct worldStateMachine object with initial location = center node
    def __init__(self):
        query = neo4j.CypherQuery(graph_db, "start n=node(1) return n")
        for record in query.stream():
            currentNode = record[0]
        self.node = currentNode
        self.centerNodeCfg = (str(currentNode["id"]))
        self.setLocation(str(currentNode["id"]))

    #################  getLocation()  ########################
    #return the current state location
    def getLocation(self):
        print 'Agent is at '+self.location
        return self.location

    #################  setLocation() #########################
    #set current state location
    def setLocation(self,location):
        self.location = location

    #################  getNode()  ############################
    #return current state node

    def  getNode(self):
        return self.node
       

    ################## moveByRelation(mv)  ####################
    #this function takes a move as it's argument and queries the database based
    #on that move, if that move is legit it makes moves to the new node and
    #chnanges worldStateMachine's location to updated location.
    
    #****NOTE****: move MUST be in the form: MOVE_TO_, where _ is the index.The reason
    #for this is that these are the names of relations in the db.
    
    def moveByRelation(self,mv):
        query = neo4j.CypherQuery(graph_db,"start n=node(*) where n.id='"
                                  +self.location+"' match p=n-[relation:"+mv+"]->m return m")
        for record in query.stream():
            returnedNode = record[0]
        self.node = returnedNode
        self.setLocation(str(self.node["id"]))

    #################  addPropertyToLocation(prop,value)  ########
    #function will add property to current location node
    def addPropertyToLocation(self,prop,value):
        query = neo4j.CypherQuery(graph_db, "START n=node(*) WHERE (n.id='"
                                  +self.location+"') set n."+str(prop)+"='"+str(value)+"' return n")
        for record in query.stream():
            returnedNode = record[0]
        self.node = returnedNode
        print str(value)+' added to blocks world'


    #################  deletePropertyFromLocation(prop)   ########
    #function will delete property from current node
    def deletePropertyFromLocation(self,prop):
        #first set property to NULL
        query = neo4j.CypherQuery(graph_db, "START n=node(*) WHERE (n.id='"
                                  +self.location+"') set n."+str(prop)+"=NULL return n")

        for record in query.stream():
            currentNode = record[0]
        self.node = currentNode

        

    ##################  getValueOfPropertyAtLocation(prop)  ########
    # function returns value of property passed of current node
    def getValueOfPropertyAtLocation(self,prop):
        query = neo4j.CypherQuery(graph_db,"start n=node(*) where n.id='"
                                  +self.location+"' return n."+str(prop))

        for record in query.stream():
            returnValue = record[0]
        return returnValue
=======
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
from GUIApp import *

#uncomment for debug logging
#logging.basicConfig(level=logging.DEBUG)

#graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

neo4j.authenticate("blocksworld5.sb01.stations.graphenedb.com:24789","blocksWorld5", "TZrxoHKHzmBVSwFoelLX")
graph_db = neo4j.GraphDatabaseService("http://blocksworld5.sb01.stations.graphenedb.com:24789/db/data/")

class worldStateMachine:

    #current world State data
    location = ''
    node = ''
    centerNodeCfg = ''

    ################# value semantics  #######################
    #constuct worldStateMachine object with initial location = center node
    def __init__(self):
        query = neo4j.CypherQuery(graph_db, "start n=node(1) return n")
        for record in query.stream():
            currentNode = record[0]
        self.node = currentNode
        self.centerNodeCfg = (str(currentNode["id"]))
        self.setLocation(str(currentNode["id"]))

    #################  getLocation()  ########################
    #return the current state location
    def getLocation(self):
        print 'Agent is at '+self.location
        return self.location

    #################  setLocation() #########################
    #set current state location
    def setLocation(self,location):
        self.location = location

    #################  getNode()  ############################
    #return current state node

    def  getNode(self):
        return self.node
       

    ################## moveByRelation(mv)  ####################
    #this function takes a move as it's argument and queries the database based
    #on that move, if that move is legit it makes moves to the new node and
    #chnanges worldStateMachine's location to updated location.
    
    #****NOTE****: move MUST be in the form: MOVE_TO_, where _ is the index.The reason
    #for this is that these are the names of relations in the db.
    
    def moveByRelation(self,mv):
        query = neo4j.CypherQuery(graph_db,"start n=node(*) where n.id='"
                                  +self.location+"' match p=n-[relation:"+mv+"]->m return m")
        for record in query.stream():
            returnedNode = record[0]
        self.node = returnedNode
        self.setLocation(str(self.node["id"]))

    #################  addPropertyToLocation(prop,value)  ########
    #function will add property to current location node
    def addPropertyToLocation(self,prop,value):
        query = neo4j.CypherQuery(graph_db, "START n=node(*) WHERE (n.id='"
                                  +self.location+"') set n."+str(prop)+"='"+str(value)+"' return n")
        for record in query.stream():
            returnedNode = record[0]
        self.node = returnedNode
        print str(value)+' added to blocks world'


    #################  deletePropertyFromLocation(prop)   ########
    #function will delete property from current node
    def deletePropertyFromLocation(self,prop):
        #first set property to NULL
        query = neo4j.CypherQuery(graph_db, "START n=node(*) WHERE (n.id='"
                                  +self.location+"') set n."+str(prop)+"=NULL return n")

        for record in query.stream():
            currentNode = record[0]
        self.node = currentNode

        

    ##################  getValueOfPropertyAtLocation(prop)  ########
    # function returns value of property passed of current node
    def getValueOfPropertyAtLocation(self,prop):
        query = neo4j.CypherQuery(graph_db,"start n=node(*) where n.id='"
                                  +self.location+"' return n."+str(prop))

        for record in query.stream():
            returnValue = record[0]
        return returnValue
>>>>>>> d9d0307acca9d18bcb4a78b1feb3eab0fe1266ee
