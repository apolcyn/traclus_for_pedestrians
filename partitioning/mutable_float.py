'''
Created on Jan 8, 2016

@author: Alex
'''

class MutableFloat(object):
    def __init__(self, val):
        self.val = val
        
    def increment(self, other):
        self.val += other
    
    def multiply(self, other):
        self.val *= other
        
    def get_val(self):
        return self.val
