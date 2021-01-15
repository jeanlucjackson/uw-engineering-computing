'''
Created on Oct 12, 2016

@author: jeanl
'''

if __name__ == '__main__':
    from GeneralBase import GeneralBase
    
    #a = GeneralBase(16,'16ced')
    #b = GeneralBase(2,'11101001')
    a = GeneralBase(16,'ad4')
    b = GeneralBase(2,'1111011')
    
    print "Testing Format:"
    print "(operator tested) (first value) (operator) (second value)"
    print "(Result from GeneralBase)"
    print "(Result from python formatting function) = python(_)"
    print
    print "Begin Testing..."
    print
    
    print a
    print "{:x} = python(a)".format(a.value['value'])
    print b
    print "{:b} = python(b)".format(b.value['value'])
    
    print
    print "Adding {} + {}".format(a,b)
    c = a + b
    
    print c
    print "{:x} = python(c)".format(c.value['value'])
    
    print
    print "Adding {} + {}".format(b,a)
    d = b + a
    print d
    print "{:b} = python(d)".format(d.value['value'])
    
    print
    print "Subtracting {} - {}".format(a,b)
    e = a - b
    print e
    print "{:x} = python(e)".format(e.value['value'])
    
    print
    print "Subtracting {} - {}".format(b,a)
    f = b - a
    print f
    print "{:b} = python(f)".format(f.value['value'])
    
    print
    print "Multiplying {} * {}".format(a,b)
    g = a*b
    print g
    print "{:x} = python(g)".format(g.value['value'])
    
    print
    print "Multiplying {} * {}".format(b,a)
    h = b*a
    print h
    print "{:b} = python(h)".format(h.value['value'])
    
    print
    print "Integer Dividing {} // {}".format(a,b)
    i = a//b
    print i
    print "{:x} = python(i)".format(i.value['value'])
    
    print
    print "Integer Dividing {} // {}".format(b,a)
    j = b//a
    print j
    print "{:b} = python(j)".format(j.value['value'])
    
    print
    print "Modulo {} % {}".format(a,b)
    k = a % b
    print k
    print "{:x} = python(k)".format(k.value['value'])
    
    print
    print "Modulo {} % {}".format(b,a)
    l = b % a
    print l
    print "{:b} = python(l)".format(l.value['value'],)
    print
    
    print "Code to Test per Mackenzie"
    a = GeneralBase(2,256)

    b = GeneralBase(8,256)

    c = GeneralBase(16,256)

    d = a * (b + c)
    dtest = 256*(256+256)

    for i in range(2,17):

        d.ChangeBase(i)
        print i, d
        
    print "python base 2 {:b}".format(dtest)
    print "python base 8 {:o}".format(dtest)
    print "python base 16 {:x}".format(dtest)
    
    x = GeneralBase(16,255)
    print x
    y = GeneralBase(16,'ff')
    print y
