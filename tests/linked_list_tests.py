'''
Created on Jan 2, 2016

@author: Alex
'''
import unittest
from linked_list import LinkedList

class Test(unittest.TestCase):
    
    def build_test_ob(self, values):
        return {'values': values}

    def setUp(self):
        self.test_cases = []
        self.test_cases.append(self.build_test_ob([0, 1, 2, 3, 4, 5]))
        self.test_cases.append(self.build_test_ob([0]))
        self.test_cases.append(self.build_test_ob([]))

    def test_linked_list(self):
        for test_ob in self.test_cases:
            list = LinkedList()
            for val in test_ob['values']:
                list.add_last(val)
            r_list = LinkedList()
            for val in list:
                r_list.add_first(val)
            i = 0
            for val in list:
                self.assertEqual(val, test_ob['values'][i])
                i += 1
            i = len(test_ob['values']) - 1
            for val in r_list:
                self.assertEqual(val, test_ob['values'][i])
                i -= 1
            
                
                
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_linked_list']
    unittest.main()