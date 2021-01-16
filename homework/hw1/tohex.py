'''
Jean-Luc Jackson
CEE cinco zero cinco HW #1
10/04/16

Problem 3 - Binary and Hex code converter

tobin(s) -- input DECIMAL -> return HEX

'''

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

'''
Testing Code
-test random integer
-test zero
-test negative integer
'''
print "Testing integer that doesn't result in hex letters"
print "tohex(25):", tohex('25')
print "python fxn:",hex(25)[2:]

print '\n'

print "Testing integer that results in hex letters"
print "tohex(98734):", tohex('98734')
print "python fxn  :", hex(98734)[2:]

print '\n'

print "Testing zero"
print "tohex(0)  :", tohex('0')
print "python fxn:","{0:b}".format(0)

print '\n'

print "Testing negative integer"
print "tohex(-123):", tohex('-123')
print "python fxn :", (hex(-123)[0] + hex(-123)[3:])
