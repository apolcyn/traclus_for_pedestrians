'''
Created on Jan 6, 2016

@author: Alex
'''
import unittest
from line_segment_averaging import number_average,\
    line_segment_averaging_set_generator
from linked_list import LinkedList
from tests import unit_base_tests

def simple_func(num):
    return num

class LineSegmentAveragingTest(unit_base_tests.UnitBaseTests):    
    def test_bad_input(self):
        self.assertRaises(Exception, number_average, [], simple_func)
    
    def test_number_averaging_normal(self):
        self.assertEquals(number_average([0.0, 1.0, 2.0, 3, 4, 5], simple_func), 2.5)
        self.assertEquals(number_average([0.0, 1.0, 2.0, 3, 4, 5], simple_func), 2.5)
        self.assertEquals(number_average([0, 1, 2, 3, 4, 11], simple_func), 3.5)
        list = LinkedList()
        list.add_last(0)
        self.assertEquals(number_average(list, simple_func), 0)
        
    def test_line_segment_generator(self):
        lines = [self.create_line_seg([(0, 0), (1, 2)]), \
                 self.create_line_seg([(3, 2), (3, 4)]), \
                 self.create_line_seg([(4, 5), (2, 3)])]
        test_ob = {'horizontal_position':3, 'lines': [] }
        for line in lines:
            test_ob['lines'].append(lines)
        expected = map(lambda seg: {'horizontal_pos':3, 'lines': seg }, lines)
        
        i = 0
        for item in line_segment_averaging_set_generator(test_ob):
            self.assertEquals(expected[i], item)
            i += 1
        
        self.assertEquals([line_segment_averaging_set_generator(test_ob)], expected)
        
    def test_empty_lines(self):
        test_ob = {'horizontal_position': 4, 'lines': []}
        self.assertEquals([line_segment_averaging_set_generator(test_ob)], [])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()