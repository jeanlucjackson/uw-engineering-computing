'''
Jean-Luc Jackson
CEE cinco zero cinco HW #4
11/07/16
'''

#Import Directories
import os
import sys
import sqlite3 as DBI
import copy

# Import Path Classes
from Path import *


class Midterm_Graph(object):
    '''
    Class Hosts A Graph Object.
    Reads Data From Provided .txt File
    Creates/Stores A Series of Node-Line Relationships
    Contained Attributes - Line Objects, Node Objects
    Contained Algorithms - Path Finder, Shortest Path Finder
    '''


    def __init__(self, folder_name):
        '''
        Creates a Graph object by reading from 'Graph.db' database located in folder_name.
        '''
        # Changes Directory To Folder Location
        os.chdir( folder_name )
        self.folder_name = folder_name
        self.dbFilename = 'Graph.db'
        
        
        # Nodes and Lines already exist in database at DBAddress.
        # Connect to database at provided address
        try:
            self.db = DBI.connect(self.dbFilename)
            self.cu = self.db.cursor()
            self.db.text_factory = str
            print "Connected to database at {}.".format(self.dbFilename)
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)

        
    def __str__(self):
        pass
        
   
    def findPaths(self, startNode, destNode, pastPath=Path(), allPaths=[],first=True):
        '''
        This Method Travels Down Lines Until destNode Has Been Reached.
        Returns List Containing Path Objects Which Reached destNodeID.
        Takes arguments: -startNode, From Which Subsequent Paths Are Found
                         -destNode, Final Node We're Seeking As Our Destination
                         -pastPath, Path We've Traveled Up To This Point
                         -allPaths, List Containing Path Objects Seeking destNote
        '''
        # If it's the first recursion (just got called), clear the previous findPath data
        if first:
            allPaths = []
            # Create database table with this Trip's name
            self.createTripTable('{}to{}'.format(startNode,destNode))
            
        
        # If We've Visited This Node Before, Don't Go Any Further
        # Return An Empty List
        for nodeName in pastPath.getNodeHistory():
            if startNode == nodeName:
                #print "Line has already been stepped through."
                lastLine = pastPath.getLineHistory()[-1]
                lastLineLength = self.DBgetLineLength(lastLine)
                
                # remove last line and length so we don't save it
                pastPath -= Path([],[lastLine],lastLineLength)
                return []
        
        # If We've Reached Our Destination, Don't Go Any Further
        # Return The Path Up to This Point
        if startNode == destNode:
            # Add Destination Node to Path (Step On Node)
            pastPath += Path([startNode],[],0.0)
            # Find The Last Line And Node
            lastLine = pastPath.getLineHistory()[-1]
            lastLineLength = self.DBgetLineLength(lastLine)
            lastNode = pastPath.getNodeHistory()[-1]
            
            # Save finalPath
            finalPath = copy.deepcopy(pastPath) 
            
            #Remove Previous Line, Node, And Line Length
            pastPath -= Path([lastNode],[lastLine],lastLineLength)
            
            return [finalPath]
        
        # If This Node Has Not Been Visited         
        # Add Current Node to Path (Step On Node)
        pastPath += Path([startNode],[],0.0)
        self.cu.execute("""
            SELECT f.'flight number'
            FROM FlightData as f
            WHERE f.[From] = ?
            """, [startNode])
        lineIDs = [row[0] for row in self.cu]
        
        # Find Path For Each Line Attached to startNode
        for line in lineIDs:
            # Get node (airport) we're traveling to from this line (flight) we're on
            self.cu.execute("""
                SELECT f.[To] FROM FlightData as f
                WHERE f.'flight number' = ? 
                """,[line])
            endNode = self.cu.fetchone()[0]
             
            # find this line's length
            lineLength = self.DBgetLineLength(line)
            # Calculate layover by difference in last flight's arrival and this flight's depart
            # Takes into account that if a layover is < 30 mins we add 24hrs
            try: # if this isn't the first flight, there will be a line history
                lastFlight = pastPath.getLineHistory()[-1]
                layover = self.DBgetLayoverTime(lastFlight,line)
            except IndexError:
                # if it's the first flight, there will be no history, so no layover
                layover = 0
                
            lineLength += layover
            
            tempPath = pastPath + Path([],[line],lineLength)
            nextPath = self.findPaths(endNode,destNode,tempPath,allPaths,False)
            
            if len(nextPath) == 0 and ( line not in pastPath.getLineHistory() )\
            and ( endNode not in pastPath.getNodeHistory() ):
                #nodes = [n.getID() for n in pastPath.getNodeHistory()]
                pastPath += Path([],[line],lineLength)
            
            allPathsIDs = [p.getID() for p in allPaths]
            if len(nextPath) == 1 and nextPath[0] not in allPaths:
                allPaths.append(nextPath[0])
        
        if first:
            self.savePathsToDB(allPaths)
        return allPaths
    
    def savePathsToDB(self,allPaths):
        # Build a string that represents the Trip name
        # Each trip gets its own table in database
        try:
            initialNode = allPaths[0].getNodeHistory()[0]
            lastNode = allPaths[0].getNodeHistory()[-1]
            tripName = "{}to{}".format(initialNode,lastNode)
        except IndexError:
            return
        
        # allPaths is a list containing Path objects.
        # Loop through this list of Paths and add them to the database
        RouteID = 0
        for path in allPaths:
            RouteID += 1
            nodeHistory = path.getNodeHistory()
            lineHistory = path.getLineHistory()
            totalLength = path.getLength()
            
            # Insert trip summary at first row of each Route group
            tripSummary = [ initialNode, lastNode,  RouteID ]
            self.cu.execute("""
                INSERT INTO {} ([From] , [To] , RouteID)
                VALUES ( ? , ? , ? )
                """.format(tripName),tripSummary) 
            
            # Loop through the lineHistory of this current Path and add
            # each flight in the history to the proper table in the database.
            seq = 0
            print "lineH = {}".format(lineHistory)
            print "nodeH = {}".format(nodeHistory)
            for line in lineHistory:
                print seq
                fromNode = nodeHistory[seq]
                toNode = nodeHistory[seq+1]
                via = lineHistory[seq]
                stepLength = self.DBgetLineLength(line)
                toSave = [fromNode, via, toNode, RouteID, seq + 1, stepLength]
                seeql = """
                    INSERT INTO
                    {}     ([From] , [Via] , [To] , RouteID , Seq , 'Trip Time')
                    VALUES ( ?      , ?     , ?    , ?      , ?   , ? )
                    """.format(tripName)
                self.cu.execute(seeql,toSave)
                seq += 1
        
            self.cu.execute("""
                UPDATE {} SET 'Trip Time' = {}
                WHERE RouteID = ?
                AND Via is NULL;
                """.format(tripName,totalLength),[RouteID])
        
        self.db.commit()
        print "\nAll possible routes from {} to {} saved to database.\n".format(initialNode,lastNode)
        
                  
    def findShortestPath(self, startID, endID):
        '''
        Find smallest length value from Trip Summary rows
        SELECT the row with the smallest 'Trip Time' where there is no Via value
        Convert time integer back to time time
        '''
        try:
            db = DBI.connect(self.dbFilename)
            cu = self.db.cursor()
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)
        
        tripName = '{}to{}'.format(startID,endID)
        
        # Find row with minimum length
        cu.execute("""
            SELECT t.RouteID
            FROM {} as t
            WHERE t.'Trip Time' in
                (SELECT MIN(t.'Trip Time') FROM {} as t
                 WHERE t.Via is NULL);
            """.format(tripName,tripName))
        RouteID = cu.fetchone()[0]
        
        return self.printRoute(startID,endID,RouteID)
    
    
    def findLongestPath(self, startID, endID):
        '''
        Find smallest length value from Trip Summary rows
        SELECT the row with the smallest 'Trip Time' where there is no Via value
        Convert time integer back to time time
        '''
        try:
            db = DBI.connect(self.dbFilename)
            cu = self.db.cursor()
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)
        
        tripName = '{}to{}'.format(startID,endID)
        
        # Find row with minimum length
        cu.execute("""
            SELECT t.RouteID
            FROM {} as t
            WHERE t.'Trip Time' in
                (SELECT MAX(t.'Trip Time') FROM {} as t
                 WHERE t.Via is NULL);
            """.format(tripName,tripName))
        RouteID = cu.fetchone()[0]
        
        return self.printRoute(startID,endID,RouteID)
        
        
    def printRoute(self,startID,endID,RouteID):
        # Prints the path of a given RouteID
        try:
            db = DBI.connect(self.dbFilename)
            cu = self.db.cursor()
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)
            
        tripName = '{}to{}'.format(startID,endID)
            
        # Find Summary Row of interest
        cu.execute("""
            SELECT t.'Trip Time'
            FROM {} as t
            WHERE t.RouteID = ?
            AND t.Via is NULL;
            """.format(tripName),[RouteID])
        length = cu.fetchone()[0]
            
        hours = (length/60)
        mins = (length%60)
        timeString = str(hours) + ':' + str(mins)
        
        # Get INITIAL city&state
        cu.execute("""
            SELECT a.City, a.State
            FROM AirportData as a
            WHERE a.Airport = ?;
            """,[startID])
        [startCity, startSta] = [i for i in cu.fetchone()]
        # Get DEST city&state
        cu.execute("""
            SELECT a.City, a.State
            FROM AirportData as a
            WHERE a.Airport = ?;
            """,[endID])
        [endCity, endSta] = [i for i in cu.fetchone()]
        
        s = '\n'
        # Get whole trip itinerary for shortest route
        cu.execute("""
            SELECT t.Seq, t.Via, t.[From], t.[To], t.'Trip Time'
            FROM {} as t
            WHERE t.RouteID = ?
            """.format(tripName),[RouteID])
        for row in cu.fetchall():
            if None in row: # Route Summary row contains 'None's
                s += 'Trip: {} | {}, {}  to  {} | {}, {}\n'.\
                format(startID,startCity,startSta,endID,endCity,endSta)
                s += 'Total length of time traveling: {} hours\n'.format(timeString)
            else: # Grab and label data for printing
                seq = row[0]
                via = row[1]
                fro = row[2]
                to = row[3]
                time = row[4]
                cu.execute("""
                    SELECT a.City, a.State, f.Depart, f.Arrival
                    FROM AirportData as a, FlightData as f
                    WHERE a.Airport = ?
                    AND f.'flight number' = ?;
                    """,[fro,via])
                [fromCity, fromSta,depart,arrive] = [i for i in cu.fetchone()]
                # Get TO city&state
                cu.execute("""
                    SELECT a.City, a.State
                    FROM AirportData as a
                    WHERE a.Airport = ?;
                    """,[to])
                [toCity, toSta] = [i for i in cu.fetchone()]
                
                s += 'Flight #{}: {} from {}, {} ({}) departing at {}, '\
                .format(seq,via,fromCity,fromSta,fro,depart)
                s += 'arriving in {}, {} ({}) at {}\n'.format(toCity,toSta,to,arrive)
        
        return s
            
    
    def createTripTable(self,name):
        self.cu.executescript("""
            DROP TABLE IF EXISTS {};
            CREATE TABLE {} (
                id           INTEGER not null primary key AUTOINCREMENT,
                [From]       CHAR(3),
                Via          TEXT,
                [To]         CHAR(3),
                RouteID      INTEGER,
                Seq          INTEGER,
                'Trip Time'  INTEGER
            );
            """.format(name,name))
            
    
    def DBgetLineLength(self, line):
        try:
            db = DBI.connect(self.dbFilename)
            cu = self.db.cursor()
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)
        
        cu.execute("""
            SELECT f.Depart, f.Arrival
            FROM FlightData as f
            WHERE f.'flight number' = ?;
            """,[line])
        
        [departAt, arriveAt] = [i for i in cu.fetchone()]
        depSplit = departAt.split(':')
        depInt = int(depSplit[0])*60 + int(depSplit[1])
        arrSplit = arriveAt.split(':')
        arrInt = int(arrSplit[0])*60 + int(arrSplit[1])
        
        return arrInt - depInt
    
    def DBgetLayoverTime(self,lastFlight,nextFlight):
        try:
            db = DBI.connect(self.dbFilename)
            cu = db.cursor()
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)
        
        # get time integer of last flight's arrival 
        cu.execute("""
            SELECT f.Arrival
            FROM FlightData as f
            WHERE f.'flight number' = ?
            """,[lastFlight])
        lastArrival = cu.fetchone()[0]
        arrSplit = lastArrival.split(':')
        arrInt = int(arrSplit[0])*60 + int(arrSplit[1])
        
        # get time integer of next flight's departure
        cu.execute("""
            SELECT f.Depart
            FROM FlightData as f
            WHERE f.'flight number' = ?
            """,[nextFlight])
        nextDepart = cu.fetchone()[0]
        depSplit = nextDepart.split(':')
        depInt = int(depSplit[0])*60 + int(depSplit[1])
        
        # calculate layover
        layover = depInt - arrInt
        if (layover < 30) or (layover < 0): # if we missed our flight
            layover += 24*60                # our trip just got 24 hrs longer
            
        return layover
