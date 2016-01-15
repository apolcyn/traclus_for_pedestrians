'''
Created on Jan 13, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from planar import Point
from coordination import the_whole_enchilada
import math
from representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY

class JumboShrimpTest(UnitBaseTests):
    
    def verify_point_iterable_almost_equals_list(self, iterable, expected_list):
        total_count = 0
        
        for rep_line_seg in iterable:
            self.assertTrue(total_count < len(expected_list))
            count = 0
            for point in rep_line_seg:
                self.assertTrue(count < len(expected_list[total_count]))
                self.assertTrue(point.almost_equals(expected_list[total_count][count]))
                count += 1
            self.assertEquals(count, len(expected_list[total_count]))
            total_count += 1
        self.assertEquals(total_count, len(expected_list))
        
    def test_two_line_segs(self):
        points = [[Point(0, 1), Point(1, 1)], \
                  [Point(0, 0), Point(1, 0)]]
        expected = [[Point(0, 0.5), (1, 0.5)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=100, min_neighbors=1, min_num_trajectories_in_cluster=2, min_vertical_lines=2, min_prev_dist=1.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_two_line_segs_two_clusters(self):
        points = [[Point(0, 1), Point(1, 1)], \
                  [Point(0, 0), Point(1, 0)]]
        expected = [[Point(0, 1), Point(1, 1)], \
                  [Point(0, 0), Point(1, 0)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=0.5, min_neighbors=0, min_num_trajectories_in_cluster=1, min_vertical_lines=1, min_prev_dist=1.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_three_by_three_two_clusters(self):
        points = [[Point(0, 1), Point(1, 1), Point(2, 1)], \
                  [Point(0, 0), Point(1, 0), Point(2, 0)], \
                  [Point(0, 3), Point(1, 3), Point(2, 3)]]
        expected = [[Point(0, 0.5), Point(1, 0.5), Point(2, 0.5)], \
                  [Point(0, 3), Point(1, 3), Point(2, 3)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=1, min_neighbors=0, min_num_trajectories_in_cluster=1, min_vertical_lines=1, min_prev_dist=1.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_one_long_line_joins_two_short_lines(self):
        points = [[Point(0, 1), Point(1, 1), Point(2, 1), Point(3, 1), Point(4, 1)], \
                  [Point(0, 0), Point(1, 0)], \
                  [Point(3, 2), Point(4, 2)]]
        expected = [[Point(0, 0.5), Point(1, 2.0/3), Point(2, 1), Point(3, 4.0/3), Point(4, 1.5)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=2, min_neighbors=3, min_num_trajectories_in_cluster=3, min_vertical_lines=1, min_prev_dist=1.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
    def test_two_45_degree_line_segments(self):
        points = [[Point(0, 1), Point(1, 0)], \
                  [Point(1, 2), Point(2, 1)]]
        expected = [[Point(0.5, 1.5), Point(1.5, 0.5)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=math.sqrt(2.0), min_neighbors=1, min_num_trajectories_in_cluster=2, \
                                  min_vertical_lines=2, \
                                  min_prev_dist=math.sqrt(2.0) - DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_two_vertical_line_segments(self):
        points = [[Point(0, 0), Point(0, 1)], \
                  [Point(1, 0), Point(1, 1)]]
        expected = [[Point(0.5, 0.0), (0.5, 1)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=100, min_neighbors=0, min_num_trajectories_in_cluster=1, min_vertical_lines=1, min_prev_dist=0)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_two_minus_45_degree_lines_segs(self):
        points = [[Point(1, 0), Point(2, 1)], \
                  [Point(0, 1), Point(1, 2)]]
        expected = [[Point(0.5, 0.5), Point(1.5, 1.5)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=math.sqrt(2.0) + DECIMAL_MAX_DIFF_FOR_EQUALITY, \
                                  min_neighbors=1, min_num_trajectories_in_cluster=2, \
                                  min_vertical_lines=2, \
                                  min_prev_dist=math.sqrt(2.0) - DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)
        
    def test_partition_happens_with_single_long_line_seg(self):
        points = [[Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]]
        expected = [[Point(0, 0), Point(3, 3)]]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=math.sqrt(2.0) + DECIMAL_MAX_DIFF_FOR_EQUALITY, \
                                  min_neighbors=1, min_num_trajectories_in_cluster=1, \
                                  min_vertical_lines=1, \
                                  min_prev_dist=math.sqrt(2.0) - DECIMAL_MAX_DIFF_FOR_EQUALITY)
        self.verify_point_iterable_almost_equals_list(iterable=res, expected_list=expected)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()