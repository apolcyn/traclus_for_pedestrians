'''
Created on Dec 29, 2015

@author: Alex
'''
import unittest
from planar import Point
from trajectory import Trajectory
import math

class TrajectoryPartitionTest(unittest.TestCase):

    def build_test_object(self, points, optimal_partition, start, end):
        traj = Trajectory(0)
        traj.points = map(lambda point: Point(point[0], point[1]), points)
        return {'trajectory': traj, 'start': start, 'end': end, \
                'optimal_partition': optimal_partition}

    def setUp(self):
        self.test_trajectories = []
        
        points = [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]
        test_object = self.build_test_object(points, [0, 1, 2, 3, 4, 5, 6], 0, 6)
        self.test_trajectories.append(test_object)
        
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        test_object = self.build_test_object(points, [0, 3], 0, 3)
        self.test_trajectories.append(test_object)
        
        points = [(0, 0), (math.sqrt(3.0), 1), (2, 2), (3, 3), (4, 4)]
        test_object = self.build_test_object(points, [0, 1, 2, 4], 0, 4)
        self.test_trajectories.append(test_object)
        
        test_object = self.build_test_object([(0, 0), (1, 1)], [0, 1], 0, 1)
        self.test_trajectories.append(test_object)
    
    def test_optimal_paritioning(self):
        for test_case in self.test_trajectories:
            partition = test_case['trajectory'].get_optimal_parition(test_case['start'], \
                                                                     test_case['end'])
            self.assertEqual(partition, test_case['optimal_partition'], \
                             "failed on " + str(test_case))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()