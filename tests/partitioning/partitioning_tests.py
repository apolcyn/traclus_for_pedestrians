'''
Created on Jan 8, 2016

@author: Alex
'''
import unittest
from partitioning.trajectory_partitioning import partition_trajectory
from tests.unit_base_tests import UnitBaseTests

class PartitioningTest(UnitBaseTests):
    
    def get_mock_cost_computer(self, cost_table):
        def func(list, low, high, cost_table=cost_table):
            if cost_table[low][high] == None:
                raise Exception("hit an invalid index")
            return cost_table[low][high]
        return func
    
    def test_gets_borders(self):
        par_cost_table = [[None, None], [None, None]]
        no_par_cost_table = [[None, None], [None, None]]
        list = [None] * 2
        expected = [0, 1]
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table))
        self.verify_iterable_works_more_than_once(expected, actual)
        
    def test_get_borders_of_three_item_list(self):
        par_cost_table = [[None, None, 4], [None, None, None], [None, None, None]]
        no_par_cost_table = [[None, None, 5], [None, None, None], [None, None, None]]
        list = [None] * 3
        expected = [0, 2]
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table))
        self.verify_iterable_works_more_than_once(expected, actual)
        
    def test_get_all_of_three_item_list(self):
        par_cost_table = [[None, None, 6], [None, None, None], [None, None, None]]
        no_par_cost_table = [[None, None, 5], [None, None, None], [None, None, None]]
        list = [None] * 3
        expected = [0, 1, 2]
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table))
        self.verify_iterable_works_more_than_once(expected, actual)
        
    def test_get_all_of_four_item_list(self):
        par_cost_table = \
        [[None, None, 3, 3], \
         [None, None, None, 4], \
         [None, None, None, None], \
         [None, None, None, None]]
        
        no_par_cost_table = \
        [[None, None, 2, 2], \
         [None, None, None, 3], \
         [None, None, None, None], \
         [None, None, None, None]]
        
        list = [None] * 4
        expected = [0, 1, 2, 3]
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table))
        self.verify_iterable_works_more_than_once(expected, actual)
        
    def test_get_some_of_four_item_list(self):
        par_cost_table = \
        [[None, None, 2, 3], \
         [None, None, None, None], \
         [None, None, None, None], \
         [None, None, None, None]]
        
        no_par_cost_table = \
        [[None, None, 2, 2], \
         [None, None, None, None], \
         [None, None, None, None], \
         [None, None, None, None]]
        
        list = [None] * 4
        
        expected_partition = [0, 2, 3]
        actual = partition_trajectory(list, self.get_mock_cost_computer(par_cost_table), \
                                      self.get_mock_cost_computer(no_par_cost_table))
        self.verify_iterable_equals_list(actual, expected_partition)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()