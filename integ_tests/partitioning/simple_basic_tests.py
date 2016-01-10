'''
Created on Jan 9, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from planar import Point
from partitioning.trajectory_partitioning import call_partition_trajectory
from partitioning.trajectory_partitioning import partition_trajectory
from partitioning.trajectory_partitioning import partition_cost_computer
from partitioning.trajectory_partitioning import no_partition_cost_computer

class Test(UnitBaseTests):

    def test_simple_line_segment(self):
        trajectory = [Point(0, 0), Point(1, 1)]
        expected_par = [0, 1]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
    def test_obvious_NOT_partition(self):
        trajectory = [Point(0, 0), Point(1, 1), Point(2, 0)]
        expected_par = [0, 1, 2]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
        
    def test_longer_obvious_NOT_partition(self):
        trajectory = [Point(0, 0), Point(1, 1), Point(2, 0), Point(3, 1), Point(4, 0)]
        expected_par = [0, 1, 2, 3, 4]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
        
    def test_obvious_partition(self):
        trajectory = [Point(0, 0), Point(10000, 1), Point(20000, 0)]
        expected_par = [0, 2]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
        
    def test_longer_obvious_partition(self):
        trajectory = [Point(0, 0), Point(10000, 1), Point(20000, 0), Point(30000, 2), Point(40000, 1)]
        expected_par = [0, 4]
        self.verify_iterable_works_more_than_once(expected_par, \
                                                  call_partition_trajectory(trajectory_point_list=trajectory))
    
    def test_not_enough_points(self):
        self.assertRaises(ValueError, call_partition_trajectory, [Point(1, 1)])
        self.assertRaises(ValueError, call_partition_trajectory, [])
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()