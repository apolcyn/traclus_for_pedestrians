'''
Created on Jan 10, 2016

@author: Alex
'''
import unittest
from partitioning.mutable_float import MutableNumber
from partitioning.trajectory_partitioning import cummulative_distance_function_getter
from tests.unit_base_tests import UnitBaseTests

class CummulativeDistanceFunctionTest(UnitBaseTests):

    def mock_distance_function(self, a, b):
        return a + b
    
    def mock_accumulator_func_getter(self, func):
        total = MutableNumber(0)
        def _func(num):
            total.increment(func(num))
            return total.get_val()
        return _func

    def test_accumulates_distances(self):
        cum_dist_func = cummulative_distance_function_getter(individual_distance_func=self.mock_distance_function, \
                                                             accumulator_func_getter=self.mock_accumulator_func_getter)        
        list = [0, 2, 4, 6, 8]
        other = 3
        res = []
        for num in list:
            res.append(cum_dist_func(num, other))
        
        expected = [3, 8, 15, 24, 35]
        self.verify_iterable_works_more_than_once(res, expected)
        
        cum_dist_func = cummulative_distance_function_getter(individual_distance_func=self.mock_distance_function, \
                                                             accumulator_func_getter=self.mock_accumulator_func_getter)        
        list = [0, 2, 4, 6, 8]
        other = 2
        res = []
        for num in list:
            res.append(cum_dist_func(num, other))
        
        expected = [2, 6, 12, 20, 30]
        self.verify_iterable_works_more_than_once(res, expected)
                

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()