'''
Created on Nov 12, 2016

@author: jeanl
'''
import FlightDB as fDB
from Midterm_Graph import *

DBAddress = './Database/Graph.db'
AirAddress = './Database/AirportData.csv'
FlyAddress = './Database/FlightData.csv'
folder_name = './Database'

# Make a Database
database = fDB.FlightDB(folder_name)

GraphAddress = 'C:\Users\jeanl\workspace\CEE505 Midterm\src\Database'

# Try finding routes
g = Midterm_Graph(GraphAddress)
g.findPaths('MIA','SEA')
#print "Shortest Path"
#print g.findShortestPath('LGA', 'SFO')
print "Longest Path"
print g.findLongestPath('MIA','SEA')
