'''
Created on Jan 10, 2016

@author: Alex
'''
import unittest
from coordination import filter_by_indices
from tests.unit_base_tests import UnitBaseTests

class Test(UnitBaseTests):

    def test_normal_case(self):
        indices = [0, 3, 5]
        vals = ['a', 'b', 'c', 'd', 'e', 'f']
        expected = ['a', 'd', 'f']
        res = filter_by_indices(good_indices=indices, vals=vals)
        self.verify_iterable_works_more_than_once(res, expected)
        
    def test_two_values(self):
        indices = [0, 1]
        vals = ['a', 'b']
        expected = ['a', 'b']
        res = filter_by_indices(good_indices=indices, vals=vals)
        self.verify_iterable_works_more_than_once(res, expected)
        
    def test_single_value_case(self):
        indices = [0]
        vals = ['a']
        expected = ['a']
        self.verify_iteration_raises(ValueError, filter_by_indices(good_indices=indices, vals=vals))
        
    def test_indices_too_high(self):
        indices = [0, 3, 5]
        vals = ['a', 'b', 'c', 'd', 'e']
        res = filter_by_indices(good_indices=indices, vals=vals)
        self.verify_iteration_raises(exception_type=IndexError, \
                                     iterable=filter_by_indices(good_indices=indices, vals=vals))
        
    def test_nonzero_first_index(self):
        indices = [1, 3, 5]
        res = filter_by_indices(good_indices=[1, 3, 5], vals=[2, 4, 2])
        self.verify_iteration_raises(exception_type=Exception, \
                                     iterable=filter_by_indices(good_indices=[1, 3, 5], vals=[2, 4, 2]))
                
    def test_empty_input(self):
        self.verify_iteration_raises(exception_type=ValueError, \
                                     iterable=filter_by_indices(good_indices=[], vals=[]))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_normal_case']
    unittest.main()