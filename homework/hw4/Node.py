'''
Jean-Luc Jackson & Connor Lester
CEE cinco zero cinco HW #4
11/07/16
'''

from Vector import *


class Node(object):
    '''
    Class Hosts a Node Object.
    Contained Attributes - Node ID and Vector Object.
    Vector Object Functions as Coordinates For Node's Position. 
    '''
    
    def __init__(self, ID, v):
        '''
        Constructor.
        ''' 
        # Store ID
        self.ID = ID
        # Store Node Coordinates As Vector
        self.coord = Vector(v)
        # Keep A List of Attached Lines (their IDs)
        self.lineIDs = []
               
    def getPosition(self):
        '''
        Returns Coordinates of the Node (Vector Object).
        '''
        return self.coord

    '''STANDARD CALLS'''
    def __str__(self): # Print Statement
        s = "Node {} located at coordinates ({}, {}).".format(self.ID,self.coord[0],self.coord[1])
        return s
    
    '''INFORMATION CALLS'''    
    def getID(self):
        '''
        Returns Node ID.
        '''
        return self.ID
    
    def getLineIDs(self):
        '''
        Returns Line ID List.
        '''
        return self.lineIDs
    
    '''ACTION CALLS'''
    def attach(self, lineID):
        '''
        Attaches Node to the Provided Line. 
        Adds Line ID to Internal Line ID List.
        '''
        # If the Line Provided Is Not Attached
        if lineID not in self.lineIDs:
            self.lineIDs.append(lineID)
            self.lineIDs.sort()
            print "Node {} attached to line {}.".format(self.ID,lineID)
         
        # If the Line Provided Is Attached   
        else:
            print "Error: Node {} already connected to line {}."\
            .format(self.ID,lineID)
           
    def detach(self, lineID):
        '''
        Detaches Node From the Provided Line. 
        Adds Line ID to Internal Line ID List.
        '''
        # If the Node is Attached to At Least One Line
        if len(self.lineIDs) > 0:
            # If the Node is Attached to the Provided Line
            if lineID in self.lineIDs:
                self.lineIDs.remove(lineID)
                print "Node {} detached from line {}."\
                .format(self.ID,lineID) 
            
            # If the Node is Not Attached to the Provided Line
            else:
                print "Error: Node {} is not connected to line {}.".format(self.ID,lineID)
        
        # If the Node is Not Attached to Any Lines         
        else:
            print "Error: Node {} is not connected to any lines.".format(self.ID)
