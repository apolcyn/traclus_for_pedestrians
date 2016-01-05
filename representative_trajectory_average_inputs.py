'''
Created on Jan 1, 2016

@author: Alex
'''
from linked_list import LinkedList
from linked_list import LinkedListNode
from operator import attrgetter

class TrajectoryLineSegmentEndpoint:
    def __init__(self, horizontal_position, line_segment, line_segment_id, list_node):
        self.horizontal_position = horizontal_position
        self.line_segment = line_segment
        self.line_segment_id = line_segment_id
        self.list_node = list_node

def get_representative_trajectory_average_inputs(trajectory_line_segments, min_lines, min_prev_dist):
    cur_active = [False] * len(trajectory_line_segments)
    line_segment_endpoints = []
    cur_id = 0
    active_list = LinkedList()
        
    for traj_segment in trajectory_line_segments:
        list_node = LinkedListNode(traj_segment)
        line_segment_endpoints.append(TrajectoryLineSegmentEndpoint(traj_segment.line_segment.start.x, \
                                                                    traj_segment, cur_id, list_node))
        line_segment_endpoints.append(TrajectoryLineSegmentEndpoint(traj_segment.line_segment.end.x, \
                                                                    traj_segment, cur_id, list_node))
        cur_id += 1
        
    sorted(line_segment_endpoints, key=attrgetter('horizontal_position'))
    insert_list = [] 
    delete_list = []
    out = []
        
    i = 0
    while i < len(line_segment_endpoints):
        insert_list[:] = []
        delete_list[:] = []
        prev_pos = line_segment_endpoints[i].horizontal_position
        
        while i < len(line_segment_endpoints) and line_segment_endpoints[i].horizontal_position == prev_pos:
            if not cur_active[line_segment_endpoints[i].line_segment_id]:
                insert_list.append(line_segment_endpoints[i])
                cur_active[line_segment_endpoints[i].line_segment_id] = True
            elif cur_active[line_segment_endpoints[i].line_segment_id]:
                delete_list.append(line_segment_endpoints[i])
                cur_active[line_segment_endpoints[i].line_segment_id] = False
            i += 1
            
        for line_seg in insert_list:
            active_list.add_last_node(line_seg.list_node)
        temp = []
        for line_seg in active_list:
            temp.append(line_seg)
        out.append({'lines': temp, 'horizontal_position': prev_pos})
        for line_seg in delete_list:
            active_list.remove_node(line_seg.list_node)
    
    return out
            