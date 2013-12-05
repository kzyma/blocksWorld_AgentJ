##file: AStarHeuristics.py
##Author: Ken Zyma
## this file contains heuristic functions for block world basic functions.

#Heutistics

#always returns 0, used for simple testing as code
#was developed.
def DijkstraAlgorithm(cfg,goal):
        return 0

#2 and zero block heurstic
def zerOrTwoMoveHeuristic(cfg,goal):
        return numOf2MovesBasic(cfg,goal)+n(cfg)-numOfZeroMoves(cfg,goal)        

#more advnaced version of same Heuristic
def zerOrTwoMoveVersionTwoHeuristic(cfg,goal):
        return numOf2MovesAdvanced(cfg,goal)+n(cfg)-numOfZeroMoves(cfg,goal) 


#utiltiy functions
def numOfZeroMoves(cfg,goal):
        numOfZeroMoves = 0;
        cfgSubSet=buildSubset(cfg)
        goalSubSet=buildSubset(goal)
        #check for zero-moves
        for x in cfgSubSet:
                if x in goalSubSet:
                        numOfZeroMoves += 1
        return numOfZeroMoves

#if base1==base2 and some number is on both stacks with incorrect
#numbers under it, this must be a 2 move. numOf2MovesBasic counts only this.
def numOf2MovesBasic(cfg,goal):
        numOf2Moves = 0
        cfgStack = []
        goalStack = []
        
        for i in range(len(cfg)):
                for j in range(len(goal)):
                               if cfg[i][0]==goal[j][0]:
                                       cfgStack.append(cfg[i][1:])
                                       goalStack.append(goal[j][1:])
        for k in range(len(cfgStack)):
                for i in range(len(cfgStack[k])):
                        for j in range(len(goalStack[k])):
                                if (cfgStack[k][i]==goalStack[k][j])and(cfgStack[k][:j+1]!=goalStack[k][:j+1]):
                                        numOf2Moves += 1
         
        return numOf2Moves

def numOf2MovesAdvanced(cfg,goal):
        numOf2Moves = 0
        #if base1==base2 and some number is on both stacks with incorrect
        #numbers under it, this must be a 2 move. numOf2MovesBasic counts only this.
        numOf2Moves += numOf2MovesBasic(cfg,goal)
        #i believes if two or more numbers are in the same ordering they should be BUT,
        #there are incorret numbers under...these both must be 2 move to get them back into
        #the original configuration. Also we must make sure this does not conflict and double
        #count our basic Algorithm.
        for k in range(len(cfg)):
                for i in range(len(cfg[k])-1):
                        for j in range(len(goal)-1):
                                for l in range(len(goal[j])):
                                        if (cfg[k][i]==goal[j][l])and((i!=len(cfg[k])-1))and((l!=len(goal[j])-1)):
                                                if(cfg[k][i+1]==goal[j][l+1])and(cfg[k][:i]!=goal[j][:l]):
                                                        numOf2Moves += 1
         
        return numOf2Moves


def buildSubset(cfg):
        cfgSubSet=[]
        for i in range(len(cfg)):
                for j in range(len(cfg[i])):
                        cfgSubSet.append(cfg[i][:j+1])
        return cfgSubSet

def wrongBase(cfg,goal):
        wrongBase=0
        for i in range(len(cfg)):
                for j in range(len(goal)):
                        if(cfg[i][0]==goal[j][0]):
                                wrongBase += 1
        return wrongBase

def n(cfg):
        num = 0
        for i in range(len(cfg)):
               num += len(cfg[i])
        return num


