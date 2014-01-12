################ BlocksWorld_AgentJ ##############
	AgentJ is a package containing the files to create and run an agent in the blocks world domain. The agents included can move from node to node, search the world for artifacts, place artifacts into the world, and take them out. Included in this package are the following subdirectories/files:

	CreateBlocksWorld: Contains file used to create a world for the agent to traverse and unit tests for createWorld_BW.  This database is saved in a neo4j database using py2neo.
	
	AgentClasses: Contains base class and derived class(es) for the agent. This folder also contains algorithms the agent uses, such as A Star (used for path finding).

	naturalLanguageProcessing: This file is necessary for taking input from the GUI in Application.py and translating to it's proper function call for the Agent. If you create a new agent and want to still use our Application.py, you must update the naturalLanguageProcessing as well to include any new functionality as possible i/o.

	Application.py: this is the main GUI application to be run. It can also be used as a good example of how to use the Agent/World State classes together to explore blocks world.

**for more information on the structure of this project and theory, see the "AgentInBlocksWorldPresentation" powerpoint or keynote.**


################### Authors: ####################
	Ken Zyma (Kutztown University)
	Erin Fowler (Kutztown University)
	Patrick Schemm (Kutztown University)
	Nathan Trone (Kutztown University)

	A special thanks also goes out to Dr. Riesks (Kutztown University). A lot of the fundamental code for this project (denoted by (*) throughout the source code) was either straight from or derived from his blocks world, used in CSC447: Artificial Intelligence 1.


################## Install: #######################

In order to use the full package of files the following 'extras' are needed (warning::if you use another version of any of the software it MAY not work):
 
- neo4j version 2.0.0-M06
- py2neo 1.6.1
- nltk 3.0 (Natural Language Toolkit--this is used sparingly now, only for 'tokenizing' but much more integration will be added as the project progresses)

1) Run a neo4j server on a local machine. This should default to localhost:7474, if it does not see "running on another server" below.

2) Creating the World: Go to CreateBlocksWorld, open and run createWorld_BW.py. Next run generateBW(*). *this parameter should be blocks world size.

3) The world is now created, now open and run Application.py file. A GUI screen will appear and allow commands to be typed in. Try a few such as:
   "Where are you?"
   "Go to node _____"
   " Search this node"
   "What are you holding"
   "help"

**Running On Another Server**
If you wish set up a database at another location there are two files that must be altered to work properly : 
1) createWorld_BW.py
2) worldState_BW.py

The variable graph_db at the top of both of these files must be changed to match the location of your database, where that be locally at a different port or remote. A sample of how to do this is also found commented out right after this. For more information on this see the py2neo documentation.

################### Bugs: ########################

Version 1 (december 2013):
	*Problems with the constructor in AgentJBaseClass*
	If you receive an error about any problems with the constructor in AgentJBase: The agent is defaulted to be placed into the world at index 1 (in our cases that was always the 'center node'. If for some reason this does not exists an exception will be raised. This may happen for the following reasons found thus far:
	   You used cypher to clear a database. If you cleared all nodes and relationships using a cypher query, then when you go to create a new database the index will NOT start at 1. You must go into your neo4j folder, go to data, and delete the graph.db folder. 
	
