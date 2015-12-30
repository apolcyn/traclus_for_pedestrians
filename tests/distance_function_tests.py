'''
Created on Dec 29, 2015

@author: Alex
'''
import unittest
import distance_functions
import math
from planar import LineSegment
from planar import Point
from distance_functions import parrallel_distance, perpendicular_distance,\
    angular_distance
        
class DistanceFunctionTest(unittest.TestCase):
    
    DECIMAL_PRECISION = 11

    def build_test_object(self, perp_dist, parr_dist, angle_dist):
        return {'perp_dist': perp_dist, 'parr_dist': parr_dist, \
                 'angle_dist': angle_dist, 'lines': []}
    
    def add_line(self, test_object, start_a, end_a, start_b, end_b):
        line = LineSegment.from_points([Point(start_a, end_a), Point(start_b, end_b)])
        test_object['lines'].append(line)
 
    def setUp(self):
        self.test_lines = []
        
        temp = self.build_test_object(2.0, 0.0, 0.0)
        self.add_line(temp, 0, 0, 2, 0)
        self.add_line(temp, 0, 2, 2, 2)
        self.test_lines.append(temp)
        
        temp = self.build_test_object(2.0, 2.0, 0.0)
        self.add_line(temp, 0, 0, 2, 0)
        self.add_line(temp, 4, 2, 10, 2)
        self.test_lines.append(temp)
        
        temp = self.build_test_object(10.0/3, 2.0, 2.0)
        self.add_line(temp, 0, 0, 2, 0)
        self.add_line(temp, 4, 2, 4, 6)
        self.test_lines.append(temp)
        
        temp = self.build_test_object(math.sqrt(2), 3 * math.sqrt(2), math.sqrt(2))
        self.add_line(temp, 0.0, 0.0, 2.0, 0.0)
        self.add_line(temp, 4.0, 4.0, 6.0, 6.0)
        self.test_lines.append(temp)
        
        temp = self.build_test_object(0.0, 0.0, 0.0)
        self.add_line(temp, 0.0, 2.0, 4.3, 8.3)
        self.add_line(temp, 0.0, 2.0, 4.3, 8.3)
        
        temp = self.build_test_object(0.0, 0.0, 0.0)
        self.add_line(temp, 0.0, 2.0, 2.0, 2.0)
        self.add_line(temp, 0.0, 2.0, 2.0, 2.0)
        
    def test_perpendicular_distance(self):
        self.distance_test(perpendicular_distance, 'perp_dist')
        
    def test_parrallel_distance(self):
        self.distance_test(parrallel_distance, 'parr_dist')
        
    def test_angle_distance(self):
        self.distance_test(angular_distance, 'angle_dist')
        
    def distance_test(self, distance_func, distance_type):
        for line_pair in self.test_lines:
            dist = distance_func(line_pair['lines'][0], line_pair['lines'][1])
            other = distance_func(line_pair['lines'][1], line_pair['lines'][0])
            self.assertAlmostEqual(dist, other, \
                            DistanceFunctionTest.DECIMAL_PRECISION, \
                            "distance measure not symmetric. " + \
                             "found distance of " + str(dist) + " and " + str(other))
            self.assertAlmostEqual(dist, line_pair[distance_type], 
                            DistanceFunctionTest.DECIMAL_PRECISION, \
                             "incorrect distance measure for " + str(line_pair) + \
                             " found distance of " + str(dist))  

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()