'''
Created on Dec 31, 2015

@author: Alex
'''
import unittest
from traclus_dbscan import TrajectoryCluster, TrajectoryLineSegment
from planar.line import LineSegment
from planar import Point

class TrajectoryClusterTests(unittest.TestCase):

    def build_test_object(self, line_segments, expected_count, num_trajectories, expected_error = False):
        return {'line_segments': line_segments, 'num_trajectories': num_trajectories, \
                'expected_count': expected_count, 'expected_error': expected_error}

    def new_line_seg(self, traj_id):
        return TrajectoryLineSegment(LineSegment.from_points([Point(0, 0), Point(1, 1)]), traj_id)

    def setUp(self):
        self.test_cases = []
        
        line_segs = [self.new_line_seg(0), self.new_line_seg(1), self.new_line_seg(2), self.new_line_seg(3)]
        self.test_cases.append(self.build_test_object(line_segs, 4, 4))
        
        line_segs = [self.new_line_seg(0), self.new_line_seg(0), self.new_line_seg(2), self.new_line_seg(3)]
        self.test_cases.append(self.build_test_object(line_segs, 3, 4))
        
        line_segs = [self.new_line_seg(0), self.new_line_seg(0), self.new_line_seg(0), self.new_line_seg(0)]
        self.test_cases.append(self.build_test_object(line_segs, 1, 1000))
        
        line_segs = [self.new_line_seg(10000), self.new_line_seg(90), self.new_line_seg(23), self.new_line_seg(23)]
        self.test_cases.append(self.build_test_object(line_segs, 3, 10001))
        
        line_segs = [self.new_line_seg(10000), self.new_line_seg(90), self.new_line_seg(23), self.new_line_seg(23)]
        self.test_cases.append(self.build_test_object(line_segs, 3, 10000, True))
        
        line_segs = [self.new_line_seg(10000), self.new_line_seg(90), self.new_line_seg(23), self.new_line_seg(23)]
        self.test_cases.append(self.build_test_object(line_segs, 3, 99, True))
        
        self.test_cases.append(self.build_test_object([], 0, 100000))

    def create_cluster(self, segments, num_trajectories):
        cluster = TrajectoryCluster(num_trajectories)
        
        for single_segment in segments:
            cluster.add_member(single_segment)
            
        return cluster

    def test_trajectory_counting(self):
        for test_ob in self.test_cases:
            if test_ob['expected_error']:
                #self.create_cluster(test_ob['line_segments'], test_ob['num_trajectories'])
                self.assertRaises((Exception, IndexError), self.create_cluster, test_ob['line_segments'], test_ob['num_trajectories'])
            else:
                cluster = self.create_cluster(test_ob['line_segments'], test_ob['num_trajectories'])
                self.assertEqual(test_ob['expected_count'], cluster.num_trajectories_contained(), \
                                 " found " + str(cluster.num_trajectories_contained()) + " for " + str(test_ob))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()