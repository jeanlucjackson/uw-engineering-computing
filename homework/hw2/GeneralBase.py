'''
Created on Oct 10, 2016

@author: jeanl
'''
# import functions from Problem3
import Problem3 as p
from operator import *
from operator import __floordiv__

class GeneralBase(object):
    '''
    GeneralBase containing a base and a value, corresponding to a number in a certain base (e.g. binary, hexadecimal) with a certain value.
    Value can be passed in either base 10 or in the base passed by the user. 
    '''

    def __init__(self, b = 10, v = 0):
        '''
        Constructor
        Value can be passed in either base 10 or in the base passed by the user.
        FromBaseToInteger handles the error if user passes a float type or if the value is beyond base16
        '''
        self.value = dict(base = b, value = p.FromBaseToInteger(v,b))
        
    def __str__(self):
        s = "{} (base {})".format( p.FromIntegerToBase(self.value['value'],self.value['base']), self.value['base'] )
        return s
        
    def Base(self):
        return int(self.value['base'])
    
    def ChangeBase(self, NewBase ):
        self.value.update({"base":NewBase})
        
    def __add__(self,y):
        result = self.value['value'] + y.value['value']
        return GeneralBase(self.value['base'], result)
        
    def __sub__(self,y):
        result = self.value['value'] - y.value['value']
        return GeneralBase(self.value['base'], result)
    
    def __mul__(self,y):
        result = self.value['value'] * y.value['value']
        return GeneralBase(self.value['base'], result)
        
    def __floordiv__(self,y):
        result = self.value['value'] // y.value['value']
        return GeneralBase(self.value['base'], result)
        
    def __mod__(self,y):
        result = self.value['value'] - (__floordiv__(self,y).value['value'] * y.value['value'])
        return GeneralBase(self.value['base'], result)
        
