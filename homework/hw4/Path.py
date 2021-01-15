'''
Jean-Luc Jackson & Connor Lester
CEE 505 HW #4
11/07/16
'''

class Path(object):
    '''
    Class Hosts a Path Object.
    Contained Attributes - Path ID, Length, and Node/Line Histories.
    '''

    def __init__(self, nodeHistory=[], lineHistory=[], length=0.0):
        '''
        CHANGE SO THAT passes node objects and line objects and can calculate length
        by looping through lineHistory and summing up line.getLength() values.
        affects Path() implementation in Graph class
        '''
        # Initialize List of Nodes Visited - Contains Node Objects
        self.nodeHistory = nodeHistory
        # Initialize List of Lines Traveled - Contains Line Objects
        self.lineHistory = lineHistory
        # Initialize Length to Zero
        self.length = float(length)
        
        # Create pathID
        s = ''
        for i in range(0,len(nodeHistory)):
            s += str(nodeHistory[i].getID()) + ' -> '
        self.ID = '( ' + s[:len(s) - 4] + ' )'
        
    '''STANDARD CALLS'''
    def __str__(self): # Print Statement
        s = "Path {} has a length {} and has seen {} nodes and {} lines."\
        .format(self.ID,self.length, len(self.nodeHistory), len(self.lineHistory))
        return s
    
    def __add__(self,otherPath): # Add Error If Trying To Add Integer/Float
        # Step Through Line - Add Line to lineHistory
        newLineHistory = self.lineHistory + otherPath.getLineHistory()
        # Step On Node - Add Node to nodeHistory
        newNodeHistory = self.nodeHistory + otherPath.getNodeHistory()
        # Increase Path's Length
        newLength = self.length + otherPath.getLength()
        return Path(newNodeHistory, newLineHistory, newLength)
    
    def __sub__(self,otherPath): # Add Error If Trying To Subtract Integer/Float
        # Step Back Through Line - Remove Line From lineHistory
        newLineHistory = self.lineHistory
        newNodeHistory = self.nodeHistory
        for line in otherPath.getLineHistory():
            newLineHistory = self.lineHistory
            self.lineHistory.remove(line)
        # Step On Node - Removed Node From nodeHistory
        for node in otherPath.getNodeHistory():
            newNodeHistory = self.nodeHistory
            self.nodeHistory.remove(node)
        # Decrease Path's Length
        newLength = self.length - otherPath.getLength()
        return Path(newNodeHistory, newLineHistory, newLength)
       
    '''INFORMATION CALLS'''       
    def getID(self):
        return self.ID
    
    def getLength(self):
        # Return the Current Length
        return self.length
    
    def getNodeHistory(self):
        # Return Current nodeHistory
        return self.nodeHistory
    
    def getLineHistory(self):
        # Return Current lineHistory
        return self.lineHistory
