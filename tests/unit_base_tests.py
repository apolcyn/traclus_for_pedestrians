'''
Created on Jan 6, 2016

@author: Alex
'''
import unittest
from planar import LineSegment
from planar import Point
from traclus_dbscan import TrajectoryLineSegment

class UnitBaseTests(unittest.TestCase):
    def create_line_seg(self, traj_id, original_position):
        return TrajectoryLineSegment(LineSegment.from_points([Point(0, 0), Point(1, 1)]), traj_id, original_position)

    def verify_iterable_equals_list(self, iterable_ob, list_ob):
        count = 0
        for item in iterable_ob:
            count += 1
        
        self.assertEqual(count, len(list_ob))
        if count > 0:
            i = 0
            for item in iterable_ob:
                self.assertEquals(item, list_ob[i])
                i += 1
            self.assertEquals(i, count, "wasn't able to iterate over items a second time")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()