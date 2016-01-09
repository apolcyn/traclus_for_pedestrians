'''
Created on Jan 7, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from partitioning.trajectory_partitioning import partition_cost_computer
from partitioning.trajectory_partitioning import no_partition_cost_computer
from partitioning.mutable_float import MutableFloat

class PartitionCostComputerTest(unittest.TestCase):
    
    def mock_line_segment_iterable_getter(self, num_list, expected_low, expected_high):
        def mock(list, low, high, line_seg_getter):
            if low != expected_low or high != expected_high:
                raise Exception("unexpected index val")
            return num_list[low:high + 1]
        return mock
    
    def mock_geometric_series_model_cost_computer(self):
        total = MutableFloat(1.0)
        def mock(num):
            total.multiply(num)
            return total.get_val()
        return mock
    
    def mock_adder_model_cost_computer(self, func):
        total = MutableFloat(0.0)
        def mock(num):
            total.increment(func(num))
            return total.get_val()
        return mock
    
    def mock_global_dist_func(self, func):
        total = MutableFloat(0.0)
        def mock(num, other_num):
            total.increment(func(num, other_num))
            return total.get_val()
        return mock
    
    def abs_val_distance_func(self, a, b):
        return abs(a - b)      
    
    def mock_partition_line_getter(self, cost, expected_low, expected_high):
        def mock(list, low, high):
            if low != expected_low or high != expected_high:
                raise Exception("unexpected index")
            return cost
        return mock

    def test_partition_cost_multipler_distance_func(self):
        segments = [0, 9, 3, 1, 3, 5, 7, 9]
        seg_iterable_getter = self.mock_line_segment_iterable_getter(segments, 3, 8)
        partition_line_getter = self.mock_partition_line_getter(4, 3, 8)
        model_cost_computer = self.mock_adder_model_cost_computer(lambda num: num * 3)
        distance_function = self.mock_global_dist_func(lambda x, y: abs(x * y))
        
        cost = partition_cost_computer(segments, 3, 8, seg_iterable_getter, \
                                       partition_line_getter, model_cost_computer, distance_function)
        self.assertEquals(112, cost)
        
    def test_partition_cost_abs_diff_distance_func(self):
        segments = [0, 9, 3, 1, 3, 5, 7, 9]
        seg_iterable_getter = self.mock_line_segment_iterable_getter(segments, 3, 8)
        partition_line_getter = self.mock_partition_line_getter(4, 3, 8)
        model_cost_computer = self.mock_adder_model_cost_computer(lambda num: num * 3)
        distance_function = self.mock_global_dist_func(lambda x, y: abs(x - y))
        
        cost = partition_cost_computer(segments, 3, 8, seg_iterable_getter, \
                                       partition_line_getter, model_cost_computer, distance_function)
        self.assertEquals(25, cost)
        
    def test_no_partition_cost_normal_case(self):
        segments = [1, 3, 5, 7, 9, -1, 2, 3]
        seg_iterable_getter = self.mock_line_segment_iterable_getter(segments, 0, 4)
        model_cost_computer = self.mock_adder_model_cost_computer(lambda num: num * 3)
        
        cost = no_partition_cost_computer(segments, 0, 4, seg_iterable_getter, model_cost_computer)
        
        self.assertEquals(75, cost)
        
    def test_no_partition_cost_normal_subtracter_dist_function(self):
        segments = [1, 3, 5, 7, 9, -2, 3, 4]
        seg_iterable_getter = self.mock_line_segment_iterable_getter(segments, 0, 4)
        model_cost_computer = self.mock_adder_model_cost_computer(lambda num: num * -3)
        
        cost = no_partition_cost_computer(segments, 0, 4, seg_iterable_getter, model_cost_computer)
        
        self.assertEquals(-75, cost)
        
    def test_bad_input_indices(self):
        segments = [1, 3, 5, 7, 9, -2, 3, 4]
        seg_iterable_getter = self.mock_line_segment_iterable_getter(segments, 0, 4)
        model_cost_computer = self.mock_adder_model_cost_computer(lambda num: num * 3)
        partition_line_getter = self.mock_partition_line_getter(4, 5, 3)
        distance_function = self.mock_global_dist_func(lambda x, y: None)
        
        self.assertRaises(IndexError, no_partition_cost_computer, segments, 5, 3, \
                          seg_iterable_getter, model_cost_computer)
        self.assertRaises(IndexError, partition_cost_computer, segments, 5, 3, seg_iterable_getter, \
                                       partition_line_getter, model_cost_computer, distance_function)
        
        partition_line_getter = self.mock_partition_line_getter(4, 2, 2)
        
        self.assertRaises(IndexError, no_partition_cost_computer, segments, 2, 2, \
                          seg_iterable_getter, model_cost_computer)
        self.assertRaises(IndexError, partition_cost_computer, segments, 2, 2, seg_iterable_getter, \
                                       partition_line_getter, model_cost_computer, distance_function)
        
    def test_no_line_segs_provided(self):
        segments = [1, 3, 5, 7, 9, -2, 3, 4]
        seg_iterable_getter = lambda l, low, high, func: []
        model_cost_computer = self.mock_adder_model_cost_computer(lambda num: num * 3)
        partition_line_getter = self.mock_partition_line_getter(4, 5, 3)
        distance_function = self.mock_global_dist_func(lambda x, y: None)
        
        self.assertRaises(Exception, no_partition_cost_computer, segments, 5, 3, \
                          seg_iterable_getter, model_cost_computer)
        self.assertRaises(Exception, partition_cost_computer, segments, 5, 3, seg_iterable_getter, \
                                       partition_line_getter, model_cost_computer, distance_function)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()