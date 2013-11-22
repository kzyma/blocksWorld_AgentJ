blocksWorld_AgentJ
==================

Repository is a central location for KU Artificial Intelligence I project. Creating an intelligent agent for traversing Blocks World n.

I. ................................createWorld_BW.py notes to Start................................

  +as of right now the following needs to be done to create BW. Right now it's kind of thrown together, but hopefully tommorow I will have the oppertunity work on the code and finish it up...so for now i'll explain as I go.
  
  1) you need to have neo4j server running.
  
  2) in python run:
      >>> n = generateBW(insert BW number here)
    
  3) next you will need to print this by just typing:
      >>> n 
    
  4) you will now get all of the nodes and relations that the python program created, the reason you need to do it this way for now is becuase i cannot figure out how to omit the brackets ,[ ], from a list..which I am working on. So now copy everythiing inside of these (omit brackets)..
  
    example to copy:
    node({'id': '1a2a'}), node({'id': '201a'}), node({'id': '102a'}), rel(0, 'MOVEzeroTOone', 1), rel(0, 'MOVEoneTOzero',     2), rel(2, 'MOVEzeroTOtable', 0), rel(1, 'MOVEzeroTOtable', 0)
  
  5) Now here is workaround #2, python does not permit you to pass more than 255 args into a function, so for now just use a pointer to this. Like the following:
      >>> args = PASTE EVERYTHING YOU COPIED FROM STEP 4
    
  6) Finally!, run:
      >>>> graph_db.create(*args)
      
II. ............................worldState_BW.py and AgentJBaseClass.py notes.............................

  +these two classes contain things that I have been testing out for how we can build our application. i think it will be alot easier if we build a few classes to use with basic functionality build in. Agent and World_state are unfortunatly right now tightly coupled, so they must both be used, this is however, built from a design I was talking to Dr. R about after class today and something he recommended for the project.
  
  
    +Basically worldSate_BW holds the current state of our Blocks World (what node agent is at, ect) and as you can see in the file will handle ALL talking to our database. To make it easier consider the following:
    
    1)our Agent wants to know where he is, so he must 'sense' where he is (ask the world for current location)
    2) our agent wants to move to a new state. He must do so by moving 'block by block' until reaching his (sorry erin or 'her') goal. 
    
    +Thus the only 2 things our block can do is 'see' where he is, and 'move' to an adjacent block. EVERY other action can be derived from these two 'senses'. So contained in the files are those two senses with an example at the bottom of AgentJBase.py under "unit tests" on how I used the classes. Next, I am going to work on another basic 'sense' for the agent, that is leaving something in blocks world, and searching a node for anything left there...woohoo
