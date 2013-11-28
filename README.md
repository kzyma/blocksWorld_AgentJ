blocksWorld_AgentJ
==================

Repository is a central location for KU Artificial Intelligence I project. Creating an intelligent agent for traversing Blocks World n.

note*-If there is any issue calling the constructor of AgentJBase---it may have been cuased by deleting all nodes/relationships in a blocks world, but not reseting the index to again start at 1 when creating a new blocks world. If you are running on local server you must actually stop the server, delete the ./data folder, start the server and re-run. If done in graphene I believe this isnt an issue. The reason for this is AgentJBase's constructor puts the agent in the world at index 1, so if that doesnt exist an exeption is thrown.
