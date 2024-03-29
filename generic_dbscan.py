'''
Created on Dec 30, 2015

@author: Alex
'''
import collections

class ClusterCandidate:
    def __init__(self):
        self.cluster = None
        self.__is_noise = False
        
    def is_classified(self):
        return self.__is_noise or self.cluster != None
    
    def is_noise(self):
        return self.__is_noise
    
    def set_as_noise(self):
        self.__is_noise = True
    
    def assign_to_cluster(self, cluster):
        self.cluster = cluster
        self.__is_noise = False
        
    def distance_to_candidate(self, other_candidate):
        raise NotImplementedError()
    
    def find_neighbors(self, candidates, epsilon):
        neighbors = []
        
        for item in candidates:
            if item != self and self.distance_to_candidate(item) <= epsilon:
                neighbors.append(item)
                
        return neighbors
    
class Cluster:
    def __init__(self):
        self.members = []
        self.member_set = set()
        
    def add_member(self, item):
        if item in self.member_set:
            raise Exception("item: " + str(item) + " already exists in this cluster")
        self.member_set.add(item)
        self.members.append(item)
        
    def __repr__(self):
        return str(self.members)
        
class ClusterFactory():
    def new_cluster(self):
        return Cluster()
        
def dbscan(cluster_candidates, epsilon, min_neighbors, cluster_factory):
    clusters = []
    item_queue = collections.deque()
    
    for item in cluster_candidates:
        if not item.is_classified():  
            neighbors = item.find_neighbors(cluster_candidates, epsilon)
            if len(neighbors) >= min_neighbors:
                cur_cluster = cluster_factory.new_cluster()
                cur_cluster.add_member(item)
                item.assign_to_cluster(cur_cluster)
                
                for other_item in neighbors:
                    other_item.assign_to_cluster(cur_cluster)
                    cur_cluster.add_member(other_item)
                    item_queue.append(other_item)
                    
                expand_cluster(item_queue, cur_cluster, epsilon, \
                               min_neighbors, cluster_candidates)
                clusters.append(cur_cluster)
            else:
                item.set_as_noise()
                
    return clusters
                
def expand_cluster(item_queue, cluster, epsilon, min_neighbors, cluster_candidates):
    while len(item_queue) > 0:
        item = item_queue.popleft()
        neighbors = item.find_neighbors(cluster_candidates, epsilon)
        if len(neighbors) >= min_neighbors:
            for other_item in neighbors:
                if not other_item.is_classified():
                    item_queue.append(other_item)
                if other_item.is_noise() or not other_item.is_classified():
                    other_item.assign_to_cluster(cluster)
                    cluster.add_member(other_item)    
                
                  
    
    
    
    