'''
Created on Jan 13, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from planar import Point
from coordination import the_whole_enchilada

class JumboShrimpTest(UnitBaseTests):

    def test_two_line_segs(self):
        points = [[Point(0, 1), Point(1, 1)], \
                  [Point(0, 0), Point(1, 0)]]
        expected = [Point(0, 0.5), (1, 0.5)]
        res = the_whole_enchilada(point_iterable_list=points, \
                                  epsilon=100, min_neighbors=1, min_num_trajectories_in_cluster=1, min_vertical_lines=2, min_prev_dist=1.0)
        self.verify_iterable_works_more_than_once(iterable=res, list_ob=expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()