#########################################################################
##
##file: AgentJBaseClass.py
##Author: Ken Zyma
##Project: Blocks World and Agency
##
##This file contains utility functions for AgentJ Class
##Edited by: Erin Fowler Nov 26, 2013
##Changes made:  Below functions moved from AgentJBaseClass and put in new class
###########################################################################

#******************************convertNtoStr()**************************
#Actions:       takes n and converts to string
#Return:	returns dictionary
#********************************************************************
def convertNtoStr(n):
        return {
                '1': "one",
                '2': "two",
                '3': "three",
                '4': "four",
                '5': "five",
                '6': "six",
                '7': "seven",
                '8': "eight",
                '9': "nine",
                '0': "zero",
                '-1': "table",
                }.get(n,"none")

#*********************************reconstructCfg()**************************
#Actions:       re-build the BW cfg from it's id
#Return:	configuration
#********************************************************************
def reconstructCfg(nodeID):
        cfg=[]
        i=1
        while i<len(nodeID):
                current=nodeID[(i-1):i]
                temp=[]
                while current!='a':
                        if (current != '0'):
                                temp.append(int(current))
                        i = i+1
                        current=nodeID[(i-1):i]
                cfg.append(temp)
                i = i+1
        return cfg

#*********************************unstranslateMv()**************************
#Actions:  takes a split move, looks for it in node and returns its idx
#Return:   returns an int
#********************************************************************
def untranslateMv(a,node):
        #take care of special case--table
        if (a=="-1"):
                return -1
        #all other cases
        for i in node:
                if int(a) in i:
                        return node.index(i)
                
#*********************************numbize()**************************
#Actions:       generate a number, is called in genCfgId()
#Return:	returns a number
#Changes:       None
#********************************************************************
def numbize(nList):
        num=0
        for n in nList:
                num*=100
                num+=n
        return num

#***********************genCfgId()*****************************************
#Actions: generate configuration ID in the form of a string
#         stacks separated by a's and blocks separated by 0's
#Returns: string configuration ID
#**************************************************************************
def genCfgId(cfg):
        nL=map(numbize,cfg)
        nL.sort()
        cfId=''
        for n in nL:
                cfId+=str(n)+'a'
        return cfId

