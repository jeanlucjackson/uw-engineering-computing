''' 
Jean-Luc Jackson 
CEE 505 HW #3 
10/28/16 
Functions used by CEE220Scores.py 
''' 

def ReadFile(address):
  '''
  Opens file for reading at specified address. 
  '''
  try:
    f = open(address,'r')
    return f
  except IOError:
    print "Could not open file for reading at: ({})".format(address)
    
def WriteFile(address):
  try:
    f = open(address,'w')
    return f
  except IOError:
    print "Could not open file for writing at: ({})".format(address)
    
def SumGroups(dIter,dReturn,groups):
  '''
  Iterates over keys in dIter. If the key matches a category in groups, the value  for that key
  is added to the corresponding current value in dReturn (usually dReturn starts  with all 0 values).
  '''
  for key in dIter:
    if dIter[key] == '':
      adder = 0
    else:
      try:
        adder = float(dIter[key])
      except ValueError:
        adder = 0 
 
    if key.lower().find(groups[0].lower()) > -1:
      dReturn[groups[0]] = dReturn[groups[0]] + adder
      
    if key.lower().find(groups[1].lower()) > -1:
      dReturn[groups[1]] = dReturn[groups[1]] + adder
    
    if key.lower().find(groups[2].lower()) > -1:
      dReturn[groups[2]] = dReturn[groups[2]] + adder
    
    if key.lower().find(groups[3].lower()) > -1:
      dReturn[groups[3]] = dReturn[groups[3]] + adder
      
  return dReturn


def GradeStudent(studentScores,targetScores,weights):
  '''
  Calculates the Score & Grade for a given student's studentScores, compared to  targetScores.
  Uses passed weights dictionary to weigh score calculation.  '''
  score = 0
  for key in targetScores:
    score += weights[key] * (studentScores[key] / targetScores[key])
    
  grade = round( (score - 0.20)/0.20 , 1 )
  
  if grade <= 0.7:
    grade = 0
    
  return {"Score":min(score,1.0),"Grade":grade}
