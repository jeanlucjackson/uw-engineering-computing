'''
Created on Nov 12, 2016

@author: jeanl
'''
import sys
import os
import sqlite3 as DBI


class FlightDB(object):
    
    def __init__(self,folder_name):
        
        os.chdir( folder_name )
        self.folder_name = folder_name
        self.dbFilename = 'Graph.db'
        
        # Delete database from previous run first
        try:
            os.remove(self.dbFilename)
            print "Last run's database deleted."
        except OSError:
            pass
        
        # Connect to database at provided address
        try:
            self.db = DBI.connect(self.dbFilename)
            self.cu = self.db.cursor()
            self.db.text_factory = str
            print "Connected to database at {}.".format(self.dbFilename)
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)
            
        # Create Table from FlightData
        try:
            print "flights"
            self.cu.executescript(self.createFlightTable())
            self.db.commit()
            print "FlightData table created." 
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)
            
        # Create Table from AirportData
        try:
            print "airports"
            self.cu.executescript(self.createAirportTable())
            self.db.commit()
            print "AirportData table created." 
        except DBI.Error as e:
            print "sqlite3 failed with error: {}".format(e)
            sys.exit(1)
            
        self.FileToDB(self.folder_name)
        self.closeDB()
        
        
    def FileToDB(self,folder_name):
        # Read .csv file and INSERT each line into AirportData table
        try:
            fIn = open('AirportData.csv','r')
            firstLine = fIn.readline().split(',')
            headers = [item.strip() for item in firstLine]
            indeces = range(1,len(headers)+1)
            mapper = dict(zip(headers,indeces))
            mapper[0] = 'id'
            print "Headers = ", mapper
            
            for line in fIn:
                splitted = line.split(',')
                stripped = [l.strip('\n') for l in splitted]
                print "Line = ", stripped
                self.cu.execute(self.addToAirportTable(),stripped)
                self.db.commit()
            
            print "File ({}) used to create database.\n".format(folder_name)
        except IOError:
            print "Could not open file for reading at: ({})".format(folder_name)
            sys.exit(1)
            
        try:
            fIn = open('FlightData.csv','r')
            firstLine = fIn.readline().split(',')
            headers = [item.strip() for item in firstLine]
            indeces = range(1,len(headers)+1)
            mapper = dict(zip(headers,indeces))
            mapper[0] = 'id'
            print "Headers = ", mapper
            
            for line in fIn:
                splitted = line.split(',')
                stripped = [l.strip('\n') for l in splitted]
                print "Line = ", stripped
                self.cu.execute(self.addToFlightTable(),stripped)
                self.db.commit()
            
            print "File ({}) used to create database.\n".format(folder_name)
        except IOError:
            print "Could not open file for reading at: ({})".format(folder_name)
            sys.exit(1)
            
            
    def closeDB(self):
        self.db.close()  
                  
                  
    def addToAirportTable(self):
        return """
            INSERT INTO AirportData ( Airport, City, State, longitude, latitude, x, y )
            VALUES ( ? , ? , ? , ? , ? , ? , ? );
            """
    
    def addToFlightTable(self):
        return """
            INSERT INTO FlightData ( 'flight number', Operator, [From], [To], Depart, Arrival )
            VALUES ( ? , ? , ? , ? , ? , ? );
            """
        
    def createAirportTable(self):
        return """
            DROP TABLE IF EXISTS AirportData;
        
            CREATE TABLE AirportData (
                id            INTEGER not null primary key AUTOINCREMENT,
                Airport       TEXT,
                City          CHAR(25),    
                State         TEXT,
                longitude     FLOAT(4),
                latitude      FLOAT(4),
                x             FLOAT(3),
                y             FLOAT(3)    
                );
            """
    
    def createFlightTable(self):
        return """
            DROP TABLE IF EXISTS FlightData;
        
            CREATE TABLE FlightData (
                id              INTEGER not null primary key AUTOINCREMENT,
                'flight number' TEXT,
                Operator        CHAR(25),
                [From]          TEXT,
                [To]            TEXT,
                Depart          TIME,
                Arrival         TIME        
                );
            """
