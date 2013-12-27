##########################################################################
##file: naturalLanguageProcessing.py
##Author: Ken Zyma
##Project: Blocks World and Agency
##
##Dependencies: nltk
##
##This file processes input for use in the AgentJBase class.
##
###########################################################################

import nltk
from nltk.corpus import treebank
from copy import copy
from copy import deepcopy

def delimiteByAnd(tokenList):
    list = []
    
    if 'and' in tokenList:
        i = tokenList.index('and')
        list.append(tokenList[:i])
        list.append(tokenList[(i+1):])
    else:
        list.append(tokenList)

    return list


def testForCurrentLocation(x):
    if (('location' in x) or (('where' in x)and('are' in x)and('you' in x))):
        return True
    else:
        return False

def testForMakeMove(x):
    if ((('go' in x)and('to' in x)) or (('move' in x)and('to' in x )) or
            (('continue' in x)and('to' in x))):
        return True
    else:
        return False

def findConfig(x):
    startIndex = x.index('[')
    #compute last instance of ]
    y = deepcopy(x)
    y.reverse()
    endIndex = len(x)- (y.index(']')+1)
    
    configTokens = x[startIndex:(endIndex+1)]

    #concatonate tokens and return result
    cfgString = ''
    for x in configTokens:
        cfgString = cfgString+x

    return cfgString

def testForSearchNode(x):
    if ((('search' in x) or (('look' in x)and('around' in x)) or (('look' in x)and('for' in x))
            or (('examine' in x)and('node' in x))or (('examine' in x)and('configuration' in x))
            or (('examine' in x)and('config' in x))or (('examine' in x)and('cfg' in x)))):
        return True
    else:
        return False

def testForPickUp(x):
    if ((('pick' in x)and('up' in x)) or (('grab' in x))or
            (('pick' in x)and('object' in x))):
        return True
    else:
        return False

def testForPutDown(x):
    if ((('put' in x)and('down' in x)) or (('drop' in x))or
            (('place' in x)and('object' in x))):
        return True
    else:
        return False

def testAskAboutHolding(x):
    if ((('what' in x)and('holding' in x)) or (('what' in x)and('carrying' in x))or
            (('you' in x)and('carrying' in x))or (('what' in x)and('holding' in x))):
        return True
    else:
        return False

def testSearchAllBwForAnything(x):
    if ((('search' in x)and('all' in x)) or (('search' in x)and('entire' in x))or
            (('look' in x)and('all' in x))or (('look' in x)and('entire' in x))):
        return True
    else:
        return False

def testHelp(x):
    if ('help' in x):
        return True
    else:
        return False

def convertSpeechToFunction(input):
    outputList = []

    #store as all lowercase
    input = input.lower()
    #convert to tokens
    token = (nltk.word_tokenize(input))
    
    #test for 'and', and separate to process each function
    delimited = delimiteByAnd(token)

    for x in delimited:
        if testForCurrentLocation(x):
            outputList.append("Agent.currentLocation()")
        elif testForMakeMove(x):
            config = findConfig(x)
            outputList.append("Agent.goToNode("+config+")")
        elif testSearchAllBwForAnything(x):
            outputList.append("Agent.searchBwForAnyObject()")
        elif testForSearchNode(x):
            outputList.append("Agent.examineLocation()")
        elif testForPickUp(x):
            outputList.append("Agent.pickItUp()")
        elif testForPutDown(x):
            outputList.append("Agent.putItDown()")
        elif testAskAboutHolding(x):
            outputList.append("Agent.currentlyCarrying()")
        elif testHelp(x):
            outputList.append("Agent.help()")
        else:
            outputList.append("Agent.error()")
            
        
    return outputList 

