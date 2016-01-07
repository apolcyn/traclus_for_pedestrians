'''
Created on Jan 6, 2016

@author: Alex
'''
import unittest
from representative_line_finding import get_average_vector, rotate_line_segment
from unit_base_tests import UnitBaseTests
from planar import Vec2
import math
from representative_trajectory_average_inputs import DECIMAL_MAX_DIFF_FOR_EQUALITY

class RepresentativeLineFindingTests(UnitBaseTests):

    def test_get_average_vector(self):
        lines = [self.create_simple_line_seg((0, 0), (1, 1)), \
                 self.create_simple_line_seg((1, 1), (3, -7)), \
                 self.create_simple_line_seg((1, 0), (-4, 4)), \
                 self.create_simple_line_seg((4, 2), (1, -3))]
        self.assertEquals(get_average_vector(lines), Vec2(-5, -8))
        self.assertEquals(get_average_vector([self.create_simple_line_seg((0, 1), (2, 9))]), Vec2(2, 8))

        
    def test_get_average_vector_empty_input(self):
        self.assertRaises(Exception, get_average_vector, [])
        self.assertRaises(Exception, get_average_vector, None)
        
    def test_rotate_line_segment_right_hemisphere(self):
        before = self.create_simple_line_seg((0, 1), (1, 2))
        after = self.create_simple_line_seg((1 / math.sqrt(2.0), 1 / math.sqrt(2.0)), \
                                            (math.sqrt(2.0) + 1 / math.sqrt(2.0), 1 / math.sqrt(2.0)))
        self.assertTrue(rotate_line_segment(before, -45).almost_equals(after))
        self.assertTrue(rotate_line_segment(after, 45).almost_equals(before))
        
    def test_basic_central_rotate_45(self):
        before = self.create_simple_line_seg((0, 0), (1, 1))
        after = self.create_simple_line_seg((0, 0), (math.sqrt(2), 0))
        self.assertTrue(rotate_line_segment(before, -45).almost_equals(after))
        self.assertTrue(rotate_line_segment(after, 45).almost_equals(before))
        
    def test_basic_central_rotate_90(self):
        before = self.create_simple_line_seg((0, 0), (0, 1))
        after = self.create_simple_line_seg((0, 0), (1, 0))
        self.assertEquals(rotate_line_segment(before, -90), after)
        self.assertEquals(rotate_line_segment(after, 90), before)
        
    def test_basic_centrial_rotate_90_left_hemi(self):
        before = self.create_simple_line_seg((0, 0), (-1, 0))
        after = self.create_simple_line_seg((0, 0), (0, -1))
        self.assertEquals(rotate_line_segment(before, 90), after)
        self.assertEquals(rotate_line_segment(after, -90), before)
        
    def test_rotate_by_zero(self):
        test_ob = self.create_simple_line_seg((0, 1), (1, 2))
        self.assertEquals(rotate_line_segment(test_ob, 0.0), test_ob)
        
    def test_bad_angle(self):
        test_ob = self.create_simple_line_seg((0, 1), (1, 2))
        self.assertRaises(Exception, rotate_line_segment, test_ob, -90.1)
        self.assertRaises(Exception, rotate_line_segment, test_ob, 90.1)
        self.assertRaises(Exception, rotate_line_segment, test_ob, 181)
        self.assertRaises(Exception, rotate_line_segment, test_ob, -181)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()