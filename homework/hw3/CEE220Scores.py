CEE220Scores Program (Python Code)  
''' 
Jean-Luc Jackson 
CEE cinco zero cinco HW #3 
10/28/16 
''' 
### Import functions 
from ClassGradesFunctions import * 
import numpy as np 
import matplotlib.pyplot as plt 

### File Initialization 
# Open orignal scores file for reading 
filename = 'CEE_220_Scores.txt' 
#filename = 'CEE_220_AlternativeList.txt' 
fIn = ReadFile(filename) 
print "\nFile ", filename, " opened.\n" 

### Organize Headers 
# Create list of Headers and Points Possible 
assignments = fIn.readline().split('\t') #read next line & split it up by tabs (\t)
headers = [item.strip() for item in assignments] #strip to remove \n strings
print "Headers: ", headers, "\n" 

points = fIn.readline().split('\t') #read next line & split it up by tabs (\t)
pointsPoss = [item.strip() for item in points] #strip to remove \n strings
print "Possible Points: ", pointsPoss, "\n"

# Create Dictionary that maps possible points to each assignment (keys = Headers,  values = PossiblePoints) 
AssignmentGrader = dict(zip(headers,pointsPoss)) 
print "AssignmentGrader: ", AssignmentGrader, "\n"

### Compute Target Score for each Assignment Group (HW, Labs, etc)
groups = ["Assignment","Lab","Midterm","Final","Score","Grade"] 
weights = {"Assignment":0.25,"Lab":0.05,"Midterm":0.40,"Final":0.30}
targetScores = dict.fromkeys(groups[:(len(groups) - 2)],0)

# Calculate Target Scores using SumGroups() function 
targetGrader = AssignmentGrader.copy() 
for thing in AssignmentGrader: #remove any bonus assignments from target
if thing.lower().find('bonus') > -1:
  targetGrader.pop(thing)
  
targetScores = SumGroups(targetGrader, targetScores, groups) 
print "Target Scores: ", targetScores, "\n"

### Create Student Dictionaries organized by Groups 
gradeVec = [] #used for plotting later 
students = {} #dictionary to collect all students and their points

rows = 0 
for line in fIn:
  rows += 1
  # Clean up each line for reading
  splitline = line.split('\t')
  #studentName = splitline[0]
  studentLine = dict(zip(headers,splitline))
  studentName = studentLine["Student"]
  
  # Use line's data to sum up into groups
  studentScores = dict.fromkeys(groups,0)
  studentScores = SumGroups(studentLine, studentScores, groups) # sum up points for each group
  students[studentName] = studentScores  # add this dictionary to global  dictionary 
  
  # Calculate Score and Grade for each student
  scoreGrade = GradeStudent(studentScores,targetScores,weights)
  students[studentName]["Score"] = scoreGrade["Score"]
  students[studentName]["Grade"] = scoreGrade["Grade"]
  gradeVec.append(scoreGrade["Grade"]) # add current student's grade to grade vector for plotting
  
print "There are {} students.\n".format(rows) 

### Plotting Statistical Analysis - Histogram 
bins = [x/100.0 for x in range(5,405,10)] 
plt.hist(gradeVec, bins) 
plt.ylabel('number of students') 
plt.xlabel('assigned numeric grade') 
plt.title('Grade distribution for CEE 220 ({})'.format(filename))
plotfilename = filename[:(len(filename) - 4)] + '.png' 
plt.savefig(plotfilename) 
print "Figure saved as {}.\n".format(plotfilename) 
plt.show() 
  
# Close file to prevent corruption 
fIn.close() 
if fIn.closed:
  print "File ",filename, " is closed.\n" 
else:
  print "File ",filename, " not properly closed.\n" 
