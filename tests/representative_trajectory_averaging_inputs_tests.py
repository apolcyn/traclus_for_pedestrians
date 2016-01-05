'''
Created on Jan 1, 2016

@author: Alex
'''
import unittest
from representative_trajectory_average_inputs import get_representative_trajectory_average_inputs
from traclus_dbscan import TrajectoryLineSegment
from planar import Point
from planar.line import LineSegment
from unittest import TestSuite
import random

class RepresentativeTrajectoryAverageInputsTest(unittest.TestCase):
    def create_line(self, horizontal_start, horizontal_end, line_set_ids, trajectory_id=None):
        return {'trajectory_line_segment': \
                TrajectoryLineSegment(LineSegment.from_points([Point(horizontal_start, random.randint(0, 10000)), \
                                                               Point(horizontal_end, random.randint(0, 10000))]), \
                                      random.randint(0, 10000)), \
                'line_set_ids': line_set_ids, 'trajectory_id': trajectory_id}
        
    def create_line_set(self, horizontal_position):
        return {'horizontal_position': horizontal_position, 'lines': set()}
  
    def build_test_ob(self, test_trajectory_line_segments, expected_line_sets, min_lines, min_prev_dist=0.0):
        counter = 0
        for line_seg in test_trajectory_line_segments:
            if line_seg['trajectory_id'] == None:
                line_seg['trajectory_id'] = counter
                counter += 1000
                
        all_line_segments = map(lambda test_segment: test_segment['trajectory_line_segment'], \
                                    test_trajectory_line_segments)
        for test_line_segment in test_trajectory_line_segments:
            for line_set_id in test_line_segment['line_set_ids']:
                expected_line_sets[line_set_id]['lines'].add(test_line_segment['trajectory_line_segment'])
                
        return {'trajectory_line_segments': all_line_segments, \
                'expected_line_sets': expected_line_sets, 'min_lines': min_lines, 'min_prev_dist': min_prev_dist}

        
    def verify(self, test_ob):
        self.assertEquals(1, 1)
        trajectory_average_inputs = \
        get_representative_trajectory_average_inputs(test_ob['trajectory_line_segments'], test_ob['min_lines'], \
                                                     test_ob['min_prev_dist'])
        expected_line_sets = test_ob['expected_line_sets']
        i = 0
        self.assertEquals(len(expected_line_sets), len(trajectory_average_inputs))
            
        for averaging_input in trajectory_average_inputs:
            self.assertEquals(len(averaging_input['lines']), len(expected_line_sets[i]['lines']))
            for line in averaging_input['lines']:
                self.assertTrue(line in expected_line_sets[i]['lines'])
            self.assertEquals(averaging_input['horizontal_position'], expected_line_sets[i]['horizontal_position'])
        self.assertEquals(1, 2)
        
    def test_overlapping(self):  
        lines = [self.create_line(0.0, 2.0, [0, 1, 2]), \
            self.create_line(1.0, 3.0, [1, 2, 3]), \
            self.create_line(2.0, 4.0, [2, 3, 4]), \
            self.create_line(3.0, 5.0, [3, 4, 5])]
        line_sets = [self.create_line_set(0.0), \
            self.create_line_set(1.0), \
            self.create_line_set(2.0), \
            self.create_line_set(3.0), \
            self.create_line_set(4.0), \
            self.create_line_set(5.0)]
        self.verify(self.build_test_ob(lines,line_sets, 1))
        
    def test_two_lines_required(self):
        lines = [self.create_line(0.0, 2.0, [0, 1]), \
            self.create_line(1.0, 3.0, [0, 1, 2]), \
            self.create_line(2.0, 4.0, [1, 2, 3]), \
            self.create_line(3.0, 5.0, [2, 3])]
        line_sets = [self.create_line_set(1.0), \
            self.create_line_set(2.0), \
            self.create_line_set(3.0), \
            self.create_line_set(4.0)]
        self.verify(self.build_test_ob(lines,line_sets, 2))
        
    def test_three_lines_required(self):
        lines = [self.create_line(0.0, 2.0, [0]), \
            self.create_line(1.0, 3.0, [0, 1]), \
            self.create_line(2.0, 4.0, [0, 1]), \
            self.create_line(3.0, 5.0, [1])]
        line_sets = [self.create_line_set(2.0), \
            self.create_line_set(3.0)]
        self.verify(self.build_test_ob(lines,line_sets, 3))
        
    def test_no_sets_output(self):
        lines = [self.create_line(0.0, 2.0, []), \
            self.create_line(1.0, 3.0, []), \
            self.create_line(2.0, 4.0, []), \
            self.create_line(3.0, 5.0, [])]
        line_sets = []
        self.verify(self.build_test_ob(lines,line_sets, 4))
        
    def test_single_point_lines(self):
        lines = [self.create_line(0.0, 3.0, [0, 1, 2, 3]), \
            self.create_line(1.0, 1.0, [1]), \
            self.create_line(1.0, 1.0, [1]), \
            self.create_line(1.0, 2.0, [1, 2]), \
            self.create_line(2.0, 5.0, [2, 3, 4]), \
            self.create_line(5.0, 5.0, [4])
        ]
        line_sets = [self.create_line_set(0.0), \
            self.create_line_set(1.0), \
            self.create_line_set(2.0), \
            self.create_line_set(3.0), \
            self.create_line_set(5.0), \
        ]
        self.verify(self.build_test_ob(lines,line_sets, 1))
        
    def test_only_point_line_satisfies_line_requirement(self):
        lines = [self.create_line(0.0, 3.0, [0, 1, 2]), \
            self.create_line(1.0, 3.0, [0, 1, 2]), \
            self.create_line(2.0, 3.0, [1, 2]), \
            self.create_line(3.0, 5.0, [3, 4])]
        line_sets = [self.create_line_set(3.0)]
        self.verify(self.build_test_ob(lines,line_sets, 4))
        
    def test_non_zero_min_prev_distance_param(self):
        lines = [self.create_line(0.0, 1.0, [0, 1]), \
            self.create_line(1.0, 3.0, [1, 2]), \
            self.create_line(1.5, 3.0, [2]), \
            self.create_line(3.0, 3.7, [2, 3])
        ]
        line_sets = [self.create_line_set(0.0), \
            self.create_line_set(1.0), \
            self.create_line_set(3.0), \
            self.create_line_set(3.7), \
        ]
        self.verify(self.build_test_ob(lines,line_sets, 1, min_prev_dist=0.7))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()