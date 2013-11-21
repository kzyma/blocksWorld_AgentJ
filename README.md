blocksWorld_AgentJ
==================

Repository is a central location for KU Artificial Intelligence I project. Creating an intelligent agent for traversing Blocks World n.

I. *createWorld_BW.py startup notes*

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
