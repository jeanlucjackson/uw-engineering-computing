'''
Created on Oct 11, 2016

@author: jeanl
'''

#if __name__ == '__main__':
    
# define function
def frombin(s):
    # Make sure s is string, initialize counter & collector
    s = str(s)
    i = 0
    dec = 0
    for n in s:
        dig = int(n)
        dec += dig * pow(2, len(s) - 1 - i)
        i += 1
    
    return dec

# define function
def fromhex(s):
    # Create dictionary to convert from base16 base to base10
    d = dict(a=10,b=11,c=12,d=13,e=14,f=15)
    # Make sure s is string, initialize counter & collector
    s = str(s)
    i = 0
    dec = 0
    for n in s:
        # Check if the current character is a number or letter
        if d.has_key(n):
            dig = d[n]                              # if letter, lookup in dictionary
        else:
            dig = int(n)                            # if number, just use number
        dec += dig * pow(16, len(s) - 1 - i)
        i += 1
    
    return dec

def FromBaseToInteger(value, base):
    '''
    Used within GeneralBase to to convert incoming values of any base to integers (base 10)
    for internal computation efficiency.
    Currently does not handle cases where base > 16. JL20161018
    '''
    # Stop if the base is > 16
    if base > 16:
        print "Base must be within 2 and 16. Changing base from {} to 10 and proceeding with value of {}...".format(base,value)
        base = 10
    
    # Convert value with any base to a base10 object
    # if it's already an integer, just return its originally passed value
    if type(value) == int:
        return value
    
    # If user provided a float value to GeneralBase, this is the first time that we will encounter an error. Report such an error.
    elif type(value) == float:
        print "FromBaseToInteger Message:"
        print "Value cannot be float type ({:.2f}). Converting float to integer ({}) and proceeding...".format(value, int(value))
        return int(value)
    
    # Create dictionary to convert from any base to base10 - d must be modified for bases > 16
    d = dict(a=10,b=11,c=12,d=13,e=14,f=15)
    # Make sure s is string, initialize counter & collector
    input = str(value)
    
    # Initialize & Loop
    i = 0
    dec = 0
    for n in input:
        # Check if the current character is a number or letter
        if d.has_key(n):
            dig = d[n]                              # if letter, lookup in dictionary
        else:
            dig = int(n)                            # if number, just use number
        dec += dig * pow(base, len(input) - 1 - i)
        i += 1
    
    return dec

def FromIntegerToBase(i,base):
    '''
    Used within GeneralBase to convert internal integer "value" from dictionary
    to necessary base value for reporting purposes.
    This function is only called *after* FromBaseToInteger, so it currently does NOT handle cases where
    the input is NOT an integer. Change as necessary. JL20161018
    '''
    
    # Create DEC to HEX dictionary - d must be modified for bases > 16
    d = {10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'}
    
    # Convert input to integer value & intialize collector
    v = abs(int(i))
    rem = ''
    
    # Cover s = 0 case
    if v == 0:
        rem = 0
    
    # Loop through inputted string
    while v > 0:
        if d.has_key(v%base):
            rem = d[v%base] + rem
        else:
            rem = str(v%base) + rem    # add new remainder onto FRONT of string
        
        v = v/base
    
    # if the original input was negative, add a negative sign to the beginning of string
    if int(i) < 0:
        rem = '-' + rem
        
    return rem



# define function
def tobin(s):
    # Convert input to integer value & intialize collector
    v = abs(int(s))
    rem = str(v%2)
    v = v/2
    
    # Loop through inputted string
    while v > 0:
        rem = str(v%2) + rem    # add new remainder onto FRONT of string
        v = v/2                 # binary is base 2
    
    # if the original input was negative, add a negative sign to the beginning of string
    if int(s) < 0:
        rem = '-' + rem
        
    return rem

# define function
def tohex(s):
    # Create DEC to HEX dictionary
    d = {10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'}
    
    # Convert input to integer value & intialize collector
    v = abs(int(s))
    rem = ''
    
    # Cover s = 0 case
    if v == 0:
        rem = 0
    
    # Loop through inputted string
    while v > 0:
        if d.has_key(v%16):
            rem = d[v%16] + rem
        else:
            rem = str(v%16) + rem    # add new remainder onto FRONT of string
        
        v = v/16                 # hex is base 16
    
    # if the original input was negative, add a negative sign to the beginning of string
    if int(s) < 0:
        rem = '-' + rem
        
    return rem
