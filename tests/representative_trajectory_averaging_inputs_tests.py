'''
Created on Jan 1, 2016

@author: Alex
'''
import unittest
from representative_trajectory_average_inputs import get_representative_trajectory_average_inputs,\
    get_sorted_line_seg_endpoints, DECIMAL_MAX_DIFF_FOR_EQUALITY
from traclus_dbscan import TrajectoryLineSegment
from planar import Point
from planar.line import LineSegment
from unittest import TestSuite
import random

class RepresentativeTrajectoryAverageInputsTest(unittest.TestCase):
    def create_line(self, horizontal_start, horizontal_end, line_set_ids, trajectory_id):
        return {'trajectory_line_segment': \
                TrajectoryLineSegment(LineSegment.from_points([Point(horizontal_start, random.randint(0, 10000)), \
                                                               Point(horizontal_end, random.randint(0, 10000))]), \
                                      trajectory_id), \
                'line_set_ids': line_set_ids}
        
    def create_line_set(self, horizontal_position):
        return {'horizontal_position': horizontal_position, 'lines': set()}
  
    def build_test_ob(self, test_trajectory_line_segments, expected_line_sets, min_lines, min_prev_dist=0.0):
        all_line_segments = map(lambda test_segment: test_segment['trajectory_line_segment'], \
                                    test_trajectory_line_segments)
        for test_line_segment in test_trajectory_line_segments:
            for line_set_id in test_line_segment['line_set_ids']:
                expected_line_sets[line_set_id]['lines'].add(test_line_segment['trajectory_line_segment'])
                
        return {'trajectory_line_segments': all_line_segments, \
                'expected_line_sets': expected_line_sets, 'min_lines': min_lines, 'min_prev_dist': min_prev_dist}
        
    def create_line_seg_endpoint_test_ob(self, horizontal_position, line):
        return {'horizontal_position': horizontal_position, 'line': line}
        
    def verify(self, test_ob):
        self.assertEquals(1, 1)
        trajectory_average_inputs = \
        get_representative_trajectory_average_inputs(test_ob['trajectory_line_segments'], test_ob['min_lines'], \
                                                     test_ob['min_prev_dist'])
        expected_line_sets = test_ob['expected_line_sets']
        self.assertEquals(len(expected_line_sets), len(trajectory_average_inputs))
            
        for i in xrange(0, len(trajectory_average_inputs)):
            averaging_input = trajectory_average_inputs[i]
            self.assertEquals(len(averaging_input['lines']), len(expected_line_sets[i]['lines']), \
                              "expected: " + str(len(expected_line_sets[i]['lines'])) + \
                              " but found: " + str(len(averaging_input['lines'])) + \
                              ". comparison failed for line set number " + str(i))
            for line in averaging_input['lines']:
                self.assertTrue(line in expected_line_sets[i]['lines'])
            self.assertAlmostEquals(averaging_input['horizontal_position'], \
                                    expected_line_sets[i]['horizontal_position'], 11, DECIMAL_MAX_DIFF_FOR_EQUALITY)
                    
    def test_line_seg_endpoint_sorting(self):
        lines = [self.create_line(0.0, 2.0, [0, 1, 2], 0), \
            self.create_line(1.0, 3.0, [1, 2, 3], 1), \
            self.create_line(2.0, 4.0, [2, 3, 4], 2), \
            self.create_line(3.0, 5.0, [3, 4, 5], 3)]
        
        expected = [0.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 5.0]
        
        actual = get_sorted_line_seg_endpoints(map(lambda line: line['trajectory_line_segment'], lines))
        self.assertEquals(len(expected), len(actual))
        
        for i in range(0, len(actual)):
            self.assertAlmostEquals(expected[i], actual[i].horizontal_position, 11, DECIMAL_MAX_DIFF_FOR_EQUALITY)
            
        
    def test_overlapping_one_line_required(self):  
        lines = [self.create_line(0.0, 2.0, [0, 1, 2], 0), \
            self.create_line(1.0, 3.0, [1, 2, 3], 1), \
            self.create_line(2.0, 4.0, [2, 3, 4], 2), \
            self.create_line(3.0, 5.0, [3, 4, 5], 3)]
        line_sets = [self.create_line_set(0.0), \
            self.create_line_set(1.0), \
            self.create_line_set(2.0), \
            self.create_line_set(3.0), \
            self.create_line_set(4.0), \
            self.create_line_set(5.0)]
        self.verify(self.build_test_ob(lines,line_sets, 1))
        
    def test_two_lines_required(self):
        lines = [self.create_line(0.0, 2.0, [0, 1], 0), \
            self.create_line(1.0, 3.0, [0, 1, 2], 1), \
            self.create_line(2.0, 4.0, [1, 2, 3], 2), \
            self.create_line(3.0, 5.0, [2, 3], 3)]
        line_sets = [self.create_line_set(1.0), \
            self.create_line_set(2.0), \
            self.create_line_set(3.0), \
            self.create_line_set(4.0)]
        self.verify(self.build_test_ob(lines,line_sets, 2))
        
    def test_non_adjacent_same_trajectory_segments_overlap(self):
        lines = [self.create_line(0.0, 2.0, [0], 0), \
            self.create_line(2.0, 3.0, [1], 0), \
            self.create_line(3.0, 2.0, [2], 0), \
            self.create_line(2.0, 5.0, [3, 4], 0)] 
        line_sets = [self.create_line_set(0.0), \
            self.create_line_set(2.0), \
            self.create_line_set(3.0), \
            self.create_line_set(2.0), \
            self.create_line_set(5.0),]
        self.verify(self.build_test_ob(lines,line_sets, 2))
        
    def test_three_lines_required(self):
        lines = [self.create_line(0.0, 2.0, [0], 0), \
            self.create_line(1.0, 3.0, [0, 1], 1), \
            self.create_line(2.0, 4.0, [0, 1], 2), \
            self.create_line(3.0, 5.0, [1], 3)]
        line_sets = [self.create_line_set(2.0), \
            self.create_line_set(3.0)]
        self.verify(self.build_test_ob(lines,line_sets, 3))
        
    def test_no_sets_output(self):
        lines = [self.create_line(0.0, 2.0, [], 0), \
            self.create_line(1.0, 3.0, [], 1), \
            self.create_line(2.0, 4.0, [], 2), \
            self.create_line(3.0, 5.0, [], 3)]
        line_sets = []
        self.verify(self.build_test_ob(lines,line_sets, 4))
        
    def test_one_point(self):
        lines = [self.create_line(3.0, 3.0, [0], 0)]
        line_sets = [self.create_line_set(3.0)]
        self.verify(self.build_test_ob(lines,line_sets, 1))
        
    def test_single_point_lines(self):
        lines = [self.create_line(0.0, 3.0, [0, 1, 2, 3], 0), \
            self.create_line(1.0, 1.0, [1], 1), \
            self.create_line(1.0, 1.0, [1], 2), \
            self.create_line(1.0, 2.0, [1, 2], 3), \
            self.create_line(2.0, 5.0, [2, 3, 4], 4), \
            self.create_line(5.0, 5.0, [4], 5)
        ]
        line_sets = [self.create_line_set(0.0), \
            self.create_line_set(1.0), \
            self.create_line_set(2.0), \
            self.create_line_set(3.0), \
            self.create_line_set(5.0), \
        ]
        self.verify(self.build_test_ob(lines,line_sets, 1))
        
    def test_only_point_line_satisfies_line_requirement(self):
        lines = [self.create_line(0.0, 3.0, [0], 0), \
            self.create_line(1.0, 3.0, [0], 1), \
            self.create_line(2.0, 3.0, [0], 2), \
            self.create_line(3.0, 5.0, [0], 3)]
        line_sets = [self.create_line_set(3.0)]
        self.verify(self.build_test_ob(lines,line_sets, 4))
        
    def test_non_zero_min_prev_distance_param(self):
        lines = [self.create_line(0.0, 1.0, [0, 1], 0), \
            self.create_line(1.0, 3.0, [1, 2], 1), \
            self.create_line(1.5, 3.0, [2], 2), \
            self.create_line(3.0, 3.7, [2, 3], 3)
        ]
        line_sets = [self.create_line_set(0.0), \
            self.create_line_set(1.0), \
            self.create_line_set(3.0), \
            self.create_line_set(3.7), \
        ]
        self.verify(self.build_test_ob(lines,line_sets, 1, min_prev_dist=0.7))
        
    def test_non_zero_min_prev_dist_with_two_lines_required(self):
        lines = [self.create_line(0.0, 1.0, [0], 0), \
            self.create_line(1.0, 3.0, [0, 1], 1), \
            self.create_line(1.5, 3.0, [1], 2), \
            self.create_line(3.0, 3.7, [1, 2], 3), \
            self.create_line(3.7, 3.7, [2], 4)
        ]
        line_sets = [self.create_line_set(1.0), \
            self.create_line_set(3.0), \
            self.create_line_set(3.7), \
        ]
        self.verify(self.build_test_ob(lines,line_sets, 2, min_prev_dist=0.7))
        
    def test_non_zer_min_prev_dist_and_two_lines_required_and_same_traj(self):
        lines = [self.create_line(0.0, 1.0, [0], 0), \
            self.create_line(1.0, 1.5, [], 0), \
            self.create_line(1.5, 3.0, [], 0), \
            self.create_line(3.0, 3.7, [1], 0), \
            self.create_line(3.7, 3.7, [2], 0)
        ]
        line_sets = [self.create_line_set(1.0), \
            self.create_line_set(3.0), \
            self.create_line_set(3.7), \
        ]
        self.verify(self.build_test_ob(lines,line_sets, 2, min_prev_dist=0.7))
        
    def test_all_one_trajectory(self):
        lines = [self.create_line(0.0, 2.0, [0], 0), \
            self.create_line(2.0, 3.0, [1], 0), \
            self.create_line(3.0, 4.0, [2], 0), \
            self.create_line(4.0, 8.0, [3, 4], 0)]
        line_sets = [self.create_line_set(0.0), \
                     self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(4.0), \
                     self.create_line_set(8.0)]
        self.verify(self.build_test_ob(lines,line_sets, 1))
        
    def test_same_trajectories_dont_sum_up(self):
        lines = [self.create_line(0.0, 2.0, [], 0), \
            self.create_line(2.0, 3.0, [], 0), \
            self.create_line(3.0, 4.0, [], 0), \
            self.create_line(4.0, 8.0, [], 0)]
        line_sets = []
        self.verify(self.build_test_ob(lines,line_sets, 2))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()