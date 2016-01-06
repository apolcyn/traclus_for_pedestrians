'''
Created on Jan 6, 2016

@author: Alex
'''
import unittest
from planar import LineSegment
from planar import Point
from traclus_dbscan import TrajectoryLineSegment

class UnitBaseTests(unittest.TestCase):
    def create_line_seg(self, traj_id):
        return TrajectoryLineSegment(LineSegment.from_points([Point(0, 0), Point(1, 1)]), traj_id)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()