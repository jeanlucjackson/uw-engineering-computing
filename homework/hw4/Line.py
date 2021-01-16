'''
Jean-Luc Jackson & Connor Lester
CEE cinco zero cinco HW #4
11/07/16
'''

class Line(object):
    '''
    Class Hosts A Line Object.
    Contained Attributes - Line ID, Node Objects And Node IDs.
    '''
    
    def __init__(self, ID, nodeIobj, nodeJobj):
        '''
        Constructor.
        '''
        # Store ID
        self.ID = ID
        # Store/Sort Node Object As List
        self.nodes = [nodeIobj, nodeJobj]
        self.nodes.sort()
        # Store/Sort Node Coordinates As List
        self.nodeIDs = [nodeIobj.ID, nodeJobj.ID]
        self.nodeIDs.sort()
    
    '''STANDARD CALLS'''
    def __str__(self): # Print Statement
        s = "Line {} connects node {} to node {}.".format(self.ID,self.nodeIDs[0],self.nodeIDs[1])
        return s
    
    def __len__(self): # Raises An Error
        raise TypeError("Line object has no integer length. Use getLength() for line length.")
    
    '''INFORMATION CALLS'''              
    def getLength(self):
        '''
        Uses Vector Math to Calculate the Length of the Line (See Vector Class).
        Returns the Length of the Line as a Float.
        '''
        try:
            a = (self.nodes[0].coord)
            b = (self.nodes[1].coord)
            ab = (b-a)
            c = (ab[0]**2+ab[1]**2)**(0.5)
            return c
        
        # If Line Is Not Connected To Two Nodes (Line Has Zero Length)
        except:
            raise IndexError("Line {} is not fully connected and has no length."\
                             .format(self.ID))
            
    def getID(self):
        '''
        Returns Line ID.
        '''
        return self.ID
    
    def getNodeIDs(self):
        '''
        Returns Node ID List.
        '''
        return self.nodeIDs
    
    '''ACTION CALLS'''
    def attach(self, nodeobj):
        '''
        Attaches Line to the Provided Node. 
        Adds Node to Internal Node List.
        Adds Node ID to Internal Node ID List.
        '''
        # If the Line is Not Full And If the Provided Node is Not Already Attached
        if len(self.nodeIDs) < 2 and (nodeobj not in self.nodes):
            # Appends Node Object
            self.nodes.append(nodeobj)
            self.nodes.sort()
            # Appends Node ID
            self.nodeIDs.append(nodeobj.ID)
            self.nodeIDs.sort()
            print "Line {} attached to node {}. Line now connects nodes {} and {}."\
            .format(self.ID,nodeobj.ID,self.nodeIDs[0],self.nodeIDs[1])
            # Calls Node Attachment And Passes Line ID
            nodeobj.attach(self.ID)
        
        # If the Line is Full Xor the Provided Node is Already Attached    
        else:
            print "Error: Line {} already connected to nodes {} and {}."\
            .format(self.ID,self.nodeIDs[0],self.nodeIDs[1]),\
            "Use detach() before attaching to another node."
    
    def detach(self, nodeobj):
        '''
        Detaches Line From the Provided Node. 
        Removes Node From Internal Node List.
        Removes Node ID From Internal Node ID List.
        '''
        # If the Line is Attached to At Least One Node
        if len(self.nodes) > 0:
            # If the Line is Attached to the Provide Node
            if nodeobj in self.nodes:
                self.nodes.remove(nodeobj)
                self.nodeIDs.remove(nodeobj.ID)
                print "Line {} detached from node {}.".format(self.ID,nodeobj.ID)
                # Calls Node Detachment And Passes Line ID
                nodeobj.detach(self.ID)
            
            # If the Line is Not Attached to the Provided Node
            else:
                print "Error: Line {} is not connected to node {}."\
                .format(self.ID,nodeobj.ID),\
                "Use attach() to do so."
        
        # If the Line is Not Attached to Any Nodes      
        else:
            print "Error: Line {} is not connected to any nodes. Use attach() to do so.".format(self.ID)
