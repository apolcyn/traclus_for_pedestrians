'''
Created on Dec 31, 2015

@author: Alex
'''
from dbscan import Cluster, ClusterCandidate
from planar.line import LineSegment
from _ctypes import ArgumentError

class TrajectoryLineSegment(ClusterCandidate):
    def __init__(self, line_segment, trajectory_id, position_in_trajectory):
        ClusterCandidate.__init__(self)
        if line_segment == None or trajectory_id < 0:
            raise ArgumentError()
        
        self.line_segment = line_segment
        self.trajectory_id = trajectory_id
        self.position_in_trajectory = position_in_trajectory

class TrajectoryCluster(Cluster):
    def __init__(self, num_trajectories_exist):
        Cluster.__init__(self)
        self.trajectories = [False] * num_trajectories_exist
        self.trajectory_count = 0
        
    def add_member(self, item):
        Cluster.add_member(self, item)
        if not self.trajectories[item.trajectory_id]:
            self.trajectory_count += 1
            self.trajectories[item.trajectory_id] = True
        
    def num_trajectories_contained(self):
        return self.trajectory_count
    
    