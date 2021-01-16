'''
Jean-Luc Jackson & Connor Lester
CEE cinco zero cinco HW #4
11/07/16
'''

#Import Directories
import os
import copy
import matplotlib.pyplot as plt

# Import Our Classes
from Line import *
from Node import *
from Path import *

class Graph(object):
    '''
    Class Hosts A Graph Object.
    Reads Data From Provided .txt File
    Creates/Stores A Series of Node-Line Relationships
    Contained Attributes - Line Objects, Node Objects
    Contained Algorithms - Path Finder, Shortest Path Finder
    '''

    def __init__(self, folder_name):
        '''
        Creates a Graph Object By Reading 'nodes.txt' and 'lines.txt'
        Files Located Provided Folder.
        '''
        
        # Changes Directory To Folder Location
        os.chdir( folder_name )
        self.folder_name = folder_name
        #print "Directory changed to {}. Building Graph...".format(folder_name)
        
        # Read 'nodes.txt' and Generate List Of Nodes
        #print "\nReading Nodes..."
        self.nodes = []
        f = open('nodes.txt', 'r')
        for line in f:
            splitline = line.strip().split('\t')
            nodeID = splitline[0]
            nodeX = float(splitline[1])
            nodeY = float(splitline[2])
            
            #Generates Node Object
            thisNode = Node(nodeID,Vector([nodeX,nodeY]))
            #print thisNode
            self.nodes.append(thisNode)
        f.close()
        
        # Read 'lines.txt' and Generate List Of Lines
        #print "\nReading Lines..."
        self.lines = []
        f = open('lines.txt', 'r')
        for line in f:
            splitline = line.strip().split('\t')
            lineID = splitline[0]
            nodeIid = splitline[1]
            nodeJid = splitline[2]
            nodeIobj = filter(lambda x: x.ID == nodeIid, self.nodes)[0]
            nodeJobj = filter(lambda x: x.ID == nodeJid, self.nodes)[0]
            
            # Generates Line Object
            thisLine = Line(lineID,nodeIobj,nodeJobj)
            #print thisLine
            self.lines.append(thisLine)
            
            # Attach Line IDs to Nodes
            nodeIobj.attach(lineID)
            nodeJobj.attach(lineID)
            
        f.close()
        
        self.pathDict = dict()
    
    '''STANDARD CALLS'''
    def __str__(self): # Print Statement
        '''
        Returns Number of Total Lines and Nodes As String.
        '''
        s = "Graph is made of {} lines and {} nodes.".format(self.numLines(),self.numNodes())
        return s
    
    '''INFORMATION CALLS'''
    def getNode(self,nodeID):   
        try:
            nodeID = str(nodeID)
            return [i for i in self.nodes if i.getID() == nodeID][0]
            
        # If Node Does Not Exist In Graph Object
        except IndexError:
            raise IndexError("Node {} does not exist.".format(nodeID))
        
    def getAllNodes(self):
        return [n.getID() for n in self.nodes]
  
    def numNodes(self):
        '''
        Returns the Number (Integer) of Nodes That Exist Within This Graph Object.
        '''
        return len(self.nodes)




    def getNodePosition(self,nodeID): # Exception Handling Included In getNode()
        '''
        Calls the Get Position Function For A Given Line.
        '''
        node = self.getNode(nodeID)
        return node.getPosition()  
    
    def getLine(self,lineID):
        try:
            lineID = str(lineID)
            return [i for i in self.lines if i.getID() == lineID][0]
        
        # If Line Does Not Exist In Graph Object
        except IndexError:
            raise IndexError("Line {} does not exist.".format(lineID))
    
    def numLines(self):
        '''
        Returns the Number (Integer) of Lines That Exist Within This Graph Object.
        '''
        return len(self.lines)
    
    def getLineLength(self,lineID): # Exception Handling Included In getLine()
        '''
        Calls the Length Function For A Given Line.
        '''
        line = self.getLine(lineID)
        return line.getLength()                 
    
    def getLineGivenNodes(self,nodeIid,nodeJid): # Exception Handling Included In getNode()
        '''
        Finds the Line Connecting Given Nodes
        '''
        iLines = self.getNode(str(nodeIid)).getLineIDs()
        jLines = self.getNode(nodeJid).getLineIDs()
        try:      
            lineID = [i for i in iLines if i in jLines]
            return [j for j in self.lines if j.getID() is lineID][0]
        
        # If No Lines Attached To Provided Nodes
        except IndexError:
            raise IndexError("No line exists between nodes {} and {}.".format(nodeIid,nodeJid))
            
    def getNodeGivenLine(self,nodeIid,lineID): # Exception Handling Included In getNode() and getLine()
        '''
        Finds the Second Node For A Given Node and Line
        '''       
        nodeIid = str(nodeIid)
        lineID = str(lineID)
        
        nodeIid = self.getNode(nodeIid).getID()
        lineID = self.getLine(lineID).getID()




        #If Line Connects To Provided Node
        try:
            nodeIid = [i for i in self.getLine(lineID).getNodeIDs()\
                       if i is nodeIid][0]
                
            #If Line Connects To Another Node
            try:
                nodeJid = [i for i in self.getLine(lineID).getNodeIDs()\
                           if i is not nodeIid][0]
                return self.getNode(nodeJid)
                
            # If Line Does Not Connect To Another Node
            except:
                raise IndexError("Error: No node exists at the other end of line {} from node {}."\
                .format(lineID,nodeIid))
            
        # If Line Does Not Connect To Provided Node
        except: 
            raise IndexError("Error: Line {} does not connect to node {}.".format(lineID, nodeIid))       
        
    def printGraph(self):
        '''
        Provides Graph Visulization
        '''
        try:            
            # Create List of X and Y Coordinates
            x = []
            y = []
            minx, miny, maxx, maxy = 0.0, 0.0, 0.0, 0.0
            for line in self.lines:
                x = [line.nodes[0].coord[0],line.nodes[1].coord[0]]
                y = [line.nodes[0].coord[1],line.nodes[1].coord[1]]
                plt.plot(x,y)
                
                #Format Plot Size
                x.append(minx)
                x.append(maxx)
                y.append(miny)
                y.append(maxy)
                minx, miny, maxx, maxy = min(x), min(y), max(x), max(y)
    
            # Format Plot
            plt.title('Visual Graph')
            plt.axis([minx-1,maxx+1,miny-1,maxy+1])
            plt.grid(True)
            
            # Label Nodes
            for n in self.nodes:
                plt.annotate('{}'.format(n.getID()), xy = (n.getPosition()[0],n.getPosition()[1]), textcoords='data')
                
            # Save Figure & Plot
            plotfilename = self.folder_name + '.png'
            plt.savefig(plotfilename)
            plt.show()
        
        # If Any Free Lines or Nodes
        except:
            raise IndexError("Lines or nodes are not fully attached.")
    
    '''ACTION CALLS'''    
    def attach(self,lineID,nodeID): # Exception Handling Included In getNode() and getLine()
        '''
        Calls Line Attachment Function. 
        '''
        line = self.getLine(lineID)
        node = self.getNode(nodeID)
        line.attach(node)
        
    def detach(self,lineID,nodeID): # Exception Handling Included In getNode() and getLine()
        '''
        Calls Line Detachment Function. 
        '''
        line = self.getLine(lineID)
        node = self.getNode(nodeID)
        line.detach(node)
    
    '''PATH FINDING CALLS'''
    def findPaths(self, startNodeID, destNodeID, pastPath=Path(), allPaths=[],first=True):
        '''
        This Method Travels Down Lines Until destNode Has Been Reached.
        Returns List Containing Path Objects Which Reached destNodeID.
        Takes arguments: -startNodeID, From Which Subsequent Paths Are Found
                         -destNode, Final Node We're Seeking As Our Destination
                         -pastPath, Path We've Traveled Up To This Point
                         -allPaths, List Containing Path Objects Seeking destNoteID
        '''
        # If it's the first recursion (just got called), clear the previous findPath data
        if first:
            allPaths = []
        
        # Find Node Objects From IDs
        startNode = self.getNode(startNodeID)
        destNode = self.getNode(destNodeID)
                
        # If We've Visited This Node Before, Don't Go Any Further
        # Return An Empty List
        for i in pastPath.getNodeHistory():
            if startNodeID == i.getID():
                #print "Line has already been stepped through."
                lastLine = pastPath.getLineHistory()[-1]
                # remove last line and length so we don't save it
                pastPath -= Path([],[lastLine],lastLine.getLength())
                return []
        
        # If We've Reached Our Destination, Don't Go Any Further
        # Return The Path Up to This Point
        if startNode == destNode:
            # Add Destination Node to Path (Step On Node)
            pastPath += Path([startNode],[],0.0)
            # Find The Last Line And Node
            lastLine = pastPath.getLineHistory()[-1]
            lastNode = pastPath.getNodeHistory()[-1]
            finalPath = copy.deepcopy(pastPath)
            
            #Save finalPath
            finalPath = copy.deepcopy(pastPath)
            #Remove Previous Line, Node, And Line Length
            pastPath -= Path([lastNode],[lastLine],lastLine.getLength())
            
            #print "Previous {}".format(pastPath)
            self.savePathsToDict(allPaths)
            return [finalPath]
        
        # If This Node Has Not Been Visited         
        # Add Current Node to Path (Step On Node)
        pastPath += Path([startNode],[],0.0)
        lineIDs = startNode.getLineIDs()
        # Find Path For Each Line Attached to startNode
        for lineID in lineIDs:
            # Find Line Object From ID
            line = self.getLine(lineID)    
            # Find endNode Down Line Object
            endNode = self.getNodeGivenLine(startNodeID, lineID)
            endNodeID = endNode.getID()
            #Find nextPath Usind The End Node
            tempPath = pastPath + Path([],[line],line.getLength())
            nextPath = self.findPaths(endNodeID,destNodeID,tempPath,allPaths,False)
            
            if len(nextPath) == 0 and self.getLine(lineID) not in pastPath.getLineHistory() and endNode not in pastPath.getNodeHistory():
                nodes = [n.getID() for n in pastPath.getNodeHistory()]
                pastPath += Path([],[line],line.getLength())
            
            if len(nextPath) == 1 and nextPath[0] not in allPaths:
                allPaths.append(nextPath[0])
        
        return allPaths
    
    def savePathsToDict(self, allPaths):
        try:
            initialNode = allPaths[0].getNodeHistory()[0].getID()
            lastNode = allPaths[0].getNodeHistory()[-1].getID()
        except IndexError:
            return
        
        pathName = "{}-{}".format(initialNode,lastNode)
        self.pathDict[pathName] = allPaths
        #print "Internal PathDict = {}".format(self.pathDict)
        
    def getPathDict(self):
        return self.pathDict
        
                  
    def findShortestPath(self, startID, endID):
        '''
        
        '''
        try:
            s = "{}-{}".format(startID,endID)
            pathsOf = self.pathDict[s]
        except KeyError:
            raise KeyError('Paths have not yet been found between nodes {} and {}. Use findPaths first.'.format(startID,endID))
        
        minL = 0
        shortestPath = pathsOf[0]
        for path in pathsOf[1:]:
            if path.getLength() < shortestPath.getLength():
                shortestPath = path
        
        nodeHistory = shortestPath.getNodeHistory()
        printHistory = [node.getID() for node in nodeHistory]
        printString = '( '
        for n in range(0,len(printHistory) - 1):
            printString += printHistory[n] + ' -> ' 
        printString += printHistory[-1] + ' )'
        
        sRet = "The shortest path from {} to {} is {} with a total length of {:.2f}."\
        .format(startID,endID,printString,shortestPath.getLength())
        
        return sRet
