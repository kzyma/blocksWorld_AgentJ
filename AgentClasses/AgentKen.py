##########################################################################
##
##file: AgentKen.py
##Author: Ken Zyma
##date: December 2013
##      
##This file contains agent Ken, derived off of agentJ. Agent Ken makes using
##  the natural language processing more entertaining by providing 'canned'
##  expressions for output.
###########################################################################

from AgentJBaseClass import *

class AgentKen(AgentJBase):
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
