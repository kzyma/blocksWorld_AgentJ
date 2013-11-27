from AgentJBaseClass import *


############## test App for AgentJBase ##########################
# this is meant to test code and show how our objects could     #
# possiblty interact to eventually create our main application  #
#                                                               #

Agent = AgentJBase()

print 'Current Starting Location of Agent is:'
print Agent.sensory_getCurrentLocation()

print 'Agent  MOVE (indx 1) TO (indx 2)'
Agent.makeMove(1,2)
print 'Agents current Location:'
print Agent.sensory_getCurrentLocation()

print 'go to node by id 1a2a3a'
Agent.goToNodeById('1a2a3a')
print 'Agents current Location:'
print Agent.sensory_getCurrentLocation()

print 'go to configuration [[1,3,2]]'
cfg=[[1,3,2]]
Agent.goToNodeByConfig(cfg)
print Agent.sensory_getCurrentLocation()

print 'go to configuration [[1],[2],[3]]'
cfg=[[1],[2],[3]]
Agent.goToNodeByConfig(cfg)
print Agent.sensory_getCurrentLocation()

print 'go to node by id "1a302a"'
Agent.goToNodeById("1a302a")
print Agent.sensory_getCurrentLocation()

print 'go to configuration [[1,2,3]]'
cfg=[[1,2,3]]
Agent.goToNodeByConfig(cfg)
print Agent.sensory_getCurrentLocation()

print 'go to configuration [[1],[3,2]]'
cfg=[[1],[3,2]]
Agent.goToNodeByConfig(cfg)
print Agent.sensory_getCurrentLocation()

print 'go to configuration [[3],[1,2]]'
cfg=[[3],[1,2]]
Agent.goToNodeByConfig(cfg)
print Agent.sensory_getCurrentLocation()

print 'go to configuration [[1],[2],[3]]'
cfg=[[1],[2],[3]]
Agent.goToNodeByConfig(cfg)
print Agent.sensory_getCurrentLocation()

print 'put down object: TROPHY'
Agent.putDownObject("Trophy")

print 'now lets go back to config [[3],[1,2]]'
cfg=[[3],[1,2]]
Agent.goToNodeByConfig(cfg)
print Agent.sensory_getCurrentLocation()

print 'lets go back to our center node..[[1],[2],[3]]'
cfg=[[1],[2],[3]]
Agent.goToNodeByConfig(cfg)
print Agent.sensory_getCurrentLocation()

print 'is our object still here?'
print Agent.peek("object")

print 'yup, im gonna pick it up'
print Agent.pickUp("object")

print 'I picked it up....is it still in the world?'
print Agent.peek("object")
print 'Nope!'

print 'Now lets try to put down, pick up, and evaluate a function'
print 'put down 1+2'
Agent.putDownFunction("1+2")
print 'lets see if its there..'
print Agent.peek("function")
print 'sweet, now im going to pick it up, and evaluate it'
holding = Agent.pickUp("function")
print Agent.evaluateItem(holding)

print 'creating global function i=(str(1+2+3))'
i=((1+2+3))
print 'place i in the world, take it out and evaluate'
Agent.putDownFunction(i)
holding = Agent.pickUp("function")
print Agent.evaluateItem(holding)

