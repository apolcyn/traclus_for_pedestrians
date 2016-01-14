'''
Created on Jan 13, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from line_segment_averaging import get_representative_line_from_trajectory_line_segments
from planar import Point

class FindRepresentativeLineSegmentsTest(UnitBaseTests):

    def testName(self):
        pass
    
    def test_simple_lines(self):
        line_segments = [self.create_trajectory_line_seg((0, 0), (1, 0), 0), \
                         self.create_trajectory_line_seg(start=(0, 1), end=(1, 1), traj_id=1)]
        res = get_representative_line_from_trajectory_line_segments(line_segments, 1, 1)
        expected = [Point(0, 0.5), Point(1, 0.5)]
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()