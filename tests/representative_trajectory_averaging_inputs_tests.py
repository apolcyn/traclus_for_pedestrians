'''
Created on Jan 1, 2016

@author: Alex
'''
import unittest
from representative_trajectory_average_inputs import get_representative_trajectory_average_inputs
from traclus_dbscan import TrajectoryLineSegment
from planar import Point
from planar.line import LineSegment
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
 
    def build_test_ob(self, test_trajectory_line_segments, expected_line_sets, min_lines):
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
                'expected_line_sets': expected_line_sets, 'min_lines': min_lines}

    def setUp(self):
        self.test_cases = []
        
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
        test_ob = self.build_test_ob(lines,line_sets, 1)
        self.test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 2.0, [0, 1]), \
                 self.create_line(1.0, 3.0, [0, 1, 2]), \
                 self.create_line(2.0, 4.0, [1, 2, 3]), \
                 self.create_line(3.0, 5.0, [2, 3])]
        line_sets = [self.create_line_set(1.0), \
                     self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(4.0)]
        test_ob = self.build_test_ob(lines,line_sets, 2)
        self.test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 2.0, [0]), \
                 self.create_line(1.0, 3.0, [0, 1]), \
                 self.create_line(2.0, 4.0, [0, 1]), \
                 self.create_line(3.0, 5.0, [1])]
        line_sets = [self.create_line_set(2.0), \
                     self.create_line_set(3.0)]
        test_ob = self.build_test_ob(lines,line_sets, 3)
        self.test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 2.0, []), \
                 self.create_line(1.0, 3.0, []), \
                 self.create_line(2.0, 4.0, []), \
                 self.create_line(3.0, 5.0, [])]
        line_sets = []
        test_ob = self.build_test_ob(lines,line_sets, 4)
        self.test_cases.append(test_ob)  
        
    def get_point_lines_test_cases(self):
        test_cases = []
        lines = [self.create_line(0.0, 3.0, [0, 1, 2, 3]), \
                 self.create_line(1.0, 1.0, [1]), \
                 self.create_line(1.0, 1.0, [1]), \
                 self.create_line(1.0, 2.0, [1, 2]), \
                 self.create_line(2.0, 5.0, [3, 4, 5]), \
                 self.create_line(5.0, 5.0, [5])]
        line_sets = [self.create_line_set(0.0), \
                     self.create_line_set(1.0), \
                     self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(5.0), \
                     ]
        test_ob = self.build_test_ob(lines,line_sets, 1)
        test_cases.append(test_ob)
        
    def get_min_vert_lines_test_cases(self):
        test_cases = []
        lines = [self.create_line(0.0, 3.0, [0, 1, 2, 3]), \
                 self.create_line(1.0, 3.0, [1, 2]), \
                 self.create_line(2.0, 3.0, [2, 3]), \
                 self.create_line(3.0, 5.0, [3, 4])]
        line_sets = [self.create_line_set(0.0), \
                     self.create_line_set(1.0), \
                     self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(5.0), \
                     ]
        test_ob = self.build_test_ob(lines,line_sets, 1)
        test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 3.0, [0, 1]), \
                 self.create_line(1.0, 3.0, [0, 1]), \
                 self.create_line(2.0, 3.0, [0, 1]), \
                 self.create_line(3.0, 5.0, [1])]
        line_sets = [self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                    ]
        test_ob = self.build_test_ob(lines,line_sets, 3)
        test_cases.append(test_ob)
        return test_cases
    
    def get_min_prev_dist_test_obs(self):
        test_cases = []
        lines = [self.create_line(0.0, 1.0, [0, 1]), \
                 self.create_line(1.0, 3.0, [1, 2]), \
                 self.create_line(1.5, 3.0, [2]), \
                 self.create_line(3.0, 3.7, [2, 3])]
        line_sets = [self.create_line_set(0.0), \
                     self.create_line_set(1.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(3.7), \
                     ]
        test_ob = self.build_test_ob(lines,line_sets, 1, min_prev_dist=0.7)
        test_cases.append(test_ob)
        
        return test_cases
        
    def test_inputs_point_lines(self):
        for test_ob in self.get_point_lines_test_cases():
            self.verify(test_ob)  

    def test_inputs_min_verts_param(self):
        for test_ob in self.get_min_vert_lines_test_cases():
            self.verify(test_ob)  
            
    def test_inputs_min_prev_dist_param(self): 
        for test_ob in self.get_min_prev_dist_obs(self):
            self.verify(test_ob)
            
            
    def test_get_representative_trajectory_average_inputs(self):
        for test_ob in self.test_cases:
            self.verify(test_ob)
                
    def verify(self, test_ob):
        trajectory_average_inputs = \
        get_representative_trajectory_average_inputs(test_ob['trajectory_line_segments'], test_ob['min_lines'])
        expected_line_sets = test_ob['expected_line_sets']
        i = 0
        self.assertEqual(len(expected_line_sets), len(trajectory_average_inputs))
            
        for input in trajectory_average_inputs:
            self.assertEquals(len(input['lines']), len(expected_line_sets[i]['lines']))
            for line in input['lines']:
                self.assertTrue(line in expected_line_sets[i]['lines'])
            self.assertEquals(input['horizontal_position'], expected_line_sets[i]['horizontal_position'])
            
def get_all_test_cases():
            self.test_cases = []
        
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
        test_ob = self.build_test_ob(lines,line_sets, 1)
        self.test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 2.0, [0, 1]), \
                 self.create_line(1.0, 3.0, [0, 1, 2]), \
                 self.create_line(2.0, 4.0, [1, 2, 3]), \
                 self.create_line(3.0, 5.0, [2, 3])]
        line_sets = [self.create_line_set(1.0), \
                     self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(4.0)]
        test_ob = self.build_test_ob(lines,line_sets, 2)
        self.test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 2.0, [0]), \
                 self.create_line(1.0, 3.0, [0, 1]), \
                 self.create_line(2.0, 4.0, [0, 1]), \
                 self.create_line(3.0, 5.0, [1])]
        line_sets = [self.create_line_set(2.0), \
                     self.create_line_set(3.0)]
        test_ob = self.build_test_ob(lines,line_sets, 3)
        self.test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 2.0, []), \
                 self.create_line(1.0, 3.0, []), \
                 self.create_line(2.0, 4.0, []), \
                 self.create_line(3.0, 5.0, [])]
        line_sets = []
        test_ob = self.build_test_ob(lines,line_sets, 4)
        self.test_cases.append(test_ob)  
        
                test_cases = []
        lines = [self.create_line(0.0, 3.0, [0, 1, 2, 3]), \
                 self.create_line(1.0, 1.0, [1]), \
                 self.create_line(1.0, 1.0, [1]), \
                 self.create_line(1.0, 2.0, [1, 2]), \
                 self.create_line(2.0, 5.0, [3, 4, 5]), \
                 self.create_line(5.0, 5.0, [5])]
        line_sets = [self.create_line_set(0.0), \
                     self.create_line_set(1.0), \
                     self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(5.0), \
                     ]
        test_ob = self.build_test_ob(lines,line_sets, 1)
        test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 3.0, [0, 1, 2, 3]), \
                 self.create_line(1.0, 3.0, [1, 2]), \
                 self.create_line(2.0, 3.0, [2, 3]), \
                 self.create_line(3.0, 5.0, [3, 4])]
        line_sets = [self.create_line_set(0.0), \
                     self.create_line_set(1.0), \
                     self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(5.0), \
                     ]
        test_ob = self.build_test_ob(lines,line_sets, 1)
        test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 3.0, [0, 1]), \
                 self.create_line(1.0, 3.0, [0, 1]), \
                 self.create_line(2.0, 3.0, [0, 1]), \
                 self.create_line(3.0, 5.0, [1])]
        line_sets = [self.create_line_set(2.0), \
                     self.create_line_set(3.0), \
                    ]
        test_ob = self.build_test_ob(lines,line_sets, 3)
        test_cases.append(test_ob)
        
        lines = [self.create_line(0.0, 1.0, [0, 1]), \
                 self.create_line(1.0, 3.0, [1, 2]), \
                 self.create_line(1.5, 3.0, [2]), \
                 self.create_line(3.0, 3.7, [2, 3])]
        line_sets = [self.create_line_set(0.0), \
                     self.create_line_set(1.0), \
                     self.create_line_set(3.0), \
                     self.create_line_set(3.7), \
                     ]
        test_ob = self.build_test_ob(lines,line_sets, 1, min_prev_dist=0.7)
        test_cases.append(test_ob)
        
            
def test_generator(test_ob):
    def test(self, test_ob):
        self.verify(test_ob)
    return test   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = get_all_test_cases()
    counter = 0
    for test_ob in test_cases:
        test_name = "test_%s" % counter
        counter += 1
        test = test_generator(test_ob)
        setattr(RepresentativeTrajectoryAverageInputsTest, test_name, test)
    unittest.main()