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
        
    def test_single_value_case(self):
        indices = [0]
        vals = ['a']
        expected = ['a']
        res = filter_by_indices(good_indices=indices, vals=vals)
        self.verify_iterable_works_more_than_once(res, expected)
        
    def test_indices_too_high(self):
        indices = [0, 3, 5]
        vals = ['a', 'b', 'c', 'd', 'e']
        expected = ['a', 'd', 'f']
        res = filter_by_indices(good_indices=indices, vals=vals)
        func = lambda iter: [x for x in iter]
        self.assertRaises(Exception, func, res)
        
    def test_nonzero_first_index(self):
        indices = [1, 3, 5]
        res = filter_by_indices(good_indices=[1, 3, 5], vals=[2, 4, 2])
        func = lambda iter: [x for x in iter]
        self.assertRaises(Exception, func, res)
                
    def test_empty_input(self):
        res = filter_by_indices(good_indices=[], vals=[])
        func = lambda iter: [x for x in iter]
        self.assertRaises(Exception, func, res)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_normal_case']
    unittest.main()