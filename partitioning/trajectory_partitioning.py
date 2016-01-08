'''
Created on Jan 7, 2016

@author: Alex
'''
from planar.line import LineSegment
from planar import Point
from string import lower
from generator_initializer import GeneratorInitializer

def partition_trajectory(trajectory_point_list, partition_cost_computer, no_partition_cost_computer):
    return range(0, len(list))

def partition_cost_computer(trajectory_point_list, low_index, high_index, line_segment_iterable_getter, \
                            partition_line_getter, model_cost_computer, distance_function):
    if low_index >= high_index:
        raise IndexError("illegal indices to partition func")
    
    partition_line = partition_line_getter(trajectory_point_list, low_index, high_index)
    model_cost = model_cost_computer(partition_line)
    encoding_cost = 0.0
    
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, None):
        encoding_cost = distance_function(line_segment, partition_line)
        
    return model_cost + encoding_cost

def no_partition_cost_computer(trajectory_point_list, low_index, high_index, \
                               line_segment_iterable_getter, model_cost_computer):
    if low_index >= high_index:
        raise IndexError("illegal indices to no partition func")
    
    total_cost = 0.0
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, None):
        total_cost = model_cost_computer(line_segment)
    
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