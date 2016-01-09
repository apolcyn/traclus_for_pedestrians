'''
Created on Jan 7, 2016

@author: Alex
'''
from planar.line import LineSegment
from planar import Point
from string import lower
from generator_initializer import GeneratorInitializer

def partition_trajectory(trajectory_point_list, partition_cost_func, no_partition_cost_func):
    low = 0
    high = 2
    partition_indices = []
    partition_indices.append(0)
    
    while high < len(trajectory_point_list):
        cost_par = partition_cost_func(trajectory_point_list, low, high)
        cost_no_par = no_partition_cost_func(trajectory_point_list, low, high)
        
        if cost_par > cost_no_par:
            partition_indices.append(high - 1)
            low = high - 1
        
        high += 1
    
    if partition_indices[-1] != len(trajectory_point_list) - 1:
        partition_indices.append(len(trajectory_point_list) - 1)
            
    return partition_indices

def partition_cost_computer(trajectory_point_list, low_index, high_index, line_segment_iterable_getter, \
                            partition_line_getter, model_cost_computer, distance_func_computer):
    if low_index >= high_index:
        raise IndexError("illegal indices to partition func")
    
    partition_line = partition_line_getter(trajectory_point_list, low_index, high_index)
    model_cost = model_cost_computer(partition_line)
    
    encoding_cost = None
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, None):
        encoding_cost = distance_func_computer(line_segment, partition_line)
        
    if encoding_cost == None:
        raise Exception("undefined encoding cost, there were no line segments")
        
    return model_cost + encoding_cost

def no_partition_cost_computer(trajectory_point_list, low_index, high_index, \
                               line_segment_iterable_getter, model_cost_computer):
    if low_index >= high_index:
        raise IndexError("illegal indices to no partition func")
    
    total_cost = None
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, None):
        total_cost = model_cost_computer(line_segment)
        
    if total_cost == None:
        raise Exception("undefined total cost, there were no line segments")
    
    return total_cost

def get_line_segment_from_points(point_a, point_b):
    return LineSegment.from_points([point_a, point_b])

def get_trajectory_line_segment_iterator(list, low, high, get_line_segment_from_points_func):
    if high <= low:
        raise Exception("high must be greater than low index")
            
    def line_segment_generator(func=get_line_segment_from_points_func):
        cur_pos = low
        
        while cur_pos < high:
            yield func(list[cur_pos], list[cur_pos + 1])
            cur_pos += 1
            
    return GeneratorInitializer(line_segment_generator)